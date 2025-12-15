"""
Trip Planner Streamlit Frontend
Beautiful UI for multi-agent trip planning system
"""
import streamlit as st
import requests
import json
from pathlib import Path

# Import components
from components.sidebar import render_sidebar
from components.progress import show_agent_status, show_loading_animation
from components.itinerary import display_itinerary

# Page configuration
st.set_page_config(
    page_title="AI Trip Planner",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
css_file = Path(__file__).parent / "styles" / "custom.css"
if css_file.exists():
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# API configuration
API_URL = "http://localhost:8000"


def call_api(request_data: dict):
    """
    Call the backend API to plan trip
    
    Args:
        request_data: Trip request data
    
    Returns:
        API response
    """
    try:
        response = requests.post(
            f"{API_URL}/plan",
            json=request_data,
            timeout=300  # 5 minutes timeout
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to backend API. Make sure the backend server is running on http://localhost:8000")
        st.info("💡 Start the backend with: `cd backend && python main.py`")
        return None
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. The trip planning took too long. Please try again.")
        return None
    except requests.exceptions.HTTPError as e:
        st.error(f"❌ API Error: {e}")
        return None
    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")
        return None


def main():
    """Main application"""
    
    # Header
    st.markdown("""
        <h1 style='text-align: center; color: white; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; margin-bottom: 2rem;'>
            🌍 AI-Powered Trip Planner
        </h1>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <p style='text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 2rem;'>
            Plan your perfect trip with AI agents using live data and real-time cost estimates
        </p>
    """, unsafe_allow_html=True)
    
    # Render sidebar and get user inputs
    user_inputs = render_sidebar()
    
    # Main content area
    if user_inputs["plan_button"]:
        # Validate inputs
        if not user_inputs["destination"]:
            st.error("❌ Please enter a destination")
            return
        
        if not user_inputs["interests"]:
            st.warning("⚠️ Please select at least one interest")
            return
        
        # Show loading
        with st.spinner("🌍 Planning your perfect trip..."):
            # Show agent progress
            st.markdown("### 🤖 AI Agents Working...")
            
            progress_container = st.container()
            with progress_container:
                show_agent_status("researcher", "Gathering destination information...", False)
                show_agent_status("budget", "Analyzing costs...", False)
                show_agent_status("planner", "Creating itinerary...", False)
            
            # Prepare request
            request_data = {
                "destination": user_inputs["destination"],
                "num_days": user_inputs["num_days"],
                "budget_usd": user_inputs["budget"],
                "travel_style": user_inputs["travel_style"],
                "interests": user_inputs["interests"]
            }
            
            # Call API
            result = call_api(request_data)
            
            if result:
                # Update progress
                progress_container.empty()
                with progress_container:
                    show_agent_status("researcher", "Completed research", True)
                    show_agent_status("budget", "Completed budget analysis", True)
                    show_agent_status("planner", "Completed itinerary", True)
                
                st.success("✅ Trip planning completed!")
                
                # Display itinerary
                if result.get("itinerary"):
                    display_itinerary(result["itinerary"])
                    
                    # Download button
                    itinerary_json = json.dumps(result["itinerary"], indent=2)
                    st.download_button(
                        label="📥 Download Itinerary (JSON)",
                        data=itinerary_json,
                        file_name=f"itinerary_{user_inputs['destination'].lower().replace(' ', '_')}.json",
                        mime="application/json"
                    )
                else:
                    st.warning("⚠️ No itinerary was generated")
                
                # Show error if any
                if result.get("error"):
                    st.error(f"❌ Error: {result['error']}")
    
    else:
        # Welcome message
        st.markdown("""
            <div style='background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                <h2 style='color: #667eea;'>👋 Welcome to AI Trip Planner!</h2>
                <p style='font-size: 1.1rem; color: #666;'>
                    Our intelligent multi-agent system will help you plan the perfect trip:
                </p>
                <ul style='font-size: 1rem; color: #666; line-height: 2;'>
                    <li>🔍 <strong>Researcher Agent</strong> - Finds real attractions using live APIs</li>
                    <li>💰 <strong>Budget Agent</strong> - Analyzes costs with real 2024 data</li>
                    <li>📋 <strong>Planner Agent</strong> - Creates personalized day-by-day itineraries</li>
                </ul>
                <p style='font-size: 1.1rem; color: #667eea; margin-top: 1.5rem;'>
                    👈 Fill in your preferences in the sidebar and click "Plan My Trip" to get started!
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Features
        st.markdown("---")
        st.markdown("### ✨ Features")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
                <div style='background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); padding: 1.5rem; border-radius: 12px; text-align: center;'>
                    <h3>🌐 Live Data</h3>
                    <p>Real-time attraction data from OpenTripMap API</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div style='background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); padding: 1.5rem; border-radius: 12px; text-align: center;'>
                    <h3>💵 Real Costs</h3>
                    <p>Accurate 2024 pricing from Numbeo & Budget Your Trip</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div style='background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%); padding: 1.5rem; border-radius: 12px; text-align: center;'>
                    <h3>🤖 AI Agents</h3>
                    <p>Multi-agent collaboration with LangGraph</p>
                </div>
            """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
