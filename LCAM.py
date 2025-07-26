# --- START OF FILE LCAM.py ---

# CEAF v3.0 - Loss Cataloging and Analysis Module (LCAM)

import logging
from collections import defaultdict
from typing import List, Dict, Any, Optional
from AMA import MemoryExperience  # Assuming AMA.py is in the same path

logger = logging.getLogger(__name__)


class LossCatalogingAndAnalysisModule:
    """
    Analyzes failure experiences to extract wisdom, identify patterns,
    and provide actionable insights for decision-making.
    """

    def __init__(self):
        # A simple archive mapping failure patterns to a list of experiences
        self.failure_archive: Dict[str, List[MemoryExperience]] = defaultdict(list)
        # A more advanced structure could map failure IDs to detailed analysis
        self.failure_analysis: Dict[str, Dict[str, Any]] = {}
        logger.info("Initialized Loss Cataloging and Analysis Module (LCAM)")

    def catalog_failure(self, experience: MemoryExperience):
        """Adds a failure experience to the archive and performs initial analysis."""
        if experience.experience_type != 'failure' or not experience.failure_pattern:
            return

        # Use a unique ID for each experience if available, e.g., from metadata
        exp_id = experience.metadata.get("interaction_id", str(experience.timestamp))

        self.failure_archive[experience.failure_pattern].append(experience)

        # Perform a simple, initial analysis
        self.failure_analysis[exp_id] = {
            "pattern": experience.failure_pattern,
            "context_summary": experience.content[:150],
            "learning_value": experience.learning_value,
            "timestamp": experience.timestamp
        }
        logger.info(f"LCAM: Cataloged failure with pattern '{experience.failure_pattern}'")

    def get_insights_for_context(self, query: str, memory_context: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyzes the current query and memory context to find relevant loss patterns.

        This is a simple implementation. A more advanced version would use embeddings.
        """
        insights = []
        # Simple keyword matching for demonstration
        for pattern, experiences in self.failure_archive.items():
            if pattern in query:
                # Provide a summary of the most recent, relevant failure
                latest_exp = max(experiences, key=lambda e: e.timestamp)
                insights.append({
                    "insight_type": "direct_pattern_match",
                    "failure_pattern": pattern,
                    "lesson": f"Previously encountered '{pattern}'. Key takeaway was related to: {latest_exp.content[:100]}...",
                    "suggested_caution": True
                })

        if len(insights) > 2:  # Limit the number of insights
            return insights[:2]
        return insights

    def save_state(self, filepath: str):
        # For now, we can skip saving/loading LCAM state as it's derived from AMA.
        # A more advanced version would save its own analysis artifacts.
        logger.info(f"LCAM state is derived from AMA, skipping explicit save to {filepath}")
        pass

    def load_state(self, filepath: str, all_experiences: List[MemoryExperience]):
        # Rebuild the archive from the main memory
        logger.info(f"LCAM rebuilding state from main memory...")
        self.failure_archive.clear()
        self.failure_analysis.clear()
        for exp in all_experiences:
            self.catalog_failure(exp)
        logger.info(f"LCAM state rebuilt. Found {len(self.failure_analysis)} cataloged failures.")