# backend.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import sqlite3
import json
import hashlib
import os
from typing import Dict, List, Optional

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database initialization
def init_db():
    conn = sqlite3.connect('atme_college.db')
    cursor = conn.cursor()
    
    # Students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            usn TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            points INTEGER DEFAULT 100,
            level INTEGER DEFAULT 1,
            avatar TEXT DEFAULT '🎓',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Chat history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usn TEXT NOT NULL,
            user_message TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            points_earned INTEGER DEFAULT 0,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usn) REFERENCES students (usn)
        )
    ''')
    
    # Achievements table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usn TEXT NOT NULL,
            achievement_key TEXT NOT NULL,
            achievement_name TEXT NOT NULL,
            earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usn) REFERENCES students (usn)
        )
    ''')
    
    # Mood tracking table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mood_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usn TEXT NOT NULL,
            mood TEXT NOT NULL,
            points_earned INTEGER DEFAULT 0,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usn) REFERENCES students (usn)
        )
    ''')
    
    # Daily bonuses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_bonuses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usn TEXT NOT NULL,
            claimed_date DATE NOT NULL,
            points_earned INTEGER DEFAULT 10,
            FOREIGN KEY (usn) REFERENCES students (usn)
        )
    ''')
    
    conn.commit()
    conn.close()

