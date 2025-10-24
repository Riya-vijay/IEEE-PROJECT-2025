import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'student_points' not in st.session_state:
    st.session_state.student_points = 100
if 'last_login' not in st.session_state:
    st.session_state.last_login = datetime.now().date()
if 'achievements' not in st.session_state:
    st.session_state.achievements = []
if 'mood_data' not in st.session_state:
    st.session_state.mood_data = []

# Student profile
student_profile = {
    "name": "ATME Student",
    "department": "",
    "points": 100,
    "usn": "4AT23EC001",
    "level": 1,
    "avatar": "🎓"
}

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

# Department colors and emojis
DEPARTMENT_THEMES = {
    "CSE": {"color": "#FF6B6B", "emoji": "💻", "bg_gradient": "linear-gradient(135deg, #FF6B6B 0%, #FF8E8E 100%)"},
    "ECE": {"color": "#4ECDC4", "emoji": "🔬", "bg_gradient": "linear-gradient(135deg, #4ECDC4 0%, #67E6DC 100%)"},
    "Data Science": {"color": "#45B7D1", "emoji": "📊", "bg_gradient": "linear-gradient(135deg, #45B7D1 0%, #67C8E6 100%)"},
    "AIML": {"color": "#96CEB4", "emoji": "🤖", "bg_gradient": "linear-gradient(135deg, #96CEB4 0%, #B4E6C8 100%)"},
    "Cyber Security": {"color": "#FECA57", "emoji": "🛡️", "bg_gradient": "linear-gradient(135deg, #FECA57 0%, #FFE08A 100%)"},
    "Mechanical": {"color": "#FF9FF3", "emoji": "🔧", "bg_gradient": "linear-gradient(135deg, #FF9FF3 0%, #FFC2F5 100%)"},
    "Civil": {"color": "#54A0FF", "emoji": "🏗️", "bg_gradient": "linear-gradient(135deg, #54A0FF 0%, #7FB9FF 100%)"},
    "EEE": {"color": "#5F27CD", "emoji": "⚡", "bg_gradient": "linear-gradient(135deg, #5F27CD 0%, #7B4CDF 100%)"},
    "CSD": {"color": "#FF9F43", "emoji": "🎨", "bg_gradient": "linear-gradient(135deg, #FF9F43 0%, #FFB76B 100%)"}
}

# Achievements system
ACHIEVEMENTS = {
    "first_chat": {"name": "First Conversation", "emoji": "💬", "points": 20},
    "daily_user": {"name": "Daily User", "emoji": "🔥", "points": 15},
    "question_master": {"name": "Question Master", "emoji": "❓", "points": 25},
    "wellness_warrior": {"name": "Wellness Warrior", "emoji": "🧠", "points": 30},
    "department_expert": {"name": "Department Expert", "emoji": "🎯", "points": 40},
    "chat_champion": {"name": "Chat Champion", "emoji": "🏆", "points": 50}
}

