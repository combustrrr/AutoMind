#!/usr/bin/env python3
"""Facade for the AutoMind expert system.

Provides a thin wrapper around the knowledge base and inference engine so that
interactive front-ends (CLI, UI) can drive the reasoning loop.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple
import time

from .inference_engine import InferenceEngine, Question
from .knowledge_base import KnowledgeBase


class CarExpertSystem:
    """High-level controller for car reasoning sessions."""

    def __init__(self, data_file: str = "data/car_data_enriched.csv", strategy: str = "entropy") -> None:
        self.kb = KnowledgeBase(data_file=data_file)
        self.engine = InferenceEngine(self.kb, strategy=strategy)
        self.questions_asked = 0
        self.session_start_time = None

    def reset(self) -> None:
        self.engine.reset()
        self.questions_asked = 0
        self.session_start_time = time.time()

    def next_question(self) -> Optional[Question]:
        question = self.engine.select_question()
        if question:
            self.questions_asked += 1
        return question

    def submit_answer(self, question_id: str, value: Any, confidence: float) -> None:
        self.engine.record_answer(question_id, value, confidence)

    def hypotheses(self, top_n: int = 3) -> List[Tuple[str, float]]:
        return self.engine.hypotheses(top_n)

    def ready_to_guess(self) -> bool:
        return self.engine.is_confident()

    def best_guess(self) -> Optional[Dict[str, Any]]:
        model, probability = self.engine.belief_state.best()
        if not model:
            return None
        frame = self.kb.get_frame(model)
        return {
            "model": model,
            "probability": probability,
            "frame": frame.as_dict(),
        }

    def get_session_performance(self) -> Dict[str, Any]:
        """Returns metrics about the current session's performance."""
        duration = time.time() - self.session_start_time if self.session_start_time else 0
        conclusion = self.best_guess()
        
        return {
            "questions_asked": self.questions_asked,
            "session_duration_seconds": duration,
            "conclusion_reached": conclusion is not None,
            "final_confidence": conclusion['probability'] if conclusion else 0,
        }

    def trace(self) -> Dict[str, Any]:
        return self.engine.trace()

    def describe_model(self, model: str) -> Dict[str, Any]:
        frame = self.kb.get_frame(model)
        return {
            "model": frame.model,
            "brand": frame.get("brand_label", frame.get("brand")),
            "body_type": frame.get("body_type"),
            "fuel_type": frame.get("fuel_type"),
            "price_range": frame.get("price_range"),
            "luxury": frame.get("luxury"),
            "price_segment": frame.get("price_segment"),
            "usage_profile": frame.get("usage_profile"),
            "persona": frame.get("persona"),
            "family_size": frame.get("family_size"),
            "engine_band": frame.get("engine_band"),
            "drive_context": frame.get("drive_context"),
            "keywords": frame.get("keywords"),
        }

    def list_rules(self) -> List[Dict[str, Any]]:
        rules = []
        for rule in self.kb.explain_rules():
            rules.append({
                "name": rule.name,
                "conditions": dict(rule.conditions),
                "conclusion": dict(rule.conclusion),
                "description": rule.description,
            })
        return rules


__all__ = ["CarExpertSystem"]