# Comprehensive Knowledge Base (same as frontend)
ATME_KNOWLEDGE = {
    "college address": "🏫 **ATME College of Engineering**\n📍 **Address:** Adichunchanagiri Road, Mysuru - 570028, Karnataka\n🌍 **Location:** Near BGS Health Centre, Mysuru\n📞 **Phone:** 0821-1234567\n🕒 **Office Hours:** 9:00 AM - 5:00 PM (Mon-Sat)",
    
    "contact information": "📞 **ATME Contact Details:**\n• **College Office:** 0821-1234567\n• **Principal Office:** 0821-1234568\n• **Admission Office:** 0821-1234569\n• **Email:** info@atme.edu.in\n• **Website:** www.atme.edu.in\n• **Emergency:** 0821-1234580",
    
    "academic calendar": "📅 **Academic Year 2024-25**\n\n**Odd Semester (2024):**\n• Semester Start: August 1, 2024\n• Mid-term Exams: October 15-30, 2024\n• End Semester Exams: December 8-23, 2024\n• Winter Break: December 24 - January 5, 2025\n\n**Even Semester (2025):**\n• Semester Start: January 6, 2025\n• Mid-term Exams: March 15-30, 2025\n• End Semester Exams: May 15-30, 2025\n• Summer Break: June 1 - July 31, 2025",
    
    "exam dates": "📚 **Semester Exams Schedule 2024-25:**\n\n**Odd Semester Exams:**\n• Theory Exams: December 8-23, 2024\n• Practical Exams: December 1-7, 2024\n• Project Evaluation: December 1-10, 2024\n\n**Even Semester Exams:**\n• Theory Exams: May 15-30, 2025\n• Practical Exams: May 8-14, 2025\n• Project Evaluation: May 8-17, 2025\n\n**Hall Tickets:** Available 15 days before exams on portal.atme.edu.in",
    
    "library information": "📖 **ATME Central Library**\n\n**⏰ Timings:**\n• Monday-Friday: 8:00 AM - 8:00 PM\n• Saturday: 9:00 AM - 5:00 PM\n• Sunday: Closed\n\n**📚 Collection:**\n• 50,000+ Books\n• 100+ National & International Journals\n• 5000+ E-books\n• 50+ Online Databases\n\n**💻 Facilities:**\n• Digital Library (24/7 online access)\n• Photocopy & Printing Services\n• Reading Rooms (AC & Non-AC)\n• Group Discussion Rooms",
    
    "hostel facilities": "🏠 **ATME Hostels**\n\n**Accommodation:**\n• Separate hostels for Boys & Girls\n• Single, Double, Triple occupancy rooms\n• 24/7 Security & CCTV surveillance\n• Wi-Fi enabled campuses\n\n**💵 Fee Structure (Per Year):**\n• Hostel Fee: ₹45,000\n• Mess Charges: ₹15,000\n• **Total: ₹60,000**\n\n**🏋️ Facilities:**\n• Gymnasium\n• Reading Room\n• Indoor Games\n• Common TV Room\n• Hot Water Supply",
    
    "fee structure": "💰 **Fee Structure (Per Semester)**\n\n**Breakup:**\n• Tuition Fee: ₹45,000\n• Development Fee: ₹15,000\n• Examination Fee: ₹5,000\n• Library Fee: ₹2,000\n• Sports Fee: ₹1,000\n• Other Charges: ₹2,000\n\n**💵 Total: ₹70,000 per semester**\n\n**Payment Methods:**\n• Online: portal.atme.edu.in\n• Bank Transfer\n• Cash: College accounts office",
    
    "bus facilities": "🚌 **College Bus Service**\n\n**⏰ Timings:**\n• Morning Pickup: 7:00 AM - 8:30 AM\n• Evening Drop: 4:30 PM - 6:30 PM\n\n**🗺️ Major Routes:**\n1. Vijayanagar → Kuvempunagar → College\n2. Saraswathipuram → Gokulam → College\n3. Hebbal → Hootagalli → College\n4. Bannimantap → JSS Layout → College\n\n**💵 Bus Pass:** ₹8,000 per semester",
    
    "sports facilities": "⚽ **Sports Complex & Facilities**\n\n**Outdoor Facilities:**\n• Cricket Ground with practice nets\n• Basketball Court (2 courts)\n• Volleyball Court\n• Football Ground\n• Badminton Courts (4 courts)\n• Athletic Track\n\n**Indoor Facilities:**\n• Gymnasium with trainer\n• Table Tennis (6 tables)\n• Chess & Carrom\n• Yoga Hall",
    
    "placement information": "💼 **Training & Placement Cell**\n\n**👨‍🏫 TPO:** Dr. S. R. Kumar\n**🏢 Office:** Placement Block, Ground Floor\n**📞 Phone:** 0821-1234573\n**📧 Email:** placement@atme.edu.in\n\n**🏢 Recruiting Companies:**\n• **IT Giants:** Infosys, Wipro, TCS, IBM, Accenture\n• **Core Companies:** Intel, Texas Instruments, L&T, Bosch\n• **Startups:** Multiple tech startups\n\n**📊 Placement Statistics (2023):**\n• 85% Placement Rate\n• Highest Package: ₹18 LPA\n• Average Package: ₹6.5 LPA",
    
    "ieee events": "⚡ **ATME IEEE Student Branch**\n\n**👨‍🏫 Faculty Advisor:** Dr. Priya Sharma\n**🎯 Student Chair:** [Your Name Here]\n\n**📅 Upcoming Events:**\n• **IEEE Mini Project Exhibition** - Tomorrow!\n• Technical workshops every month\n• Guest lectures from industry experts\n• Project competitions\n\n**🤝 Benefits:**\n• Access to IEEE resources\n• Networking opportunities\n• Skill development workshops",
    
    "college website": "🌐 **ATME Digital Platforms**\n\n**Main Platforms:**\n• **Website:** www.atme.edu.in\n• **Student Portal:** portal.atme.edu.in\n• **Learning Management:** lms.atme.edu.in\n• **Email:** username@atme.edu.in\n\n**Portal Features:**\n• Attendance tracking\n• Marks and grades\n• Fee payment\n• Hall ticket download\n• Course materials",
    
    "cse department": "💻 **Computer Science & Engineering**\n\n**👨‍🏫 HOD:** Dr. Suresh Kumar\n**📧 Email:** hod.cse@atme.edu.in\n**🏢 Office:** CSE Block, 1st Floor\n**📞 Phone:** 0821-1234575\n\n**🎯 Specializations:**\n• Artificial Intelligence & Machine Learning\n• Data Science\n• Cyber Security\n• Full Stack Development\n• Cloud Computing",
    
    "ece department": "🔬 **Electronics & Communication Engineering**\n\n**👩‍🏫 HOD:** Dr. Priya Sharma\n**📧 Email:** hod.ece@atme.edu.in\n**🏢 Office:** ECE Block, 2nd Floor\n**📞 Phone:** 0821-1234576\n\n**🎯 Specializations:**\n• VLSI Design\n• Communication Systems\n• Embedded Systems\n• Signal Processing\n• IoT & Sensors",
    
    "cse labs": "💻 **CSE Laboratories Schedule**\n\n**Programming Lab:**\n• Mon-Fri: 9:00 AM - 5:00 PM\n• Special sessions: Sat 9AM-1PM\n\n**AI/ML Lab:**\n• 24/7 access with faculty permission\n• GPU computing resources available\n\n**Project Lab:**\n• Extended hours during project time\n• Group discussions allowed",
    
    "ece labs": "🔬 **ECE Laboratories Schedule**\n\n**Basic Electronics Lab:**\n• Mon/Wed/Fri: 9:00 AM - 5:00 PM\n\n**DSP Lab:**\n• Tue/Thu: 2:00 PM - 5:00 PM\n\n**VLSI Lab:**\n• Special slots with appointment\n• Advanced equipment available",
    
    "mechanical department": "🔧 **Mechanical Engineering**\n\n**👨‍🏫 HOD:** Dr. Sanjay Verma\n**📧 Email:** hod.mech@atme.edu.in\n**🏢 Office:** Mechanical Block, Ground Floor\n**📞 Phone:** 0821-1234577\n\n**🎯 Specializations:**\n• Thermal Engineering\n• Manufacturing Technology\n• Machine Design\n• Automobile Engineering\n• Robotics & Automation",
    
    "civil department": "🏗️ **Civil Engineering**\n\n**👩‍🏫 HOD:** Dr. Sunita Rao\n**📧 Email:** hod.civil@atme.edu.in\n**🏢 Office:** Civil Block, 1st Floor\n**📞 Phone:** 0821-1234578\n\n**🎯 Specializations:**\n• Structural Engineering\n• Environmental Engineering\n• Geotechnical Engineering\n• Construction Management\n• Transportation Engineering",
    
    "eee department": "⚡ **Electrical & Electronics Engineering**\n\n**👨‍🏫 HOD:** Dr. Mohan Das\n**📧 Email:** hod.eee@atme.edu.in\n**🏢 Office:** EEE Block, 2nd Floor\n**📞 Phone:** 0821-1234579\n\n**🎯 Specializations:**\n• Power Systems\n• Control Systems\n• Renewable Energy\n• Power Electronics\n• Electrical Machines",
    
    "data science department": "📊 **Data Science Department**\n\n**👩‍🏫 HOD:** Dr. Anjali Mehta\n**🏢 Office:** New Academic Block, 3rd Floor\n\n**💻 Lab Facilities:**\n• Data Analytics Lab with high-end systems\n• Hadoop cluster for big data\n• Python, R programming environments\n• Tableau for visualization",
    
    "aiml department": "🤖 **AI & ML Department**\n\n**👨‍🏫 HOD:** Dr. Rajesh Khanna\n**🏢 Office:** New Academic Block, 4th Floor\n\n**🔬 Research Areas:**\n• Machine Learning Algorithms\n• Deep Learning & Neural Networks\n• Natural Language Processing\n• Computer Vision\n• Robotics & Automation",
    
    "cyber security department": "🛡️ **Cyber Security Department**\n\n**👩‍🏫 HOD:** Dr. Priya Nair\n**🏢 Office:** New Academic Block, 2nd Floor\n\n**🔒 Lab Facilities:**\n• Secure Computing Lab\n• Isolated network environment\n• Kali Linux systems\n• Penetration testing tools",
    
    "upcoming events": "🎯 **Upcoming Events at ATME (2024-25)**\n\n**Technical Events:**\n• **IEEE Mini Project Exhibition** - Tomorrow!\n• **Technical Symposium 'TECHNOVATE'** - November 20-22, 2024\n• **Hackathon 2024** - December 10-11, 2024\n• **Paper Presentation Contest** - January 15, 2025\n\n**Cultural Events:**\n• **Cultural Fest 'Utsav'** - December 15-17, 2024\n• **Freshers Party** - August 30, 2024\n• **Annual Day** - March 15, 2025\n\n**Sports Events:**\n• **Sports Week** - January 20-25, 2025\n• **Inter-department Tournaments** - Monthly",
    
    "cultural fest": "🎭 **Cultural Fest 'Utsav' 2024**\n\n**📅 Dates:** December 15-17, 2024\n**📍 Venue:** College Auditorium & Grounds\n\n**🎪 Major Events:**\n• **Dance Competition** (Solo & Group)\n• **Music Competition** (Vocal & Instrumental)\n• **Drama & Street Play**\n• **Fashion Show**\n• **Fine Arts Exhibition**\n• **Literary Events**\n\n**🏆 Prizes:**\n• Trophy for overall championship\n• Cash prizes for winners\n• Certificates for all participants",
    
    "technical fest": "🔧 **Technical Fest 'TECHNOVATE' 2024**\n\n**📅 Dates:** November 20-22, 2024\n**🎯 Theme:** \"Innovation for Sustainable Future\"\n\n**💻 Major Competitions:**\n• **Code Marathon** (24-hour coding)\n• **Project Expo** (Hardware & Software)\n• **Paper Presentation**\n• **Robo Race**\n• **Circuit Design**\n• **Quiz Competition**\n\n**👥 Workshops:**\n• IoT & Embedded Systems\n• AI & Machine Learning\n• Web Development\n• Robotics\n\n**💰 Prize Money:** Up to ₹50,000",
    
    "college clubs": "👥 **Student Clubs & Associations**\n\n**Technical Clubs:**\n• **Coding Club** - Weekly programming sessions\n• **Robotics Club** - Project building & competitions\n• **IEEE Student Branch** - Technical activities\n• **CSI Chapter** - Computer society events\n\n**Cultural Clubs:**\n• **Literary Club** - Debates, writing competitions\n• **Music Club** - Practice sessions & performances\n• **Dance Club** - Various dance forms training\n• **Drama Club** - Theater performances\n\n**Other Clubs:**\n• **Eco Club** - Environmental activities\n• **Sports Club** - Regular tournaments\n• **Photography Club** - Workshops & exhibitions",
    
    "mental health": "🧠 **Student Counseling & Mental Health**\n\n**👨‍⚕️ Counselor:** Dr. Anitha Psychologist\n**📞 Appointment:** 0821-1234582\n**🏢 Location:** Administrative Block, 2nd Floor\n\n**⏰ Counseling Hours:**\n• Monday-Friday: 10:00 AM - 4:00 PM\n• Saturday: 10:00 AM - 1:00 PM\n\n**🤝 Services:**\n• Academic stress management\n• Career counseling\n• Personal issues guidance\n• Group therapy sessions\n• Crisis intervention\n\n**🔒 Confidentiality:** All sessions are strictly confidential",
    
    "hello": "👋 **Hello! I'm ATME College Assistant!** 🤖\n\nI can help you with:\n• 📚 Academic information\n• 🏫 College facilities\n• 🎯 Department details\n• 🎉 Events and activities\n• 💼 Placement information\n• 🧠 Mental health support\n\nWhat would you like to know?",
    
    "hi": "👋 **Hi there! Welcome to ATME College!** 🎓\n\nI'm here to help you with any questions about our college. Ask me about exams, facilities, departments, or events!",
    
    "help": "🆘 **Here's how I can help you:**\n\n**Academic Questions:**\n• Ask about exams, schedules, fees\n• Library timings and facilities\n• Academic calendar\n\n**College Facilities:**\n• Hostel information\n• Bus services\n• Sports facilities\n• Placement cell\n\n**Departments:**\n• Department-specific information\n• Lab schedules\n• HOD contacts\n\n**Events:**\n• Upcoming college events\n• Cultural fest details\n• Technical competitions\n\nJust ask me anything! 💬"
}

