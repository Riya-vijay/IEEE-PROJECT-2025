import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'student_points' not in st.session_state:
    st.session_state.student_points = {}
if 'mental_health_data' not in st.session_state:
    st.session_state.mental_health_data = {}
if 'last_login' not in st.session_state:
    st.session_state.last_login = {}

# All data in one file
STUDENT_PROFILES = {
    "4AD23EC079": {
        "name": "Team Leader", 
        "department": "ECE", 
        "points": 100,
        "avatar": "👨‍💻",
        "joined_date": "2023-08-01"
    },
    "4AD23EC080": {
        "name": "V V RIYA VIJAY", 
        "department": "ECE", 
        "points": 85,
        "avatar": "👩‍🎓",
        "joined_date": "2023-08-01"
    },
    "4AD23CS075": {
        "name": "Yeshaswini Madhumita", 
        "department": "CS-Design", 
        "points": 95,
        "avatar": "👩‍💻",
        "joined_date": "2023-08-01"
    },
    "4AD23EC081": {
        "name": "Sandesh Mrashi", 
        "department": "ECE", 
        "points": 78,
        "avatar": "👨‍🔬",
        "joined_date": "2023-08-01"
    }
}

ATME_KNOWLEDGE = {
    "When are semester exams?": "📚 **Exams start December 8th, 2025**. Check department notice board for detailed timetable.",
    "IEEE exhibition details": "🎯 **IEEE Mini Project Exhibition TOMORROW!** ⏰ 10:00 AM | 🏛️ College Auditorium | 🏆 Exciting prizes!",
    "Library timings": "📖 **Library Hours**: Mon-Fri: 8:00 AM - 8:00 PM | Sat: 9:00 AM - 5:00 PM | Sun: Closed",
    "Hostel facilities": "🏠 **Hostels**: Separate for boys/girls | ✅ WiFi | ✅ Mess | ✅ 24/7 Security | 📞 Warden: 0821-1234567",
    "Cafeteria timings": "🍽️ **Cafeteria**: 8:00 AM - 8:00 PM | 🎯 Student discounts available",
    "ECE lab schedules": "🔬 **ECE Labs**: Mon/Wed/Fri: 9:00 AM - 5:00 PM | Tue/Thu: Practical sessions",
    "Contact HOD of ECE": "👩‍🏫 **HOD ECE**: Dr. Priya Sharma | 🏢 Block B, 1st Floor | 📧 hod.ece@atme.edu",
    "Placement preparation": "💼 **Placement Cell**: Regular training sessions | 📊 Mock interviews | 📝 Resume building workshops",
    "Fee structure": "💰 **Fee Details**: Engineering: ₹85,000/semester | Hostel: ₹60,000/year | Mess: ₹25,000/semester",
    "Sports facilities": "⚽ **Sports Complex**: Cricket ground | Basketball court | Gym | Indoor games | 🏆 Annual sports week",
    "Bus timings": "🚌 **College Bus**: First bus: 7:30 AM | Last bus: 6:30 PM | Routes cover major areas of Mysore"
}

# Enhanced predictive questions with categories
PREDICTIVE_QUESTIONS = {
    "academics": ["When are semester exams?", "How to download hall ticket?", "Exam time table", "Revaluation process"],
    "facilities": ["Library timings", "Hostel facilities", "Cafeteria timings", "Sports facilities", "Bus timings"],
    "departments": ["ECE lab schedules", "Contact HOD of ECE", "CSE lab schedules", "Placement preparation"],
    "events": ["IEEE exhibition details", "Upcoming college events", "Cultural fest dates", "Technical workshops"]
}

