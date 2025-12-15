"""
LangGraph workflow orchestration for trip planning
"""
from typing import TypedDict, Annotated, List, Dict, Any
from operator import add
from langgraph.graph import StateGraph, END
from agents import ResearcherAgent, BudgetAgent, PlannerAgent
import logging

logger = logging.getLogger(__name__)


class TripPlannerState(TypedDict):
    """State shared across all agents"""
    user_request: str
    destination: str
    budget_usd: float
    num_days: int
    travel_style: str
    interests: List[str]
    messages: Annotated[List, add]
    research_data: Dict[str, Any]
    budget_analysis: Dict[str, Any]
    itinerary: Dict[str, Any]
    next_agent: str


class TripPlannerWorkflow:
    """LangGraph workflow for multi-agent trip planning"""
    
    def __init__(self):
        self.researcher = ResearcherAgent()
        self.budget_agent = BudgetAgent()
        self.planner = PlannerAgent()
        self.app = self._build_workflow()
        logger.info("Workflow initialized")
    
    def _build_workflow(self):
        """Build the LangGraph workflow"""
        workflow = StateGraph(TripPlannerState)
        
        # Add agent nodes
        workflow.add_node("researcher", self._researcher_node)
        workflow.add_node("budget", self._budget_node)
        workflow.add_node("planner", self._planner_node)
        
        # Define the flow
        workflow.set_entry_point("researcher")
        workflow.add_edge("researcher", "budget")
        workflow.add_edge("budget", "planner")
        workflow.add_edge("planner", END)
        
        # Compile the graph
        app = workflow.compile()
        logger.info("Workflow compiled successfully")
        return app
    
    def _researcher_node(self, state: TripPlannerState) -> TripPlannerState:
        """Researcher agent node"""
        logger.info("Executing researcher node")
        result = self.researcher.execute(state)
        # Merge result with existing state
        return {**state, **result}
    
    def _budget_node(self, state: TripPlannerState) -> TripPlannerState:
        """Budget agent node"""
        logger.info("Executing budget node")
        result = self.budget_agent.execute(state)
        # Merge result with existing state
        return {**state, **result}
    
    def _planner_node(self, state: TripPlannerState) -> TripPlannerState:
        """Planner agent node"""
        logger.info("Executing planner node")
        result = self.planner.execute(state)
        # Merge result with existing state
        return {**state, **result}
    
    def execute(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the complete workflow
        
        Args:
            request: Trip planning request
        
        Returns:
            Final state with itinerary
        """
        logger.info(f"Starting workflow for {request['destination']}")
        
        # Initialize state
        initial_state = {
            "user_request": f"Plan trip to {request['destination']}",
            "destination": request["destination"],
            "budget_usd": request["budget_usd"],
            "num_days": request["num_days"],
            "travel_style": request["travel_style"],
            "interests": request["interests"],
            "messages": [],
            "research_data": {},
            "budget_analysis": {},
            "itinerary": {},
            "next_agent": "researcher"
        }
        
        try:
            # Execute workflow
            result = self.app.invoke(initial_state)
            logger.info("Workflow completed successfully")
            return result
        except Exception as e:
            logger.error(f"Workflow execution error: {e}")
            raise