# COMPREHENSIVE ATME COLLEGE KNOWLEDGE BASE
ATME_KNOWLEDGE = {
    # ========== GENERAL COLLEGE INFORMATION ==========
    "College address and location": """
🏫 **ATME College of Engineering**
📍 **Address:** ATME College of Engineering, Adichunchanagiri Road, Mysuru - 570028, Karnataka
🌍 **Location:** Near BGS Health Centre, Mysuru
📞 **Phone:** 0821-1234567
🕒 **Office Hours:** 9:00 AM - 5:00 PM (Mon-Sat)
    """,
    
    "Contact information": """
📞 **ATME Contact Details:**
• **College Office:** 0821-1234567
• **Principal Office:** 0821-1234568
• **Admission Office:** 0821-1234569
• **Email:** info@atme.edu.in
• **Website:** www.atme.edu.in
• **Emergency:** 0821-1234580
    """,
    
    "Academic calendar": """
📅 **Academic Year 2024-25**

**Odd Semester (2024):**
• Semester Start: August 1, 2024
• Mid-term Exams: October 15-30, 2024
• End Semester Exams: December 8-23, 2024
• Winter Break: December 24 - January 5, 2025

**Even Semester (2025):**
• Semester Start: January 6, 2025
• Mid-term Exams: March 15-30, 2025
• End Semester Exams: May 15-30, 2025
• Summer Break: June 1 - July 31, 2025
    """,
    
    "Semester exam dates": """
📚 **Semester Exams Schedule 2024-25:**

**Odd Semester Exams:**
• Theory Exams: December 8-23, 2024
• Practical Exams: December 1-7, 2024
• Project Evaluation: December 1-10, 2024

**Even Semester Exams:**
• Theory Exams: May 15-30, 2025
• Practical Exams: May 8-14, 2025
• Project Evaluation: May 8-17, 2025
    """,
    
    "How to download hall ticket": """
🎫 **Hall Ticket Download Procedure:**

1. **Visit:** portal.atme.edu.in
2. **Login** with your USN and password
3. Go to **'Examination'** section
4. Click **'Download Hall Ticket'**
5. **Print** the hall ticket
6. Get it **signed by HOD** and **stamped**
    """,
    
    "Library timings and facilities": """
📖 **ATME Central Library**

**⏰ Timings:**
• Monday-Friday: 8:00 AM - 8:00 PM
• Saturday: 9:00 AM - 5:00 PM
• Sunday: Closed

**📚 Collection:**
• 50,000+ Books
• 100+ National & International Journals
• 5000+ E-books
• 50+ Online Databases
    """,
    
    "Hostel facilities and fees": """
🏠 **ATME Hostels**

**Accommodation:**
• Separate hostels for Boys & Girls
• Single, Double, Triple occupancy rooms
• 24/7 Security & CCTV surveillance
• Wi-Fi enabled campuses

**💵 Fee Structure (Per Year):**
• Hostel Fee: ₹45,000
• Mess Charges: ₹15,000
• **Total: ₹60,000**
    """,
    
    "Fee structure and payment": """
💰 **Fee Structure (Per Semester)**

**Breakup:**
• Tuition Fee: ₹45,000
• Development Fee: ₹15,000
• Examination Fee: ₹5,000
• Library Fee: ₹2,000
• Sports Fee: ₹1,000
• Other Charges: ₹2,000

**💵 Total: ₹70,000 per semester**
    """,
    
    "Bus facilities and routes": """
🚌 **College Bus Service**

**⏰ Timings:**
• Morning Pickup: 7:00 AM - 8:30 AM
• Evening Drop: 4:30 PM - 6:30 PM

**💵 Bus Pass:** ₹8,000 per semester
    """,
    
    "Sports facilities": """
⚽ **Sports Complex & Facilities**

**Outdoor Facilities:**
• Cricket Ground with practice nets
• Basketball Court (2 courts)
• Volleyball Court
• Football Ground
• Badminton Courts (4 courts)
• Athletic Track

**Indoor Facilities:**
• Gymnasium with trainer
• Table Tennis (6 tables)
• Chess & Carrom
• Yoga Hall
    """,
    
    "Placement cell information": """
💼 **Training & Placement Cell**

**👨‍🏫 TPO:** Dr. S. R. Kumar
**🏢 Office:** Placement Block, Ground Floor
**📞 Phone:** 0821-1234573

**🏢 Recruiting Companies:**
• **IT Giants:** Infosys, Wipro, TCS, IBM, Accenture
• **Core Companies:** Intel, Texas Instruments, L&T, Bosch
• **Startups:** Multiple tech startups
    """,
    
    "IEEE student branch": """
⚡ **ATME IEEE Student Branch**

**👨‍🏫 Faculty Advisor:** Dr. Priya Sharma
**📅 Upcoming Events:**
• **IEEE Mini Project Exhibition** - Tomorrow!
• Technical workshops every month
• Guest lectures from industry experts
    """,
    
    "College website and portal": """
🌐 **ATME Digital Platforms**

**Main Platforms:**
• **Website:** www.atme.edu.in
• **Student Portal:** portal.atme.edu.in
• **Learning Management:** lms.atme.edu.in
    """,

    # ========== DEPARTMENT SPECIFIC INFORMATION ==========
    
    "CSE department HOD": """
💻 **Computer Science & Engineering Department**

**👨‍🏫 HOD:** Dr. Suresh Kumar
**📧 Email:** hod.cse@atme.edu.in
**🏢 Office:** CSE Block, 1st Floor
**📞 Phone:** 0821-1234575
    """,
    
    "CSE lab schedules": """
💻 **CSE Laboratories Schedule**

**Programming Lab:**
• Mon-Fri: 9:00 AM - 5:00 PM
• Special sessions: Sat 9AM-1PM

**AI/ML Lab:**
• 24/7 access with faculty permission
• GPU computing resources available
    """,
    
    "CSE placement preparation": """
💼 **CSE Placement Preparation**

**Regular Activities:**
• Coding tests every Saturday
• Mock interviews every month
• Technical training sessions
• Resume building workshops
    """,
    
    "ECE department HOD": """
🔬 **Electronics & Communication Engineering**

**👩‍🏫 HOD:** Dr. Priya Sharma
**📧 Email:** hod.ece@atme.edu.in
**🏢 Office:** ECE Block, 2nd Floor
**📞 Phone:** 0821-1234576
    """,
    
    "ECE lab schedules": """
🔬 **ECE Laboratories Schedule**

**Basic Electronics Lab:**
• Mon/Wed/Fri: 9:00 AM - 5:00 PM

**DSP Lab:**
• Tue/Thu: 2:00 PM - 5:00 PM

**VLSI Lab:**
• Special slots with appointment
• Advanced equipment available
    """,
    
    "Mechanical department HOD": """
🔧 **Mechanical Engineering Department**

**👨‍🏫 HOD:** Dr. Sanjay Verma
**📧 Email:** hod.mech@atme.edu.in
**🏢 Office:** Mechanical Block, Ground Floor
**📞 Phone:** 0821-1234577
    """,
    
    "Civil department HOD": """
🏗️ **Civil Engineering Department**

**👩‍🏫 HOD:** Dr. Sunita Rao
**📧 Email:** hod.civil@atme.edu.in
**🏢 Office:** Civil Block, 1st Floor
**📞 Phone:** 0821-1234578
    """,
    
    "EEE department HOD": """
⚡ **Electrical & Electronics Engineering**

**👨‍🏫 HOD:** Dr. Mohan Das
**📧 Email:** hod.eee@atme.edu.in
**🏢 Office:** EEE Block, 2nd Floor
**📞 Phone:** 0821-1234579
    """,
    
    "Data Science department": """
📊 **Data Science Department**

**👩‍🏫 HOD:** Dr. Anjali Mehta
**🏢 Office:** New Academic Block, 3rd Floor

**💻 Lab Facilities:**
• Data Analytics Lab with high-end systems
• Hadoop cluster for big data
• Python, R programming environments
    """,
    
    "AIML department": """
🤖 **AI & ML Department**

**👨‍🏫 HOD:** Dr. Rajesh Khanna
**🏢 Office:** New Academic Block, 4th Floor

**🔬 Research Areas:**
• Machine Learning Algorithms
• Deep Learning & Neural Networks
• Natural Language Processing
• Computer Vision
    """,
    
    "Cyber Security department": """
🛡️ **Cyber Security Department**

**👩‍🏫 HOD:** Dr. Priya Nair
**🏢 Office:** New Academic Block, 2nd Floor

**🔒 Lab Facilities:**
• Secure Computing Lab
• Isolated network environment
• Kali Linux systems
• Penetration testing tools
    """,

    # ========== EVENTS AND ACTIVITIES ==========
    "Upcoming college events": """
🎯 **Upcoming Events at ATME (2024-25)**

**Technical Events:**
• **IEEE Mini Project Exhibition** - Tomorrow!
• **Technical Symposium 'TECHNOVATE'** - November 20-22, 2024
• **Hackathon 2024** - December 10-11, 2024

**Cultural Events:**
• **Cultural Fest 'Utsav'** - December 15-17, 2024
• **Freshers Party** - August 30, 2024
• **Annual Day** - March 15, 2025

**Sports Events:**
• **Sports Week** - January 20-25, 2025
    """,
    
    "Cultural fest details": """
🎭 **Cultural Fest 'Utsav' 2024**

**📅 Dates:** December 15-17, 2024
**📍 Venue:** College Auditorium & Grounds

**🎪 Major Events:**
• **Dance Competition** (Solo & Group)
• **Music Competition** (Vocal & Instrumental)
• **Drama & Street Play**
• **Fashion Show**
• **Fine Arts Exhibition**
    """,
    
    "Technical fest information": """
🔧 **Technical Fest 'TECHNOVATE' 2024**

**📅 Dates:** November 20-22, 2024
**🎯 Theme:** "Innovation for Sustainable Future"

**💻 Major Competitions:**
• **Code Marathon** (24-hour coding)
• **Project Expo** (Hardware & Software)
• **Paper Presentation**
• **Robo Race**
• **Circuit Design**
    """,
    
    "College clubs and associations": """
👥 **Student Clubs & Associations**

**Technical Clubs:**
• **Coding Club** - Weekly programming sessions
• **Robotics Club** - Project building & competitions
• **IEEE Student Branch** - Technical activities
• **CSI Chapter** - Computer society events

**Cultural Clubs:**
• **Literary Club** - Debates, writing competitions
• **Music Club** - Practice sessions & performances
• **Dance Club** - Various dance forms training
    """,
    
    "Mental health and counseling": """
🧠 **Student Counseling & Mental Health**

**👨‍⚕️ Counselor:** Dr. Anitha Psychologist
**📞 Appointment:** 0821-1234582
**🏢 Location:** Administrative Block, 2nd Floor

**⏰ Counseling Hours:**
• Monday-Friday: 10:00 AM - 4:00 PM
• Saturday: 10:00 AM - 1:00 PM
    """
}

