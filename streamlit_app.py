import streamlit as st
from utils.styling import apply_custom_css
import os

# Page config - should be the first Streamlit command
st.set_page_config(
    page_title="🎃 Hacktoberfest Mentor 2024",
    page_icon="🎃",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply custom styling
apply_custom_css()

# Initialize session state
if 'profile' not in st.session_state:
    st.session_state.profile = None
if 'issues' not in st.session_state:
    st.session_state.issues = []
if 'github_token' not in st.session_state:
    st.session_state.github_token = os.getenv('GITHUB_TOKEN', '')

def main():
    # Header with gradient background
    st.markdown("""
    <div class="hero-section">
        <div class="hero-content">
            <h1 class="hero-title">🎃 Hacktoberfest Mentor 2024</h1>
            <p class="hero-subtitle">Your guide to successful open source contributions this October</p>
            <div class="hero-badge">
                <span class="badge-text">October 1-31, 2024 • Free & Open to All</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # About Hacktoberfest Section
    st.markdown("""
    <div class="about-hacktoberfest">
        <div class="about-header">
            <h2 class="about-title">🌟 What is Hacktoberfest?</h2>
        </div>
        <div class="about-content">
            <div class="about-main">
                <p class="about-description">
                    <strong>Hacktoberfest</strong> is a <strong>month-long celebration</strong> of open source projects, 
                    their maintainers, and the entire community of contributors. Every October, developers around the 
                    world come together to support open source by making meaningful contributions to projects they love.
                </p>
                
                <div class="about-features">
                    <div class="about-feature">
                        <div class="feature-number">🎯</div>
                        <div class="feature-content">
                            <h4>Make 4 Pull Requests</h4>
                            <p>Complete 4 quality pull requests to participating repositories during October</p>
                        </div>
                    </div>
                    
                    <div class="about-feature">
                        <div class="feature-number">🌍</div>
                        <div class="feature-content">
                            <h4>Global Community</h4>
                            <p>Join thousands of developers worldwide contributing to open source</p>
                        </div>
                    </div>
                    
                    <div class="about-feature">
                        <div class="feature-number">🏆</div>
                        <div class="feature-content">
                            <h4>Earn Recognition</h4>
                            <p>Get digital badges and potential swag for successful participation</p>
                        </div>
                    </div>
                </div>
                
                <div class="about-benefits">
                    <h3>🚀 Why Participate in Hacktoberfest?</h3>
                    <div class="benefits-grid">
                        <div class="benefit-item">
                            <span class="benefit-icon">📈</span>
                            <span class="benefit-text"><strong>Skill Building:</strong> Learn from real-world codebases and improve your programming skills</span>
                        </div>
                        <div class="benefit-item">
                            <span class="benefit-icon">💼</span>
                            <span class="benefit-text"><strong>Portfolio Growth:</strong> Showcase your contributions on GitHub for potential employers</span>
                        </div>
                        <div class="benefit-item">
                            <span class="benefit-icon">🤝</span>
                            <span class="benefit-text"><strong>Networking:</strong> Connect with maintainers, mentors, and fellow developers globally</span>
                        </div>
                        <div class="benefit-item">
                            <span class="benefit-icon">🌱</span>
                            <span class="benefit-text"><strong>First PR Experience:</strong> Perfect opportunity to make your first pull request with community support</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="about-sidebar">
                <div class="timeline-card">
                    <h4>📅 Hacktoberfest 2024 Timeline</h4>
                    <div class="timeline">
                        <div class="timeline-item">
                            <span class="timeline-date">Sep 15</span>
                            <span class="timeline-desc">Registration Opens</span>
                        </div>
                        <div class="timeline-item active">
                            <span class="timeline-date">Oct 1-31</span>
                            <span class="timeline-desc">Contribution Period</span>
                        </div>
                        <div class="timeline-item">
                            <span class="timeline-date">Nov 1-15</span>
                            <span class="timeline-desc">Review Period</span>
                        </div>
                    </div>
                </div>
                
                <div class="stats-card">
                    <h4>📊 Last Year's Impact</h4>
                    <div class="stat-row">
                        <span class="stat-number">500K+</span>
                        <span class="stat-label">Participants</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-number">2M+</span>
                        <span class="stat-label">Pull Requests</span>
                    </div>
                    <div class="stat-row">
                        <span class="stat-number">100K+</span>
                        <span class="stat-label">Repositories</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # How This Mentor Helps Section
    st.markdown("""
    <div class="mentor-help-section">
        <div class="mentor-header">
            <h2 class="mentor-title">🤖 How This Mentor Helps You Succeed</h2>
            <p class="mentor-subtitle">
                Getting started with open source can be overwhelming. This AI-powered mentor simplifies your journey 
                by finding the perfect Hacktoberfest repositories and issues that match your skills and experience level.
            </p>
        </div>
        
        <div class="mentor-steps">
            <div class="step-card">
                <div class="step-number">1</div>
                <div class="step-content">
                    <h3>🎯 Setup Your Profile</h3>
                    <p>Tell us your programming skills, experience level, and interests. Our system will use this to find perfect matches.</p>
                </div>
            </div>
            
            <div class="step-arrow">→</div>
            
            <div class="step-card">
                <div class="step-number">2</div>
                <div class="step-content">
                    <h3>🔍 Discover Issues</h3>
                    <p>We search through thousands of Hacktoberfest repositories to find issues labeled as 'good-first-issue' that match your profile.</p>
                </div>
            </div>
            
            <div class="step-arrow">→</div>
            
            <div class="step-card">
                <div class="step-number">3</div>
                <div class="step-content">
                    <h3>🤖 AI Recommendations</h3>
                    <p>Our local AI analyzes each issue and provides personalized recommendations with difficulty scores and time estimates.</p>
                </div>
            </div>
            
            <div class="step-arrow">→</div>
            
            <div class="step-card">
                <div class="step-number">4</div>
                <div class="step-content">
                    <h3>📚 Learn & Contribute</h3>
                    <p>Get step-by-step guidance on how to fork, clone, make changes, and submit your first pull request successfully.</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Main welcome section with the exact design from image
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Welcome card matching the image design
    st.markdown("""
    <div class="welcome-section">
        <div class="welcome-card">
            <div class="welcome-header">
                <span class="rocket-emoji">🚀</span>
                <h2 class="welcome-title">Welcome to Your Open Source Journey!</h2>
            </div>
            <p class="welcome-description">
                Get AI-powered recommendations for Hacktoberfest 2024 repositories with 
                'good-first-issue' labels that match your skills and experience level.
            </p>
            
            <div class="features-grid">
                <div class="feature-card personalized">
                    <div class="feature-icon">🎯</div>
                    <h3 class="feature-title">Personalized</h3>
                    <p class="feature-desc">Issues matched to your skills</p>
                </div>
                
                <div class="feature-card ai-powered">
                    <div class="feature-icon">🤖</div>
                    <h3 class="feature-title">AI-Powered</h3>
                    <p class="feature-desc">Smart recommendations</p>
                </div>
                
                <div class="feature-card guided">
                    <div class="feature-icon">📚</div>
                    <h3 class="feature-title">Guided</h3>
                    <p class="feature-desc">Step-by-step instructions</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Action buttons section
    st.markdown('<div class="action-section">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            if st.button("🏗️ Setup Profile", use_container_width=True, type="primary"):
                st.switch_page("pages/01_🏠_Profile_Setup.py")
        
        with col_b:
            if st.button("🔍 Find Issues", use_container_width=True, type="secondary"):
                if st.session_state.profile:
                    st.switch_page("pages/02_🔍_Find_Issues.py")
                else:
                    st.error("⚠️ Please set up your profile first!")
        
        with col_c:
            if st.button("📖 Learn How", use_container_width=True, type="secondary"):
                st.switch_page("pages/03_📖_Contribution_Guide.py")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick stats section
    st.markdown('<div class="stats-section">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">{}</div>
            <div class="stat-label">Hacktoberfest Issues Found</div>
        </div>
        """.format(len(st.session_state.issues)), unsafe_allow_html=True)
    
    with col2:
        skills_count = len(st.session_state.profile.get('skills', [])) if st.session_state.profile else 0
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">{}</div>
            <div class="stat-label">Your Skills</div>
        </div>
        """.format(skills_count), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">2024</div>
            <div class="stat-label">Hacktoberfest</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        experience = st.session_state.profile.get('experience_level', 'Not Set').title() if st.session_state.profile else 'Not Set'
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">{}</div>
            <div class="stat-label">Experience</div>
        </div>
        """.format(experience), unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # GitHub API Setup
    if not st.session_state.github_token:
        with st.expander("⚙️ Setup GitHub API Token (Recommended for Better Results)", expanded=False):
            st.markdown("""
            **🚀 Why add a GitHub token for Hacktoberfest?**
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

if __name__ == "__main__":
    main()