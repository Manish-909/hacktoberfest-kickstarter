import streamlit as st
from utils.styling import apply_custom_css
from services.profile_service import ProfileService
from services.resume_service import ResumeService
from services.mock_resume_service import MockResumeService
import os

# Apply styling
apply_custom_css()

# Initialize session state for this page
if 'profile' not in st.session_state:
    st.session_state.profile = None
if 'issues' not in st.session_state:
    st.session_state.issues = []
if 'github_token' not in st.session_state:
    st.session_state.github_token = os.getenv('GITHUB_TOKEN', '')

# Skills and interests data
SKILLS = [
    'JavaScript', 'Python', 'Java', 'TypeScript', 'React', 'Vue.js', 'Angular',
    'Node.js', 'Express', 'Django', 'Flask', 'Spring Boot', 'PHP', 'Laravel',
    'Ruby', 'Rails', 'Go', 'Rust', 'C++', 'C#', '.NET', 'Swift', 'Kotlin',
    'HTML', 'CSS', 'SCSS', 'Tailwind', 'Bootstrap', 'jQuery', 'Redux',
    'GraphQL', 'REST API', 'MongoDB', 'PostgreSQL', 'MySQL', 'SQLite',
    'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP', 'Git', 'Linux', 'Bash'
]

INTERESTS = [
    'frontend', 'backend', 'fullstack', 'mobile', 'web', 'api', 'database',
    'devops', 'cloud', 'ai', 'machine-learning', 'data-science', 'blockchain',
    'security', 'testing', 'documentation', 'ui-ux', 'performance', 'accessibility',
    'open-source', 'beginner-friendly', 'hacktoberfest', 'help-wanted', 'bug',
    'feature', 'enhancement', 'refactor', 'optimization', 'tutorial'
]

