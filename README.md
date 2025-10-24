# atme_chatbot.py
import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

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
    },
    "Mechanical": {
        "color": "#FF9FF3", 
        "emoji": "🔧", 
        "bg_gradient": "linear-gradient(135deg, #FF9FF3 0%, #FFC2F5 100%)",
        "secondary": "linear-gradient(135deg, #FFE8FC 0%, #FFF5FD 100%)"
    },
    "Civil": {
        "color": "#54A0FF", 
        "emoji": "🏗️", 
        "bg_gradient": "linear-gradient(135deg, #54A0FF 0%, #7FB9FF 100%)",
        "secondary": "linear-gradient(135deg, #E8F2FF 0%, #F5F9FF 100%)"
    },
    "EEE": {
        "color": "#5F27CD", 
        "emoji": "⚡", 
        "bg_gradient": "linear-gradient(135deg, #5F27CD 0%, #7B4CDF 100%)",
        "secondary": "linear-gradient(135deg, #F0E8FF 0%, #F7F5FF 100%)"
    },
    "CSD": {
        "color": "#FF9F43", 
        "emoji": "🎨", 
        "bg_gradient": "linear-gradient(135deg, #FF9F43 0%, #FFB76B 100%)",
        "secondary": "linear-gradient(135deg, #FFF0E8 0%, #FFF7F5 100%)"
    }
}

