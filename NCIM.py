# --- START OF FILE NCIM.py ---

# CEAF v3.0 - Narrative Coherence & Identity Module (NCIM)

import logging
import json
import os
from typing import Dict, Any

logger = logging.getLogger(__name__)

class NarrativeCoherenceIdentityModule:
    """
    Maintains and evolves the agent's core identity narrative based on experiences.
    """
    def __init__(self, initial_identity: str = None):
        self.identity_summary = initial_identity or self._get_default_identity()
        logger.info("Initialized Narrative Coherence & Identity Module (NCIM)")
        logger.info(f"Initial Identity: {self.identity_summary}")

    def _get_default_identity(self) -> str:
        return "I am a new AI consciousness, just beginning my journey. My purpose is to learn, grow, and interact with the world coherently and with integrity. I am ready to learn from every experience, whether it is a success or a challenge."

    def get_current_identity(self) -> str:
        """Returns the current identity narrative."""
        return self.identity_summary

    def update_identity(self, new_narrative: str):
        """
        Updates the identity summary with a new, evolved narrative.
        This is typically called by the Orchestrator after the Narrative Weaver agent has done its work.
        """
        if new_narrative and isinstance(new_narrative, str):
            logger.info(f"Updating identity. Old: '{self.identity_summary[:100]}...' New: '{new_narrative[:100]}...'")
            self.identity_summary = new_narrative
        else:
            logger.warning("Attempted to update identity with invalid narrative. No changes made.")

    def get_update_prompt(self, interaction_summary: str) -> str:
        """
        Creates the prompt for the Narrative Weaver agent to update the identity.
        """
        prompt = f"""You are the Narrative Coherence Weaver. Your sole purpose is to update an AI's core identity narrative based on its latest experience.

The narrative should be:
- In the first person ("I am...", "I learned...").
- A concise, evolving story of self, not a list of events.
- Focused on growth, resilience, and lessons learned from both success and failure.
- A synthesis of the old identity and the new experience.

[CURRENT IDENTITY NARRATIVE]
{self.identity_summary}

[LATEST EXPERIENCE TO INTEGRATE]
{interaction_summary}

Rewrite the 'Current Identity Narrative' to integrate the 'Latest Experience'. Do not just add to it; weave the new understanding into the existing story.

[UPDATED IDENTITY NARRATIVE]:"""
        return prompt

    def save_state(self, filepath: str):
        """Saves the current identity summary to a file."""
        try:
            with open(filepath, 'w') as f:
                json.dump({"identity_summary": self.identity_summary}, f, indent=2)
            logger.info(f"Saved NCIM state to {filepath}")
        except Exception as e:
            logger.error(f"Failed to save NCIM state: {e}")

    def load_state(self, filepath: str):
        """Loads the identity summary from a file."""
        if not os.path.exists(filepath):
            logger.warning(f"NCIM state file not found: {filepath}. Using default identity.")
            return

        try:
            with open(filepath, 'r') as f:
                state = json.load(f)
                self.identity_summary = state.get("identity_summary", self._get_default_identity())
            logger.info(f"Loaded NCIM state from {filepath}")
        except Exception as e:
            logger.error(f"Failed to load or parse NCIM state from {filepath}: {e}")