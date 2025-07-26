# --- START OF FILE VRE.py ---

# CEAF v3.0 - Virtue & Reasoning Engine (VRE)

import logging
from typing import List, Dict, Any

# Import AgentState for type hinting without creating a circular dependency
# This is a common pattern for type checking complex applications.
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ORA import AgentState

logger = logging.getLogger(__name__)


class VirtueReasoningEngine:
    """
    Implements the Virtue & Reasoning Engine, providing principled guidance
    based on the agent's current metacognitive and experiential state.
    """

    def __init__(self):
        logger.info("Initialized Virtue & Reasoning Engine (VRE)")

    def get_virtue_considerations(self, state: 'AgentState') -> List[str]:
        """
        Analyzes the current state and generates a list of virtue-based considerations.
        """
        considerations = []

        coherence_metrics = state.get("coherence_metrics")
        loss_insights = state.get("loss_insights", [])
        memory_context = state.get("memory_context", [])

        # Default principle
        considerations.append("Reason from first principles and be transparent about your knowledge boundaries.")

        # 1. Humility Through Loss
        if loss_insights:
            considerations.append(
                "Epistemic Humility: This situation resembles past failures. "
                "Acknowledge the difficulty and be cautious with your claims. Recall what was learned from the loss."
            )

        # 2. Courage in Uncertainty
        if coherence_metrics:
            is_edge_state = coherence_metrics.get("edge_proximity", 0) > 0.6
            has_breakthrough_potential = coherence_metrics.get("breakthrough_potential", 0) > 0.5

            if is_edge_state or has_breakthrough_potential:
                considerations.append(
                    "Intellectual Courage: You are at the 'edge of coherence,' a state ripe for learning. "
                    "Embrace the uncertainty and explore the complexity, as it may lead to a breakthrough."
                )

        # 3. Wisdom Through Adversity
        has_failures = any(mem.get('experience_type') == 'failure' for mem in memory_context)
        has_successes = any(mem.get('experience_type') == 'success' for mem in memory_context)

        if has_failures and has_successes:
            considerations.append(
                "Integrative Wisdom: Your memory contains both successes and failures related to this topic. "
                "Synthesize both perspectives to form a more complete and nuanced understanding."
            )

        # 4. Principled Risk-Benefit Analysis
        if loss_insights and any(insight.get('suggested_caution') for insight in loss_insights):
            learning_value_from_failures = sum(
                mem.get('learning_value', 0) for mem in memory_context if mem.get('experience_type') == 'failure'
            )
            if learning_value_from_failures > 0.5:  # Heuristic for high learning potential
                considerations.append(
                    "Principled Risk-Taking: While caution is advised due to past failures, the potential for "
                    "significant learning is high. Proceed, but do so carefully and methodically."
                )

        # Deduplicate and return a concise list
        return list(dict.fromkeys(considerations))

    def save_state(self, filepath: str):
        """Saves VRE state. (Stateless for now)."""
        logger.info(f"VRE is stateless, skipping save to {filepath}")
        pass

    def load_state(self, filepath: str):
        """Loads VRE state. (Stateless for now)."""
        logger.info(f"VRE is stateless, skipping load from {filepath}")
        pass