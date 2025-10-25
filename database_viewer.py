# database_viewer.py
import sqlite3
import pandas as pd
import streamlit as st

def view_database():
    st.set_page_config(page_title="Database Viewer", layout="wide")
    st.title("🔍 ATME Database Viewer")
    
    try:
        conn = sqlite3.connect('atme_college.db')
        
        # List all tables
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        st.sidebar.header("📊 Database Tables")
        selected_table = st.sidebar.selectbox("Select Table:", [table[0] for table in tables])
        
        if selected_table:
            # Display table data
            df = pd.read_sql_query(f"SELECT * FROM {selected_table}", conn)
            st.subheader(f"📋 {selected_table} Table")
            st.dataframe(df)
            
            # Show statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Records", len(df))
            with col2:
                st.metric("Columns", len(df.columns))
            with col3:
                if 'points' in df.columns:
                    st.metric("Total Points", df['points'].sum())
        
        # Student statistics
        st.subheader("🎓 Student Statistics")
        students_df = pd.read_sql_query("SELECT * FROM students", conn)
        if not students_df.empty:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Students", len(students_df))
            with col2:
                st.metric("Avg Points", int(students_df['points'].mean()))
            with col3:
                st.metric("Max Points", students_df['points'].max())
            with col4:
                st.metric("Top Department", students_df['department'].mode().iloc[0] if not students_df.empty else "N/A")
            
            # Department distribution
            dept_stats = students_df['department'].value_counts()
            st.bar_chart(dept_stats)
        
        conn.close()
        
    except Exception as e:
        st.error(f"Database not found or error: {e}")
        st.info("Make sure the backend has been run at least once to create the database.")

if __name__ == "__main__":
    view_database()