# Mental health resources
MENTAL_HEALTH_TIPS = [
    "🧘 **Take deep breaths** - 4 seconds in, 4 seconds hold, 6 seconds out",
    "📝 **Journal your thoughts** - Writing helps clear your mind",
    "🚶 **Take a walk** - Even 10 minutes can refresh your mind",
    "💤 **Prioritize sleep** - 7-8 hours improves focus and mood",
    "🎵 **Listen to music** - Calming music reduces stress",
    "🍎 **Eat healthy snacks** - Nutrition affects mental health",
    "📞 **Talk to friends** - Social connections are important"
]

# Gamification achievements
ACHIEVEMENTS = {
    "first_chat": {"name": "First Conversation", "points": 20, "icon": "💬"},
    "daily_user": {"name": "Daily User", "points": 15, "icon": "🔥"},
    "wellness_warrior": {"name": "Wellness Warrior", "points": 30, "icon": "🧠"},
    "question_master": {"name": "Question Master", "points": 25, "icon": "❓"},
    "chat_champion": {"name": "Chat Champion", "points": 50, "icon": "🏆"}
}

def check_achievements(usn, action):
    """Award achievements based on user actions"""
    achievements_unlocked = []
    
    if action == "first_chat" and usn not in st.session_state.get('unlocked_achievements', {}):
        achievements_unlocked.append(ACHIEVEMENTS["first_chat"])
        STUDENT_PROFILES[usn]["points"] += 20
    
    if action == "wellness_check":
        achievements_unlocked.append(ACHIEVEMENTS["wellness_warrior"])
        STUDENT_PROFILES[usn]["points"] += 30
    
    return achievements_unlocked

def get_personalized_welcome(usn):
    """Generate personalized welcome message"""
    profile = STUDENT_PROFILES[usn]
    hour = datetime.now().hour
    
    if hour < 12:
        greeting = "🌅 Good morning"
    elif hour < 17:
        greeting = "☀️ Good afternoon"
    else:
        greeting = "🌙 Good evening"
    
    return f"{greeting}, {profile['name']}! {profile['avatar']}"

def show_mental_health_dashboard(usn):
    """Display mental health dashboard"""
    st.sidebar.markdown("---")
    st.sidebar.subheader("🧠 Wellness Center")
    
    # Mood tracker
    mood = st.sidebar.select_slider(
        "How are you feeling today?",
        options=["😔 Really stressed", "😟 Anxious", "😐 Okay", "😊 Good", "🤩 Excellent!"],
        value="😐 Okay"
    )
    
    if st.sidebar.button("💝 Update Wellness & Get Points"):
        STUDENT_PROFILES[usn]["points"] += 15
        st.sidebar.success("+15 wellness points! 🎉")
        check_achievements(usn, "wellness_check")
        
        # Show mental health tip
        tip = random.choice(MENTAL_HEALTH_TIPS)
        st.sidebar.info(f"**Wellness Tip**: {tip}")
    
    # Quick stress reliever
    if st.sidebar.button("🚨 Quick Stress Buster"):
        with st.sidebar:
            st.info("🧘 **5-4-3-2-1 Grounding Technique**")
            st.write("Look around and find:")
            st.write("5 things you can **see**")
            st.write("4 things you can **touch**")
            st.write("3 things you can **hear**")
            st.write("2 things you can **smell**")
            st.write("1 thing you can **taste**")

