# frontend.py
import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import requests
import json

# Backend API configuration
BACKEND_URL = "http://localhost:5000/api"

# Initialize session state
if 'student_data' not in st.session_state:
    st.session_state.student_data = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'achievements' not in st.session_state:
    st.session_state.achievements = []
if 'leaderboard' not in st.session_state:
    st.session_state.leaderboard = []
if 'mood_data' not in st.session_state:
    st.session_state.mood_data = []
if 'last_login' not in st.session_state:
    st.session_state.last_login = None
if 'study_timer' not in st.session_state:
    st.session_state.study_timer = None
if 'notes' not in st.session_state:
    st.session_state.notes = []
if 'todo_list' not in st.session_state:
    st.session_state.todo_list = []
if 'resource_links' not in st.session_state:
    st.session_state.resource_links = []

# Department options for ATME
DEPARTMENTS = [
    "Select Department",
    "Computer Science and Engineering (CSE)",
    "Electronics and Communication Engineering (ECE)", 
    "Data Science",
    "Artificial Intelligence and Machine Learning (AIML)",
    "Cyber Security",
    "Mechanical Engineering",
    "Civil Engineering",
    "Electrical and Electronics Engineering (EEE)",
    "Computer Science and Design (CSD)"
]

# Enhanced Knowledge Base with more topics
ATME_KNOWLEDGE = {
    "hello": "👋 **Hello! I'm ATME College Assistant!** 🤖\n\nI can help you with:\n• 📚 Academic information\n• 🏫 College facilities\n• 🎯 Department details\n• 🎉 Events and activities\n• 💼 Placement information\n• 🧠 Mental health support\n• ⏰ Study timer & tools\n• 📝 Notes & To-do lists\n\nWhat would you like to know?",
    
    "hi": "👋 **Hi there! Welcome to ATME College!** 🎓\n\nI'm here to help you with any questions about our college. Ask me about exams, facilities, departments, or events!",
    
    "college address": "🏫 **ATME College of Engineering**\n📍 **Address:** Adichunchanagiri Road, Mysuru - 570028, Karnataka\n🌍 **Location:** Near BGS Health Centre, Mysuru\n📞 **Phone:** 0821-1234567\n🕒 **Office Hours:** 9:00 AM - 5:00 PM (Mon-Sat)",
    
    "contact information": "📞 **ATME Contact Details:**\n• **College Office:** 0821-1234567\n• **Principal Office:** 0821-1234568\n• **Admission Office:** 0821-1234569\n• **Email:** info@atme.edu.in\n• **Website:** www.atme.edu.in\n• **Emergency:** 0821-1234580",
    
    "academic calendar": "📅 **Academic Year 2024-25**\n\n**Odd Semester (2024):**\n• Semester Start: August 1, 2024\n• Mid-term Exams: October 15-30, 2024\n• End Semester Exams: December 8-23, 2024\n• Winter Break: December 24 - January 5, 2025\n\n**Even Semester (2025):**\n• Semester Start: January 6, 2025\n• Mid-term Exams: March 15-30, 2025\n• End Semester Exams: May 15-30, 2025\n• Summer Break: June 1 - July 31, 2025",
    
    "exam dates": "📚 **Semester Exams Schedule 2024-25:**\n\n**Odd Semester Exams:**\n• Theory Exams: December 8-23, 2024\n• Practical Exams: December 1-7, 2024\n• Project Evaluation: December 1-10, 2024\n\n**Even Semester Exams:**\n• Theory Exams: May 15-30, 2025\n• Practical Exams: May 8-14, 2025\n• Project Evaluation: May 8-17, 2025",
    
    "library information": "📖 **ATME Central Library**\n\n**⏰ Timings:**\n• Monday-Friday: 8:00 AM - 8:00 PM\n• Saturday: 9:00 AM - 5:00 PM\n• Sunday: Closed\n\n**📚 Collection:**\n• 50,000+ Books\n• 100+ National & International Journals\n• 5000+ E-books\n• 50+ Online Databases",
    
    "hostel facilities": "🏠 **ATME Hostels**\n\n**Accommodation:**\n• Separate hostels for Boys & Girls\n• Single, Double, Triple occupancy rooms\n• 24/7 Security & CCTV surveillance\n• Wi-Fi enabled campuses\n\n**💵 Fee Structure (Per Year):**\n• Hostel Fee: ₹45,000\n• Mess Charges: ₹15,000\n• **Total: ₹60,000**",
    
    "placement information": "💼 **Training & Placement Cell**\n\n**👨‍🏫 TPO:** Dr. S. R. Kumar\n**🏢 Office:** Placement Block, Ground Floor\n**📞 Phone:** 0821-1234573\n**📧 Email:** placement@atme.edu.in\n\n**🏢 Recruiting Companies:**\n• **IT Giants:** Infosys, Wipro, TCS, IBM, Accenture\n• **Core Companies:** Intel, Texas Instruments, L&T, Bosch\n\n**📊 Placement Statistics (2023):**\n• 85% Placement Rate\n• Highest Package: ₹18 LPA\n• Average Package: ₹6.5 LPA",
    
    "cse department": "💻 **Computer Science & Engineering**\n\n**👨‍🏫 HOD:** Dr. Suresh Kumar\n**📧 Email:** hod.cse@atme.edu.in\n**🏢 Office:** CSE Block, 1st Floor\n**📞 Phone:** 0821-1234575\n\n**🎯 Specializations:**\n• Artificial Intelligence & Machine Learning\n• Data Science\n• Cyber Security\n• Full Stack Development\n• Cloud Computing",
    
    "study tips": "📚 **Effective Study Tips:**\n\n• 🕒 **Pomodoro Technique:** Study 25 mins, break 5 mins\n• 📝 **Active Recall:** Test yourself frequently\n• 🔄 **Spaced Repetition:** Review material over time\n• 🎯 **Set Clear Goals:** Specific, measurable targets\n• 🏃 **Take Breaks:** Refresh your mind regularly\n• 💧 **Stay Hydrated:** Drink water while studying\n• 🚫 **Avoid Multitasking:** Focus on one task at a time",
    
    "time management": "⏰ **Time Management Tips:**\n\n• 📅 **Use a Planner:** Schedule your study sessions\n• 🎯 **Priority Matrix:** Urgent vs Important tasks\n• ⏱️ **Time Blocking:** Dedicate blocks for specific tasks\n• 🚀 **Eat the Frog:** Do hardest tasks first\n• 📊 **Track Time:** Use timers to monitor progress\n• 🔄 **Weekly Review:** Plan your upcoming week",
    
    "career guidance": "🎯 **Career Development Tips:**\n\n• 💼 **Build Portfolio:** Work on real projects\n• 🔗 **Networking:** Connect with alumni & professionals\n• 📄 **Resume Building:** Keep updating your resume\n• 🎤 **Soft Skills:** Develop communication skills\n• 🌐 **Online Presence:** LinkedIn & GitHub profiles\n• 📚 **Continuous Learning:** Learn new technologies",
    
    "mental health": "🧠 **Mental Wellness Tips:**\n\n• 🧘 **Mindfulness:** Practice meditation daily\n• 🏃 **Exercise:** Physical activity reduces stress\n• 😴 **Sleep Well:** 7-8 hours of quality sleep\n• 🍎 **Healthy Diet:** Nutritious food for brain health\n• 👥 **Social Connection:** Talk to friends & family\n• 🎨 **Hobbies:** Engage in creative activities\n• 🆘 **Seek Help:** College counselor available"
}

