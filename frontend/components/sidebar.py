"""
Sidebar component for user input
"""
import streamlit as st


def render_sidebar():
    """Render the sidebar with input form"""
    
    with st.sidebar:
        st.markdown("## 🌍 Trip Preferences")
        st.markdown("---")
        
        # Destination input
        destination = st.text_input(
            "📍 Destination",
            placeholder="e.g., Paris, Tokyo, New York",
            help="Enter the city you want to visit"
        )
        
        # Number of days
        num_days = st.number_input(
            "📅 Number of Days",
            min_value=1,
            max_value=30,
            value=4,
            help="How many days will you be traveling?"
        )
        
        # Budget
        budget = st.number_input(
            "💰 Budget (USD)",
            min_value=100,
            max_value=50000,
            value=2500,
            step=100,
            help="Your total budget for the trip"
        )
        
        # Travel style
        travel_style = st.selectbox(
            "✨ Travel Style",
            options=["budget", "mid-range", "luxury"],
            index=1,
            help="Choose your preferred travel style"
        )
        
        # Interests
        st.markdown("### 🎯 Interests")
        interests = []
        
        col1, col2 = st.columns(2)
        with col1:
            if st.checkbox("Museums", value=True):
                interests.append("museums")
            if st.checkbox("Landmarks", value=True):
                interests.append("landmarks")
            if st.checkbox("Food", value=True):
                interests.append("food")
            if st.checkbox("Nature"):
                interests.append("nature")
        
        with col2:
            if st.checkbox("Shopping"):
                interests.append("shopping")
            if st.checkbox("Nightlife"):
                interests.append("nightlife")
            if st.checkbox("Culture"):
                interests.append("culture")
            if st.checkbox("Adventure"):
                interests.append("adventure")
        
        st.markdown("---")
        
        # Plan button
        plan_button = st.button(
            "🚀 Plan My Trip",
            use_container_width=True,
            type="primary"
        )
        
        return {
            "destination": destination,
            "num_days": num_days,
            "budget": budget,
            "travel_style": travel_style,
            "interests": interests if interests else ["museums"],
            "plan_button": plan_button
        }
