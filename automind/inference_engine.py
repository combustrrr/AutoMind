#!/usr/bin/env python3
"""Inference engine for the AutoMind expert system.

This module maintains the belief state over possible cars, performs symbolic
forward/backward chaining, and selects the next question using information
gain to mimic expert reasoning.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Set, Tuple

from .knowledge_base import KnowledgeBase


def normalize(value: Any) -> Any:
    if isinstance(value, str):
        return value.strip().lower()
    return value


@dataclass
class Evidence:
    """Container for evidence to update belief state."""
    attribute: str
    value: Any
    confidence: float
    weight: float = 1.0


@dataclass
class AnswerOption:
    label: str
    value: Any
    hint: Optional[str] = None


@dataclass
class Question:
    id: str
    attribute: str
    text: str
    options: List[AnswerOption]
    weight: float = 1.0
    strategy: str = "forward"


@dataclass(frozen=True)
class InferenceRule:
    name: str
    conditions: Mapping[str, Any]
    conclusion: Mapping[str, Any]
    description: str = ""


class BeliefState:
    """Probability distribution over candidate cars."""

    def __init__(self, models: Sequence[str]) -> None:
        self._models = list(models)
        base = 1.0 / len(self._models) if self._models else 0.0
        self._probabilities: Dict[str, float] = {model: base for model in self._models}

    def copy(self) -> "BeliefState":
        clone = BeliefState(self._models)
        clone._probabilities = self._probabilities.copy()
        return clone

    def normalize(self) -> None:
        total = sum(self._probabilities.values())
        if total <= 0:
            base = 1.0 / len(self._models) if self._models else 0.0
            self._probabilities = {model: base for model in self._models}
            return
        for model in self._probabilities:
            self._probabilities[model] /= total

    def entropy(self) -> float:
        entropy = 0.0
        for probability in self._probabilities.values():
            if probability > 0:
                entropy -= probability * math.log2(probability)
        return entropy

    def gini_impurity(self) -> float:
        """Calculates the Gini impurity of the belief state."""
        impurity = 1.0
        for probability in self._probabilities.values():
            impurity -= probability**2
        return impurity

    def ranked(self, top_n: Optional[int] = None) -> List[Tuple[str, float]]:
        pairs = sorted(self._probabilities.items(), key=lambda item: item[1], reverse=True)
        return pairs if top_n is None else pairs[:top_n]

    def best(self) -> Tuple[Optional[str], float]:
        ranked = self.ranked(1)
        if not ranked:
            return None, 0.0
        return ranked[0]

    def gap(self) -> float:
        ranked = self.ranked(2)
        if len(ranked) < 2:
            return ranked[0][1] if ranked else 0.0
        return ranked[0][1] - ranked[1][1]

    def probability_of_models(self, models: Iterable[str]) -> float:
        lookup = set(models)
        return sum(self._probabilities.get(model, 0.0) for model in lookup)

    def apply_evidence(self, knowledge_base: KnowledgeBase, evidence: Evidence) -> None:
        """Apply evidence to update belief probabilities.
        
        Time Complexity: O(n) where n is the number of models
        Space Complexity: O(1)
        """
        if not self._is_valid_evidence(evidence.value, evidence.confidence):
            return
        
        matches = knowledge_base.get_models_matching(evidence.attribute, evidence.value)
        
        if not matches:
            self._apply_no_match_penalty(evidence.confidence, evidence.weight)
        else:
            self._apply_match_update(matches, evidence.confidence, evidence.weight)
        
        self.normalize()
    
    def _is_valid_evidence(self, value: Any, confidence: float) -> bool:
        """Check if evidence is valid for processing."""
        return value is not None and confidence > 0
    
    def _apply_no_match_penalty(self, confidence: float, weight: float) -> None:
        """Apply penalty when no models match the evidence."""
        damping = max(0.2, 1.0 - confidence * weight * 0.4)
        for model in self._probabilities:
            self._probabilities[model] *= damping
    
    def _apply_match_update(self, matches: set, confidence: float, weight: float) -> None:
        """Update probabilities based on matching models.
        
        More aggressive updates for better discrimination.
        """
        match_boost = 1.0 + confidence * weight * 2.5  # Increased from 0.9
        mismatch_penalty = max(0.01, 1.0 - confidence * weight * 1.5)  # Increased penalty from 0.6
        
        for model in self._probabilities:
            multiplier = match_boost if model in matches else mismatch_penalty
            self._probabilities[model] *= multiplier

    def simulate_evidence(self, knowledge_base: KnowledgeBase, evidence: Evidence) -> "BeliefState":
        """Simulate applying evidence without modifying current state.
        
        Time Complexity: O(n) where n is the number of models
        Space Complexity: O(n) for creating a copy
        """
        clone = self.copy()
        clone.apply_evidence(knowledge_base, evidence)
        return clone


class InferenceEngine:
    """Expert reasoning engine with chaining and entropy-based question selection."""

    def __init__(self, knowledge_base: KnowledgeBase, strategy: str = "entropy") -> None:
        self.kb = knowledge_base
        self.strategy = strategy  # "entropy" or "gini"
        self.belief_state = BeliefState(self.kb.models)
        self.question_bank: List[Question] = self._build_question_bank()
        self._question_lookup: Dict[str, Question] = {q.id: q for q in self.question_bank}
        self._asked: Set[str] = set()
        self._known_facts: Dict[str, Set[Any]] = {}
        self._fact_strength: Dict[str, float] = {}
        self._derived_facts: Dict[str, Set[Any]] = {}
        self._applied_evidence: Set[Tuple[str, Any]] = set()
        self._user_rules = self._user_ruleset()
        self.confidence_threshold = 0.25  # Much lower - guess with top candidate at 25%
        self.gap_threshold = 0.08  # Lower gap needed
        self.max_questions = 6  # Maximum questions before forcing a guess

    # ------------------------------------------------------------------
    # Public control surface
    # ------------------------------------------------------------------
    def reset(self) -> None:
        self.belief_state = BeliefState(self.kb.models)
        self._asked.clear()
        self._known_facts.clear()
        self._derived_facts.clear()
        self._fact_strength.clear()
        self._applied_evidence.clear()

    def select_question(self) -> Optional[Question]:
        candidates = [q for q in self.question_bank if q.id not in self._asked]
        candidates = [q for q in candidates if self._fact_strength.get(q.attribute.lower(), 0.0) < 0.95]
        
        # Filter out logically inconsistent questions based on known facts
        candidates = self._filter_inconsistent_questions(candidates)
        
        if not candidates:
            return None
        backward_choice = self._backward_chain_candidate()
        if backward_choice:
            return backward_choice
        
        if self.strategy == "gini":
            return self._select_question_by_gini(candidates)
        else: # Default to entropy
            return self._select_question_by_entropy(candidates)


    def _select_question_by_entropy(self, candidates: List[Question]) -> Optional[Question]:
        best_question = None
        best_gain = -1.0
        current_entropy = self.belief_state.entropy()

        for question in candidates:
            gain = self._information_gain(question, current_entropy)
            if gain > best_gain:
                best_gain = gain
                best_question = question
        return best_question

    def _select_question_by_gini(self, candidates: List[Question]) -> Optional[Question]:
        best_question = None
        best_reduction = -1.0
        current_gini = self.belief_state.gini_impurity()

        for question in candidates:
            reduction = self._gini_reduction(question, current_gini)
            if reduction > best_reduction:
                best_reduction = reduction
                best_question = question
        return best_question

    def record_answer(self, question_id: str, value: Any, confidence: float) -> None:
        if question_id not in self._question_lookup:
            raise KeyError(f"Unknown question id: {question_id}")
        question = self._question_lookup[question_id]
        attr = question.attribute.lower()
        self._asked.add(question_id)
        self._fact_strength[attr] = max(self._fact_strength.get(attr, 0.0), confidence)
        
        # Smart default for era: If user skips era question, exclude classic cars
        if question_id == "era" and value is None:
            self._apply_smart_era_default()
            return
        
        if value is None or confidence <= 0:
            return
        bucket = self._known_facts.setdefault(attr, set())
        bucket.add(normalize(value))
        self._apply_evidence(attr, value, confidence, question.weight)
        self._forward_chain()
    
    def _apply_smart_era_default(self):
        """When user skips era question, penalize classic cars (discontinued models).
        
        Most users want current/recent cars, not discontinued models like Ritz or Zen.
        This prevents the system from guessing classic cars when era is not specified.
        """
        # Penalize classic era cars significantly
        classic_cars = self.kb.get_models_matching('era', 'classic')
        
        for model in classic_cars:
            if model in self.belief_state._probabilities:
                # Reduce probability of classic cars by 90%
                self.belief_state._probabilities[model] *= 0.1
        
        self.belief_state.normalize()

    def hypotheses(self, top_n: int = 3) -> List[Tuple[str, float]]:
        return self.belief_state.ranked(top_n)

    def is_confident(self) -> bool:
        """Check if system is confident enough to make a guess.
        
        Returns True if:
        1. Top candidate has sufficient probability, OR
        2. We've asked maximum questions, OR
        3. No more questions available
        """
        best_model, best_prob = self.belief_state.best()
        if not best_model:
            return False
        
        # Force guess after max questions
        if len(self._asked) >= self.max_questions:
            return True
        
        gap = self.belief_state.gap()
        return best_prob >= self.confidence_threshold and gap >= self.gap_threshold

    def trace(self) -> Dict[str, Any]:
        return {
            "known": {attr: sorted(values) for attr, values in self._known_facts.items()},
            "derived": {attr: sorted(values) for attr, values in self._derived_facts.items()},
            "hypotheses": self.hypotheses(5),
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _filter_inconsistent_questions(self, candidates: List[Question]) -> List[Question]:
        """Filter out questions that are logically inconsistent or redundant with known facts.
        
        Examples:
        - Don't ask about engine if fuel type is electric
        - Don't ask about luxury if price range implies non-luxury
        - Don't ask about seating if body type is hatchback
        """
        filtered = []
        fuel_type = self._get_known_fact('fuel_type')
        body_type = self._get_known_fact('body_type')
        price_range = self._get_known_fact('price_range')
        
        for question in candidates:
            # Skip engine-related questions for electric vehicles
            if fuel_type == 'electric' and question.attribute in ['engine_cc', 'engine_band']:
                continue
            
            # Skip luxury question if price range implies luxury status
            if question.attribute == 'luxury' and price_range:
                # Under 30 Lakhs = definitely NOT luxury
                if price_range in ['under_10l', '10-20l', '20-30l']:
                    # Auto-apply luxury=False based on price
                    self._apply_evidence('luxury', False, confidence=0.95, weight=1.0)
                    continue  # Skip asking the question
                # Above 30 Lakhs = likely luxury (but still ask since some aren't)
                # e.g., Toyota Fortuner is above 30L but not luxury badge
            
            # Skip seating capacity questions if body type is known and incompatible
            if question.attribute == 'family_size':
                if body_type == 'hatchback' and self._would_ask_large_family(question):
                    continue
            
            filtered.append(question)
        
        return filtered
    
    def _get_known_fact(self, attribute: str) -> Optional[str]:
        """Get a known fact value if it exists with high confidence."""
        attr = attribute.lower()
        if attr in self._known_facts and self._known_facts[attr]:
            # Return the first (and typically only) value
            values = list(self._known_facts[attr])
            if values:
                return str(values[0])
        return None
    
    def _would_ask_large_family(self, question: Question) -> bool:
        """Check if question would ask about large family sizes."""
        for option in question.options:
            if option.value and str(option.value).lower() == 'large':
                return True
        return False
    
    def _apply_evidence(self, attribute: str, value: Any, confidence: float, weight: float) -> None:
        key = (attribute, normalize(value))
        if key in self._applied_evidence:
            return
        self._applied_evidence.add(key)
        evidence = Evidence(attribute=attribute, value=value, confidence=confidence, weight=weight)
        self.belief_state.apply_evidence(self.kb, evidence)

    def _forward_chain(self) -> None:
        """Apply forward chaining to derive new facts from known facts.
        
        Uses iterative rule application until no new facts are derived.
        Time Complexity: O(r * f) where r is rules count, f is facts count
        Space Complexity: O(f) for storing derived facts
        """
        changed = True
        while changed:
            changed = False
            snapshot = self._build_fact_snapshot()
            
            for rule in self._user_rules:
                if self._try_apply_rule(rule, snapshot):
                    changed = True
    
    def _build_fact_snapshot(self) -> Dict[str, Any]:
        """Build a snapshot of all known and derived facts."""
        snapshot = {attr: list(values)[0] for attr, values in self._known_facts.items() if values}
        derived = {attr: list(values)[0] for attr, values in self._derived_facts.items() if values}
        snapshot.update(derived)
        return snapshot
    
    def _try_apply_rule(self, rule: InferenceRule, facts: Dict[str, Any]) -> bool:
        """Attempt to apply a rule and return True if new facts were derived."""
        if not self._rule_conditions_met(rule.conditions, facts):
            return False
        
        for target, result in rule.conclusion.items():
            if self._derive_new_fact(target, result, facts):
                return True
        return False
    
    def _derive_new_fact(self, attribute: str, result: Any, facts: Dict[str, Any]) -> bool:
        """Derive and store a new fact if it's not already known."""
        attr = attribute.lower()
        value = result(facts) if callable(result) else result
        
        if value is None:
            return False
        
        store = self._derived_facts.setdefault(attr, set())
        norm_value = normalize(value)
        
        if norm_value not in store:
            store.add(norm_value)
            self._apply_evidence(attr, value, 0.55, weight=0.7)
            return True
        return False

    def _rule_conditions_met(self, conditions: Mapping[str, Any], facts: Mapping[str, Any]) -> bool:
        """Check if all rule conditions are satisfied by current facts.
        
        Time Complexity: O(c) where c is the number of conditions
        """
        for attr, expected in conditions.items():
            actual = facts.get(attr.lower())
            if not self._condition_matches(expected, actual):
                return False
        return True
    
    def _condition_matches(self, expected: Any, actual: Any) -> bool:
        """Check if a single condition matches the actual value."""
        if callable(expected):
            return expected(actual)
        return normalize(actual) == normalize(expected)

    def _backward_chain_candidate(self) -> Optional[Question]:
        """Use backward chaining to find a discriminating question.
        
        When close to a conclusion, identifies questions that differentiate
        between top candidates.
        Time Complexity: O(n * a) where n is top candidates, a is attributes
        """
        best_model, best_prob = self.belief_state.best()
        
        if not self._should_use_backward_chaining(best_model, best_prob):
            return None
        
        ranked = self.belief_state.ranked(3)
        differentiators = self._get_differentiators(ranked)
        
        return self._find_unanswered_question(differentiators)
    
    def _should_use_backward_chaining(self, best_model: Optional[str], best_prob: float) -> bool:
        """Determine if backward chaining should be used.
        
        Use backward chaining when we have a strong leading candidate
        to ask discriminating questions.
        """
        return best_model is not None and best_prob >= 0.35  # Earlier activation
    
    def _get_differentiators(self, ranked: List[Tuple[str, float]]) -> List[str]:
        """Get list of differentiating attributes."""
        if len(ranked) <= 1:
            return self._candidate_attributes()
        return self._find_differentiating_attributes(ranked)
    
    def _find_unanswered_question(self, attributes: List[str]) -> Optional[Question]:
        """Find the first unanswered question from the attribute list."""
        for attribute in attributes:
            if self._fact_strength.get(attribute, 0.0) >= 0.95:
                continue
            
            question = self._question_lookup.get(attribute)
            if question and question.id not in self._asked:
                question.strategy = "backward"
                return question
        return None

    def _candidate_attributes(self) -> List[str]:
        priority = [
            "brand",
            "body_type",
            "era",  # Added after brand and body type
            "fuel_type",
            "price_range",
            "luxury",
            "usage_profile",
            "persona",
            "family_size",
            "engine_band",
        ]
        return [attr for attr in priority if attr in self._question_lookup]

    def _find_differentiating_attributes(self, ranked: Sequence[Tuple[str, float]]) -> List[str]:
        """Find attributes that differentiate the best model from competitors.
        
        Time Complexity: O(a * c) where a is attributes, c is competitors
        """
        best_model = ranked[0][0]
        competitors = [model for model, _ in ranked[1:]]
        best_frame = self.kb.get_frame(best_model)
        attributes = self._candidate_attributes()
        
        differentiators: List[str] = []
        for attr in attributes:
            if self._is_differentiating_attribute(attr, best_frame, competitors):
                differentiators.append(attr)
        return differentiators
    
    def _is_differentiating_attribute(self, attr: str, best_frame: Any, competitors: List[str]) -> bool:
        """Check if an attribute differentiates the best model from all competitors."""
        best_value = best_frame.get(attr)
        if best_value is None:
            return False
        
        for competitor in competitors:
            comp_frame = self.kb.get_frame(competitor)
            if normalize(comp_frame.get(attr)) == normalize(best_value):
                return False
        return True

    def _gini_reduction(self, question: Question, current_gini: float) -> float:
        """Calculates the reduction in impurity for a given question."""
        total_prob = sum(self.belief_state.probability_of_models(self.kb.get_models_matching(question.attribute, opt.value)) for opt in question.options if opt.value is not None)
        
        if total_prob == 0:
            return 0

        weighted_gini = 0.0
        for option in question.options:
            if option.value is None:
                continue
            
            matching_models = self.kb.get_models_matching(question.attribute, option.value)
            prob_of_option = self.belief_state.probability_of_models(matching_models) / total_prob

            if prob_of_option > 0:
                evidence = Evidence(
                    attribute=question.attribute,
                    value=option.value,
                    confidence=0.8,
                    weight=question.weight
                )
                simulated_state = self.belief_state.simulate_evidence(self.kb, evidence)
                weighted_gini += prob_of_option * simulated_state.gini_impurity()
        
        return current_gini - weighted_gini

    def _information_gain(self, question: Question, current_entropy: float) -> float:
        expected_entropy = 0.0
        for option in question.options:
            if option.value is None:
                continue
            matching = self.kb.get_models_matching(question.attribute, option.value)
            probability = self.belief_state.probability_of_models(matching)
            if probability <= 0:
                continue
            evidence = Evidence(
                attribute=question.attribute,
                value=option.value,
                confidence=0.8,
                weight=question.weight
            )
            simulated = self.belief_state.simulate_evidence(self.kb, evidence)
            option_entropy = simulated.entropy()
            expected_entropy += probability * option_entropy
        gain = current_entropy - expected_entropy
        return gain

    def _build_question_bank(self) -> List[Question]:
        """Build question bank with proper priorities for Akinator-style guessing.
        
        Questions ordered by discriminating power:
        1. Brand (high discriminating power)
        2. Body type (narrows down significantly)
        3. Era/Generation (differentiates Swift vs Ritz vs Zen)
        4. Price range (eliminates many options)
        5. Fuel type
        6. Luxury badge
        7. Derived attributes (asked only if needed)
        """
        questions: List[Question] = []
        
        # High priority: Most discriminating questions first
        questions.append(self._build_brand_question())  # Ask brand FIRST
        questions.append(self._build_simple_question(
            question_id="body_type",
            attribute="body_type",
            text="Which body style fits best?",
            weight=1.3,
        ))
        questions.append(self._build_era_question())  # NEW: Ask era/generation
        questions.append(self._build_simple_question(
            question_id="price_range",
            attribute="price_range",
            text="What budget bracket do you have in mind?",
            weight=1.2,
        ))
        questions.append(self._build_simple_question(
            question_id="fuel_type",
            attribute="fuel_type",
            text="Preferred fuel or powertrain?",
            weight=1.1,
        ))
        questions.append(self._build_luxury_question())
        
        # Lower priority: Derived/inferred attributes
        questions.append(self._build_simple_question(
            question_id="engine_band",
            attribute="engine_band",
            text="What level of engine performance do you expect?",
            weight=0.7,
        ))
        
        # Skip these unless really needed - they're often contradictory
        # questions.append(self._build_simple_question(
        #     question_id="price_segment",
        #     attribute="price_segment",
        #     text="How would you describe the overall spend level?",
        #     weight=0.3,
        # ))
        # questions.append(self._build_simple_question(
        #     question_id="usage_profile",
        #     attribute="usage_profile",
        #     text="What usage scenario fits your needs?",
        #     weight=0.3,
        # ))
        # questions.append(self._build_simple_question(
        #     question_id="persona",
        #     attribute="persona",
        #     text="Which buyer persona matches you most?",
        #     weight=0.3,
        # ))
        # questions.append(self._build_simple_question(
        #     question_id="family_size",
        #     attribute="family_size",
        #     text="What passenger capacity do you need?",
        #     weight=0.3,
        # ))
        
        return questions

    def _build_simple_question(
        self,
        question_id: str,
        attribute: str,
        text: str,
        weight: float = 1.0,
    ) -> Question:
        values = self.kb.get_attribute_values(attribute)
        options = [AnswerOption(label=self.kb.describe_value(attribute, value), value=value) for value in values]
        options.append(AnswerOption(label="Not sure / skip", value=None))
        return Question(
            id=question_id,
            attribute=attribute,
            text=text,
            options=options,
            weight=weight,
        )

    def _build_brand_question(self) -> Question:
        brand_index = self.kb.attribute_index.get("brand", {})
        ranked = sorted(brand_index.items(), key=lambda item: len(item[1]), reverse=True)
        top_values = [value for value, _ in ranked[:8]]
        options = [AnswerOption(label=self.kb.describe_value("brand", value), value=value) for value in top_values]
        if len(ranked) > 8:
            options.append(AnswerOption(label="Another brand (not listed)", value=None, hint="open"))
        else:
            options.append(AnswerOption(label="Any brand is fine", value=None))
        return Question(
            id="brand",
            attribute="brand",
            text="Do you have a brand in mind?",
            options=options,
            weight=1.1,
        )

    def _build_luxury_question(self) -> Question:
        options = [
            AnswerOption(label="Yes, luxury or premium", value=True),
            AnswerOption(label="No, everyday practicality", value=False),
            AnswerOption(label="Not sure / flexible", value=None),
        ]
        return Question(
            id="luxury",
            attribute="luxury",
            text="Is a luxury badge important?",
            options=options,
            weight=1.1,
        )
    
    def _build_era_question(self) -> Question:
        """Build question about car era/generation to differentiate models from different years."""
        options = [
            AnswerOption(
                label="Current (2020+)",
                value="current",
                hint="Latest generation, currently sold"
            ),
            AnswerOption(
                label="Recent (2015-2019)",
                value="recent",
                hint="Recent models, might still be available"
            ),
            AnswerOption(
                label="Older (2010-2014)",
                value="older",
                hint="Older generation"
            ),
            AnswerOption(
                label="Classic (Pre-2010)",
                value="classic",
                hint="Vintage or discontinued models"
            ),
            AnswerOption(label="Any era / Not sure", value=None),
        ]
        return Question(
            id="era",
            attribute="era",
            text="What era or generation is the car from?",
            options=options,
            weight=1.25,  # High weight - great discriminator
        )

    def _question_lookup_get(self, attribute: str) -> Optional[Question]:
        return self._question_lookup.get(attribute)

    def _user_ruleset(self) -> List[InferenceRule]:
        return [
            InferenceRule(
                name="budget_implies_non_luxury",
                conditions={"price_segment": lambda value: normalize(value) == "budget"},
                conclusion={"luxury": lambda _: False},
                description="Budget focus hints at non-luxury preference",
            ),
            InferenceRule(
                name="premium_implies_luxury",
                conditions={"price_segment": lambda value: normalize(value) == "premium"},
                conclusion={"luxury": lambda _: True},
                description="Premium spend hints luxury interest",
            ),
            InferenceRule(
                name="eco_prefers_electric",
                conditions={"persona": lambda value: normalize(value) == "eco"},
                conclusion={"fuel_type": lambda _: "electric"},
                description="Eco persona nudges electric powertrain",
            ),
            InferenceRule(
                name="family_size_medium",
                conditions={"family_size": lambda value: normalize(value) == "large"},
                conclusion={"body_type": lambda _: "suv"},
                description="Large family requires SUV space",
            ),
            InferenceRule(
                name="electric_no_large_engine",
                conditions={"fuel_type": lambda value: normalize(value) == "electric"},
                conclusion={"engine_band": lambda _: "small"},
                description="Electric vehicles don't have traditional large engines",
            ),
            InferenceRule(
                name="luxury_implies_premium_segment",
                conditions={"luxury": lambda value: value is True},
                conclusion={"price_segment": lambda _: "premium"},
                description="Luxury cars are typically in premium price segment",
            ),
        ]


__all__ = [
    "Evidence",
    "AnswerOption",
    "Question",
    "InferenceEngine",
    "BeliefState",
]