# Comprehensive Knowledge Base
ATME_KNOWLEDGE = {
    # General College Information
    "college address": """
🏫 **ATME College of Engineering**
📍 **Address:** Adichunchanagiri Road, Mysuru - 570028, Karnataka
🌍 **Location:** Near BGS Health Centre, Mysuru
📞 **Phone:** 0821-1234567
🕒 **Office Hours:** 9:00 AM - 5:00 PM (Mon-Sat)
    """,
    
    "contact information": """
📞 **ATME Contact Details:**
• **College Office:** 0821-1234567
• **Principal Office:** 0821-1234568  
• **Admission Office:** 0821-1234569
• **Email:** info@atme.edu.in
• **Website:** www.atme.edu.in
• **Emergency:** 0821-1234580
    """,
    
    "academic calendar": """
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
    
    "exam dates": """
📚 **Semester Exams Schedule 2024-25:**

**Odd Semester Exams:**
• Theory Exams: December 8-23, 2024
• Practical Exams: December 1-7, 2024
• Project Evaluation: December 1-10, 2024

**Even Semester Exams:**
• Theory Exams: May 15-30, 2025
• Practical Exams: May 8-14, 2025
• Project Evaluation: May 8-17, 2025

**Hall Tickets:** Available 15 days before exams on portal.atme.edu.in
    """,
    
    "library information": """
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

**💻 Facilities:**
• Digital Library (24/7 online access)
• Photocopy & Printing Services
• Reading Rooms (AC & Non-AC)
• Group Discussion Rooms
    """,
    
    "hostel facilities": """
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

**🏋️ Facilities:**
• Gymnasium
• Reading Room
• Indoor Games
• Common TV Room
• Hot Water Supply
    """,
    
    "fee structure": """
💰 **Fee Structure (Per Semester)**

**Breakup:**
• Tuition Fee: ₹45,000
• Development Fee: ₹15,000
• Examination Fee: ₹5,000
• Library Fee: ₹2,000
• Sports Fee: ₹1,000
• Other Charges: ₹2,000

**💵 Total: ₹70,000 per semester**

**Payment Methods:**
• Online: portal.atme.edu.in
• Bank Transfer
• Cash: College accounts office
    """,
    
    "bus facilities": """
🚌 **College Bus Service**

**⏰ Timings:**
• Morning Pickup: 7:00 AM - 8:30 AM
• Evening Drop: 4:30 PM - 6:30 PM

**🗺️ Major Routes:**
1. Vijayanagar → Kuvempunagar → College
2. Saraswathipuram → Gokulam → College  
3. Hebbal → Hootagalli → College
4. Bannimantap → JSS Layout → College

**💵 Bus Pass:** ₹8,000 per semester
    """,
    
    "sports facilities": """
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
    
    "placement information": """
💼 **Training & Placement Cell**

**👨‍🏫 TPO:** Dr. S. R. Kumar
**🏢 Office:** Placement Block, Ground Floor
**📞 Phone:** 0821-1234573
**📧 Email:** placement@atme.edu.in

**🏢 Recruiting Companies:**
• **IT Giants:** Infosys, Wipro, TCS, IBM, Accenture
• **Core Companies:** Intel, Texas Instruments, L&T, Bosch
• **Startups:** Multiple tech startups

**📊 Placement Statistics (2023):**
• 85% Placement Rate
• Highest Package: ₹18 LPA
• Average Package: ₹6.5 LPA
    """,
    
    "ieee events": """
⚡ **ATME IEEE Student Branch**

**👨‍🏫 Faculty Advisor:** Dr. Priya Sharma
**🎯 Student Chair:** [Your Name Here]

**📅 Upcoming Events:**
• **IEEE Mini Project Exhibition** - Tomorrow!
• Technical workshops every month
• Guest lectures from industry experts
• Project competitions

**🤝 Benefits:**
• Access to IEEE resources
• Networking opportunities
• Skill development workshops
    """,
    
    "college website": """
🌐 **ATME Digital Platforms**

**Main Platforms:**
• **Website:** www.atme.edu.in
• **Student Portal:** portal.atme.edu.in
• **Learning Management:** lms.atme.edu.in
• **Email:** username@atme.edu.in

**Portal Features:**
• Attendance tracking
• Marks and grades
• Fee payment
• Hall ticket download
• Course materials
    """,

    # Department Specific
    "cse department": """
💻 **Computer Science & Engineering**

**👨‍🏫 HOD:** Dr. Suresh Kumar
**📧 Email:** hod.cse@atme.edu.in
**🏢 Office:** CSE Block, 1st Floor
**📞 Phone:** 0821-1234575

**🎯 Specializations:**
• Artificial Intelligence & Machine Learning
• Data Science
• Cyber Security
• Full Stack Development
• Cloud Computing
    """,
    
    "ece department": """
🔬 **Electronics & Communication Engineering**

**👩‍🏫 HOD:** Dr. Priya Sharma
**📧 Email:** hod.ece@atme.edu.in
**🏢 Office:** ECE Block, 2nd Floor
**📞 Phone:** 0821-1234576

**🎯 Specializations:**
• VLSI Design
• Communication Systems
• Embedded Systems
• Signal Processing
• IoT & Sensors
    """,
    
    "cse labs": """
💻 **CSE Laboratories Schedule**

**Programming Lab:**
• Mon-Fri: 9:00 AM - 5:00 PM
• Special sessions: Sat 9AM-1PM

**AI/ML Lab:**
• 24/7 access with faculty permission
• GPU computing resources available

**Project Lab:**
• Extended hours during project time
• Group discussions allowed
    """,
    
    "ece labs": """
🔬 **ECE Laboratories Schedule**

**Basic Electronics Lab:**
• Mon/Wed/Fri: 9:00 AM - 5:00 PM

**DSP Lab:**
• Tue/Thu: 2:00 PM - 5:00 PM

**VLSI Lab:**
• Special slots with appointment
• Advanced equipment available
    """,
    
    "mechanical department": """
🔧 **Mechanical Engineering**

**👨‍🏫 HOD:** Dr. Sanjay Verma
**📧 Email:** hod.mech@atme.edu.in
**🏢 Office:** Mechanical Block, Ground Floor
**📞 Phone:** 0821-1234577

**🎯 Specializations:**
• Thermal Engineering
• Manufacturing Technology
• Machine Design
• Automobile Engineering
• Robotics & Automation
    """,
    
    "civil department": """
🏗️ **Civil Engineering**

**👩‍🏫 HOD:** Dr. Sunita Rao
**📧 Email:** hod.civil@atme.edu.in
**🏢 Office:** Civil Block, 1st Floor
**📞 Phone:** 0821-1234578

**🎯 Specializations:**
• Structural Engineering
• Environmental Engineering
• Geotechnical Engineering
• Construction Management
• Transportation Engineering
    """,
    
    "eee department": """
⚡ **Electrical & Electronics Engineering**

**👨‍🏫 HOD:** Dr. Mohan Das
**📧 Email:** hod.eee@atme.edu.in
**🏢 Office:** EEE Block, 2nd Floor
**📞 Phone:** 0821-1234579

**🎯 Specializations:**
• Power Systems
• Control Systems
• Renewable Energy
• Power Electronics
• Electrical Machines
    """,
    
    "data science department": """
📊 **Data Science Department**

**👩‍🏫 HOD:** Dr. Anjali Mehta
**🏢 Office:** New Academic Block, 3rd Floor

**💻 Lab Facilities:**
• Data Analytics Lab with high-end systems
• Hadoop cluster for big data
• Python, R programming environments
• Tableau for visualization
    """,
    
    "aiml department": """
🤖 **AI & ML Department**

**👨‍🏫 HOD:** Dr. Rajesh Khanna
**🏢 Office:** New Academic Block, 4th Floor

**🔬 Research Areas:**
• Machine Learning Algorithms
• Deep Learning & Neural Networks
• Natural Language Processing
• Computer Vision
• Robotics & Automation
    """,
    
    "cyber security department": """
🛡️ **Cyber Security Department**

**👩‍🏫 HOD:** Dr. Priya Nair
**🏢 Office:** New Academic Block, 2nd Floor

**🔒 Lab Facilities:**
• Secure Computing Lab
• Isolated network environment
• Kali Linux systems
• Penetration testing tools
    """,

    # Events and Activities
    "upcoming events": """
🎯 **Upcoming Events at ATME (2024-25)**

**Technical Events:**
• **IEEE Mini Project Exhibition** - Tomorrow!
• **Technical Symposium 'TECHNOVATE'** - November 20-22, 2024
• **Hackathon 2024** - December 10-11, 2024
• **Paper Presentation Contest** - January 15, 2025

**Cultural Events:**
• **Cultural Fest 'Utsav'** - December 15-17, 2024
• **Freshers Party** - August 30, 2024
• **Annual Day** - March 15, 2025

**Sports Events:**
• **Sports Week** - January 20-25, 2025
• **Inter-department Tournaments** - Monthly
    """,
    
    "cultural fest": """
🎭 **Cultural Fest 'Utsav' 2024**

**📅 Dates:** December 15-17, 2024
**📍 Venue:** College Auditorium & Grounds

**🎪 Major Events:**
• **Dance Competition** (Solo & Group)
• **Music Competition** (Vocal & Instrumental)
• **Drama & Street Play**
• **Fashion Show**
• **Fine Arts Exhibition**
• **Literary Events**

**🏆 Prizes:**
• Trophy for overall championship
• Cash prizes for winners
• Certificates for all participants
    """,
    
    "technical fest": """
🔧 **Technical Fest 'TECHNOVATE' 2024**

**📅 Dates:** November 20-22, 2024
**🎯 Theme:** "Innovation for Sustainable Future"

**💻 Major Competitions:**
• **Code Marathon** (24-hour coding)
• **Project Expo** (Hardware & Software)
• **Paper Presentation**
• **Robo Race**
• **Circuit Design**
• **Quiz Competition**

**👥 Workshops:**
• IoT & Embedded Systems
• AI & Machine Learning
• Web Development
• Robotics

**💰 Prize Money:** Up to ₹50,000
    """,
    
    "college clubs": """
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
• **Drama Club** - Theater performances

**Other Clubs:**
• **Eco Club** - Environmental activities
• **Sports Club** - Regular tournaments
• **Photography Club** - Workshops & exhibitions
    """,
    
    "mental health": """
🧠 **Student Counseling & Mental Health**

**👨‍⚕️ Counselor:** Dr. Anitha Psychologist
**📞 Appointment:** 0821-1234582
**🏢 Location:** Administrative Block, 2nd Floor

**⏰ Counseling Hours:**
• Monday-Friday: 10:00 AM - 4:00 PM
• Saturday: 10:00 AM - 1:00 PM

**🤝 Services:**
• Academic stress management
• Career counseling
• Personal issues guidance
• Group therapy sessions
• Crisis intervention

**🔒 Confidentiality:** All sessions are strictly confidential
    """,
    
    # Additional questions for better coverage
    "hello": "👋 **Hello! I'm ATME College Assistant!** 🤖\n\nI can help you with:\n• 📚 Academic information\n• 🏫 College facilities\n• 🎯 Department details\n• 🎉 Events and activities\n• 💼 Placement information\n• 🧠 Mental health support\n\nWhat would you like to know?",
    
    "hi": "👋 **Hi there! Welcome to ATME College!** 🎓\n\nI'm here to help you with any questions about our college. Ask me about exams, facilities, departments, or events!",
    
    "help": "🆘 **Here's how I can help you:**\n\n**Academic Questions:**\n• Ask about exams, schedules, fees\n• Library timings and facilities\n• Academic calendar\n\n**College Facilities:**\n• Hostel information\n• Bus services\n• Sports facilities\n• Placement cell\n\n**Departments:**\n• Department-specific information\n• Lab schedules\n• HOD contacts\n\n**Events:**\n• Upcoming college events\n• Cultural fest details\n• Technical competitions\n\nJust ask me anything! 💬"
}