def get_department_theme(department):
    """Get department theme based on selection"""
    for dept, theme in DEPARTMENT_THEMES.items():
        if dept in department:
            return theme
    return {"color": "#667eea", "emoji": "🎓", "bg_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"}

def get_department_questions(department):
    """Get questions relevant to selected department"""
    general_questions = [
        "College address and location",
        "Contact information", 
        "Academic calendar",
        "Semester exam dates",
        "How to download hall ticket",
        "Library timings and facilities",
        "Hostel facilities and fees",
        "Fee structure and payment",
        "Bus facilities and routes",
        "Placement cell information",
        "Upcoming college events",
        "Mental health and counseling"
    ]
    
    dept_questions = []
    if "CSE" in department:
        dept_questions = ["CSE department HOD", "CSE lab schedules", "CSE placement preparation"]
    elif "ECE" in department:
        dept_questions = ["ECE department HOD", "ECE lab schedules"]
    elif "Data Science" in department:
        dept_questions = ["Data Science department"]
    elif "AIML" in department:
        dept_questions = ["AIML department"]
    elif "Cyber" in department:
        dept_questions = ["Cyber Security department"]
    elif "Mechanical" in department:
        dept_questions = ["Mechanical department HOD"]
    elif "Civil" in department:
        dept_questions = ["Civil department HOD"]
    elif "Electrical" in department or "EEE" in department:
        dept_questions = ["EEE department HOD"]
    elif "Design" in department or "CSD" in department:
        dept_questions = ["College clubs and associations"]
    
    return general_questions + dept_questions

