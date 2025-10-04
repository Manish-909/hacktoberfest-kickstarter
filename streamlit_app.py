import streamlit as st
from utils.styling import apply_custom_css
import os

# Page config - should be the first Streamlit command
st.set_page_config(
    page_title="🎃 Hacktoberfest Mentor 2025",
    page_icon="🎃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
apply_custom_css()

# Initialize session state FIRST - before any other code that uses it
if 'profile' not in st.session_state:
    st.session_state.profile = None
if 'issues' not in st.session_state:
    st.session_state.issues = []
if 'github_token' not in st.session_state:
    st.session_state.github_token = os.getenv('GITHUB_TOKEN', '')

# Sidebar Navigation
with st.sidebar:
    st.markdown("## 🎃 Navigation")
    st.markdown("---")
    
    # Navigation options
    nav_option = st.selectbox(
        "Choose a page:",
        ["🏠 Home", "🏢 Profile Setup", "🔍 Find Issues", "📖 Contribution Guide"],
        index=0
    )
    
    # Handle navigation
    if nav_option == "🏢 Profile Setup":
        if st.button("Go to Profile Setup", use_container_width=True):
            st.info("🏢 Please navigate to the 'Profile Setup' page using the pages sidebar.")
    elif nav_option == "🔍 Find Issues":
        if st.button("Go to Find Issues", use_container_width=True):
            if st.session_state.profile:
                st.info("🔍 Please navigate to the 'Find Issues' page using the pages sidebar.")
            else:
                st.error("Please set up your profile first!")
    elif nav_option == "📖 Contribution Guide":
        if st.button("Go to Guide", use_container_width=True):
            st.info("📖 Please navigate to the 'Contribution Guide' page using the pages sidebar.")
    
    st.markdown("---")
    
    # Profile Status
    if st.session_state.profile:
        st.success("✅ Profile Set Up")
        st.write(f"**Experience:** {st.session_state.profile.get('experience_level', 'Unknown').title()}")
        st.write(f"**Skills:** {len(st.session_state.profile.get('skills', []))}")
        st.write(f"**Interests:** {len(st.session_state.profile.get('interests', []))}")
    else:
        st.warning("⚠️ No Profile Set Up")
        st.write("Complete your profile to get personalized recommendations.")
    
    st.markdown("---")
    
    # Quick Stats
    st.markdown("### 📈 Quick Stats")
    st.write(f"🎯 Issues Found: {len(st.session_state.issues)}")
    st.write(f"🎅 Hacktoberfest 2025")
    
    # GitHub Token Status
    if st.session_state.github_token:
        st.success("✅ GitHub Token Set")
    else:
        st.warning("⚠️ No GitHub Token")
        st.caption("Add a token for better API limits")


def main():
    # Header with gradient background
    st.markdown("""
    <div class="hero-section">
        <div class="hero-content">
            <h1 class="hero-title">🎃 Hacktoberfest Mentor 2025</h1>
            <p class="hero-subtitle">Your guide to successful open source contributions this October</p>
            <div class="hero-badge">
                <span class="badge-text">October 1-31, 2025 • Free & Open to All</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # About Hacktoberfest Section
    st.markdown("### 🌟 What is Hacktoberfest?")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **Hacktoberfest** is a **month-long celebration** of open source projects, their maintainers, 
        and the entire community of contributors. Every October, developers around the world come together 
        to support open source by making meaningful contributions to projects they love.
        """)
        
        # Features in expandable sections for better organization
        with st.expander("🎯 **Main Goals & Requirements**", expanded=True):
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.info("🎯 **Make 4 Pull Requests**\n\nComplete 4 quality pull requests to participating repositories during October")
            with col_b:
                st.info("🌍 **Global Community**\n\nJoin thousands of developers worldwide contributing to open source")
            with col_c:
                st.info("🏆 **Earn Recognition**\n\nGet digital badges and potential swag for successful participation")
        
        with st.expander("🚀 **Why Participate in Hacktoberfest?**", expanded=False):
            st.markdown("""
            - 📈 **Skill Building:** Learn from real-world codebases and improve your programming skills
            - 💼 **Portfolio Growth:** Showcase your contributions on GitHub for potential employers  
            - 🤝 **Networking:** Connect with maintainers, mentors, and fellow developers globally
            - 🌱 **First PR Experience:** Perfect opportunity to make your first pull request with community support
            """)
    
    with col2:
        # Timeline Card
        st.markdown("#### 📅 Hacktoberfest 2025 Timeline")
        st.success("📅 **Sep 15** - Registration Opens")
        st.warning("🗓️ **Oct 1-31** - Contribution Period (ACTIVE)")
        st.info("🔍 **Nov 1-15** - Review Period")
        
        # Stats Card
        st.markdown("#### 📈 Last Year's Impact")
        col_stats1, col_stats2 = st.columns(2)
        with col_stats1:
            st.metric("Participants", "500K+")
            st.metric("Repositories", "100K+")
        with col_stats2:
            st.metric("Pull Requests", "2M+")
            st.metric("Countries", "100+")
    
    # How This Mentor Helps Section
    st.markdown("---")
    st.markdown("## 🤖 How This Mentor Helps You Succeed")
    st.markdown("""
    Getting started with open source can be overwhelming. This AI-powered mentor simplifies your journey 
    by finding the perfect Hacktoberfest repositories and issues that match your skills and experience level.
    """)
    
    # Create 4 columns for the steps
    step_col1, step_col2, step_col3, step_col4 = st.columns(4)
    
    with step_col1:
        st.markdown("""
        <div style='text-align: center; padding: 20px; background: rgba(102, 126, 234, 0.1); border-radius: 10px; border: 1px solid rgba(102, 126, 234, 0.3);'>
            <h3>1. 🎯 Setup Profile</h3>
            <p>Tell us your programming skills, experience level, and interests. Our system will use this to find perfect matches.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with step_col2:
        st.markdown("""
        <div style='text-align: center; padding: 20px; background: rgba(78, 205, 196, 0.1); border-radius: 10px; border: 1px solid rgba(78, 205, 196, 0.3);'>
            <h3>2. 🔍 Discover Issues</h3>
            <p>We search through thousands of Hacktoberfest repositories to find issues labeled as 'good-first-issue' that match your profile.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with step_col3:
        st.markdown("""
        <div style='text-align: center; padding: 20px; background: rgba(240, 147, 251, 0.1); border-radius: 10px; border: 1px solid rgba(240, 147, 251, 0.3);'>
            <h3>3. 🤖 AI Recommendations</h3>
            <p>Our local AI analyzes each issue and provides personalized recommendations with difficulty scores and time estimates.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with step_col4:
        st.markdown("""
        <div style='text-align: center; padding: 20px; background: rgba(46, 160, 67, 0.1); border-radius: 10px; border: 1px solid rgba(46, 160, 67, 0.3);'>
            <h3>4. 📚 Learn & Contribute</h3>
            <p>Get step-by-step guidance on how to fork, clone, make changes, and submit your first pull request successfully.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main welcome section 
    st.markdown("---")
    st.markdown("## 🚀 Welcome to Your Open Source Journey!")
    st.markdown("""
    Get AI-powered recommendations for Hacktoberfest 2025 repositories with 
    'good-first-issue' labels that match your skills and experience level.
    """)
    
    # Features in columns
    feature_col1, feature_col2, feature_col3 = st.columns(3)
    
    with feature_col1:
        st.markdown("""
        <div style='text-align: center; padding: 20px; background: rgba(240, 147, 251, 0.1); border-radius: 12px; border: 1px solid rgba(240, 147, 251, 0.3);'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>🎯</div>
            <h3 style='color: #f093fb; margin-bottom: 0.75rem;'>Personalized</h3>
            <p style='color: #8b949e;'>Issues matched to your skills</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_col2:
        st.markdown("""
        <div style='text-align: center; padding: 20px; background: rgba(78, 205, 196, 0.1); border-radius: 12px; border: 1px solid rgba(78, 205, 196, 0.3);'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>🤖</div>
            <h3 style='color: #4ecdc4; margin-bottom: 0.75rem;'>AI-Powered</h3>
            <p style='color: #8b949e;'>Smart recommendations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with feature_col3:
        st.markdown("""
        <div style='text-align: center; padding: 20px; background: rgba(102, 126, 234, 0.1); border-radius: 12px; border: 1px solid rgba(102, 126, 234, 0.3);'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>📚</div>
            <h3 style='color: #667eea; margin-bottom: 0.75rem;'>Guided</h3>
            <p style='color: #8b949e;'>Step-by-step instructions</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Action buttons section
    st.markdown("---")
    st.markdown("### 🛠️ Get Started")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏢 Setup Profile", use_container_width=True, type="primary"):
            st.success("🏢 Navigate to the 'Profile Setup' page to get started!")
    
    with col2:
        if st.button("🔍 Find Issues", use_container_width=True, type="secondary"):
            if st.session_state.profile:
                st.success("🔍 Navigate to the 'Find Issues' page to discover opportunities!")
            else:
                st.error("⚠️ Please set up your profile first!")
    
    with col3:
        if st.button("📖 Learn How", use_container_width=True, type="secondary"):
            st.info("📖 Navigate to the 'Contribution Guide' page to learn how to contribute!")
    
    # Quick stats section
    st.markdown("---")
    st.markdown("### 📈 Your Journey Stats")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Issues Found", 
            value=len(st.session_state.issues),
            help="Number of Hacktoberfest issues discovered"
        )
    
    with col2:
        skills_count = len(st.session_state.profile.get('skills', [])) if st.session_state.profile else 0
        st.metric(
            label="Your Skills", 
            value=skills_count,
            help="Programming languages and skills in your profile"
        )
    
    with col3:
        st.metric(
            label="Hacktoberfest", 
            value="2025",
            help="Current Hacktoberfest year"
        )
    
    with col4:
        experience = st.session_state.profile.get('experience_level', 'Not Set').title() if st.session_state.profile else 'Not Set'
        st.metric(
            label="Experience Level", 
            value=experience,
            help="Your current programming experience level"
        )
    
    # GitHub API Setup
    if not st.session_state.github_token:
        with st.expander("⚙️ Setup GitHub API Token (Recommended for Better Results)", expanded=False):
            st.markdown("""
            **🚀 Why add a GitHub token for Hacktoberfest 2025?**
            - **Higher API rate limits** (5000 requests/hour vs 60)
            - **Access to more Hacktoberfest repositories** and issues
            - **Better AI recommendations** with complete repository data
            - **Faster issue discovery** across all participating projects
            
            **📝 How to get a token:**
            1. Go to [GitHub Settings → Developer Settings → Personal Access Tokens](https://github.com/settings/tokens)
            2. Click "Generate new token (classic)"
            3. Select "public_repo" scope only
            4. Copy and paste below
            """)
            
            github_token = st.text_input("GitHub Personal Access Token:", 
                                       type="password", 
                                       placeholder="ghp_xxxxxxxxxxxxxxxxxxxx",
                                       help="This token is stored only in your session and never saved permanently")
            
            if st.button("💾 Save Token for This Session"):
                if github_token.startswith('ghp_'):
                    st.session_state.github_token = github_token
                    st.success("✅ GitHub token saved! You now have access to 5000 API requests per hour.")
                    st.rerun()
                else:
                    st.error("❌ Invalid token format. Token should start with 'ghp_'")
    
    # Beginner's Quick Start Guide
    with st.expander("🌱 **New to Open Source? Start Here!**", expanded=False):
        st.markdown("""
        ### 📚 Complete Beginner's Guide to Hacktoberfest 2025
        
        **What you'll need:**
        - 💻 A computer with internet access
        - 🔑 A GitHub account (free at [github.com](https://github.com))
        - ✨ Enthusiasm to learn and contribute!
        
        **Step-by-step process:**
        1. **Sign up for Hacktoberfest** at [hacktoberfest.com](https://hacktoberfest.com) 
        2. **Set up your profile** using this tool to find issues that match your skills
        3. **Find beginner-friendly issues** - look for labels like `good-first-issue`, `beginner-friendly`
        4. **Fork the repository** - creates your own copy to work on
        5. **Clone to your computer** - download the code locally
        6. **Make your changes** - fix bugs, add features, improve documentation
        7. **Commit and push** - save and upload your changes
        8. **Create a Pull Request** - propose your changes to the original project
        
        **🎯 Your Goal:** Submit 4 quality pull requests between October 1-31, 2025
        
        **✨ Tips for Success:**
        - Start with documentation fixes or small bug fixes
        - Read the project's CONTRIBUTING.md file first
        - Follow the project's code style and guidelines
        - Be patient - maintainers are volunteers too!
        - Ask questions in issues if you're stuck
        
        **🏆 What You'll Gain:**
        - Real-world coding experience
        - GitHub portfolio improvements  
        - Connections in the developer community
        - Potential swag and digital rewards
        - Confidence in open source contribution
        """)
        
        # Quick action buttons for beginners
        col_guide1, col_guide2 = st.columns(2)
        with col_guide1:
            if st.button("🎓 Learn Git/GitHub Basics", help="External link to Git tutorial"):
                st.info("🌐 Visit: https://try.github.io for interactive Git tutorial")
        with col_guide2:
            if st.button("📚 Read Hacktoberfest Rules", help="External link to official rules"):
                st.info("🌐 Visit: https://hacktoberfest.com/participation for official rules")

if __name__ == "__main__":
    main()