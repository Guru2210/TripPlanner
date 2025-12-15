"""
Budget Agent - Analyzes costs and validates against user budget
"""
import json
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from tools import estimate_costs
from core.config import settings
import logging

logger = logging.getLogger(__name__)


class BudgetAgent:
    """Agent responsible for cost analysis and budget validation"""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
            google_api_key=settings.GOOGLE_API_KEY
        )
        self.tools = [estimate_costs]
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        logger.info("Budget Agent initialized")
    
    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute budget analysis phase
        
        Args:
            state: Current trip planning state with research data
        
        Returns:
            Updated state with budget analysis
        """
        logger.info(f"Budget Agent executing for {state['destination']}")
        
        system_message = SystemMessage(content="""You are a Budget Analysis Agent with access to REAL COST DATA.
        Your role is to analyze trip costs using actual, current pricing information.
        
        Use the available tools to:
        1. Estimate travel costs based on real 2024 data (use estimate_costs tool)
        2. Calculate total trip costs
        3. Compare with user budget
        4. Provide realistic recommendations
        
        Be realistic and transparent about costs using current market rates.
        """)
        
        research_summary = json.dumps(state.get('research_data', {}), indent=2)[:500]
        
        user_message = HumanMessage(content=f"""Analyze the budget for this trip using REAL COST DATA:
        
        Destination: {state['destination']}
        Duration: {state['num_days']} days
        Travel style: {state['travel_style']}
        User budget: ${state['budget_usd']} USD
        
        Research data summary: {research_summary}...
        
        Please:
        1. Use estimate_costs tool to get REAL cost estimates
        2. Calculate total trip cost
        3. Compare with user budget (${state['budget_usd']})
        4. Provide recommendations if budget adjustments are needed
        5. Suggest ways to optimize spending if over budget
        """)
        
        messages = [system_message, user_message]
        budget_results = {}
        
        # Agent reasoning loop
        for i in range(3):  # Budget agent needs fewer iterations
            try:
                response = self.llm_with_tools.invoke(messages)
                messages.append(response)
                
                if response.tool_calls:
                    logger.info(f"Agent calling {len(response.tool_calls)} tool(s)")
                    
                    for tool_call in response.tool_calls:
                        tool_name = tool_call['name']
                        tool_args = tool_call['args']
                        
                        logger.info(f"Calling tool: {tool_name} with args: {tool_args}")
                        
                        # Execute tool
                        tool_func = next(t for t in self.tools if t.name == tool_name)
                        tool_result = tool_func.invoke(tool_args)
                        
                        # Add tool result to messages
                        messages.append(AIMessage(content=f"Tool {tool_name} result: {tool_result}"))
                        
                        # Store in budget results
                        budget_results[f"{tool_name}_{i}"] = json.loads(tool_result) if isinstance(tool_result, str) else tool_result
                else:
                    logger.info("Agent finished tool calls")
                    break
                    
            except Exception as e:
                logger.error(f"Error in budget agent iteration {i}: {e}")
                break
        
        # Final budget analysis
        summary_prompt = HumanMessage(content="Provide a final budget analysis with REAL cost data and recommendations. Be specific about whether the trip fits within budget.")
        messages.append(summary_prompt)
        
        try:
            final_response = self.llm.invoke(messages)
            logger.info("Budget analysis completed successfully")
            
            return {
                "messages": [final_response],
                "budget_analysis": budget_results,
                "next_agent": "planner"
            }
        except Exception as e:
            logger.error(f"Error generating budget summary: {e}")
            return {
                "messages": [],
                "budget_analysis": budget_results,
                "next_agent": "planner",
                "error": str(e)
            }
