# 🌍 AI-Powered Trip Planner

Production-ready multi-agent trip planning system with FastAPI backend and beautiful Streamlit frontend.

## 🎯 Features

- **Multi-Agent System**: 3 specialized AI agents (Researcher, Budget, Planner)
- **Live Data**: Real-time attraction data from OpenTripMap API
- **Real Costs**: Accurate 2024 pricing from Numbeo & Budget Your Trip
- **Beautiful UI**: Modern Streamlit interface with gradient design
- **LangGraph Orchestration**: Sophisticated agent workflow management
- **REST API**: FastAPI backend with streaming support

## 📁 Project Structure

```
TripPlanner/
├── backend/
│   ├── agents/          # AI agents (researcher, budget, planner)
│   ├── tools/           # Tools (search, costs, distance)
│   ├── models/          # Pydantic schemas
│   ├── core/            # Configuration & workflow
│   └── main.py          # FastAPI application
├── frontend/
│   ├── components/      # UI components
│   ├── styles/          # Custom CSS
│   └── app.py           # Streamlit application
├── requirements.txt
├── .env.example
└── README.md
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` and add:
- **GOOGLE_API_KEY** (Required): Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **OPENTRIPMAP_API_KEY** (Optional): Get from [OpenTripMap](https://opentripmap.io/product)
- **GEOAPIFY_API_KEY** (Optional): Get from [Geoapify](https://www.geoapify.com/)

### 3. Start Backend Server

```bash
cd backend
python main.py
```

The API will be available at `http://localhost:8000`

### 4. Start Frontend (New Terminal)

```bash
cd frontend
streamlit run app.py
```

The UI will open at `http://localhost:8501`

## 🎨 Usage

1. **Open the Streamlit UI** at http://localhost:8501
2. **Fill in your preferences** in the sidebar:
   - Destination city
   - Number of days
   - Budget (USD)
   - Travel style (budget/mid-range/luxury)
   - Interests (museums, landmarks, food, etc.)
3. **Click "Plan My Trip"**
4. **Watch the AI agents work**:
   - 🔍 Researcher gathers destination data
   - 💰 Budget analyzes costs
   - 📋 Planner creates itinerary
5. **View your personalized itinerary** with day-by-day plans!

## 🔧 API Endpoints

### `GET /`
Root endpoint with API info

### `GET /health`
Health check endpoint

### `POST /plan`
Plan a trip (synchronous)

**Request Body:**
```json
{
  "destination": "Paris",
  "num_days": 4,
  "budget_usd": 2500,
  "travel_style": "mid-range",
  "interests": ["museums", "landmarks", "food"]
}
```

**Response:**
```json
{
  "request_id": "trip_abc123",
  "status": "completed",
  "itinerary": {
    "destination": "Paris",
    "duration_days": 4,
    "itinerary_text": "..."
  }
}
```

### `POST /plan/stream`
Plan a trip with streaming updates (Server-Sent Events)

## 🤖 Agent Architecture

### Researcher Agent
- Searches for real tourist attractions via OpenTripMap API
- Calculates distances between locations
- Provides detailed attraction information with ratings

### Budget Agent
- Estimates costs using real 2024 data
- Validates against user budget
- Provides cost breakdown by category
- Suggests optimizations if over budget

### Planner Agent
- Creates day-by-day itineraries
- Includes timings and cost estimates
- Explains reasoning for each choice
- Synthesizes research and budget data

## 🛠️ Tools

1. **search_attractions**: Fetch real attractions from OpenTripMap
2. **estimate_costs**: Calculate costs from real 2024 data
3. **calculate_distance**: Compute distances and travel times

## 📊 Supported Destinations

Pre-loaded cost data for:
- Paris, France
- Tokyo, Japan
- New York, USA
- London, UK
- Bali, Indonesia
- Bangkok, Thailand
- Barcelona, Spain
- Dubai, UAE
- Rome, Italy
- Sydney, Australia

*Other destinations use default estimates*

## 🎨 UI Features

- **Gradient Design**: Modern purple gradient theme
- **Responsive Layout**: Works on desktop and mobile
- **Real-time Progress**: Watch agents work in real-time
- **Card-based Itinerary**: Beautiful day-by-day cards
- **Download Option**: Export itinerary as JSON

## 🔐 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| GOOGLE_API_KEY | Yes | Google Gemini API key |
| OPENTRIPMAP_API_KEY | No | OpenTripMap API key (free tier) |
| GEOAPIFY_API_KEY | No | Geoapify API key (free tier) |
| LLM_MODEL | No | LLM model (default: gemini-2.0-flash-exp) |
| LLM_TEMPERATURE | No | Temperature (default: 0.7) |
| API_PORT | No | Backend port (default: 8000) |

## 📝 Development

### Run Backend in Development Mode

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Access API Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI

### Run Frontend in Development Mode

```bash
cd frontend
streamlit run app.py --server.runOnSave true
```

## 🐛 Troubleshooting

### Backend won't start
- Check if port 8000 is available
- Verify GOOGLE_API_KEY is set in `.env`
- Check Python version (3.8+ required)

### Frontend shows connection error
- Ensure backend is running on http://localhost:8000
- Check CORS settings in `backend/core/config.py`

### No attractions found
- Verify OPENTRIPMAP_API_KEY is valid
- Check internet connection
- Try a different destination

## 📦 Dependencies

- **FastAPI**: REST API framework
- **Streamlit**: Frontend UI framework
- **LangGraph**: Agent orchestration
- **LangChain**: LLM integration
- **Google Generative AI**: Gemini 2.5 Flash
- **GeoPy**: Distance calculations
- **Requests**: HTTP client

## 🚀 Deployment

### Docker (Coming Soon)

```bash
docker-compose up
```

### Cloud Deployment

1. **Backend**: Deploy to Google Cloud Run, AWS Lambda, or Heroku
2. **Frontend**: Deploy to Streamlit Cloud
3. **Environment**: Set environment variables in deployment platform

## 📄 License

MIT License

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

## 📧 Support

For issues or questions, please open a GitHub issue.

---

**Built with ❤️ using LangGraph, FastAPI, and Streamlit**
