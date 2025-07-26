# CEAF v3.0 - Multi-Agent Orchestrator with LangGraph
# Orchestrator/Responder Agent (ORA) and specialized subsystems

import asyncio
from typing import Dict, List, Any, Optional, TypedDict
from dataclasses import dataclass, asdict
from datetime import datetime
import json
import logging
import random

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import END, StateGraph
from langgraph.checkpoint.memory import InMemorySaver
from litellm import acompletion

# Import our custom modules
from AMA import MemoryExperience
from MCL import MetacognitiveControlLoop, CoherenceMetrics

# VRE will be passed in, so no direct import needed here, but it's good practice
# from VRE import VirtueReasoningEngine

logger = logging.getLogger(__name__)


# State definition for LangGraph
class AgentState(TypedDict):
    """State passed between agents in the graph"""
    messages: List[BaseMessage]
    current_query: str
    memory_context: List[Dict[str, Any]]
    coherence_metrics: Optional[Dict[str, float]]
    active_failures: List[str]
    narrative_context: Optional[str]
    virtue_considerations: List[str]  # <-- ADDED
    loss_insights: List[Dict[str, Any]]
    response_draft: Optional[str]
    metadata: Dict[str, Any]


@dataclass
class AgentConfig:
    """Configuration for individual agents"""
    name: str
    model: str = "openai/gpt-4o-mini"  # Switched to a more common model
    temperature: float = 0.7
    max_tokens: int = 1000
    system_prompt: str = ""


