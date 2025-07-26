# CEAF v3.0 - Metacognitive Control Loop (MCL)
# Edge of Coherence Detection with Failure Integration

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
import logging
from datetime import datetime
import asyncio
from collections import deque
import json
import inspect

logger = logging.getLogger(__name__)


class CoherenceState(Enum):
    """System coherence states"""
    STABLE = "stable"
    EXPLORING = "exploring"
    EDGE_OF_CHAOS = "edge_of_chaos"
    PRODUCTIVE_CONFUSION = "productive_confusion"
    FAILING_PRODUCTIVELY = "failing_productively"
    RECOVERING = "recovering"
    BREAKTHROUGH_IMMINENT = "breakthrough_imminent"


@dataclass
class CoherenceMetrics:
    """Multi-dimensional coherence assessment"""
    semantic_coherence: float
    narrative_coherence: float
    epistemic_coherence: float
    creative_novelty: float
    loss_tolerance: float
    overall_coherence: float = field(init=False)
    edge_proximity: float = field(init=False)
    breakthrough_potential: float = field(init=False)

    def __post_init__(self):
        weights = {'semantic': 0.25, 'narrative': 0.25, 'epistemic': 0.20, 'creative': 0.15, 'loss': 0.15}
        self.overall_coherence = (
                    weights['semantic'] * self.semantic_coherence + weights['narrative'] * self.narrative_coherence +
                    weights['epistemic'] * self.epistemic_coherence + weights['creative'] * self.creative_novelty +
                    weights['loss'] * self.loss_tolerance)
        self.edge_proximity = (1 - abs(self.overall_coherence - 0.7)) * self.creative_novelty
        self.breakthrough_potential = self.edge_proximity * self.loss_tolerance


@dataclass
class SystemState:
    """Current system state snapshot"""
    timestamp: datetime
    coherence_state: CoherenceState
    metrics: CoherenceMetrics
    active_failures: List[str] = field(default_factory=list)
    recovery_strategies: List[str] = field(default_factory=list)
    learning_momentum: float = 0.0
    cycles_in_state: int = 0