# Department themes with vibrant colors
DEPARTMENT_THEMES = {
    "CSE": {
        "color": "#FF6B6B", 
        "emoji": "💻", 
        "bg_gradient": "linear-gradient(135deg, #FF6B6B 0%, #FF8E8E 100%)",
        "secondary": "linear-gradient(135deg, #FFE8E8 0%, #FFF5F5 100%)"
    },
    "ECE": {
        "color": "#4ECDC4", 
        "emoji": "🔬", 
        "bg_gradient": "linear-gradient(135deg, #4ECDC4 0%, #67E6DC 100%)",
        "secondary": "linear-gradient(135deg, #E8FDFB 0%, #F5FFFE 100%)"
    },
    "Data Science": {
        "color": "#45B7D1", 
        "emoji": "📊", 
        "bg_gradient": "linear-gradient(135deg, #45B7D1 0%, #67C8E6 100%)",
        "secondary": "linear-gradient(135deg, #E8F7FC 0%, #F5FBFF 100%)"
    },
    "AIML": {
        "color": "#96CEB4", 
        "emoji": "🤖", 
        "bg_gradient": "linear-gradient(135deg, #96CEB4 0%, #B4E6C8 100%)",
        "secondary": "linear-gradient(135deg, #F0F9F4 0%, #F7FCF9 100%)"
    },
    "Cyber Security": {
        "color": "#FECA57", 
        "emoji": "🛡️", 
        "bg_gradient": "linear-gradient(135deg, #FECA57 0%, #FFE08A 100%)",
        "secondary": "linear-gradient(135deg, #FFF9E8 0%, #FFFCF5 100%)"
    }
}

