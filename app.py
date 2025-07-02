import streamlit as st
import json
import os
from datetime import datetime
import pandas as pd

# Configure page
st.set_page_config(
    page_title="Team Agreement Form",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin: 0;
    }
    
    /* Agreement Card */
    .agreement-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
    }
    
    .agreement-title {
        color: #2d3748;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
    }
    
    .agreement-content {
        color: #4a5568;
        line-height: 1.8;
        font-size: 1rem;
    }
    
    .agreement-content ul {
        padding-left: 0;
        list-style: none;
    }
    
    .agreement-content li {
        margin: 1rem 0;
        padding-left: 2rem;
        position: relative;
    }
    
    .agreement-content li:before {
        content: "✓";
        position: absolute;
        left: 0;
        color: #48bb78;
        font-weight: bold;
        font-size: 1.2rem;
    }
    
    /* Form Styling */
    .form-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .form-title {
        color: #2d3748;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
    }
    
    /* Member Card */
    .member-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-left: 4px solid #48bb78;
        transition: transform 0.2s ease;
    }
    
    .member-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.12);
    }
    
    .member-name {
        color: #2d3748;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .member-details {
        color: #718096;
        font-size: 0.9rem;
        margin: 0.3rem 0;
    }
    
    .member-role {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        display: inline-block;
        margin-top: 0.5rem;
    }
    
    /* Success Animation */
    .success-message {
        background: linear-gradient(135deg, #48bb78, #38a169);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        text-align: center;
        font-weight: 500;
        animation: slideIn 0.5s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f7fafc 0%, #edf2f7 100%);
    }
    
    /* Input Styling */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        transition: border-color 0.2s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Stats Cards */
    .stats-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    .stats-number {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .stats-label {
        font-size: 1rem;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# Data file path
DATA_FILE = "team_members.json"

# Initialize session state
if 'members' not in st.session_state:
    st.session_state.members = []
    # Load existing data
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                st.session_state.members = json.load(f)
        except:
            st.session_state.members = []

if 'show_success' not in st.session_state:
    st.session_state.show_success = False

# Helper functions
def save_data():
    """Save member data to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(st.session_state.members, f, indent=2)

def add_member(member_data):
    """Add new member to the list"""
    member_data['id'] = len(st.session_state.members) + 1
    member_data['accepted_at'] = datetime.now().isoformat()
    st.session_state.members.append(member_data)
    save_data()
    st.session_state.show_success = True

def is_email_exists(email):
    """Check if email already exists"""
    return any(member['email'].lower() == email.lower() for member in st.session_state.members)

# Main header
st.markdown("""
<div class="main-header">
    <h1>📋 Final Year Project Agreement</h1>
    <p>Please read the agreement carefully and provide your details to join the project team</p>
</div>
""", unsafe_allow_html=True)

# Create main layout
col1, col2 = st.columns([2, 1])

with col1:
    # Agreement Statement
    st.markdown("""
    <div class="agreement-card">
        <div class="agreement-title">
            📜 Agreement Statement
        </div>
        <div class="agreement-content">
            <p><strong>We, the undersigned, hereby declare that we have mutually discussed, agreed upon, and accepted the above-mentioned project idea for our final year engineering major project.</strong></p>
            
            <p><strong>We further confirm that:</strong></p>
            
            <ul>
                <li>We have no objection whatsoever to the project idea, its development process, methodology, or final outcomes.</li>
                <li>We mutually agree to contribute sincerely and collaboratively towards the successful execution and submission of the project.</li>
                <li>In the event of any technical, operational, or other challenges, all matters will be resolved amicably and collectively, without blaming any individual or member.</li>
                <li>We accept that the success or failure of the project is a shared responsibility, and no member shall hold another solely responsible for the outcome.</li>
            </ul>
            
            <p><strong>This agreement is made in good faith, with the purpose of ensuring harmony, clarity, and professional conduct within the team throughout the project lifecycle.</strong></p>
            
            <p style="background: #f7fafc; padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                <strong>Note:</strong> This agreement is binding upon all members until the successful completion, submission, and acceptance of the final project by the institution.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Team Member Details Form
    st.markdown("""
    <div class="form-container">
        <div class="form-title">
            👤 Team Member Details
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Form
    with st.form("member_form", clear_on_submit=True):
        # Personal Information
        st.subheader("📝 Personal Information")
        col1_form, col2_form = st.columns(2)
        
        with col1_form:
            name = st.text_input("Full Name *", placeholder="Enter your full name")
            email = st.text_input("Email Address *", placeholder="your.email@university.edu")
            student_id = st.text_input("Student ID *", placeholder="Enter your student ID")
        
        with col2_form:
            phone = st.text_input("Phone Number *", placeholder="+1 (555) 123-4567")
            department = st.selectbox("Department *", [
                "", "Electronics and Telecommunication", "Electrical Engineering", "Computer Engineering",
                "Civil Engineering", "Chemical Engineering", "Aerospace Engineering",
                "Biomedical Engineering", "Information Technology"
            ])
            year = st.selectbox("Academic Year *", [
                "", "Final Year (4th Year)", "Third Year", "Second Year", "First Year"
            ])
        
        # Project Information
        st.subheader("💼 Project Information")
        col3_form, col4_form = st.columns(2)
        
        with col3_form:
            role = st.selectbox("Project Role *", [
                "", "Team Lead", "Frontend Developer", "Backend Developer",
                "Full Stack Developer", "UI/UX Designer", "Data Analyst",
                "Researcher", "Quality Assurance", "Documentation Specialist"
            ])
        
        with col4_form:
            specialization = st.text_input("Area of Specialization *", 
                                         placeholder="e.g., Machine Learning, Web Development")
        
        # Agreement Checkboxes
        st.subheader("✅ Confirmation & Agreement")
        
        agree_terms = st.checkbox(
            "I have read and understood the project agreement statement and accept all terms and conditions mentioned above."
        )
        
        agree_collaboration = st.checkbox(
            "I commit to collaborate sincerely and contribute actively to the successful completion of this project."
        )
        
        agree_responsibility = st.checkbox(
            "I accept shared responsibility for the project outcome and agree to resolve any conflicts amicably."
        )
        
        # Submit button
        submitted = st.form_submit_button("🎯 I Accept & Join the Team", use_container_width=True)
        
        # Form validation and submission
        if submitted:
            # Validate required fields
            required_fields = {
                "Name": name,
                "Email": email,
                "Student ID": student_id,
                "Phone": phone,
                "Department": department,
                "Year": year,
                "Role": role,
                "Specialization": specialization
            }
            
            missing_fields = [field for field, value in required_fields.items() if not value]
            
            if missing_fields:
                st.error(f"❌ Please fill in the following required fields: {', '.join(missing_fields)}")
            elif not all([agree_terms, agree_collaboration, agree_responsibility]):
                st.error("❌ Please check all agreement boxes to proceed")
            elif is_email_exists(email):
                st.error("❌ This email has already signed the agreement")
            else:
                # Add member
                member_data = {
                    "name": name,
                    "email": email,
                    "student_id": student_id,
                    "phone": phone,
                    "department": department,
                    "year": year,
                    "role": role,
                    "specialization": specialization
                }
                add_member(member_data)
                st.success(f"🎉 Welcome to the team, {name}! Your agreement has been recorded successfully.")
                st.balloons()

# Sidebar - Team Members Panel
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #48bb78, #38a169); border-radius: 10px; margin-bottom: 1rem;">
        <h2 style="color: white; margin: 0;">👥 Team Members</h2>
        <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 0.9rem;">Members who have signed the agreement</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats
    total_members = len(st.session_state.members)
    st.markdown(f"""
    <div class="stats-card">
        <div class="stats-number">{total_members}</div>
        <div class="stats-label">Team Members</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Display team members
    if st.session_state.members:
        for i, member in enumerate(reversed(st.session_state.members)):
            accepted_date = datetime.fromisoformat(member['accepted_at']).strftime("%B %d, %Y")
            
            st.markdown(f"""
            <div class="member-card">
                <div class="member-name">👤 {member['name']}</div>
                <div class="member-details">📧 {member['email']}</div>
                <div class="member-details">🆔 {member['student_id']}</div>
                <div class="member-details">🏢 {member['department']}</div>
                <div class="member-details">📅 Signed: {accepted_date}</div>
                <div class="member-role">{member['role']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 2rem; color: #718096;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">👥</div>
            <p>No team members yet</p>
            <p style="font-size: 0.9rem;">Be the first to sign the agreement!</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #718096;">
    <p>🎓 Final Year Project Team Agreement System</p>
    <p style="font-size: 0.9rem;">Built with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)

# Admin section (optional)
with st.expander("🔧 Admin Panel", expanded=False):
    st.subheader("Team Management")
    
    if st.session_state.members:
        # Display as DataFrame
        df = pd.DataFrame(st.session_state.members)
        st.dataframe(df, use_container_width=True)
        
        # Download data
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Team Data (CSV)",
            data=csv,
            file_name=f"team_members_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        
        # Clear all data (with confirmation)
        if st.button("🗑️ Clear All Data", type="secondary"):
            if st.checkbox("⚠️ I confirm I want to delete all team member data"):
                st.session_state.members = []
                save_data()
                st.success("All data cleared successfully!")
                st.rerun()
    else:
        st.info("No team members to display")