
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from models.schemas import TripRequest, TripResponse
from core.workflow import TripPlannerWorkflow
from core.config import settings
import logging
import uuid
import json
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Trip Planner API",
    description="Multi-agent trip planning system with live data",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize workflow
workflow = TripPlannerWorkflow()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Trip Planner API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/plan", response_model=TripResponse)
async def plan_trip(request: TripRequest):
    """
    Plan a trip based on user preferences
    
    Args:
        request: Trip planning request with destination, budget, etc.
    
    Returns:
        Complete trip itinerary with day-by-day plans
    """
    request_id = f"trip_{uuid.uuid4().hex[:8]}"
    logger.info(f"Received trip planning request {request_id} for {request.destination}")
    
    try:
        # Convert request to dict
        request_dict = {
            "destination": request.destination,
            "budget_usd": request.budget_usd,
            "num_days": request.num_days,
            "travel_style": request.travel_style.value,
            "interests": request.interests
        }
        
        # Execute workflow
        logger.info(f"Executing workflow for request {request_id}")
        result = workflow.execute(request_dict)
        
        logger.info(f"Workflow result keys: {list(result.keys())}")
        logger.info(f"Itinerary type: {type(result.get('itinerary'))}")
        logger.info(f"Itinerary value: {result.get('itinerary')}")
        
        # Build response
        response = TripResponse(
            request_id=request_id,
            status="completed",
            itinerary=result.get("itinerary"),
            agent_updates=[],
            error=result.get("error")
        )
        
        logger.info(f"Request {request_id} completed successfully")
        return response
        
    except Exception as e:
        logger.error(f"Error processing request {request_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/plan/stream")
async def plan_trip_stream(request: TripRequest):
    """
    Plan a trip with streaming updates
    
    Args:
        request: Trip planning request
    
    Returns:
        Server-sent events stream with agent progress
    """
    request_id = f"trip_{uuid.uuid4().hex[:8]}"
    logger.info(f"Received streaming request {request_id} for {request.destination}")
    
    async def event_generator():
        try:
            # Send initial status
            yield f"data: {json.dumps({'status': 'started', 'agent': 'researcher'})}\n\n"
            
            # Convert request to dict
            request_dict = {
                "destination": request.destination,
                "budget_usd": request.budget_usd,
                "num_days": request.num_days,
                "travel_style": request.travel_style.value,
                "interests": request.interests
            }
            
            # Execute workflow (in production, you'd want to stream intermediate results)
            result = workflow.execute(request_dict)
            
            # Send completion
            yield f"data: {json.dumps({'status': 'completed', 'itinerary': result.get('itinerary')})}\n\n"
            
        except Exception as e:
            logger.error(f"Error in streaming request {request_id}: {e}")
            yield f"data: {json.dumps({'status': 'error', 'message': str(e)})}\n\n"
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD
    )