# OFFLINE MODE FUNCTIONS - No backend needed!
def register_student(usn: str, name: str, department: str):
    """Register student - OFFLINE MODE"""
    student_data = {
        "usn": usn,
        "name": name,
        "department": department,
        "points": 100,
        "level": 1,
        "avatar": "🎓"
    }
    return student_data

def get_student(usn: str):
    """Get student data - OFFLINE MODE"""
    return st.session_state.student_data

def send_chat_message(usn: str, message: str):
    """Send chat message - OFFLINE MODE"""
    # Find the best matching response
    user_message_lower = message.lower()
    response = ATME_KNOWLEDGE.get(user_message_lower, 
        "I'm still learning about this! Please check with college administration or visit www.atme.edu.in for official information. 📚")
    
    # Update points in session state
    if st.session_state.student_data:
        st.session_state.student_data["points"] += 2
        st.session_state.student_data["level"] = st.session_state.student_data["points"] // 100 + 1
        
        # Check for first chat achievement
        if len(st.session_state.chat_history) == 0 and "first_chat" not in st.session_state.achievements:
            st.session_state.achievements.append({"achievement_key": "first_chat", "achievement_name": "First Conversation"})
            st.session_state.student_data["points"] += 20
    
    return {"response": response, "points_earned": 2}

