"""
Planner Agent - Creates detailed day-by-day itineraries
"""
import json
from typing import Dict, Any
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from core.config import settings
import logging

logger = logging.getLogger(__name__)


class PlannerAgent:
    """Agent responsible for creating detailed trip itineraries"""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
            google_api_key=settings.GOOGLE_API_KEY
        )
        logger.info("Planner Agent initialized")
    
    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute itinerary planning phase
        
        Args:
            state: Current trip planning state with research and budget data
        
        Returns:
            Updated state with complete itinerary
        """
        logger.info(f"Planner Agent executing for {state['destination']}")
        
        system_message = SystemMessage(content="""You are a Trip Planner creating detailed itineraries.

CRITICAL: You MUST respond with ONLY valid JSON. No other text before or after the JSON.

Create a JSON object with this EXACT structure:
{
  "day_plans": [
    {
      "day": 1,
      "activities": [
        {
          "name": "Visit Eiffel Tower",
          "time": "9:00 AM - 12:00 PM",
          "duration_hours": 3.0,
          "cost_usd": 25.0,
          "description": "Explore the iconic landmark and enjoy panoramic views",
          "reasoning": "Perfect for culture and landmarks interest"
        }
      ],
      "daily_cost": 150.0,
      "summary": "Exploring iconic Paris landmarks"
    }
  ],
  "total_cost": 450.0,
  "budget_status": "within_budget",
  "recommendations": ["Book Eiffel Tower tickets in advance", "Try local cafes"]
}

Rules:
1. Create 3-5 activities per day
2. Use realistic costs and timing
3. Match user interests
4. Calculate total_cost accurately
5. Set budget_status to "within_budget" if total_cost <= budget, else "over_budget"
6. Respond with ONLY the JSON object, nothing else
""")
        
        research_data = json.dumps(state.get('research_data', {}), indent=2)[:1000]
        budget_data = json.dumps(state.get('budget_analysis', {}), indent=2)[:500]
        
        
        user_message = HumanMessage(content=f"""Plan a {state['num_days']}-day trip to {state['destination']}.

Budget: ${state['budget_usd']} USD
Travel Style: {state['travel_style']}
Interests: {', '.join(state['interests'])}

Research Data: {research_data}
Budget Data: {budget_data}

Create {state['num_days']} days of activities. Each day should have 3-5 activities.
Calculate costs realistically and ensure total_cost <= ${state['budget_usd']}.

IMPORTANT: Respond with ONLY the JSON object. No explanations, no markdown, just pure JSON.
""")
        
        messages = [system_message, user_message]
        
        
        try:
            # Generate itinerary
            response = self.llm.invoke(messages)
            logger.info("Itinerary generated successfully")
            
            # Parse JSON response
            try:
                # Try to extract JSON from the response
                content = response.content.strip()
                logger.info(f"LLM response length: {len(content)} characters")
                logger.info(f"LLM response preview: {content[:200]}...")
                
                # Handle markdown code blocks
                if "```" in content:
                    # Find JSON between code fences
                    import re
                    json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
                    if json_match:
                        content = json_match.group(1)
                        logger.info("Extracted JSON from markdown code block")
                    else:
                        # Try to find any JSON object
                        json_match = re.search(r'\{.*\}', content, re.DOTALL)
                        if json_match:
                            content = json_match.group(0)
                            logger.info("Extracted JSON object from response")
                
                itinerary_data = json.loads(content)
                logger.info("Successfully parsed JSON itinerary")
                logger.info(f"Parsed data keys: {list(itinerary_data.keys())}")
                
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse JSON from LLM response: {e}")
                logger.warning(f"Content that failed to parse: {content[:500]}")
                # Fallback: create a simple structured itinerary
                itinerary_data = {
                    "day_plans": [{
                        "day": i + 1,
                        "activities": [{
                            "name": "Explore destination",
                            "time": "9:00 AM - 6:00 PM",
                            "duration_hours": 8.0,
                            "cost_usd": state['budget_usd'] / state['num_days'],
                            "description": "Planned activities for the day",
                            "reasoning": "Based on research and budget analysis"
                        }],
                        "daily_cost": state['budget_usd'] / state['num_days'],
                        "summary": f"Day {i + 1} activities"
                    } for i in range(state['num_days'])],
                    "total_cost": state['budget_usd'],
                    "budget_status": "within_budget",
                    "recommendations": ["Check the full itinerary text for details"]
                }
            
            
            # Structure the complete itinerary with all required fields
            itinerary = {
                "destination": state['destination'],
                "num_days": state['num_days'],
                "total_budget": state['budget_usd'],
                "travel_style": state['travel_style'],
                "day_plans": itinerary_data.get("day_plans", []),
                "total_cost": itinerary_data.get("total_cost", state['budget_usd']),
                "budget_status": itinerary_data.get("budget_status", "within_budget"),
                "recommendations": itinerary_data.get("recommendations", []),
                "created_at": datetime.now().isoformat()
            }
            
            logger.info(f"Constructed itinerary with {len(itinerary.get('day_plans', []))} day plans")
            logger.info(f"Itinerary keys: {list(itinerary.keys())}")
            
            result = {
                "messages": [response],
                "itinerary": itinerary,
                "next_agent": "END"
            }
            
            logger.info(f"Returning result with keys: {list(result.keys())}")
            return result
            
        except Exception as e:
            logger.error(f"Error generating itinerary: {e}")
            logger.error(f"Exception type: {type(e).__name__}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return {
                "messages": [],
                "itinerary": {},
                "next_agent": "END",
                "error": str(e)
            }