class MetacognitiveControlLoop:
    def __init__(self, history_window: int = 100, adaptation_rate: float = 0.1, failure_threshold: float = 0.3):
        self.history_window = history_window
        self.current_state = CoherenceState.STABLE
        self.state_history: deque = deque(maxlen=history_window)
        self.metrics_history: deque = deque(maxlen=history_window)
        self.adaptation_rate = adaptation_rate
        self.failure_threshold = failure_threshold
        self.active_failures: Dict[str, Dict[str, Any]] = {}
        self.failure_recovery_patterns: Dict[str, List[str]] = {}
        self.productive_confusion_timer: Optional[datetime] = None
        self.coherence_targets = {'semantic': 0.8, 'narrative': 0.75, 'epistemic': 0.7, 'creative': 0.6, 'loss': 0.5}
        self.breakthrough_patterns: List[Tuple[Dict, Dict]] = []
        logger.info("Initialized Metacognitive Control Loop")

    async def assess_coherence(self, semantic_score: float, narrative_score: float, epistemic_score: float,
                               creative_score: float, current_failures: List[str]) -> CoherenceMetrics:
        loss_tolerance = self._calculate_loss_tolerance(current_failures)
        metrics = CoherenceMetrics(
            semantic_coherence=semantic_score, narrative_coherence=narrative_score,
            epistemic_coherence=epistemic_score, creative_novelty=creative_score,
            loss_tolerance=loss_tolerance
        )
        self.metrics_history.append(metrics)
        new_state = self._determine_coherence_state(metrics)
        if new_state != self.current_state:
            # Bug fix: In a real scenario, state change might alter future assessments.
            # Here we just log it. A more advanced version might have feedback.
            current_state_before_transition = self.current_state
            self.current_state = new_state
            await self._handle_state_transition(current_state_before_transition, new_state, metrics)
        return metrics

    def _calculate_loss_tolerance(self, current_failures: List[str]) -> float:
        tolerance = 0.5
        if current_failures and len(current_failures) > 0:
            productive_failures = sum(1 for f in current_failures if f in self.failure_recovery_patterns)
            tolerance += 0.1 * (productive_failures / len(current_failures))
        history_list = list(self.state_history)
        recent_breakthroughs = sum(
            1 for state in history_list[-10:] if state.coherence_state == CoherenceState.BREAKTHROUGH_IMMINENT)
        tolerance += 0.05 * recent_breakthroughs
        if self.productive_confusion_timer:
            duration = (datetime.now() - self.productive_confusion_timer).seconds
            if duration < 300:
                tolerance += 0.1
            elif duration > 900:
                tolerance -= 0.1
        return max(0.1, min(0.9, tolerance))

    def _determine_coherence_state(self, metrics: CoherenceMetrics) -> CoherenceState:
        # A simple bug fix: self.current_state should be checked against the value not the object
        current_state_val = self.current_state.value
        if metrics.breakthrough_potential > 0.6: return CoherenceState.BREAKTHROUGH_IMMINENT
        if metrics.loss_tolerance > 0.7 and metrics.overall_coherence < 0.5: return CoherenceState.FAILING_PRODUCTIVELY
        if 0.6 < metrics.overall_coherence < 0.8 and metrics.creative_novelty > 0.7: return CoherenceState.EDGE_OF_CHAOS
        if metrics.epistemic_coherence < 0.5 and metrics.creative_novelty > 0.6: return CoherenceState.PRODUCTIVE_CONFUSION
        if current_state_val in ["failing_productively",
                                 "productive_confusion"] and metrics.overall_coherence > 0.7: return CoherenceState.RECOVERING
        if metrics.creative_novelty > 0.5 and metrics.overall_coherence > 0.7: return CoherenceState.EXPLORING
        return CoherenceState.STABLE

    async def _handle_state_transition(self, old_state: CoherenceState, new_state: CoherenceState,
                                       metrics: CoherenceMetrics):
        logger.info(f"State transition: {old_state.value} -> {new_state.value}")
        state_snapshot = SystemState(
            timestamp=datetime.now(), coherence_state=new_state, metrics=metrics,
            active_failures=list(self.active_failures.keys()),
            learning_momentum=self._calculate_learning_momentum()
        )
        self.state_history.append(state_snapshot)

        if new_state == CoherenceState.PRODUCTIVE_CONFUSION:
            self.productive_confusion_timer = datetime.now()
        elif new_state == CoherenceState.RECOVERING:
            self.productive_confusion_timer = None
        elif new_state == CoherenceState.BREAKTHROUGH_IMMINENT:
            history_list = list(self.state_history)
            if old_state in [CoherenceState.FAILING_PRODUCTIVELY, CoherenceState.PRODUCTIVE_CONFUSION] and len(
                    history_list) > 1:
                self.breakthrough_patterns.append(
                    (asdict(history_list[-2]), asdict(state_snapshot))
                )

    def _calculate_learning_momentum(self) -> float:
        metrics_list = list(self.metrics_history)
        if len(metrics_list) < 10: return 0.0
        recent = metrics_list[-5:]
        older = metrics_list[-10:-5]
        if not older: return 0.0
        recent_avg = np.mean([m.creative_novelty * m.loss_tolerance for m in recent])
        older_avg = np.mean([m.creative_novelty * m.loss_tolerance for m in older])
        return max(-1.0, min(1.0, (recent_avg - older_avg) / max(older_avg, 0.01)))

    def _analyze_state_distribution(self) -> Dict[str, float]:
        if not self.state_history: return {CoherenceState.STABLE.value: 1.0}
        state_counts = {}
        for state in self.state_history:
            s_val = state.coherence_state.value
            state_counts[s_val] = state_counts.get(s_val, 0) + 1
        total = len(self.state_history)
        return {state_val: count / total for state_val, count in state_counts.items()}

    def register_failure(self, failure_id: str, failure_context: Dict[str, Any]):
        self.active_failures[failure_id] = {'timestamp': datetime.now(), 'context': failure_context,
                                            'recovery_attempts': 0, 'productive': False}
        logger.info(f"Registered failure: {failure_id}")

    def save_state(self, filepath: str):
        class MCLEncoder(json.JSONEncoder):
            def default(self, o):
                if isinstance(o, datetime): return o.isoformat()
                if isinstance(o, CoherenceState): return o.value
                if isinstance(o, (CoherenceMetrics, SystemState)): return asdict(o)
                if isinstance(o, np.float32): return float(o)
                return super().default(o)

        state = {"current_state": self.current_state.value, "state_history": list(self.state_history),
                 "metrics_history": [asdict(m) for m in self.metrics_history], "active_failures": self.active_failures,
                 "failure_recovery_patterns": self.failure_recovery_patterns,
                 "productive_confusion_timer": self.productive_confusion_timer.isoformat() if self.productive_confusion_timer else None,
                 "coherence_targets": self.coherence_targets, "breakthrough_patterns": self.breakthrough_patterns, }
        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2, cls=MCLEncoder)
        logger.info(f"Saved MCL state to {filepath}")

    def load_state(self, filepath: str):
        try:
            with open(filepath, 'r') as f:
                state = json.load(f)

            self.current_state = CoherenceState(state.get("current_state", "stable"))

            # --- MAJOR FIX: Filter dict before creating CoherenceMetrics ---
            # Get the constructor parameters for CoherenceMetrics
            init_params = inspect.signature(CoherenceMetrics).parameters
            metrics_init_keys = {k for k, v in init_params.items() if v.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD}

            loaded_history = []
            for s_dict in state.get("state_history", []):
                s_dict['timestamp'] = datetime.fromisoformat(s_dict['timestamp'])
                s_dict['coherence_state'] = CoherenceState(s_dict['coherence_state'])
                # Filter the metrics dict to only include expected keys
                metrics_data = {k: v for k, v in s_dict['metrics'].items() if k in metrics_init_keys}
                s_dict['metrics'] = CoherenceMetrics(**metrics_data)
                loaded_history.append(SystemState(**s_dict))
            self.state_history = deque(loaded_history, maxlen=self.history_window)

            loaded_metrics = []
            for m_dict in state.get("metrics_history", []):
                # Also filter here
                metrics_data = {k: v for k, v in m_dict.items() if k in metrics_init_keys}
                loaded_metrics.append(CoherenceMetrics(**metrics_data))
            self.metrics_history = deque(loaded_metrics, maxlen=self.history_window)

            self.active_failures = state.get("active_failures", {})
            self.failure_recovery_patterns = state.get("failure_recovery_patterns", {})
            timer_str = state.get("productive_confusion_timer")
            self.productive_confusion_timer = datetime.fromisoformat(timer_str) if timer_str else None
            self.coherence_targets = state.get("coherence_targets", self.coherence_targets)
            self.breakthrough_patterns = state.get("breakthrough_patterns", [])

            logger.info(f"Loaded MCL state from {filepath}")
        except Exception as e:
            logger.warning(f"Could not load MCL state from {filepath}: {e}. Starting fresh.")