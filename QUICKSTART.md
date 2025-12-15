# 🔑 QUICK START GUIDE

## ⚠️ IMPORTANT: Set Your API Key First!

Before running the application, you MUST set your Google API key:

### Step 1: Get Your Google API Key
1. Visit: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

### Step 2: Create .env File
```bash
# Copy the example file
copy .env.example .env

# Edit .env and replace 'your_google_api_key_here' with your actual key
```

Your `.env` file should look like:
```
GOOGLE_API_KEY=AIzaSyD...your_actual_key_here...
```

### Step 3: Install Dependencies

**Option A - Use Install Script (Recommended):**
```bash
.\install.bat
```

**Option B - Manual Install:**
```bash
pip install fastapi uvicorn python-dotenv requests geopy streamlit
pip install pydantic==2.6.4 pydantic-settings==2.2.1
pip install google-generativeai
pip install langchain langchain-google-genai langgraph
```

### Step 4: Start Backend
```bash
cd backend
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 5: Start Frontend (New Terminal)
```bash
cd frontend
streamlit run app.py
```

Visit: http://localhost:8501

---

## 🐛 Troubleshooting

### Error: "GOOGLE_API_KEY not set"
- Make sure you created `.env` file (not `.env.example`)
- Check that your API key is correct
- Restart the backend after setting the key

### Error: "DefaultCredentialsError"
- This means the API key isn't being read
- Verify `.env` file is in the TripPlanner root directory
- Check the file contains: `GOOGLE_API_KEY=your_key`

### Error: "Module not found"
- Run the install script: `.\install.bat`
- Or manually install dependencies as shown above

### Backend won't start
- Check if port 8000 is available
- Look for error messages in the console
- Verify all dependencies are installed

---

## 📖 Full Documentation

See [README.md](README.md) for complete documentation.