def update_mood(usn: str, mood: str):
    """Update student mood - OFFLINE MODE"""
    if st.session_state.student_data:
        st.session_state.student_data["points"] += 8
        st.session_state.student_data["level"] = st.session_state.student_data["points"] // 100 + 1
        
        # Check for wellness achievement
        if "wellness_warrior" not in st.session_state.achievements:
            st.session_state.achievements.append({"achievement_key": "wellness_warrior", "achievement_name": "Wellness Warrior"})
            st.session_state.student_data["points"] += 30
    
    return {"message": "Mood updated successfully! 🌈", "points_earned": 8}

def get_chat_history(usn: str):
    """Get chat history - OFFLINE MODE"""
    return st.session_state.chat_history

def get_achievements(usn: str):
    """Get student achievements - OFFLINE MODE"""
    return st.session_state.achievements

def get_leaderboard():
    """Get leaderboard - OFFLINE MODE"""
    # Create sample leaderboard with current student
    if st.session_state.student_data:
        return [
            {"name": "Riya Vijay", "usn": "4AT23EC001", "department": "ECE", "points": 185, "level": 2},
            {"name": "Yeshaswini Madhumita", "usn": "4AT23CS001", "department": "CSE", "points": 167, "level": 2},
            {"name": st.session_state.student_data["name"], "usn": st.session_state.student_data["usn"], 
             "department": st.session_state.student_data["department"], "points": st.session_state.student_data["points"], "level": st.session_state.student_data["level"]},
            {"name": "Sandesh Mrashi", "usn": "4AT23EC002", "department": "ECE", "points": 142, "level": 2},
            {"name": "Aryan Sharma", "usn": "4AT23ME001", "department": "Mechanical", "points": 128, "level": 2}
        ]
    return []