# Study resources by department
STUDY_RESOURCES = {
    "CSE": [
        {"name": "Python Programming", "url": "https://www.python.org", "type": "🌐 Website"},
        {"name": "Java Tutorial", "url": "https://www.w3schools.com/java", "type": "📚 Tutorial"},
        {"name": "Data Structures", "url": "https://www.geeksforgeeks.org", "type": "📖 Guide"},
        {"name": "Web Development", "url": "https://developer.mozilla.org", "type": "🔧 Resource"}
    ],
    "ECE": [
        {"name": "Electronics Tutorials", "url": "https://www.electronics-tutorials.ws", "type": "📚 Tutorial"},
        {"name": "Circuit Design", "url": "https://www.circuitlab.com", "type": "🔧 Tool"},
        {"name": "Arduino Projects", "url": "https://www.arduino.cc", "type": "⚡ Projects"}
    ],
    "Data Science": [
        {"name": "Kaggle", "url": "https://www.kaggle.com", "type": "🏆 Competitions"},
        {"name": "Towards Data Science", "url": "https://towardsdatascience.com", "type": "📚 Blog"},
        {"name": "DataCamp", "url": "https://www.datacamp.com", "type": "🎓 Courses"}
    ]
}

# SIMPLE OFFLINE FUNCTIONS
def offline_register_student(usn: str, name: str, department: str):
    student_data = {
        "usn": usn, "name": name, "department": department,
        "points": 100, "level": 1, "avatar": "🎓"
    }
    return student_data

def offline_send_chat_message(usn: str, message: str):
    user_message_lower = message.lower()
    response = ATME_KNOWLEDGE.get(user_message_lower, 
        "I'm in offline mode. Please start backend server for full functionality.")
    return {"response": response, "points_earned": 2}

# BACKEND-ENABLED FUNCTIONS
def register_student(usn: str, name: str, department: str):
    try:
        response = requests.post(f"{BACKEND_URL}/register", json={
            "usn": usn, "name": name, "department": department
        }, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("student_data")
        else:
            return offline_register_student(usn, name, department)
    except:
        return offline_register_student(usn, name, department)

def send_chat_message(usn: str, message: str):
    try:
        response = requests.post(f"{BACKEND_URL}/chat/send", json={
            "usn": usn, "message": message
        }, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return offline_send_chat_message(usn, message)
    except:
        return offline_send_chat_message(usn, message)

def update_mood(usn: str, mood: str):
    return {"message": "Mood updated! 🌈", "points_earned": 8}

def get_chat_history(usn: str):
    return st.session_state.chat_history

def get_achievements(usn: str):
    return st.session_state.achievements

def get_leaderboard():
    if st.session_state.student_data:
        return [
            {"name": "Riya Vijay", "department": "ECE", "points": 185},
            {"name": "Yeshaswini", "department": "CSE", "points": 167},
            {"name": st.session_state.student_data["name"], 
             "department": st.session_state.student_data["department"], 
             "points": st.session_state.student_data["points"]},
            {"name": "Sandesh", "department": "ECE", "points": 142},
            {"name": "Aryan", "department": "Mechanical", "points": 128}
        ]
    return []

def claim_daily_bonus(usn: str):
    return {"message": "Daily bonus claimed! 🎁", "points_earned": 10}

def get_department_theme(department):
    for dept, theme in DEPARTMENT_THEMES.items():
        if dept in department:
            return theme
    return {
        "color": "#667eea", 
        "emoji": "🎓", 
        "bg_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "secondary": "linear-gradient(135deg, #F0F4FF 0%, #F8FAFF 100%)"
    }

def create_progress_chart(points, level):
    progress = (points % 100)
    fig = go.Figure(go.Indicator(
        mode = "gauge+number", value = progress,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"Level {level} Progress"},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "#667eea"},
            'steps': [{'range': [0, 50], 'color': "lightgray"},
                     {'range': [50, 100], 'color': "gray"}]
        }))
    fig.update_layout(height=250, margin=dict(t=50, b=10, l=10, r=10))
    return fig

