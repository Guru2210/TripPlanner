@echo off
echo Installing Trip Planner Dependencies...
echo.

echo Step 1: Installing core dependencies...
pip install fastapi==0.109.0 uvicorn[standard]==0.27.0 python-dotenv==1.0.0 requests==2.31.0 geopy==2.4.1 streamlit==1.40.1 python-multipart==0.0.6

echo.
echo Step 2: Installing Pydantic...
pip install pydantic==2.6.4 pydantic-settings==2.2.1

echo.
echo Step 3: Installing Google AI...
pip install google-generativeai==0.8.3

echo.
echo Step 4: Installing LangChain...
pip install langchain-core==0.3.15 langchain-community==0.3.5 langchain-google-genai==2.0.4 langchain==0.3.7

echo.
echo Step 5: Installing LangGraph...
pip install langgraph==0.2.45

echo.
echo ✅ Installation complete!
echo.
echo To start the backend: cd backend ^&^& python main.py
echo To start the frontend: cd frontend ^&^& streamlit run app.py
pause
