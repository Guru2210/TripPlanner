"""
Itinerary display component - Updated for structured data
"""
import streamlit as st


def display_itinerary(itinerary_data: dict):
    """
    Display the complete itinerary in a beautiful format
    
    Args:
        itinerary_data: Itinerary dictionary from backend
    """
    
    if not itinerary_data:
        st.warning("No itinerary data available")
        return
    
    # Header
    st.markdown("# 🗺️ Your Personalized Itinerary")
    st.markdown("---")
    
    # Trip overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📍 Destination", itinerary_data.get("destination", "N/A"))
    
    with col2:
        num_days = itinerary_data.get('num_days', itinerary_data.get('duration_days', 0))
        st.metric("📅 Duration", f"{num_days} days")
    
    with col3:
        total_budget = itinerary_data.get('total_budget', itinerary_data.get('budget_usd', 0))
        st.metric("💰 Budget", f"${total_budget:,.0f}")
    
    with col4:
        st.metric("✨ Style", itinerary_data.get("travel_style", "N/A").title())
    
    # Cost summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_cost = itinerary_data.get('total_cost', 0)
        st.metric("💵 Total Cost", f"${total_cost:,.0f}")
    
    with col2:
        budget_status = itinerary_data.get('budget_status', 'unknown')
        status_emoji = "✅" if budget_status == "within_budget" else "⚠️"
        st.metric(f"{status_emoji} Budget Status", budget_status.replace('_', ' ').title())
    
    with col3:
        if total_cost and total_budget:
            savings = total_budget - total_cost
            st.metric("💰 Savings", f"${savings:,.0f}")
    
    st.markdown("---")
    
    # Day plans
    day_plans = itinerary_data.get('day_plans', [])
    
    if day_plans:
        st.markdown("## 📅 Day-by-Day Itinerary")
        
        for day_plan in day_plans:
            display_day_plan(day_plan)
    else:
        # Fallback to text-based itinerary
        itinerary_text = itinerary_data.get("itinerary_text", "")
        if itinerary_text:
            st.markdown("## 📋 Itinerary Details")
            st.markdown(itinerary_text)
        else:
            st.info("No detailed itinerary available")
    
    # Recommendations
    recommendations = itinerary_data.get('recommendations', [])
    if recommendations:
        st.markdown("---")
        st.markdown("## 💡 Recommendations & Tips")
        for rec in recommendations:
            st.markdown(f"- {rec}")
    
    # Data sources
    st.markdown("---")
    st.caption(f"🕐 Created: {itinerary_data.get('created_at', 'N/A')}")


def display_day_plan(day_plan: dict):
    """
    Display a single day plan with activities
    
    Args:
        day_plan: Day plan dictionary
    """
    
    day_num = day_plan.get('day', '?')
    daily_cost = day_plan.get('daily_cost', 0)
    summary = day_plan.get('summary', '')
    date = day_plan.get('date', '')
    
    # Create expander for the day
    title = f"📅 Day {day_num}"
    if date:
        title += f" - {date}"
    title += f" (${daily_cost:,.0f})"
    
    with st.expander(title, expanded=True):
        # Summary
        if summary:
            st.markdown(f"**{summary}**")
            st.markdown("")
        
        # Activities
        activities = day_plan.get('activities', [])
        
        if activities:
            for idx, activity in enumerate(activities, 1):
                display_activity(activity, idx)
        else:
            st.info("No activities planned for this day")
        
        # Daily cost
        st.markdown("---")
        st.markdown(f"**💵 Daily Total: ${daily_cost:,.0f}**")


def display_activity(activity: dict, idx: int):
    """
    Display a single activity
    
    Args:
        activity: Activity dictionary
        idx: Activity index
    """
    
    name = activity.get('name', 'Activity')
    time = activity.get('time', '')
    duration = activity.get('duration_hours', 0)
    cost = activity.get('cost_usd', 0)
    description = activity.get('description', '')
    reasoning = activity.get('reasoning', '')
    
    # Activity card
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
                padding: 1rem; 
                border-radius: 10px; 
                margin-bottom: 1rem;
                border-left: 4px solid #667eea;'>
        <h4 style='margin: 0; color: #667eea;'>⏰ {time} - {name}</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Details
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if description:
            st.markdown(f"📝 {description}")
        if reasoning:
            st.markdown(f"💡 *Why: {reasoning}*")
    
    with col2:
        st.markdown(f"**⏱️ {duration}h**")
        st.markdown(f"**💵 ${cost:,.0f}**")
    
    st.markdown("")