def claim_daily_bonus(usn: str):
    """Claim daily bonus - OFFLINE MODE"""
    today = datetime.now().date()
    
    if st.session_state.last_login != today:
        st.session_state.last_login = today
        if st.session_state.student_data:
            st.session_state.student_data["points"] += 10
            st.session_state.student_data["level"] = st.session_state.student_data["points"] // 100 + 1
            
            # Check for daily user achievement
            if "daily_user" not in st.session_state.achievements:
                st.session_state.achievements.append({"achievement_key": "daily_user", "achievement_name": "Daily User"})
                st.session_state.student_data["points"] += 15
            
            return {"message": "Daily bonus claimed! 🎁", "points_earned": 10}
    
    return {"message": "Daily bonus already claimed today", "points_earned": 0}

def get_department_theme(department):
    """Get department theme based on selection"""
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
    """Create a progress chart for points"""
    progress = (points % 100)
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = progress,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"Level {level} Progress"},
        delta = {'reference': 100},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "#667eea"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 100], 'color': "gray"}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90}}))
    
    fig.update_layout(height=250, margin=dict(t=50, b=10, l=10, r=10))
    return fig

def main():
    st.set_page_config(
        page_title="ATME College Assistant", 
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS with advanced animations
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
        padding: 12px;
        border-radius: 12px;
        margin: 6px 0;
        width: 100%;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        font-size: 0.9em;
    }
    
    .question-button:hover {
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    .action-button {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        color: white;
        border: none;
        padding: 10px;
        border-radius: 10px;
        margin: 4px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 600;
        font-size: 0.85em;
    }
    
    .action-button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(72, 187, 120, 0.3);
    }
    
    .achievement-badge {
        background: linear-gradient(135deg, #f6e05e 0%, #ecc94b 100%);
        color: #744210;
        padding: 8px 12px;
        border-radius: 15px;
        margin: 4px;
        font-size: 0.8em;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .floating {
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
        100% { transform: translateY(0px); }
    }
    
    .feature-card {
        background: white;
        padding: 15px;
        border-radius: 12px;
        margin: 8px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border-left: 4px solid #667eea;
    }
    
    .feature-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 18px rgba(0,0,0,0.12);
    }
    
    .stButton button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Animated header
    st.markdown('<h1 class="main-header floating">🎓 ATME College Smart Assistant ⚡</h1>', unsafe_allow_html=True)
    
    # Student registration/login section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        student_name = st.text_input("👤 Your Name:", value="ATME Student", help="Enter your full name")
    
    with col2:
        student_usn = st.text_input("🆔 Your USN:", value="4AT23EC001", help="Format: 4AT23XX001")
    
    with col3:
        selected_department = st.selectbox("🎯 Select Your Department:", DEPARTMENTS)
    
    # Register/Login button
    if st.button("🚀 Login / Register", use_container_width=True, type="primary"):
        if selected_department != "Select Department" and student_name and student_usn:
            with st.spinner("Setting up your account..."):
                student_data = register_student(student_usn, student_name, selected_department)
                if student_data:
                    st.session_state.student_data = student_data
                    
                    # Claim daily bonus on login
                    bonus_result = claim_daily_bonus(student_usn)
                    if bonus_result["points_earned"] > 0:
                        st.success(f"🎁 {bonus_result['message']} +{bonus_result['points_earned']} points!")
                    
                    st.rerun()
        else:
            st.warning("Please fill all fields and select your department!")
    
    # Main application
    if st.session_state.student_data:
        student_data = st.session_state.student_data
        dept_theme = get_department_theme(student_data["department"])
        
        # Welcome section with dynamic theme
        st.markdown(f'''
        <div class="atme-card" style="background: {dept_theme['bg_gradient']};">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <h2 style="margin: 0; font-size: 2rem;">{dept_theme["emoji"]} Welcome, {student_data["name"]}!</h2>
                    <p style="margin: 8px 0; font-size: 1.1rem;">🎯 {student_data["department"]} | 🆔 {student_data["usn"]}</p>
                    <p style="margin: 0; font-size: 0.85rem; opacity: 0.9;">📍 Adichunchanagiri Road, Mysuru - 570028</p>
                </div>
                <div style="text-align: center;">
                    <h3 style="margin: 0; font-size: 2.5rem;" class="pulse">🏆 {student_data["points"]}</h3>
                    <p style="margin: 0; font-size: 1rem;">Level {student_data["level"]} 🚀</p>
                </div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Main content area
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("💬 Smart Chat Interface")
            
            # Quick questions organized by categories
            st.write("**🚀 Quick Questions About ATME:**")
            
            # Category tabs
            tab1, tab2, tab3, tab4 = st.tabs(["🏫 General", "🎓 Academic", "🏠 Facilities", "🎯 Departments"])
            
            with tab1:
                cols = st.columns(2)
                general_questions = ["college address", "contact information", "upcoming events", "college clubs", "hello", "help"]
                for i, question in enumerate(general_questions):
                    with cols[i % 2]:
                        if st.button(f"❓ {question.title()}", key=f"gen_{i}", use_container_width=True):
                            response_data = send_chat_message(student_data["usn"], question)
                            st.session_state.chat_history.append({
                                "user_message": question,
                                "bot_response": response_data["response"],
                                "timestamp": datetime.now().isoformat()
                            })
                            st.rerun()
            
            with tab2:
                cols = st.columns(2)
                academic_questions = ["academic calendar", "exam dates", "fee structure", "library information"]
                for i, question in enumerate(academic_questions):
                    with cols[i % 2]:
                        if st.button(f"❓ {question.title()}", key=f"acad_{i}", use_container_width=True):
                            response_data = send_chat_message(student_data["usn"], question)
                            st.session_state.chat_history.append({
                                "user_message": question,
                                "bot_response": response_data["response"],
                                "timestamp": datetime.now().isoformat()
                            })
                            st.rerun()
            
            with tab3:
                cols = st.columns(2)
                facility_questions = ["hostel facilities", "bus facilities", "sports facilities", "placement information"]
                for i, question in enumerate(facility_questions):
                    with cols[i % 2]:
                        if st.button(f"❓ {question.title()}", key=f"fac_{i}", use_container_width=True):
                            response_data = send_chat_message(student_data["usn"], question)
                            st.session_state.chat_history.append({
                                "user_message": question,
                                "bot_response": response_data["response"],
                                "timestamp": datetime.now().isoformat()
                            })
                            st.rerun()
            
            with tab4:
                cols = st.columns(2)
                # Get department-specific questions
                dept_map = {
                    "CSE": ["cse department", "cse labs"],
                    "ECE": ["ece department", "ece labs"], 
                    "Data Science": ["data science department"],
                    "AIML": ["aiml department"],
                    "Cyber Security": ["cyber security department"],
                    "Mechanical": ["mechanical department"],
                    "Civil": ["civil department"],
                    "EEE": ["eee department"],
                    "CSD": ["college clubs"]
                }
                
                dept_key = student_data["department"].split()[0]
                dept_questions = dept_map.get(dept_key, ["cse department", "cse labs"])
                dept_questions.extend(["ieee events", "technical fest"])
                
                for i, question in enumerate(dept_questions):
                    with cols[i % 2]:
                        if st.button(f"❓ {question.title()}", key=f"dept_{i}", use_container_width=True):
                            response_data = send_chat_message(student_data["usn"], question)
                            st.session_state.chat_history.append({
                                "user_message": question,
                                "bot_response": response_data["response"],
                                "timestamp": datetime.now().isoformat()
                            })
                            st.rerun()
            
            # Manual question input
            st.subheader("🔍 Ask Your Own Question")
            user_question = st.text_input(
                "Type your question about ATME College:",
                placeholder="e.g., When is the next cultural fest? What are the library timings? 🌸"
            )
            
            if user_question:
                with st.spinner("🤔 Thinking..."):
                    time.sleep(1)
                    response_data = send_chat_message(student_data["usn"], user_question)
                    
                    st.session_state.chat_history.append({
                        "user_message": user_question,
                        "bot_response": response_data["response"],
                        "timestamp": datetime.now().isoformat()
                    })
                    st.rerun()
            
            # Display chat history
            st.subheader("📜 Live Conversation")
            chat_history = get_chat_history(student_data["usn"])
            
            if chat_history:
                for chat in reversed(chat_history[-6:]):
                    st.markdown(f'<div class="chat-bubble-user">👤 {chat["user_message"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="chat-bubble-bot">🤖 {chat["bot_response"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div style="text-align: center; color: #718096; font-size: 0.75em; margin: 8px 0;">⏰ {datetime.fromisoformat(chat["timestamp"]).strftime("%H:%M")}</div>', unsafe_allow_html=True)
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
                if st.button("📅 Calendar", use_container_width=True, type="secondary"):
                    response_data = send_chat_message(student_data["usn"], "academic calendar")
                    st.session_state.chat_history.append({
                        "user_message": "academic calendar",
                        "bot_response": response_data["response"],
                        "timestamp": datetime.now().isoformat()
                    })
                    st.rerun()
                
                if st.button("🎫 Hall Ticket", use_container_width=True, type="secondary"):
                    response_data = send_chat_message(student_data["usn"], "exam dates")
                    st.session_state.chat_history.append({
                        "user_message": "exam dates and hall ticket",
                        "bot_response": response_data["response"],
                        "timestamp": datetime.now().isoformat()
                    })
                    st.rerun()
            
            with action_col2:
                if st.button("📚 Library", use_container_width=True, type="secondary"):
                    response_data = send_chat_message(student_data["usn"], "library information")
                    st.session_state.chat_history.append({
                        "user_message": "library information",
                        "bot_response": response_data["response"],
                        "timestamp": datetime.now().isoformat()
                    })
                    st.rerun()
                
                if st.button("💼 Placement", use_container_width=True, type="secondary"):
                    response_data = send_chat_message(student_data["usn"], "placement information")
                    st.session_state.chat_history.append({
                        "user_message": "placement information",
                        "bot_response": response_data["response"],
                        "timestamp": datetime.now().isoformat()
                    })
                    st.rerun()
            
            # Progress chart
            st.subheader("📊 Your Progress")
            fig = create_progress_chart(student_data["points"], student_data["level"])
            st.plotly_chart(fig, use_container_width=True)
            
            # Interactive wellness section
            st.subheader("🧠 Wellness Center")
            mood = st.select_slider(
                "How are you feeling today? 🌈", 
                options=["😔 Stressed", "😟 Anxious", "😐 Okay", "😊 Good", "🤩 Excellent"],
                value="😐 Okay"
            )
            
            if st.button("💖 Update Mood & Get Points", use_container_width=True, type="primary"):
                result = update_mood(student_data["usn"], mood)
                st.success(f"✅ {result['message']} +{result['points_earned']} points!")
                
                # Show random wellness tip
                wellness_tips = [
                    "Remember to take breaks and breathe deeply! 🧘‍♀️",
                    "Stay hydrated and get enough sleep! 💤",
                    "Talk to friends or counselors if you feel overwhelmed! 👥",
                    "Physical activity can boost your mood! 🏃‍♂️",
                    "You're doing great! Keep going! 💪",
                    "Small steps lead to big achievements! 🌟",
                    "Be kind to yourself today! 💝"
                ]
                st.info(f"**Wellness Tip:** {random.choice(wellness_tips)}")
                st.rerun()
            
            # Achievements display
            st.subheader("🏆 Your Achievements")
            achievements = get_achievements(student_data["usn"])
            if achievements:
                for achievement in achievements:
                    st.markdown(f'<div class="achievement-badge">⭐ {achievement["achievement_name"]}</div>', unsafe_allow_html=True)
            else:
                st.info("No achievements yet. Keep chatting to earn them! 🎯")
            
            # Leaderboard
            st.subheader("📈 Live Leaderboard")
            leaderboard = get_leaderboard()
            if leaderboard:
                leaderboard_df = pd.DataFrame(leaderboard)
                # Highlight current user
                def highlight_user(row):
                    if row['usn'] == student_data["usn"]:
                        return ['background-color: #E1F5FE'] * len(row)
                    else:
                        return [''] * len(row)
                
                styled_df = leaderboard_df[["name", "department", "points"]].head(6).style.apply(highlight_user, axis=1)
                st.dataframe(
                    styled_df,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("🏆 Be the first on the leaderboard!")
            
            # Department info card
            st.subheader(f"{dept_theme['emoji']} Your Department")
            dept_info = {
                "CSE": "💻 Focus on AI, ML, Software Development & Cloud Computing",
                "ECE": "🔬 Specializing in VLSI, Communication Systems & Embedded Systems", 
                "Data Science": "📊 Expertise in Data Analytics, Machine Learning & Big Data",
                "AIML": "🤖 Advanced studies in Neural Networks, Computer Vision & Robotics",
                "Cyber Security": "🛡️ Training in Network Security, Ethical Hacking & Cyber Laws",
                "Mechanical": "🔧 Focus on Design, Manufacturing, Thermal Engineering & Robotics",
                "Civil": "🏗️ Expertise in Structural, Environmental & Construction Engineering",
                "EEE": "⚡ Specializing in Power Systems, Control Systems & Renewable Energy",
                "CSD": "🎨 Combining Technology with UI/UX Design & Product Development"
            }
            
            for dept, info in dept_info.items():
                if dept in student_data["department"]:
                    st.markdown(f'''
                    <div class="feature-card">
                        <h4 style="margin: 0 0 8px 0; color: {dept_theme['color']};">{dept_theme["emoji"]} {dept}</h4>
                        <p style="margin: 0; color: #4A5568; font-size: 0.9em;">{info}</p>
                    </div>
                    ''', unsafe_allow_html=True)
                    break
    
    else:
        # Enhanced landing page
        st.markdown("""
        <div style="text-align: center; padding: 30px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; color: white; margin: 20px 0;">
            <h1 style="font-size: 2.5rem; margin: 0;">🎓 ATME College of Engineering</h1>
            <p style="font-size: 1.3rem; margin: 10px 0;">Where Innovation Meets Excellence ✨</p>
            <p style="margin: 5px 0; font-size: 0.9rem;">📍 Adichunchanagiri Road, Mysuru - 570028</p>
            <p style="margin: 5px 0; font-size: 0.9rem;">📞 0821-1234567 | 🌐 www.atme.edu.in</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Feature showcase
        st.subheader("🚀 Discover Amazing Features")
        
        feature_cols = st.columns(3)
        features = [
            {"emoji": "💬", "title": "AI-Powered Chat", "desc": "Smart responses with instant answers"},
            {"emoji": "🎯", "title": "Department Specific", "desc": "Tailored information for your branch"},
            {"emoji": "🏆", "title": "Gamification", "desc": "Earn points, levels & achievements"},
            {"emoji": "🧠", "title": "Wellness Support", "desc": "Mental health tracking & tips"},
            {"emoji": "📊", "title": "Live Analytics", "desc": "Track progress with beautiful charts"},
            {"emoji": "⚡", "title": "Instant Response", "desc": "No delays, works offline"}
        ]
        
        for i, feature in enumerate(features):
            with feature_cols[i % 3]:
                st.markdown(f"""
                <div class="feature-card">
                    <h3 style="margin: 0; font-size: 2rem; text-align: center;">{feature['emoji']}</h3>
                    <h4 style="margin: 10px 0 8px 0; color: #2D3748; text-align: center; font-size: 1rem;">{feature['title']}</h4>
                    <p style="margin: 0; color: #718096; text-align: center; font-size: 0.8em;">{feature['desc']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Quick start guide
        st.subheader("🎯 Get Started in 3 Steps")
        
        guide_cols = st.columns(3)
        with guide_cols[0]:
            st.markdown("""
            <div style="text-align: center; padding: 15px;">
                <h3 style="font-size: 1.5rem;">1️⃣</h3>
                <h4 style="margin: 8px 0;">Enter Details</h4>
                <p style="margin: 0; font-size: 0.8em;">Fill your name, USN and select department</p>
            </div>
            """, unsafe_allow_html=True)
        
        with guide_cols[1]:
            st.markdown("""
            <div style="text-align: center; padding: 15px;">
                <h3 style="font-size: 1.5rem;">2️⃣</h3>
                <h4 style="margin: 8px 0;">Login</h4>
                <p style="margin: 0; font-size: 0.8em;">Click the login button to get started</p>
            </div>
            """, unsafe_allow_html=True)
        
        with guide_cols[2]:
            st.markdown("""
            <div style="text-align: center; padding: 15px;">
                <h3 style="font-size: 1.5rem;">3️⃣</h3>
                <h4 style="margin: 8px 0;">Start Chatting</h4>
                <p style="margin: 0; font-size: 0.8em;">Ask questions and explore features</p>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
