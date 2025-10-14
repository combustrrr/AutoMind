#!/usr/bin/env python3
"""Knowledge base and rule system for the AutoMind expert system.

This module loads car data, builds semantic frames, and applies symbolic rules
so that higher-level facts (segments, personas, usage profiles) can be used by
the inference engine. It exposes indexed accessors for fast reasoning and
question selection.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Set, Tuple


ConditionValue = Any
ConclusionValue = Any
ConditionMap = Mapping[str, ConditionValue]
ConclusionMap = Mapping[str, ConclusionValue]


@dataclass(frozen=True)
class Rule:
    """Represents a simple IF/THEN rule for forward chaining."""

    name: str
    conditions: ConditionMap
    conclusion: ConclusionMap
    description: str = ""
    weight: float = 1.0


@dataclass
class CarFrame:
    """Frame-style representation for a single car."""

    model: str
    slots: Dict[str, Any] = field(default_factory=dict)

    def get(self, slot: str, default: Any = None) -> Any:
        return self.slots.get(slot, default)

    def has(self, slot: str, expected: Any) -> bool:
        value = self.slots.get(slot)
        if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
            return normalise(expected) in {normalise(v) for v in value}
        return normalise(value) == normalise(expected)

    def as_dict(self) -> Dict[str, Any]:
        return dict(self.slots)


def normalise(value: Any) -> Any:
    """Normalise values for consistent comparisons."""
    if isinstance(value, str):
        return value.strip().lower()
    return value


class KnowledgeBase:
    """Loads cars, applies rules, and provides indexed access to facts."""

    CORE_ATTRIBUTES = [
        "brand",
        "body_type",
        "fuel_type",
        "price_range",
        "luxury",
        "engine_cc",
    ]

    DERIVED_ATTRIBUTES = [
        "price_segment",
        "engine_band",
        "usage_profile",
        "persona",
        "family_size",
        "drive_context",
    ]

    def __init__(self, data_file: str = "data/car_data_enriched.csv", rules: Optional[Sequence[Rule]] = None) -> None:
        self.data_file = data_file
        self._rules: List[Rule] = list(rules) if rules else self._default_rules()
        self.frames: Dict[str, CarFrame] = {}
        self.attribute_index: Dict[str, Dict[Any, Set[str]]] = {}
        self._attribute_labels: Dict[str, Dict[Any, str]] = {}
        self._load()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    @property
    def models(self) -> List[str]:
        return list(self.frames.keys())

    def get_frame(self, model: str) -> CarFrame:
        return self.frames[model]

    def get_attribute_values(self, attribute: str) -> List[Any]:
        values = self.attribute_index.get(attribute.lower(), {})
        return sorted(values.keys(), key=lambda v: str(v))

    def describe_value(self, attribute: str, value: Any) -> str:
        attr_map = self._attribute_labels.get(attribute.lower())
        if attr_map and value in attr_map:
            return attr_map[value]
        if isinstance(value, str):
            return value
        if isinstance(value, bool):
            return "Yes" if value else "No"
        return str(value)

    def get_models_matching(self, attribute: str, value: Any) -> Set[str]:
        attr = attribute.lower()
        value_key = normalise(value)
        matches = set()
        if attr not in self.attribute_index:
            return matches
        for key, models in self.attribute_index[attr].items():
            if normalise(key) == value_key:
                matches.update(models)
        return matches

    def attributes(self) -> List[str]:
        known = set(self.CORE_ATTRIBUTES) | set(self.DERIVED_ATTRIBUTES)
        known.update(self.attribute_index.keys())
        return sorted(known)

    def explain_rules(self) -> List[Rule]:
        return list(self._rules)

    # ------------------------------------------------------------------
    # Loading and indexing
    # ------------------------------------------------------------------
    def _load(self) -> None:
        with open(self.data_file, "r", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                frame = self._build_frame(row)
                self.frames[frame.model] = frame
                self._index_frame(frame)

    def _build_frame(self, row: MutableMapping[str, str]) -> CarFrame:
        model = row["model"].strip()
        brand_label = row["brand"].strip()
        body_type = row["body_type"].strip().lower()
        fuel_type = row["fuel_type"].strip().lower()
        price_range = row["price_range"].strip().lower()
        luxury = row["luxury"].strip().lower() in {"true", "yes", "1"}
        engine_cc = int(row.get("engine_cc", "0") or 0)
        keywords = row.get("keywords", "").strip()

        base_slots: Dict[str, Any] = {
            "model": model,
            "brand": normalise(brand_label),
            "brand_label": brand_label,
            "body_type": body_type,
            "fuel_type": fuel_type,
            "price_range": price_range,
            "luxury": luxury,
            "engine_cc": engine_cc,
            "keywords": keywords,
        }

        derived = self._run_forward_chaining(base_slots)
        slots = {**base_slots, **derived}
        return CarFrame(model=model, slots=slots)

    def _index_frame(self, frame: CarFrame) -> None:
        for attribute, value in frame.slots.items():
            attr = attribute.lower()
            if isinstance(value, (list, tuple, set)):
                values = value
            else:
                values = [value]
            for item in values:
                key = normalise(item)
                self.attribute_index.setdefault(attr, {}).setdefault(key, set()).add(frame.model)
                label = self._format_label(attr, item)
                self._attribute_labels.setdefault(attr, {})[key] = label

    # ------------------------------------------------------------------
    # Rule engine
    # ------------------------------------------------------------------
    def _run_forward_chaining(self, base_slots: Dict[str, Any]) -> Dict[str, Any]:
        derived: Dict[str, Any] = {}
        updated = True
        while updated:
            updated = False
            for rule in self._rules:
                if self._conditions_met(rule.conditions, base_slots, derived):
                    for target, result in rule.conclusion.items():
                        target_key = target.lower()
                        if target_key in derived:
                            continue
                        value = result(base_slots, derived) if callable(result) else result
                        derived[target_key] = value
                        updated = True
        return derived

    def _conditions_met(self, conditions: ConditionMap, base: Mapping[str, Any], derived: Mapping[str, Any]) -> bool:
        snapshot = {**base, **derived}
        for key, expected in conditions.items():
            key_norm = key.lower()
            value = snapshot.get(key_norm)
            if callable(expected):
                if not expected(value):
                    return False
            else:
                if isinstance(expected, (set, tuple, list)):
                    if normalise(value) not in {normalise(v) for v in expected}:
                        return False
                else:
                    if normalise(value) != normalise(expected):
                        return False
        return True

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _format_label(self, attribute: str, value: Any) -> str:
        attr = attribute.lower()
        if attr == "price_range":
            return value.replace("_", " ").replace("l", " lakhs").title()
        if attr == "price_segment":
            return {
                "budget": "Budget",
                "value": "Value seeker",
                "upper": "Upper mid-range",
                "premium": "Premium",
            }.get(normalise(value), str(value).title())
        if attr == "engine_band":
            return {
                "light": "Light (<= 1.2L)",
                "balanced": "Balanced (1.2L-1.6L)",
                "performance": "Performance (>= 1.6L)",
            }.get(normalise(value), str(value).title())
        if attr == "luxury":
            return "Luxury" if bool(value) else "Mass market"
        if attr == "fuel_type":
            return str(value).title()
        if attr == "body_type":
            return str(value).upper()
        if attr == "persona":
            return {
                "eco": "Eco conscious",
                "status": "Status driven",
                "saver": "Value focused",
                "family": "Family centric",
            }.get(normalise(value), str(value).title())
        if attr == "usage_profile":
            return {
                "city": "City commuter",
                "family": "Family cruiser",
                "adventure": "Adventure tourer",
            }.get(normalise(value), str(value).title())
        if attr == "family_size":
            return {
                "small": "Best for couples",
                "medium": "Small family",
                "large": "Large family",
            }.get(normalise(value), str(value).title())
        if isinstance(value, str):
            return value.title()
        return str(value)

    def _default_rules(self) -> List[Rule]:
        return [
            Rule(
                name="price_to_segment",
                conditions={"price_range": {"under_10l"}},
                conclusion={"price_segment": "budget"},
                description="Budget pricing implies budget segment",
            ),
            Rule(
                name="value_segment",
                conditions={"price_range": {"10-20l", "under_20l"}},
                conclusion={"price_segment": "value"},
                description="Mid pricing implies value segment",
            ),
            Rule(
                name="upper_segment",
                conditions={"price_range": {"20-30l"}},
                conclusion={"price_segment": "upper"},
                description="Upper pricing implies upper mid-range",
            ),
            Rule(
                name="premium_segment",
                conditions={"price_range": lambda v: isinstance(v, str) and "above" in v},
                conclusion={"price_segment": "premium"},
                description="Above 30L is considered premium",
            ),
            Rule(
                name="luxury_implies_premium",
                conditions={"luxury": True},
                conclusion={"price_segment": "premium"},
                description="Luxury flag promotes premium segment",
            ),
            Rule(
                name="engine_light",
                conditions={"engine_cc": lambda v: isinstance(v, int) and v and v < 1200},
                conclusion={"engine_band": "light"},
                description="Sub-1.2L engines are light",
            ),
            Rule(
                name="engine_balanced",
                conditions={"engine_cc": lambda v: isinstance(v, int) and 1200 <= v <= 1600},
                conclusion={"engine_band": "balanced"},
                description="1.2-1.6L engines are balanced",
            ),
            Rule(
                name="engine_performance",
                conditions={"engine_cc": lambda v: isinstance(v, int) and v >= 1600},
                conclusion={"engine_band": "performance"},
                description="Large displacement implies performance",
            ),
            Rule(
                name="usage_city",
                conditions={"body_type": "hatchback", "engine_band": "light"},
                conclusion={"usage_profile": "city"},
                description="Light hatchbacks suit city use",
            ),
            Rule(
                name="usage_family",
                conditions={"body_type": "sedan", "price_segment": {"value", "upper"}},
                conclusion={"usage_profile": "family"},
                description="Sedans in mid segment suit family trips",
            ),
            Rule(
                name="usage_adventure",
                conditions={"body_type": "suv", "engine_band": lambda v: v is not None and v != "light"},
                conclusion={"usage_profile": "adventure"},
                description="Bigger SUVs support adventure travel",
            ),
            Rule(
                name="persona_eco",
                conditions={"fuel_type": "electric"},
                conclusion={"persona": "eco", "drive_context": "urban"},
                description="Electric cars target eco urban buyers",
            ),
            Rule(
                name="persona_status",
                conditions={"luxury": True},
                conclusion={"persona": "status"},
                description="Luxury buyers seek status",
            ),
            Rule(
                name="persona_value",
                conditions={"price_segment": "budget"},
                conclusion={"persona": "saver"},
                description="Budget segment implies saver persona",
            ),
            Rule(
                name="family_small",
                conditions={"body_type": "hatchback"},
                conclusion={"family_size": "small"},
                description="Hatchbacks best for small families",
            ),
            Rule(
                name="family_medium",
                conditions={"body_type": "sedan"},
                conclusion={"family_size": "medium"},
                description="Sedans fit small families",
            ),
            Rule(
                name="family_large",
                conditions={"body_type": "suv"},
                conclusion={"family_size": "large"},
                description="SUVs handle large families",
            ),
            Rule(
                name="drive_highway",
                conditions={"engine_band": "performance"},
                conclusion={"drive_context": "highway"},
                description="Performance engines thrive on highways",
            ),
        ]


__all__ = ["KnowledgeBase", "CarFrame", "Rule"]
