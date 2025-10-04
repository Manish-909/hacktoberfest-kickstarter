import streamlit as st
from utils.styling import apply_custom_css
from services.profile_service import ProfileService

# Apply styling
apply_custom_css()

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
    
    # Initialize form state
    if 'form_submitted' not in st.session_state:
        st.session_state.form_submitted = False
    
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
        
        experience_level = st.radio(
            "Select your experience level:",
            options=experience_options,
            format_func=lambda x: experience_descriptions[x],
            horizontal=True,
            label_visibility="collapsed"
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
        
        for category, skills in skill_categories.items():
            with st.expander(f"📁 {category} ({len(skills)} skills)", expanded=True):
                cols = st.columns(4)
                for i, skill in enumerate(skills):
                    with cols[i % 4]:
                        if st.checkbox(skill, key=f"skill_{skill}"):
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
        
        for category, interests in interest_categories.items():
            with st.expander(f"🔖 {category} ({len(interests)} options)", expanded=True):
                cols = st.columns(3)
                for i, interest in enumerate(interests):
                    with cols[i % 3]:
                        display_name = interest.replace('-', ' ').title()
                        if st.checkbox(display_name, key=f"interest_{interest}"):
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
                st.switch_page("pages/02_🔍_Find_Issues.py")
        
        with col2:
            if st.button("📖 View Contribution Guide", use_container_width=True):
                st.switch_page("pages/03_📖_Contribution_Guide.py")
    
    # Load existing profile if available
    if st.session_state.profile and not st.session_state.form_submitted:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.info("💡 You have a saved profile. Update the form above or continue with current profile.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔍 Use Current Profile & Find Issues", type="primary"):
                st.switch_page("pages/02_🔍_Find_Issues.py")
        
        with col2:
            with st.expander("Current Profile Details"):
                st.json(st.session_state.profile)

if __name__ == "__main__":
    main()