def main():
    st.markdown("""
    <div class="page-header">
        <h1 class="page-title">🏠 Profile Setup</h1>
        <p class="page-subtitle">Tell us about your skills and interests to get personalized issue recommendations</p>
    </div>
    """, unsafe_allow_html=True)
    
    profile_service = ProfileService()
    resume_service = MockResumeService()
    
    # Initialize form state
    if 'form_submitted' not in st.session_state:
        st.session_state.form_submitted = False
    if 'resume_processed' not in st.session_state:
        st.session_state.resume_processed = False
    if 'extracted_profile' not in st.session_state:
        st.session_state.extracted_profile = None
    
    # Resume Upload Section
    st.markdown("""
    <div class="form-section">
        <h2 class="section-title">📄 Quick Setup: Upload Your Resume</h2>
        <p class="section-desc">Upload your resume and let AI automatically fill your profile preferences!</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_file = st.file_uploader(
                "Choose your resume file (PDF or DOCX)",
                type=['pdf', 'docx'],
                help="Upload your resume in PDF or DOCX format. Our AI will automatically extract your skills, experience level, and interests."
            )
            
            if uploaded_file is not None:
                st.success(f"✅ File uploaded: {uploaded_file.name} ({uploaded_file.size} bytes)")
                
                if st.button("🤖 Process Resume with AI (Demo)", type="primary", use_container_width=True):
                    with st.spinner("🔄 Processing your resume with AI simulation..."):
                        # Process the resume
                        result = resume_service.process_resume(uploaded_file)
                        
                        if result['success']:
                            st.session_state.extracted_profile = result['profile']
                            st.session_state.resume_processed = True
                            st.success("✅ Resume processed successfully! Your profile has been auto-filled below.")
                            st.balloons()
                            
                            # Show extracted information
                            with st.expander("📋 Extracted Information Preview", expanded=True):
                                col_a, col_b, col_c = st.columns(3)
                                
                                with col_a:
                                    st.info(f"**Experience Level:** {result['profile']['experienceLevel'].title()}")
                                
                                with col_b:
                                    st.info(f"**Skills Found:** {len(result['profile']['programmingSkills'])} skills")
                                
                                with col_c:
                                    st.info(f"**Interests:** {len(result['profile']['areasOfInterest'])} areas")
                                
                                if st.checkbox("Show resume preview"):
                                    st.text_area("Resume Text Preview:", result['resume_text_preview'], height=150, disabled=True)
                        else:
                            st.error(f"❌ Error processing resume: {result['error']}")
                            st.info("💡 Don't worry! You can still fill out the form manually below.")
        
        with col2:
            st.markdown("""
            <div style='padding: 20px; background: rgba(102, 126, 234, 0.1); border-radius: 10px; border: 1px solid rgba(102, 126, 234, 0.3);'>
                <h4 style='color: #667eea; margin-bottom: 1rem;'>🚀 Why Use Resume Upload?</h4>
                <ul style='color: #8b949e; padding-left: 1rem;'>
                    <li>Save time with auto-fill</li>
                    <li>AI-powered skill extraction</li>
                    <li>Intelligent interest matching</li>
                    <li>Better profile accuracy</li>
                </ul>
                <p style='color: #8b949e; font-size: 0.9rem; margin-top: 1rem;'>
                    <strong>Demo Mode:</strong> This simulates AI analysis. In production, this would use Gemini 2.5 lite API.
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    
    # Manual Form Section Header
    st.markdown("""
    <div class="form-section">
        <h2 class="section-title">📝 Manual Setup: Fill Profile Details</h2>
        <p class="section-desc">Manually enter your information or review and edit the AI-extracted data below:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show notification if AI data is being used
    if st.session_state.extracted_profile:
        st.info("🤖 퉲8 Using AI-extracted data from your resume! You can modify any selections below.")
    
    # Create form
    with st.form("profile_form", clear_on_submit=False):
        # Experience Level Section
        st.markdown("""
        <div class="form-section">
            <h3 class="section-title">🎯 Experience Level</h3>
        </div>
        """, unsafe_allow_html=True)
        
        experience_options = ['Beginner', 'Intermediate', 'Advanced']
        experience_descriptions = {
            'Beginner': '🌱 New to open source',
            'Intermediate': '💻 Some contributions made', 
            'Advanced': '🚀 Experienced contributor'
        }
        
        # Pre-select experience level if extracted from resume
        default_experience_index = 0  # Default to 'Beginner'
        if st.session_state.extracted_profile:
            extracted_exp = st.session_state.extracted_profile['experienceLevel'].title()
            if extracted_exp in experience_options:
                default_experience_index = experience_options.index(extracted_exp)
        
        experience_level = st.radio(
            "Select your experience level:",
            options=experience_options,
            format_func=lambda x: experience_descriptions[x],
            horizontal=True,
            label_visibility="collapsed",
            index=default_experience_index
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Skills Selection
        st.markdown("""
        <div class="form-section">
            <h3 class="section-title">⚡ Programming Skills</h3>
            <p class="section-desc">Select the programming languages and technologies you know:</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Organize skills by category
        skill_categories = {
            'Frontend': ['JavaScript', 'TypeScript', 'React', 'Vue.js', 'Angular', 'HTML', 'CSS', 'SCSS', 'Tailwind', 'Bootstrap'],
            'Backend': ['Python', 'Java', 'Node.js', 'Django', 'Flask', 'Spring Boot', 'PHP', 'Laravel', 'Ruby', 'Go', 'Rust'],
            'Database': ['MongoDB', 'PostgreSQL', 'MySQL', 'SQLite', 'GraphQL', 'REST API'],
            'DevOps': ['Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP', 'Git', 'Linux', 'Bash'],
            'Other': ['C++', 'C#', '.NET', 'Swift', 'Kotlin', 'jQuery', 'Redux']
        }
        
        selected_skills = []
        
        # Get extracted skills for pre-checking
        extracted_skills = []
        if st.session_state.extracted_profile:
            extracted_skills = st.session_state.extracted_profile.get('programmingSkills', [])
        
        for category, skills in skill_categories.items():
            with st.expander(f"📁 {category} ({len(skills)} skills)", expanded=True):
                cols = st.columns(4)
                for i, skill in enumerate(skills):
                    with cols[i % 4]:
                        # Pre-check skill if it was extracted from resume
                        default_checked = skill in extracted_skills
                        if st.checkbox(skill, key=f"skill_{skill}", value=default_checked):
                            selected_skills.append(skill)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Interests Selection
        st.markdown("""
        <div class="form-section">
            <h3 class="section-title">🎨 Areas of Interest</h3>
            <p class="section-desc">Choose the types of projects and issues you're interested in:</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Organize interests by type
        interest_categories = {
            'Development Areas': ['frontend', 'backend', 'fullstack', 'mobile', 'web', 'api', 'database'],
            'Technologies': ['devops', 'cloud', 'ai', 'machine-learning', 'data-science', 'blockchain', 'security'],
            'Contribution Types': ['open-source', 'beginner-friendly', 'hacktoberfest', 'help-wanted', 'bug', 'feature', 'documentation'],
            'Other': ['testing', 'ui-ux', 'performance', 'accessibility', 'enhancement', 'refactor', 'optimization', 'tutorial']
        }
        
        selected_interests = []
        
        # Get extracted interests for pre-checking
        extracted_interests = []
        if st.session_state.extracted_profile:
            extracted_interests = st.session_state.extracted_profile.get('areasOfInterest', [])
        
        for category, interests in interest_categories.items():
            with st.expander(f"🔖 {category} ({len(interests)} options)", expanded=True):
                cols = st.columns(3)
                for i, interest in enumerate(interests):
                    with cols[i % 3]:
                        display_name = interest.replace('-', ' ').title()
                        # Pre-check interest if it was extracted from resume
                        default_checked = interest in extracted_interests
                        if st.checkbox(display_name, key=f"interest_{interest}", value=default_checked):
                            selected_interests.append(interest)
        
        # Form submission
        st.markdown("<br><hr><br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("🚀 Save Profile & Find Issues", use_container_width=True)
        
        # Handle form submission
        if submitted:
            # Validation
            errors = []
            if not selected_skills:
                errors.append("Please select at least one skill")
            if not selected_interests:
                errors.append("Please select at least one area of interest")
            
            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                # Create and save profile
                profile_data = {
                    'experience_level': experience_level.lower(),
                    'skills': selected_skills,
                    'interests': selected_interests
                }
                
                st.session_state.profile = profile_data
                st.session_state.form_submitted = True
                
                # Success message with animation
                st.success("✅ Profile saved successfully!")
                st.balloons()
                
                # Show profile summary
                with st.container():
                    st.markdown("""
                    <div class="success-section">
                        <h3>🎉 Profile Created Successfully!</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"""
                        <div class="profile-summary">
                            <h4>📊 Profile Summary</h4>
                            <p><strong>Experience:</strong> {experience_level}</p>
                            <p><strong>Skills:</strong> {len(selected_skills)} selected</p>
                            <p><strong>Interests:</strong> {len(selected_interests)} selected</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("""
                        <div class="top-skills">
                            <h4>💪 Top Skills</h4>
                        """, unsafe_allow_html=True)
                        
                        for skill in selected_skills[:8]:
                            st.markdown(f"• {skill}")
                        
                        if len(selected_skills) > 8:
                            st.markdown(f"... and {len(selected_skills) - 8} more")
                        
                        st.markdown("</div>", unsafe_allow_html=True)
    
    # Navigation buttons outside the form
    if st.session_state.form_submitted and st.session_state.profile:
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔍 Find My Issues Now", use_container_width=True, type="primary"):
                st.success("✅ Profile saved! Please navigate to the 'Find Issues' page to discover opportunities.")
        
        with col2:
            if st.button("📖 View Contribution Guide", use_container_width=True):
                st.info("📖 Navigate to the 'Contribution Guide' page to learn how to contribute.")
    
    # Load existing profile if available
    if st.session_state.profile and not st.session_state.form_submitted:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.info("💡 You have a saved profile. Update the form above or continue with current profile.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔍 Use Current Profile & Find Issues", type="primary"):
                st.success("✅ Using current profile! Please navigate to the 'Find Issues' page to discover opportunities.")
        
        with col2:
            with st.expander("Current Profile Details"):
                st.json(st.session_state.profile)

if __name__ == "__main__":
    main()