def show_analytics_dashboard(usn):
    """Show personalized analytics"""
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Your Analytics")
    
    # Points progress
    profile = STUDENT_PROFILES[usn]
    points = profile["points"]
    
    # Progress to next level
    next_level = (points // 100 + 1) * 100
    progress = (points % 100) / 100
    
    st.sidebar.write(f"**Level**: {points // 100 + 1}")
    st.sidebar.progress(progress)
    st.sidebar.write(f"**{points}** / **{next_level}** points to next level")
    
    # Study time suggestion based on time
    hour = datetime.now().hour
    if 6 <= hour < 12:
        study_tip = "📚 **Morning Study Tip**: Perfect time for complex subjects!"
    elif 12 <= hour < 18:
        study_tip = "☀️ **Afternoon Tip**: Good for practical sessions and labs"
    else:
        study_tip = "🌙 **Evening Tip**: Review and revision time"
    
    st.sidebar.info(study_tip)

def show_visual_response(question, answer):
    """Create visual responses for certain questions"""
    if "exam" in question.lower():
        # Create exam countdown
        exam_date = datetime(2025, 12, 8)
        today = datetime.now()
        days_left = (exam_date - today).days
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = days_left,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': f"Days until Exams"},
            delta = {'reference': days_left + 1},
            gauge = {
                'axis': {'range': [None, 365]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 100], 'color': "lightgray"},
                    {'range': [100, 200], 'color': "gray"}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 30}}))
        
        st.plotly_chart(fig, use_container_width=True)
    
    elif "points" in question.lower() or "leaderboard" in question.lower():
        # Show points distribution
        points_data = []
        for usn, profile in STUDENT_PROFILES.items():
            points_data.append({
                "Student": profile["name"],
                "Points": profile["points"],
                "Department": profile["department"]
            })
        
        df = pd.DataFrame(points_data)
        fig = px.bar(df, x="Student", y="Points", color="Department",
                    title="🏆 Points Leaderboard Distribution")
        st.plotly_chart(fig, use_container_width=True)