def check_daily_bonus():
    """Check and award daily login bonus"""
    today = datetime.now().date()
    if st.session_state.last_login != today:
        st.session_state.student_points += 10
        st.session_state.last_login = today
        if "daily_user" not in st.session_state.achievements:
            st.session_state.achievements.append("daily_user")
        return True
    return False

def award_achievement(achievement_key):
    """Award achievement to student"""
    if achievement_key not in st.session_state.achievements:
        st.session_state.achievements.append(achievement_key)
        st.session_state.student_points += ACHIEVEMENTS[achievement_key]["points"]
        return True
    return False

def create_animated_header():
    """Create animated header with particles"""
    st.markdown("""
    <style>
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    @keyframes glow {
        0% { box-shadow: 0 0 5px rgba(59, 130, 246, 0.5); }
        50% { box-shadow: 0 0 20px rgba(59, 130, 246, 0.8); }
        100% { box-shadow: 0 0 5px rgba(59, 130, 246, 0.5); }
    }
    
    .floating { animation: float 3s ease-in-out infinite; }
    .glowing { animation: glow 2s ease-in-out infinite; }
    </style>
    """, unsafe_allow_html=True)

def create_points_animation():
    """Create points animation when points are added"""
    st.markdown("""
    <style>
    @keypoints bounceIn {
        0% { transform: scale(0.3); opacity: 0; }
        50% { transform: scale(1.05); }
        70% { transform: scale(0.9); }
        100% { transform: scale(1); opacity: 1; }
    }
    .bounce-in { animation: bounceIn 0.6s ease; }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="ATME College Assistant", 
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Add custom CSS with animations and vibrant colors
    st.markdown("""
    <style>
    .main-header {
        font-size: 3.5rem;
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4, #FECA57);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientShift 8s ease infinite;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
        text-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .atme-card {
        padding: 25px;
        border-radius: 20px;
        color: white;
        margin: 10px 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        border: none;
    }
    
    .atme-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.3);
    }
    
    .points-card {
        padding: 25px;
        border-radius: 20px;
        color: white;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        transition: all 0.3s ease;
    }
    
    .points-card:hover {
        transform: scale(1.05);
        box-shadow: 0 12px 35px rgba(0,0,0,0.25);
    }
    
    .department-card {
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
    }
    
    .department-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
    
    .chat-bubble-user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 25px 25px 5px 25px;
        margin: 15px 0;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        animation: slideInRight 0.5s ease;
    }
    
    .chat-bubble-bot {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        color: #2d3748;
        padding: 15px 20px;
        border-radius: 25px 25px 25px 5px;
        margin: 15px 0;
        max-width: 80%;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
        animation: slideInLeft 0.5s ease;
    }
    
    @keyframes slideInLeft {
        from { transform: translateX(-20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideInRight {
        from { transform: translateX(20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .question-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 15px;
        border-radius: 15px;
        margin: 8px 0;
        width: 100%;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .question-button:hover {
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    .action-button {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        border: none;
        padding: 12px;
        border-radius: 12px;
        margin: 5px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 600;
    }
    
    .action-button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(72, 187, 120, 0.4);
    }
    
    .achievement-badge {
        background: linear-gradient(135deg, #f6e05e 0%, #ecc94b 100%);
        color: #744210;
        padding: 10px 15px;
        border-radius: 20px;
        margin: 5px;
        font-size: 0.9em;
        font-weight: 600;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .stSelectbox > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        border: none;
    }
    
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Animated header
    st.markdown('<h1 class="main-header floating">🎓 ATME College Dynamic Assistant ⚡</h1>', unsafe_allow_html=True)
    
    # Student info section with vibrant cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        student_name = st.text_input("👤 Your Name:", value="ATME Student", help="Enter your full name")
    
    with col2:
        student_usn = st.text_input("🆔 Your USN:", value="4AT23EC001", help="Format: 4AT23XX001")
    
    with col3:
        selected_department = st.selectbox("🎯 Select Your Department:", DEPARTMENTS)
    
    # Update student profile
    student_profile["name"] = student_name
    student_profile["usn"] = student_usn
    student_profile["department"] = selected_department
    student_profile["points"] = st.session_state.student_points
    student_profile["level"] = st.session_state.student_points // 100 + 1
    
    # Get department theme
    dept_theme = get_department_theme(selected_department)
    
    # Check daily bonus
    if check_daily_bonus():
        st.sidebar.success("🎁 Daily login bonus: +10 points! ✨")
    
    if selected_department != "Select Department":
        # Welcome section with dynamic department theme
        st.markdown(f'''
        <div class="atme-card" style="background: {dept_theme['bg_gradient']};">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <h2 style="margin: 0; font-size: 2rem;">{dept_theme["emoji"]} Welcome, {student_name}!</h2>
                    <p style="margin: 5px 0; font-size: 1.1rem;">🎯 {selected_department} | 🆔 {student_usn}</p>
                    <p style="margin: 0; font-size: 0.9rem; opacity: 0.9;">📍 Adichunchanagiri Road, Mysuru - 570028</p>
                </div>
                <div style="text-align: center;">
                    <h3 style="margin: 0; font-size: 2.5rem;" class="pulse">🏆 {student_profile["points"]}</h3>
                    <p style="margin: 0;">Level {student_profile["level"]} 🚀</p>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Main content area
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("💬 Dynamic Chat Interface")
            
            # Animated question buttons
            st.write("**🚀 Quick Questions About ATME:**")
            questions = get_department_questions(selected_department)
            
            # Display questions in a dynamic grid
            cols = st.columns(2)
            for i, question in enumerate(questions):
                with cols[i % 2]:
                    if st.button(f"✨ {question}", key=f"q_{i}", use_container_width=True):
                        answer = ATME_KNOWLEDGE.get(question, "I'm still learning about this! Please visit college administration office for detailed information.")
                        st.session_state.chat_history.append({
                            "user": question,
                            "bot": answer, 
                            "time": datetime.now()
                        })
                        st.session_state.student_points += 2
                        student_profile["points"] = st.session_state.student_points
                        
                        # Award achievements
                        if len(st.session_state.chat_history) == 1:
                            award_achievement("first_chat")
                        if len(st.session_state.chat_history) >= 5:
                            award_achievement("question_master")
            
            # Interactive manual question input
            st.subheader("🔍 Ask Your Own Question")
            user_question = st.text_input("Type your question about ATME College:", 
                                        placeholder="e.g., When is the next cultural fest? 🌸")
            
            if user_question:
                with st.spinner("🔍 Searching ATME database..."):
                    time.sleep(1.5)  # Simulate AI thinking
                
                # Enhanced keyword matching
                answer = "I'm still learning about this! Please check with the college administration office or visit www.atme.edu.in for official information. 📚"
                for key, value in ATME_KNOWLEDGE.items():
                    if any(word in user_question.lower() for word in key.lower().split()):
                        answer = value
                        break
                
                st.session_state.chat_history.append({
                    "user": user_question,
                    "bot": answer,
                    "time": datetime.now()
                })
                st.session_state.student_points += 3
                student_profile["points"] = st.session_state.student_points
            
            # Dynamic conversation history
            st.subheader("📜 Live Conversation")
            if st.session_state.chat_history:
                for chat in reversed(st.session_state.chat_history[-6:]):
                    st.markdown(f'<div class="chat-bubble-user">👤 {chat["user"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="chat-bubble-bot">🤖 {chat["bot"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div style="text-align: center; color: #718096; font-size: 0.8em;">⏰ {chat["time"].strftime("%H:%M")}</div>', unsafe_allow_html=True)
                    st.markdown("---")
            else:
                st.info("""
                💫 **No conversations yet!** 
                - Click any question button above 
                - Or type your own question
                - Start earning points and achievements! 🎯
                """)
        
        with col2:
            # Vibrant sidebar features
            st.subheader("🎯 Quick Actions")
            
            action_col1, action_col2 = st.columns(2)
            
            with action_col1:
                if st.button("📅 Calendar", use_container_width=True):
                    st.session_state.chat_history.append({
                        "user": "Academic calendar",
                        "bot": ATME_KNOWLEDGE["Academic calendar"],
                        "time": datetime.now()
                    })
                
                if st.button("🎫 Hall Ticket", use_container_width=True):
                    st.session_state.chat_history.append({
                        "user": "How to download hall ticket", 
                        "bot": ATME_KNOWLEDGE["How to download hall ticket"],
                        "time": datetime.now()
                    })
            
            with action_col2:
                if st.button("📚 Library", use_container_width=True):
                    st.session_state.chat_history.append({
                        "user": "Library timings and facilities",
                        "bot": ATME_KNOWLEDGE["Library timings and facilities"],
                        "time": datetime.now()
                    })
                
                if st.button("💼 Placement", use_container_width=True):
                    st.session_state.chat_history.append({
                        "user": "Placement cell information",
                        "bot": ATME_KNOWLEDGE["Placement cell information"],
                        "time": datetime.now()
                    })
            
            # Interactive wellness section
            st.subheader("🧠 Wellness Center")
            mood = st.select_slider("How are you feeling today? 🌈", 
                                  options=["😔 Stressed", "😟 Anxious", "😐 Okay", "😊 Good", "🤩 Excellent"])
            
            if st.button("💖 Update Mood & Get Points", use_container_width=True):
                st.session_state.student_points += 8
                student_profile["points"] = st.session_state.student_points
                award_achievement("wellness_warrior")
                
                # Add mood to data
                st.session_state.mood_data.append({
                    "mood": mood,
                    "time": datetime.now()
                })
                
                st.success("+8 points for wellness check! 🌟")
                
                # Show dynamic wellness tip
                wellness_tips = [
                    "Remember to take breaks and breathe deeply! 🧘‍♀️",
                    "Stay hydrated and get enough sleep! 💤",
                    "Talk to friends or counselors if you feel overwhelmed! 👥",
                    "Physical activity can boost your mood! 🏃‍♂️",
                    "You're doing great! Keep going! 💪",
                    "Small steps lead to big achievements! 🌟"
                ]
                st.info(f"**Wellness Tip:** {random.choice(wellness_tips)}")
            
            # Achievements display
            if st.session_state.achievements:
                st.subheader("🏆 Your Achievements")
                achievement_cols = st.columns(2)
                for i, achievement_key in enumerate(st.session_state.achievements):
                    achievement = ACHIEVEMENTS[achievement_key]
                    with achievement_cols[i % 2]:
                        st.markdown(f'<div class="achievement-badge">{achievement["emoji"]} {achievement["name"]}</div>', unsafe_allow_html=True)
            
            # Department info with theme
            st.subheader(f"{dept_theme['emoji']} Department Info")
            dept_info = {
                "CSE": "💻 Focus on AI, ML, Software Development",
                "ECE": "🔬 VLSI, Communication, Embedded Systems", 
                "Data Science": "📊 Data Analytics, Machine Learning",
                "AIML": "🤖 AI, Neural Networks, Robotics",
                "Cyber Security": "🛡️ Network Security, Ethical Hacking",
                "Mechanical": "🔧 Design, Manufacturing, Thermal",
                "Civil": "🏗️ Structural, Environmental Engineering",
                "EEE": "⚡ Power Systems, Control Systems",
                "CSD": "🎨 UI/UX Design, Product Design"
            }
            
            for dept, info in dept_info.items():
                if dept in selected_department:
                    st.markdown(f'<div class="department-card" style="background: {dept_theme["bg_gradient"]};">{info}</div>', unsafe_allow_html=True)
                    break
    
    else:
        # Vibrant landing page when no department selected
        st.warning("🎯 Please select your department to unlock all features! 🔓")
        
        # Animated college introduction
        st.markdown("""
        <div class="atme-card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <h2 style="text-align: center; margin: 0;">🏫 ATME College of Engineering</h2>
            <p style="text-align: center; margin: 10px 0; font-size: 1.2rem;">Where Innovation Meets Excellence ✨</p>
            <div style="display: flex; justify-content: space-around; text-align: center; margin-top: 20px;">
                <div>
                    <h3 style="margin: 0;">📍</h3>
                    <p style="margin: 5px 0;">Adichunchanagiri Road<br>Mysuru - 570028</p>
                </div>
                <div>
                    <h3 style="margin: 0;">📞</h3>
                    <p style="margin: 5px 0;">0821-1234567<br>info@atme.edu.in</p>
                </div>
                <div>
                    <h3 style="margin: 0;">🌐</h3>
                    <p style="margin: 5px 0;">www.atme.edu.in<br>portal.atme.edu.in</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Feature showcase
        st.subheader("🚀 Discover Amazing Features")
        
        feature_cols = st.columns(3)
        features = [
            {"emoji": "💬", "title": "Smart Chat", "desc": "AI-powered responses"},
            {"emoji": "🎯", "title": "Department Specific", "desc": "Tailored information"},
            {"emoji": "🏆", "title": "Gamification", "desc": "Earn points & achievements"},
            {"emoji": "🧠", "title": "Wellness Support", "desc": "Mental health care"},
            {"emoji": "📊", "title": "Live Analytics", "desc": "Track your progress"},
            {"emoji": "⚡", "title": "Quick Actions", "desc": "Instant information"}
        ]
        
        for i, feature in enumerate(features):
            with feature_cols[i % 3]:
                st.markdown(f"""
                <div style="text-align: center; padding: 15px; border-radius: 15px; background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%); margin: 10px 0;">
                    <h3 style="margin: 0; font-size: 2rem;">{feature['emoji']}</h3>
                    <h4 style="margin: 10px 0; color: #2d3748;">{feature['title']}</h4>
                    <p style="margin: 0; color: #718096; font-size: 0.9em;">{feature['desc']}</p>
                </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
