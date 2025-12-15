"""
Test script to verify the setup is working
"""
import os
import sys

print("🔍 Checking Trip Planner Setup...\n")

# Check 1: .env file
print("1. Checking .env file...")
if os.path.exists(".env"):
    print("   ✅ .env file found")
    with open(".env", "r") as f:
        content = f.read()
        if "GOOGLE_API_KEY" in content and "your_google_api_key_here" not in content:
            print("   ✅ GOOGLE_API_KEY appears to be set")
        else:
            print("   ⚠️  GOOGLE_API_KEY not set or still has placeholder value")
            print("   → Please edit .env and add your actual API key")
else:
    print("   ❌ .env file not found")
    print("   → Copy .env.example to .env and add your API key")

# Check 2: Dependencies
print("\n2. Checking dependencies...")
try:
    import fastapi
    print("   ✅ FastAPI installed")
except ImportError:
    print("   ❌ FastAPI not installed")

try:
    import streamlit
    print("   ✅ Streamlit installed")
except ImportError:
    print("   ❌ Streamlit not installed")

try:
    import langchain
    print("   ✅ LangChain installed")
except ImportError:
    print("   ❌ LangChain not installed")

try:
    import langgraph
    print("   ✅ LangGraph installed")
except ImportError:
    print("   ❌ LangGraph not installed")

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    print("   ✅ LangChain Google GenAI installed")
except ImportError:
    print("   ❌ LangChain Google GenAI not installed")

# Check 3: Backend structure
print("\n3. Checking backend structure...")
required_files = [
    "backend/main.py",
    "backend/agents/researcher.py",
    "backend/agents/budget.py",
    "backend/agents/planner.py",
    "backend/tools/search_tools.py",
    "backend/tools/cost_tools.py",
    "backend/core/workflow.py",
    "backend/core/config.py"
]

all_present = True
for file in required_files:
    if os.path.exists(file):
        print(f"   ✅ {file}")
    else:
        print(f"   ❌ {file} missing")
        all_present = False

# Check 4: Frontend structure
print("\n4. Checking frontend structure...")
frontend_files = [
    "frontend/app.py",
    "frontend/components/sidebar.py",
    "frontend/components/progress.py",
    "frontend/components/itinerary.py"
]

for file in frontend_files:
    if os.path.exists(file):
        print(f"   ✅ {file}")
    else:
        print(f"   ❌ {file} missing")
        all_present = False

# Summary
print("\n" + "="*50)
if all_present and os.path.exists(".env"):
    print("✅ Setup looks good!")
    print("\nNext steps:")
    print("1. Make sure your GOOGLE_API_KEY is set in .env")
    print("2. Start backend: cd backend && python main.py")
    print("3. Start frontend: cd frontend && streamlit run app.py")
else:
    print("⚠️  Some issues found. Please fix them before running.")
    print("\nRun: .\\install.bat to install dependencies")
print("="*50)