def main():
    # Enhanced page config
    st.set_page_config(
        page_title="ATME Smart Assistant 🤖", 
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for amazing look
    st.markdown("""
    <style>
    .main-header {
        font-size: 3.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .welcome-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 20px;
        color: white;
        margin: 10px 0;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    .points-card {
        background: linear-gradient(135deg, #10B981 0%, #047857 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .department-card {
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
    }
    .chat-bubble-user {
        background: linear-gradient(135deg, #3B82F6 0%, #1D4ED8 100%);
        color: white;
        padding: 15px;
        border-radius: 20px 20px 5px 20px;
        margin: 10px 0;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .chat-bubble-bot {
        background: linear-gradient(135deg, #E5E7EB 0%, #D1D5DB 100%);
        color: black;
        padding: 15px;
        border-radius: 20px 20px 20px 5px;
        margin: 10px 0;
        max-width: 80%;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .question-button {
        background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
        color: white;
        border: none;
        padding: 12px;
        border-radius: 10px;
        margin: 5px;
        width: 100%;
        cursor: pointer;
    }
    .question-button:hover {
        background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header with animated title
    st.markdown('<h1 class="main-header">ATME College Smart Assistant 🚀</h1>', unsafe_allow_html=True)
    
    # Student login section
    col1, col2 = st.columns([1, 2])
    with col1:
        usn = st.text_input("🎯 Enter your USN:", "4AD23EC079", help="Use format: 4AD23EC079").upper()
    
    if usn in STUDENT_PROFILES:
        profile = STUDENT_PROFILES[usn]
        
        # Welcome section with cards
        welcome_col1, welcome_col2, welcome_col3 = st.columns(3)
        
        with welcome_col1:
            st.markdown(f'''
            <div class="welcome-card">
                <h3>👋 {get_personalized_welcome(usn)}</h3>
                <p>Ready to ace your day?</p>
            </div>
            ''', unsafe_allow_html=True)
        
        with welcome_col2:
            st.markdown(f'''
            <div class="points-card">
                <h3>🏆 {profile["points"]} POINTS</h3>
                <p>Keep climbing! 🚀</p>
            </div>
            ''', unsafe_allow_html=True)
        
        with welcome_col3:
            st.markdown(f'''
            <div class="department-card">
                <h3>🎯 {profile['department']}</h3>
                <p>Semester 3</p>
            </div>
            ''', unsafe_allow_html=True)
        
        # Main content area
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("💬 Smart Chat Interface")
            
            # Enhanced predictive questions with categories
            st.write("**🚀 Quick Questions (Smart Suggestions):**")
            
            # Show questions by category
            for category, questions in PREDICTIVE_QUESTIONS.items():
                with st.expander(f"📁 {category.title()} Questions"):
                    cols = st.columns(2)
                    for i, question in enumerate(questions[:4]):  # Show first 4 questions per category
                        with cols[i % 2]:
                            if st.button(f"❓ {question}", key=f"cat_{category}_{i}"):
                                # Add to chat history
                                st.session_state.chat_history.append({"user": question, "bot": ATME_KNOWLEDGE.get(question, "I'm learning! Ask college admin."), "time": datetime.now()})
                                STUDENT_PROFILES[usn]["points"] += 3
                                check_achievements(usn, "first_chat")
            
            # Manual question input
            st.subheader("🔍 Ask Anything")
            user_question = st.text_input("Type your question about ATME College:", 
                                         placeholder="e.g., When is the next cultural fest?")
            
            if user_question:
                # Simulate AI thinking
                with st.spinner("🤔 Thinking..."):
                    time.sleep(1)
                
                # Get answer
                answer = ATME_KNOWLEDGE.get(user_question, 
                                          "I'm still learning about this! Please check with the college administration or notice boards for the most accurate information.")
                
                # Add to chat history
                st.session_state.chat_history.append({
                    "user": user_question, 
                    "bot": answer, 
                    "time": datetime.now()
                })
                
                STUDENT_PROFILES[usn]["points"] += 2
            
            # Display chat history
            st.subheader("📜 Conversation History")
            for chat in reversed(st.session_state.chat_history[-10:]):  # Show last 10 messages
                st.markdown(f'<div class="chat-bubble-user">👤 {chat["user"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="chat-bubble-bot">🤖 {chat["bot"]}</div>', unsafe_allow_html=True)
                
                # Show visual responses for specific questions
                show_visual_response(chat["user"], chat["bot"])
                
                st.markdown(f'<small>⏰ {chat["time"].strftime("%H:%M")}</small>', unsafe_allow_html=True)
                st.markdown("---")
        
        with col2:
            # Sidebar features
            show_mental_health_dashboard(usn)
            show_analytics_dashboard(usn)
            
            # Enhanced leaderboard
            st.subheader("🏆 Live Leaderboard")
            leaderboard_data = []
            for usn_code, student_profile in STUDENT_PROFILES.items():
                leaderboard_data.append({
                    "Rank": "",
                    "Student": f"{student_profile['avatar']} {student_profile['name']}",
                    "Department": student_profile['department'],
                    "Points": student_profile['points']
                })
            
            leaderboard_df = pd.DataFrame(leaderboard_data)
            leaderboard_df = leaderboard_df.sort_values("Points", ascending=False)
            leaderboard_df["Rank"] = [f"🥇" if i == 0 else f"🥈" if i == 1 else f"🥉" if i == 2 else f"{i+1}." for i in range(len(leaderboard_df))]
            
            st.dataframe(leaderboard_df[["Rank", "Student", "Points"]], use_container_width=True, hide_index=True)
            
            # Daily challenge
            st.subheader("🎯 Daily Challenge")
            challenge = random.choice([
                "Ask 3 questions today! +15 points",
                "Complete wellness check! +10 points", 
                "Help a friend with college info! +20 points",
                "Share feedback about chatbot! +10 points"
            ])
            st.info(f"**Today's Mission**: {challenge}")
            
            if st.button("✅ Claim Challenge Reward"):
                STUDENT_PROFILES[usn]["points"] += random.randint(10, 25)
                st.success("🎉 Challenge completed! Points added!")
    
    else:
        st.error("❌ USN not found. Please check your USN or contact administration.")
        
        # Show available USNs for demo
        st.info("**Demo USNs**: 4AD23EC079, 4AD23EC080, 4AD23CS075, 4AD23EC081")

if __name__ == "__main__":
    main()# IEEE-PROJECT-2025
multilingual chatbot for student Queries