# Database helper functions
def get_db_connection():
    conn = sqlite3.connect('atme_college.db')
    conn.row_factory = sqlite3.Row
    return conn

# API Routes

@app.route('/api/register', methods=['POST'])
def register_student():
    """Register a new student"""
    data = request.json
    usn = data.get('usn')
    name = data.get('name')
    department = data.get('department')
    
    if not all([usn, name, department]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if student already exists
        cursor.execute('SELECT * FROM students WHERE usn = ?', (usn,))
        existing_student = cursor.fetchone()
        
        if existing_student:
            # Update last login
            cursor.execute('UPDATE students SET last_login = CURRENT_TIMESTAMP WHERE usn = ?', (usn,))
            student_data = dict(existing_student)
        else:
            # Create new student
            cursor.execute('''
                INSERT INTO students (usn, name, department, points, level, avatar)
                VALUES (?, ?, ?, 100, 1, '🎓')
            ''', (usn, name, department))
            student_data = {
                'usn': usn,
                'name': name,
                'department': department,
                'points': 100,
                'level': 1,
                'avatar': '🎓'
            }
        
        conn.commit()
        return jsonify({'success': True, 'student_data': student_data})
    
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/student/<usn>', methods=['GET'])
def get_student(usn):
    """Get student data"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT * FROM students WHERE usn = ?', (usn,))
        student = cursor.fetchone()
        
        if student:
            return jsonify({'success': True, 'student_data': dict(student)})
        else:
            return jsonify({'error': 'Student not found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/chat/send', methods=['POST'])
def send_chat_message():
    """Send a chat message and get response"""
    data = request.json
    usn = data.get('usn')
    message = data.get('message')
    
    if not usn or not message:
        return jsonify({'error': 'Missing USN or message'}), 400
    
    # Get response from knowledge base
    user_message_lower = message.lower()
    response = ATME_KNOWLEDGE.get(user_message_lower, 
        "I'm still learning about this! Please check with college administration or visit www.atme.edu.in for official information. 📚")
    
    points_earned = 2
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Update student points and level
        cursor.execute('UPDATE students SET points = points + ?, level = (points + ?) // 100 + 1 WHERE usn = ?', 
                     (points_earned, points_earned, usn))
        
        # Save chat history
        cursor.execute('''
            INSERT INTO chat_history (usn, user_message, bot_response, points_earned)
            VALUES (?, ?, ?, ?)
        ''', (usn, message, response, points_earned))
        
        # Check for first chat achievement
        cursor.execute('SELECT COUNT(*) as count FROM chat_history WHERE usn = ?', (usn,))
        chat_count = cursor.fetchone()['count']
        
        if chat_count == 1:
            # Award first chat achievement
            cursor.execute('''
                INSERT INTO achievements (usn, achievement_key, achievement_name)
                VALUES (?, 'first_chat', 'First Conversation')
            ''', (usn,))
            cursor.execute('UPDATE students SET points = points + 20 WHERE usn = ?', (usn,))
            points_earned += 20
        
        conn.commit()
        
        return jsonify({
            'success': True,
            'response': response,
            'points_earned': points_earned
        })
    
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/mood/update', methods=['POST'])
def update_mood():
    """Update student mood"""
    data = request.json
    usn = data.get('usn')
    mood = data.get('mood')
    
    if not usn or not mood:
        return jsonify({'error': 'Missing USN or mood'}), 400
    
    points_earned = 8
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Update student points
        cursor.execute('UPDATE students SET points = points + ?, level = (points + ?) // 100 + 1 WHERE usn = ?', 
                     (points_earned, points_earned, usn))
        
        # Save mood data
        cursor.execute('''
            INSERT INTO mood_data (usn, mood, points_earned)
            VALUES (?, ?, ?)
        ''', (usn, mood, points_earned))
        
        # Check for wellness achievement
        cursor.execute('SELECT COUNT(*) as count FROM mood_data WHERE usn = ?', (usn,))
        mood_count = cursor.fetchone()['count']
        
        if mood_count == 1:
            # Award wellness achievement
            cursor.execute('''
                INSERT INTO achievements (usn, achievement_key, achievement_name)
                VALUES (?, 'wellness_warrior', 'Wellness Warrior')
            ''', (usn,))
            cursor.execute('UPDATE students SET points = points + 30 WHERE usn = ?', (usn,))
            points_earned += 30
        
        conn.commit()
        
        return jsonify({
            'success': True,
            'message': 'Mood updated successfully! 🌈',
            'points_earned': points_earned
        })
    
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/chat/history/<usn>', methods=['GET'])
def get_chat_history(usn):
    """Get chat history for a student"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT user_message, bot_response, timestamp, points_earned
            FROM chat_history 
            WHERE usn = ? 
            ORDER BY timestamp DESC 
            LIMIT 50
        ''', (usn,))
        
        chat_history = []
        for row in cursor.fetchall():
            chat_history.append({
                'user_message': row['user_message'],
                'bot_response': row['bot_response'],
                'timestamp': row['timestamp'],
                'points_earned': row['points_earned']
            })
        
        return jsonify({'success': True, 'chat_history': chat_history})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/achievements/<usn>', methods=['GET'])
def get_achievements(usn):
    """Get student achievements"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT achievement_key, achievement_name, earned_at
            FROM achievements 
            WHERE usn = ? 
            ORDER BY earned_at DESC
        ''', (usn,))
        
        achievements = []
        for row in cursor.fetchall():
            achievements.append({
                'achievement_key': row['achievement_key'],
                'achievement_name': row['achievement_name'],
                'earned_at': row['earned_at']
            })
        
        return jsonify({'success': True, 'achievements': achievements})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get leaderboard data"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT name, usn, department, points, level
            FROM students 
            ORDER BY points DESC 
            LIMIT 10
        ''')
        
        leaderboard = []
        for row in cursor.fetchall():
            leaderboard.append({
                'name': row['name'],
                'usn': row['usn'],
                'department': row['department'],
                'points': row['points'],
                'level': row['level']
            })
        
        return jsonify({'success': True, 'leaderboard': leaderboard})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/daily-bonus/<usn>', methods=['POST'])
def claim_daily_bonus(usn):
    """Claim daily login bonus"""
    today = datetime.now().date()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if bonus already claimed today
        cursor.execute('SELECT * FROM daily_bonuses WHERE usn = ? AND claimed_date = ?', (usn, today))
        existing_bonus = cursor.fetchone()
        
        if existing_bonus:
            return jsonify({
                'success': True,
                'message': 'Daily bonus already claimed today',
                'points_earned': 0
            })
        
        points_earned = 10
        
        # Award daily bonus
        cursor.execute('UPDATE students SET points = points + ?, level = (points + ?) // 100 + 1 WHERE usn = ?', 
                     (points_earned, points_earned, usn))
        
        # Record bonus claim
        cursor.execute('INSERT INTO daily_bonuses (usn, claimed_date, points_earned) VALUES (?, ?, ?)', 
                     (usn, today, points_earned))
        
        # Check for daily user achievement
        cursor.execute('SELECT COUNT(*) as count FROM daily_bonuses WHERE usn = ?', (usn,))
        bonus_count = cursor.fetchone()['count']
        
        if bonus_count == 1:
            # Award daily user achievement
            cursor.execute('''
                INSERT INTO achievements (usn, achievement_key, achievement_name)
                VALUES (?, 'daily_user', 'Daily User')
            ''', (usn,))
            cursor.execute('UPDATE students SET points = points + 15 WHERE usn = ?', (usn,))
            points_earned += 15
        
        # Update last login
        cursor.execute('UPDATE students SET last_login = CURRENT_TIMESTAMP WHERE usn = ?', (usn,))
        
        conn.commit()
        
        return jsonify({
            'success': True,
            'message': 'Daily bonus claimed! 🎁',
            'points_earned': points_earned
        })
    
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/stats/<usn>', methods=['GET'])
def get_student_stats(usn):
    """Get comprehensive student statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Student basic info
        cursor.execute('SELECT * FROM students WHERE usn = ?', (usn,))
        student = cursor.fetchone()
        
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        # Chat statistics
        cursor.execute('SELECT COUNT(*) as total_chats, SUM(points_earned) as chat_points FROM chat_history WHERE usn = ?', (usn,))
        chat_stats = cursor.fetchone()
        
        # Mood statistics
        cursor.execute('SELECT COUNT(*) as mood_entries, SUM(points_earned) as mood_points FROM mood_data WHERE usn = ?', (usn,))
        mood_stats = cursor.fetchone()
        
        # Achievement statistics
        cursor.execute('SELECT COUNT(*) as total_achievements FROM achievements WHERE usn = ?', (usn,))
        achievement_stats = cursor.fetchone()
        
        stats = {
            'student_data': dict(student),
            'chat_stats': {
                'total_chats': chat_stats['total_chats'] or 0,
                'chat_points': chat_stats['chat_points'] or 0
            },
            'mood_stats': {
                'mood_entries': mood_stats['mood_entries'] or 0,
                'mood_points': mood_stats['mood_points'] or 0
            },
            'achievement_stats': {
                'total_achievements': achievement_stats['total_achievements'] or 0
            }
        }
        
        return jsonify({'success': True, 'stats': stats})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Run the Flask app
    print("🚀 ATME College Assistant Backend Server Starting...")
    print("📊 Database initialized: atme_college.db")
    print("🌐 API Server running on: http://localhost:5000")
    print("\nAvailable Endpoints:")
    print("  POST /api/register - Register student")
    print("  GET  /api/student/<usn> - Get student data")
    print("  POST /api/chat/send - Send chat message")
    print("  POST /api/mood/update - Update mood")
    print("  GET  /api/chat/history/<usn> - Get chat history")
    print("  GET  /api/achievements/<usn> - Get achievements")
    print("  GET  /api/leaderboard - Get leaderboard")
    print("  POST /api/daily-bonus/<usn> - Claim daily bonus")
    print("  GET  /api/stats/<usn> - Get student stats")
    print("  GET  /api/health - Health check")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
