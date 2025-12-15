"""
Researcher Agent - Gathers destination information using live APIs
"""
import json
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from tools import search_attractions, calculate_distance
from core.config import settings
import logging

logger = logging.getLogger(__name__)


class ResearcherAgent:
    """Agent responsible for researching destinations and gathering attraction data"""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
            google_api_key=settings.GOOGLE_API_KEY
        )
        self.tools = [search_attractions, calculate_distance]
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        logger.info("Researcher Agent initialized")
    
    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute research phase
        
        Args:
            state: Current trip planning state
        
        Returns:
            Updated state with research data
        """
        logger.info(f"Researcher Agent executing for {state['destination']}")
        
        system_message = SystemMessage(content="""You are a Destination Research Agent with access to LIVE DATA APIs.
        Your role is to gather real-time, accurate information about travel destinations.
        
        Use the available tools to:
        1. Search for real tourist attractions using search_attractions
        2. Calculate distances between locations if needed
        
        Provide detailed, factual, CURRENT information to help plan the trip.
        Focus on highly-rated attractions and realistic travel times.
        """)
        
        user_message = HumanMessage(content=f"""Research the destination: {state['destination']}
        
        User interests: {', '.join(state['interests'])}
        Trip duration: {state['num_days']} days
        Travel style: {state['travel_style']}
        
        Please gather LIVE data:
        1. Search for top tourist attractions (use search_attractions tool)
        2. Focus on attractions matching user interests
        3. Prioritize highly-rated, popular attractions
        
        Provide a comprehensive summary of findings.
        """)
        
        messages = [system_message, user_message]
        research_results = {}
        
        # Agent reasoning loop
        for i in range(settings.MAX_AGENT_ITERATIONS):
            try:
                response = self.llm_with_tools.invoke(messages)
                messages.append(response)
                
                # Check if agent wants to use tools
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
                        
                        # Store in research results
                        research_results[f"{tool_name}_{i}"] = json.loads(tool_result) if isinstance(tool_result, str) else tool_result
                else:
                    # No more tools to call, agent is done
                    logger.info("Agent finished tool calls")
                    break
                    
            except Exception as e:
                logger.error(f"Error in researcher agent iteration {i}: {e}")
                break
        
        # Final summary from researcher
        summary_prompt = HumanMessage(content="Based on your LIVE research, provide a concise summary of the destination and top recommendations with real data.")
        messages.append(summary_prompt)
        
        try:
            final_response = self.llm.invoke(messages)
            logger.info("Research phase completed successfully")
            
            return {
                "messages": [final_response],
                "research_data": research_results,
                "next_agent": "budget"
            }
        except Exception as e:
            logger.error(f"Error generating final summary: {e}")
            return {
                "messages": [],
                "research_data": research_results,
                "next_agent": "budget",
                "error": str(e)
            }
