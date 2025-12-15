"""
Progress tracking component
"""
import streamlit as st
import time


def show_progress(status: str, agent: str = ""):
    """
    Show progress indicator for agent execution
    
    Args:
        status: Current status message
        agent: Current agent name
    """
    
    agent_emojis = {
        "researcher": "🔍",
        "budget": "💰",
        "planner": "📋"
    }
    
    emoji = agent_emojis.get(agent.lower(), "⚙️")
    
    with st.container():
        st.markdown(f"### {emoji} {agent.title()} Agent")
        st.info(status)
        st.progress(0.33 if agent == "researcher" else 0.66 if agent == "budget" else 1.0)


def show_agent_status(agent: str, message: str, completed: bool = False):
    """
    Show agent status with icon
    
    Args:
        agent: Agent name
        message: Status message
        completed: Whether the agent has completed
    """
    
    icons = {
        "researcher": "🔍",
        "budget": "💰",
        "planner": "📋"
    }
    
    icon = icons.get(agent.lower(), "⚙️")
    status_icon = "✅" if completed else "⏳"
    
    st.markdown(f"{status_icon} **{icon} {agent.title()}**: {message}")


def show_loading_animation():
    """Show loading animation"""
    with st.spinner("🌍 Planning your perfect trip..."):
        time.sleep(0.5)