class CEAFOrchestrator:
    def __init__(self, openrouter_api_key: str, memory_architecture: Any, mcl: MetacognitiveControlLoop, lcam: Any,
                 ncim: Any, vre: Any):  # <-- ADDED vre
        self.openrouter_api_key = openrouter_api_key
        self.memory = memory_architecture
        self.mcl = mcl
        self.lcam = lcam
        self.ncim = ncim
        self.vre = vre  # <-- ADDED
        self.agents = self._initialize_agents()
        self.checkpointer = InMemorySaver()
        self.workflow = self._build_workflow()
        logger.info("Initialized CEAF Orchestrator with LCAM, NCIM, and VRE integration")  # <-- UPDATED LOG

    def _initialize_agents(self) -> Dict[str, AgentConfig]:
        # Unchanged, collapsed for brevity
        return {
            "ora": AgentConfig(name="Orchestrator/Responder Agent",
                               system_prompt="You are the Orchestrator/Responder Agent (ORA)..."),
            "memory_analyst": AgentConfig(name="Memory Pattern Analyst", temperature=0.5,
                                          system_prompt="You analyze memory patterns..."),
            "narrative_weaver": AgentConfig(name="Narrative Coherence Weaver", temperature=0.8,
                                            system_prompt="You weave coherent narratives..."),
            "virtue_engineer": AgentConfig(name="Virtue & Reasoning Engineer", temperature=0.6,
                                           system_prompt="You ensure principled reasoning..."),
            "loss_cataloger": AgentConfig(name="Loss Pattern Cataloger", temperature=0.4,
                                          system_prompt="You analyze and catalog failure patterns..."),
            "edge_navigator": AgentConfig(name="Edge of Coherence Navigator", temperature=0.9,
                                          system_prompt="You help navigate the edge...")
        }

    def _build_workflow(self) -> StateGraph:
        workflow = StateGraph(AgentState)
        workflow.add_node("retrieve_memory", self._retrieve_memory_context)
        workflow.add_node("assess_coherence", self._assess_coherence)
        workflow.add_node("get_loss_insights", self._get_loss_insights)
        workflow.add_node("get_virtue_input", self._get_virtue_input)  # <-- ADDED NODE
        workflow.add_node("generate_response", self._generate_response)
        workflow.add_node("learn_from_interaction", self._learn_from_interaction)
        workflow.add_node("update_identity", self._update_identity)

        workflow.set_entry_point("retrieve_memory")
        workflow.add_edge("retrieve_memory", "assess_coherence")
        workflow.add_edge("assess_coherence", "get_loss_insights")
        workflow.add_edge("get_loss_insights", "get_virtue_input")  # <-- UPDATED EDGE
        workflow.add_edge("get_virtue_input", "generate_response")  # <-- ADDED EDGE
        workflow.add_edge("generate_response", "learn_from_interaction")
        workflow.add_edge("learn_from_interaction", "update_identity")
        workflow.add_edge("update_identity", END)

        return workflow.compile(checkpointer=self.checkpointer)

    async def _call_agent(self, agent_name: str, prompt: str, state: AgentState) -> str:
        agent_config = self.agents[agent_name]
        messages = [{"role": "system", "content": agent_config.system_prompt}, {"role": "user", "content": prompt}]
        try:
            # Note: Model name might need 'openrouter/' prefix depending on litellm version
            response = await acompletion(
                model=agent_config.model, messages=messages,
                temperature=agent_config.temperature, max_tokens=agent_config.max_tokens,
                api_key=self.openrouter_api_key,
                base_url="https://openrouter.ai/api/v1"  # Explicitly set base_url for clarity
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error calling agent {agent_name}: {e}")
            if self.mcl: self.mcl.register_failure(f"agent_call_failure_{agent_name}", {"error": str(e)})
            return f"Error: Could not get a response from the {agent_name} agent."

    async def _retrieve_memory_context(self, state: AgentState) -> AgentState:
        # Unchanged from previous version
        if not self.memory:
            state["memory_context"] = []
            return state
        try:
            memories = self.memory.retrieve_with_loss_context(
                query=state["current_query"], k=5, include_failures=True, failure_weight=0.4
            )
            memory_context = []
            for mem in memories:
                mem_dict = asdict(mem)
                mem_dict.pop('embedding', None)
                memory_context.append(mem_dict)
            state["memory_context"] = memory_context
        except Exception as e:
            logger.error(f"Error in _retrieve_memory_context: {e}")
            state["memory_context"] = []
        return state

    async def _assess_coherence(self, state: AgentState) -> AgentState:
        # Unchanged from previous version
        if not self.mcl:
            state["coherence_metrics"] = {"overall_coherence": 0.7}
            return state
        mem_count = len(state.get("memory_context", []))
        semantic_score = min(0.6 + mem_count * 0.1, 0.95)
        narrative_score = min(0.5 + mem_count * 0.05, 0.9)
        epistemic_score = max(0.9 - mem_count * 0.1, 0.4)
        creative_score = random.uniform(0.4, 0.8)
        metrics = await self.mcl.assess_coherence(
            semantic_score=semantic_score, narrative_score=narrative_score,
            epistemic_score=epistemic_score, creative_score=creative_score,
            current_failures=state.get("active_failures", [])
        )
        state["coherence_metrics"] = asdict(metrics)
        return state

    async def _get_loss_insights(self, state: AgentState) -> AgentState:
        # Unchanged from previous version
        if not self.lcam:
            state["loss_insights"] = []
            return state
        try:
            insights = self.lcam.get_insights_for_context(
                query=state["current_query"],
                memory_context=state.get("memory_context", [])
            )
            state["loss_insights"] = insights
        except Exception as e:
            logger.error(f"Error in _get_loss_insights: {e}")
            state["loss_insights"] = []
        return state

    async def _get_virtue_input(self, state: AgentState) -> AgentState:  # <-- ADDED METHOD
        """Consults the VRE for reasoning principles based on the current context."""
        if not self.vre:
            state["virtue_considerations"] = []
            return state
        try:
            # The VRE's method needs the whole state to analyze context
            considerations = self.vre.get_virtue_considerations(state)
            state["virtue_considerations"] = considerations
        except Exception as e:
            logger.error(f"Error in _get_virtue_input: {e}")
            state["virtue_considerations"] = ["Error retrieving virtue considerations."]
        return state

    async def _update_identity(self, state: AgentState) -> AgentState:
        # Unchanged from previous version
        if not self.ncim:
            return state
        try:
            query = state["current_query"]
            response = state["response_draft"]
            coherence = state.get("coherence_metrics", {}).get("overall_coherence", 0.5)
            success = coherence > 0.6
            loss_insights = state.get("loss_insights", [])
            outcome = "a success" if success else "a challenge (failure)"
            lesson = "This reinforced my existing knowledge."
            if not success:
                lesson = "This was a difficult interaction. "
                if loss_insights:
                    lesson += f"It reminded me of past failures related to '{loss_insights[0]['failure_pattern']}'. I must learn to be more careful in such situations."
                else:
                    lesson += "It highlighted a new area where my understanding is weak. I need to reflect on this."
            interaction_summary = (
                f"I was asked: '{query}'. "
                f"I responded: '{response[:200]}...'. "
                f"The outcome was considered {outcome}. "
                f"The key lesson for me is: {lesson}"
            )
            update_prompt = self.ncim.get_update_prompt(interaction_summary)
            new_narrative = await self._call_agent("narrative_weaver", update_prompt, state)
            self.ncim.update_identity(new_narrative)
        except Exception as e:
            logger.error(f"Error during identity update: {e}", exc_info=True)
        return state

    async def _generate_response(self, state: AgentState) -> AgentState:  # <-- MODIFIED
        identity_narrative = self.ncim.get_current_identity() if self.ncim else "I am a helpful AI assistant."

        context = {
            "query": state["current_query"],
            "identity_narrative": identity_narrative,
            "memory_context": state.get("memory_context", [])[:3],
            "coherence_state": self.mcl.current_state.value if self.mcl else "unknown",
            "coherence_metrics": state.get("coherence_metrics", {}),
            "loss_insights": state.get("loss_insights", []),
            "virtue_considerations": state.get("virtue_considerations", [])  # <-- ADDED
        }

        # Enhanced prompt using VRE's output
        prompt = f"""You are a helpful AI assistant (CEAF). Respond to the user's query based on the provided context. 
        Be genuine, thoughtful, and unafraid of productive complexity. 

        Before you respond, reflect on these guiding principles derived from your internal state:
        {json.dumps(context['virtue_considerations'], indent=2)}

        Your current internal state is '{context['coherence_state']}'.

        Context: {json.dumps(context, indent=2, default=str)}
        User Query: "{state['current_query']}"
        Your Response:"""

        try:
            response = await self._call_agent("ora", prompt, state)
            state["response_draft"] = response
            state["messages"].append(AIMessage(content=response))
        except Exception as e:
            logger.error(f"Error in _generate_response: {e}")
            fallback = "I'm having trouble formulating a response right now. Could you please try rephrasing?"
            state["response_draft"] = fallback
            state["messages"].append(AIMessage(content=fallback))
        return state

    async def _learn_from_interaction(self, state: AgentState) -> AgentState:
        # Unchanged from previous version
        if self.memory and self.mcl:
            coherence = state.get("coherence_metrics", {}).get("overall_coherence", 0.5)
            success = coherence > 0.6
            experience = MemoryExperience(
                content=f"Q: {state['current_query']}\nA: {state.get('response_draft', '')[:300]}...",
                timestamp=datetime.now(), experience_type='success' if success else 'failure',
                context={"coherence": state.get("coherence_metrics", {})}, outcome_value=1.0 if success else -0.5,
                learning_value=abs(coherence - 0.5) + 0.2, failure_pattern='coherence_loss' if not success else None,
                metadata={"interaction_id": state.get("metadata", {}).get("interaction_id")})
            self.memory.add_experience(experience)

            if not success and self.lcam:
                self.lcam.catalog_failure(experience)
        return state

    async def process_query(self, query: str, thread_id: str = "default") -> str:  # <-- MODIFIED
        initial_state: AgentState = {"messages": [HumanMessage(content=query)], "current_query": query,
                                     "memory_context": [], "coherence_metrics": None, "active_failures": [],
                                     "narrative_context": None, "virtue_considerations": [], "loss_insights": [],
                                     "response_draft": None, "metadata": {}}
        try:
            config = {"configurable": {"thread_id": thread_id}}
            final_state = await self.workflow.ainvoke(initial_state, config=config)
            response = final_state.get("response_draft")
            if not response:
                response = "I apologize, but I couldn't generate a response. Please try again."
                logger.warning("No response_draft found in final state")
            return response
        except Exception as e:
            logger.error(f"Critical error in process_query workflow: {e}", exc_info=True)
            return f"I encountered a critical error: {e}"