def check_backend_health():
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

# NEW FEATURES
def start_study_timer():
    st.session_state.study_timer = {
        'start_time': datetime.now(),
        'running': True,
        'duration': 0
    }

def stop_study_timer():
    if st.session_state.study_timer:
        st.session_state.study_timer['running'] = False
        duration = (datetime.now() - st.session_state.study_timer['start_time']).seconds // 60
        st.session_state.study_timer['duration'] = duration
        return duration
    return 0

def add_note(title, content):
    st.session_state.notes.append({
        'id': len(st.session_state.notes) + 1,
        'title': title,
        'content': content,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M"),
        'category': 'General'
    })

def add_todo(task):
    st.session_state.todo_list.append({
        'id': len(st.session_state.todo_list) + 1,
        'task': task,
        'completed': False,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M")
    })

def get_study_resources(department):
    dept_key = next((key for key in STUDY_RESOURCES.keys() if key in department), "CSE")
    return STUDY_RESOURCES.get(dept_key, [])

def main():
    st.set_page_config(
        page_title="ATME College Assistant", 
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Check backend status
    backend_online = check_backend_health()
    
    # Enhanced Custom CSS
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
        animation: gradientShift 8s ease infinite;
    }
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .atme-card {
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin: 10px 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    .atme-card:hover {
        transform: translateY(-5px);
    }
    .feature-card {
        background: white;
        padding: 15px;
        border-radius: 10px;
        margin: 8px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    .timer-display {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #667eea;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Backend status
    if backend_online:
        st.sidebar.success("✅ Backend: ONLINE")
    else:
        st.sidebar.warning("⚠️ Backend: OFFLINE")
        st.sidebar.info("Run `python backend.py` for full features!")
    
    # Header
    st.markdown('<h1 class="main-header">🎓 ATME College Smart Assistant ⚡</h1>', unsafe_allow_html=True)
    
    # Student registration
    col1, col2, col3 = st.columns(3)
    with col1:
        student_name = st.text_input("👤 Your Name:", value="ATME Student")
    with col2:
        student_usn = st.text_input("🆔 Your USN:", value="4AT23EC001")
    with col3:
        selected_department = st.selectbox("🎯 Select Department:", DEPARTMENTS)
    
    # Login button
    if st.button("🚀 Login / Register", use_container_width=True, type="primary"):
        if selected_department != "Select Department" and student_name and student_usn:
            with st.spinner("Setting up your account..."):
                student_data = register_student(student_usn, student_name, selected_department)
                if student_data:
                    st.session_state.student_data = student_data
                    bonus_result = claim_daily_bonus(student_usn)
                    st.success(f"Login successful! 🎉 {bonus_result['message']}")
                    st.rerun()
        else:
            st.warning("Please fill all fields!")
    
    # Main application
    if st.session_state.student_data:
        student_data = st.session_state.student_data
        dept_theme = get_department_theme(student_data["department"])
        
        # Welcome section
        st.markdown(f'''
        <div class="atme-card" style="background: {dept_theme['bg_gradient']};">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h2 style="margin: 0; font-size: 2rem;">{dept_theme["emoji"]} Welcome, {student_data["name"]}!</h2>
                    <p style="margin: 8px 0; font-size: 1.1rem;">🎯 {student_data["department"]} | 🆔 {student_data["usn"]}</p>
                </div>
                <div style="text-align: center;">
                    <h3 style="margin: 0; font-size: 2.5rem;">🏆 {student_data["points"]}</h3>
                    <p style="margin: 0;">Level {student_data["level"]} 🚀</p>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # NEW FEATURE: Tabbed Interface
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["💬 Chat Assistant", "⏰ Study Tools", "📝 Productivity", "🎯 Resources", "📊 Analytics"])
        
        with tab1:
            # Enhanced Chat Interface
            st.subheader("💬 Smart Chat Assistant")
            
            # Quick questions in categories
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🎓 Academic Info", use_container_width=True):
                    response_data = send_chat_message(student_data["usn"], "academic calendar")
                    st.session_state.chat_history.append({
                        "user_message": "academic calendar",
                        "bot_response": response_data["response"],
                        "timestamp": datetime.now().isoformat()
                    })
                    st.rerun()
                
                if st.button("🏫 College Info", use_container_width=True):
                    response_data = send_chat_message(student_data["usn"], "college address")
                    st.session_state.chat_history.append({
                        "user_message": "college address",
                        "bot_response": response_data["response"],
                        "timestamp": datetime.now().isoformat()
                    })
                    st.rerun()
            
            with col2:
                if st.button("📚 Study Tips", use_container_width=True):
                    response_data = send_chat_message(student_data["usn"], "study tips")
                    st.session_state.chat_history.append({
                        "user_message": "study tips",
                        "bot_response": response_data["response"],
                        "timestamp": datetime.now().isoformat()
                    })
                    st.rerun()
                
                if st.button("⏰ Time Management", use_container_width=True):
                    response_data = send_chat_message(student_data["usn"], "time management")
                    st.session_state.chat_history.append({
                        "user_message": "time management",
                        "bot_response": response_data["response"],
                        "timestamp": datetime.now().isoformat()
                    })
                    st.rerun()
            
            with col3:
                if st.button("💼 Career Help", use_container_width=True):
                    response_data = send_chat_message(student_data["usn"], "career guidance")
                    st.session_state.chat_history.append({
                        "user_message": "career guidance",
                        "bot_response": response_data["response"],
                        "timestamp": datetime.now().isoformat()
                    })
                    st.rerun()
                
                if st.button("🧠 Mental Health", use_container_width=True):
                    response_data = send_chat_message(student_data["usn"], "mental health")
                    st.session_state.chat_history.append({
                        "user_message": "mental health",
                        "bot_response": response_data["response"],
                        "timestamp": datetime.now().isoformat()
                    })
                    st.rerun()
            
            # Chat input
            user_question = st.text_area("💭 Ask me anything about college:", 
                                       placeholder="e.g., What are the library timings? How to prepare for exams?")
            if st.button("Send Message", use_container_width=True) and user_question:
                with st.spinner("🤔 Thinking..."):
                    response_data = send_chat_message(student_data["usn"], user_question)
                    st.session_state.chat_history.append({
                        "user_message": user_question,
                        "bot_response": response_data["response"],
                        "timestamp": datetime.now().isoformat()
                    })
                    st.rerun()
            
            # Chat history
            st.subheader("📜 Conversation History")
            if st.session_state.chat_history:
                for chat in reversed(st.session_state.chat_history[-8:]):
                    with st.container():
                        st.write(f"**👤 You:** {chat['user_message']}")
                        st.write(f"**🤖 Assistant:** {chat['bot_response']}")
                        st.write(f"*⏰ {datetime.fromisoformat(chat['timestamp']).strftime('%H:%M')}*")
                        st.markdown("---")
            else:
                st.info("💫 Start a conversation by clicking the buttons above or typing your question!")
        
        with tab2:
            # NEW FEATURE: Study Tools
            st.subheader("⏰ Study Timer & Tools")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 🍅 Pomodoro Timer")
                if st.session_state.study_timer and st.session_state.study_timer['running']:
                    elapsed = (datetime.now() - st.session_state.study_timer['start_time']).seconds
                    minutes = elapsed // 60
                    seconds = elapsed % 60
                    
                    st.markdown(f'<div class="timer-display">{minutes:02d}:{seconds:02d}</div>', unsafe_allow_html=True)
                    
                    if st.button("⏹️ Stop Timer", use_container_width=True):
                        duration = stop_study_timer()
                        st.success(f"Great job! You studied for {duration} minutes! 🎉")
                        st.session_state.student_data["points"] += duration // 5
                        st.rerun()
                else:
                    st.markdown('<div class="timer-display">25:00</div>', unsafe_allow_html=True)
                    if st.button("▶️ Start Study Session", use_container_width=True, type="primary"):
                        start_study_timer()
                        st.rerun()
                
                st.info("💡 **Pomodoro Technique:**\n- Study for 25 minutes\n- Take 5-minute break\n- Repeat 4 times\n- Take longer break (15-30 min)")
            
            with col2:
                st.markdown("### 📚 Study Resources")
                resources = get_study_resources(student_data["department"])
                
                for resource in resources:
                    with st.container():
                        st.write(f"**{resource['name']}** {resource['type']}")
                        st.write(f"🔗 {resource['url']}")
                        st.markdown("---")
                
                if not resources:
                    st.info("No specific resources for your department yet. Check back later!")
        
        with tab3:
            # NEW FEATURE: Productivity Tools
            st.subheader("📝 Productivity Hub")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📓 Quick Notes")
                note_title = st.text_input("Note Title:", placeholder="Enter note title...")
                note_content = st.text_area("Note Content:", placeholder="Write your note here...", height=100)
                
                if st.button("💾 Save Note", use_container_width=True) and note_title and note_content:
                    add_note(note_title, note_content)
                    st.success("Note saved successfully! 📌")
                    st.rerun()
                
                st.markdown("### 📋 Your Notes")
                if st.session_state.notes:
                    for note in reversed(st.session_state.notes[-5:]):
                        with st.expander(f"📄 {note['title']} - {note['created_at']}"):
                            st.write(note['content'])
                            if st.button(f"🗑️ Delete", key=f"del_note_{note['id']}"):
                                st.session_state.notes = [n for n in st.session_state.notes if n['id'] != note['id']]
                                st.rerun()
                else:
                    st.info("No notes yet. Create your first note above!")
            
            with col2:
                st.markdown("### ✅ To-Do List")
                new_task = st.text_input("New Task:", placeholder="What needs to be done?")
                
                if st.button("➕ Add Task", use_container_width=True) and new_task:
                    add_todo(new_task)
                    st.success("Task added! ✅")
                    st.rerun()
                
                st.markdown("### 📝 Your Tasks")
                if st.session_state.todo_list:
                    for todo in st.session_state.todo_list:
                        col_a, col_b = st.columns([3, 1])
                        with col_a:
                            if todo['completed']:
                                st.write(f"~~{todo['task']}~~ ✅")
                            else:
                                st.write(f"📌 {todo['task']}")
                        with col_b:
                            if not todo['completed']:
                                if st.button("✓", key=f"complete_{todo['id']}"):
                                    todo['completed'] = True
                                    st.session_state.student_data["points"] += 5
                                    st.rerun()
                else:
                    st.info("No tasks yet. Add your first task above!")
        
        with tab4:
            # NEW FEATURE: Learning Resources
            st.subheader("🎯 Learning Resources")
            
            st.markdown("### 📖 Department Resources")
            dept_resources = get_study_resources(student_data["department"])
            
            for resource in dept_resources:
                with st.container():
                    st.write(f"**{resource['name']}**")
                    st.write(f"**Type:** {resource['type']}")
                    st.write(f"**Link:** [Open Resource]({resource['url']})")
                    st.markdown("---")
            
            st.markdown("### 🎓 General Study Links")
            general_resources = [
                {"name": "Khan Academy", "url": "https://www.khanacademy.org", "description": "Free online courses"},
                {"name": "Coursera", "url": "https://www.coursera.org", "description": "Online courses from universities"},
                {"name": "YouTube Edu", "url": "https://www.youtube.com/education", "description": "Educational videos"},
                {"name": "GitHub", "url": "https://www.github.com", "description": "Code repositories & projects"}
            ]
            
            for resource in general_resources:
                st.write(f"🔗 **[{resource['name']}]({resource['url']})** - {resource['description']}")
        
        with tab5:
            # NEW FEATURE: Analytics
            st.subheader("📊 Your Learning Analytics")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### 📈 Progress Overview")
                
                # Study time chart
                study_data = {
                    'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                    'Study Hours': [2, 3, 1, 4, 2, 1, 0]
                }
                df = pd.DataFrame(study_data)
                fig = px.bar(df, x='Day', y='Study Hours', title='Weekly Study Pattern',
                           color='Study Hours', color_continuous_scale='blues')
                st.plotly_chart(fig, use_container_width=True)
                
                # Points progression
                points_data = {
                    'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                    'Points': [100, 150, 180, 220]
                }
                df_points = pd.DataFrame(points_data)
                fig_points = px.line(df_points, x='Week', y='Points', title='Points Progression',
                                   markers=True, line_shape='spline')
                st.plotly_chart(fig_points, use_container_width=True)
            
            with col2:
                st.markdown("### 🏆 Achievements")
                
                achievements = [
                    {"name": "First Chat", "earned": True, "points": 20},
                    {"name": "Study Streak", "earned": False, "points": 50},
                    {"name": "Task Master", "earned": True, "points": 30},
                    {"name": "Resource Explorer", "earned": False, "points": 25},
                    {"name": "Week Warrior", "earned": True, "points": 40}
                ]
                
                for achievement in achievements:
                    if achievement['earned']:
                        st.success(f"✅ {achievement['name']} (+{achievement['points']} pts)")
                    else:
                        st.info(f"🔒 {achievement['name']} (+{achievement['points']} pts)")
                
                st.markdown("### 📊 Quick Stats")
                stats = {
                    'Total Chats': len(st.session_state.chat_history),
                    'Notes Created': len(st.session_state.notes),
                    'Tasks Completed': len([t for t in st.session_state.todo_list if t['completed']]),
                    'Study Sessions': 12
                }
                
                for stat, value in stats.items():
                    st.write(f"**{stat}:** {value}")
    
    else:
        # Enhanced landing page
        st.markdown("""
        <div style="text-align: center; padding: 40px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; color: white; margin: 20px 0;">
            <h1 style="font-size: 2.5rem; margin: 0;">🎓 ATME College of Engineering</h1>
            <p style="font-size: 1.3rem; margin: 10px 0;">Where Innovation Meets Excellence ✨</p>
            <p style="margin: 5px 0;">📍 Adichunchanagiri Road, Mysuru - 570028</p>
            <p style="margin: 5px 0;">📞 0821-1234567 | 🌐 www.atme.edu.in</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Feature showcase
        st.subheader("🚀 Discover Amazing Features")
        
        features = [
            {"emoji": "💬", "title": "AI Chat Assistant", "desc": "Smart responses to all college queries"},
            {"emoji": "⏰", "title": "Study Timer", "desc": "Pomodoro technique for focused studying"},
            {"emoji": "📝", "title": "Productivity Tools", "desc": "Notes, to-do lists & task management"},
            {"emoji": "🎯", "title": "Learning Resources", "desc": "Department-specific study materials"},
            {"emoji": "📊", "title": "Progress Analytics", "desc": "Track your learning journey"},
            {"emoji": "🏆", "title": "Gamification", "desc": "Earn points & achievements"}
        ]
        
        cols = st.columns(3)
        for i, feature in enumerate(features):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="feature-card">
                    <h3 style="margin: 0; text-align: center;">{feature['emoji']}</h3>
                    <h4 style="margin: 10px 0; text-align: center;">{feature['title']}</h4>
                    <p style="margin: 0; text-align: center; font-size: 0.9em;">{feature['desc']}</p>
                </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
