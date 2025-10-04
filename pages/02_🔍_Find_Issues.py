import streamlit as st
from utils.styling import apply_custom_css
from services.github_service import GitHubService
from services.ai_service import AIService
import pandas as pd
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

st.title("🔍 Find Perfect Issues")

def main():
    if not st.session_state.profile:
        st.warning("⚠️ Please set up your profile first to get personalized recommendations.")
        if st.button("🏠 Go to Profile Setup"):
            st.info("ℹ️ Please navigate to the Profile Setup page from the sidebar or main menu.")
        return
    
    # Display user profile summary
    with st.sidebar:
        st.markdown("### 👤 Your Profile")
        profile = st.session_state.profile
        st.write(f"**Experience:** {profile['experience_level'].title()}")
        st.write(f"**Skills:** {len(profile['skills'])}")
        st.write(f"**Interests:** {len(profile['interests'])}")
        
        if st.button("✏️ Edit Profile"):
            st.info("ℹ️ Please navigate to the Profile Setup page to edit your profile.")
    
    # Search controls
    st.markdown("### 🎯 Issue Discovery")
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_type = st.selectbox(
            "Search Strategy:",
            ["Skills Based", "AI Recommended", "Interest Based", "Difficulty Based"]
        )
    
    with col2:
        max_issues = st.slider("Max Issues:", 5, 50, 5)
    
    with col3:
        if st.button("🔍 Find Issues", use_container_width=True):
            find_issues(search_type, max_issues)
    
    # Display issues if available
    if st.session_state.issues:
        display_issues()
    else:
        st.info("👆 Click 'Find Issues' to discover open source opportunities!")

@st.cache_data(show_spinner=True)
def find_issues(search_type, max_issues):
    """Find issues based on user profile and search type"""
    
    with st.spinner("🤖 AI is analyzing thousands of GitHub issues for you..."):
        try:
            github_service = GitHubService()
            ai_service = AIService()
            
            profile = st.session_state.profile
            
            # Fetch issues from GitHub
            raw_issues = github_service.fetch_issues(
                skills=profile['skills'],
                interests=profile['interests'],
                experience_level=profile['experience_level'],
                max_results=max_issues
            )
            
            if raw_issues:
                # Get AI recommendations
                recommended_issues = ai_service.get_recommendations(raw_issues, profile)
                st.session_state.issues = recommended_issues[:max_issues]
                
                st.success(f"✅ Found {len(st.session_state.issues)} perfect issues for you!")
            else:
                st.warning("😕 No issues found matching your criteria. Try adjusting your profile.")
                
        except Exception as e:
            st.error(f"❌ Error finding issues: {str(e)}")
            # Fallback with sample data
            st.session_state.issues = get_sample_issues()

def display_issues():
    """Display found issues with rich formatting"""
    
    st.markdown("### 📋 Your Personalized Issues")
    
    # Summary stats
    col1, col2, col3, col4 = st.columns(4)
    
    issues = st.session_state.issues
    avg_score = sum(issue.get('ai_score', 0) for issue in issues) / len(issues) if issues else 0
    
    with col1:
        st.metric("Total Issues", len(issues))
    with col2:
        st.metric("Avg AI Score", f"{avg_score:.1f}/10")
    with col3:
        easy_count = sum(1 for issue in issues if issue.get('difficulty') == 'easy')
        st.metric("Easy Issues", easy_count)
    with col4:
        assigned_count = sum(1 for issue in issues if issue.get('assignee'))
        st.metric("Available", len(issues) - assigned_count)
    
    # Filters
    st.markdown("#### 🔧 Filter Issues")
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        difficulty_filter = st.selectbox("Difficulty:", ["All", "Easy", "Medium", "Hard"])
    
    with filter_col2:
        languages = list(set(issue.get('repository', {}).get('language', 'Unknown') 
                           for issue in issues if issue.get('repository', {}).get('language')))
        language_filter = st.selectbox("Language:", ["All"] + languages)
    
    with filter_col3:
        sort_by = st.selectbox("Sort by:", ["AI Score", "Stars", "Recent", "Comments"])
    
    # Apply filters
    filtered_issues = apply_filters(issues, difficulty_filter, language_filter, sort_by)
    
    # Display issues
    for i, issue in enumerate(filtered_issues):
        display_issue_card(issue, i)

def apply_filters(issues, difficulty_filter, language_filter, sort_by):
    """Apply filters to issues list"""
    filtered = issues.copy()
    
    # Difficulty filter
    if difficulty_filter != "All":
        filtered = [issue for issue in filtered 
                   if issue.get('difficulty', '').lower() == difficulty_filter.lower()]
    
    # Language filter
    if language_filter != "All":
        filtered = [issue for issue in filtered 
                   if issue.get('repository', {}).get('language') == language_filter]
    
    # Sorting
    if sort_by == "AI Score":
        filtered.sort(key=lambda x: x.get('ai_score', 0), reverse=True)
    elif sort_by == "Stars":
        filtered.sort(key=lambda x: x.get('repository', {}).get('stars', 0), reverse=True)
    elif sort_by == "Recent":
        filtered.sort(key=lambda x: x.get('updated_at', ''), reverse=True)
    elif sort_by == "Comments":
        filtered.sort(key=lambda x: x.get('comments', 0), reverse=True)
    
    return filtered

def display_issue_card(issue, index):
    """Display individual issue card"""
    
    # Create card container
    with st.container():
        # Header with score and title
        col_header1, col_header2 = st.columns([4, 1])
        
        with col_header1:
            st.markdown(f"""
            ### [{issue['title']}]({issue['url']})
            **Repository:** {issue.get('repository', {}).get('name', 'Unknown')} 
            {'⭐' * min(int(issue.get('repository', {}).get('stars', 0) / 1000), 5)}
            """)
        
        with col_header2:
            score = issue.get('ai_score', 0)
            score_color = 'green' if score >= 8 else 'orange' if score >= 6 else 'red'
            st.markdown(f"""
            <div style="text-align: center; padding: 10px; background-color: {score_color}; 
                        color: white; border-radius: 10px; font-weight: bold;">
                🤖 {score}/10
            </div>
            """, unsafe_allow_html=True)
        
        # Issue details
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Description
            if issue.get('body'):
                with st.expander("📄 Issue Description"):
                    st.write(issue['body'][:500] + ('...' if len(issue.get('body', '')) > 500 else ''))
            
            # AI Summary
            if issue.get('ai_summary'):
                st.markdown("**🧠 AI Analysis:**")
                st.info(issue['ai_summary'])
        
        with col2:
            # Repository info
            repo = issue.get('repository', {})
            st.markdown("**📊 Repository Info:**")
            st.write(f"• Language: {repo.get('language', 'Unknown')}")
            st.write(f"• Stars: {repo.get('stars', 0)}")
            st.write(f"• Comments: {issue.get('comments', 0)}")
            
            # Labels
            if issue.get('labels'):
                st.markdown("**🏷️ Labels:**")
                labels_html = ""
                for label in issue['labels'][:5]:
                    labels_html += f'<span style="background-color: #2ea043; color: white; padding: 2px 6px; border-radius: 12px; margin: 2px; font-size: 0.8em;">{label}</span> '
                st.markdown(labels_html, unsafe_allow_html=True)
        
        # Action buttons
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        
        with col_btn1:
            # Use styled HTML button for better appearance and compatibility
            st.markdown(
                f'<a href="{issue["url"]}" target="_blank" style="text-decoration: none;">' 
                f'<button style="width: 100%; padding: 0.5rem; background-color: #0066cc; color: white; '
                f'border: none; border-radius: 5px; cursor: pointer; font-size: 0.9rem;">' 
                f'🔗 View Issue</button></a>', 
                unsafe_allow_html=True
            )
        
        with col_btn2:
            if st.button(f"📖 How to Contribute", key=f"guide_{index}", use_container_width=True):
                st.session_state.selected_issue = issue
                st.success("Issue selected! Navigate to the Contribution Guide page to see how to contribute.")
        
        with col_btn3:
            difficulty = issue.get('difficulty', 'unknown')
            difficulty_emoji = {'easy': '🟢', 'medium': '🟡', 'hard': '🔴'}.get(difficulty, '⚪')
            st.write(f"{difficulty_emoji} {difficulty.title()}")
        
        st.markdown("---")

def get_sample_issues():
    """Sample issues for fallback"""
    return [
        {
            'id': 1,
            'title': 'Add dark mode toggle to navigation bar',
            'body': 'Users have requested a dark mode toggle in the main navigation. This would improve accessibility and user experience.',
            'url': 'https://github.com/example/repo/issues/123',
            'repository': {
                'name': 'awesome-web-app',
                'language': 'JavaScript',
                'stars': 2500
            },
            'labels': ['enhancement', 'good first issue', 'hacktoberfest'],
            'comments': 5,
            'difficulty': 'easy',
            'ai_score': 8.5,
            'ai_summary': 'Perfect beginner issue involving CSS and JavaScript. Well-documented with clear requirements.',
            'updated_at': '2025-10-01T10:00:00Z'
        },
        {
            'id': 2,
            'title': 'Implement user authentication with JWT',
            'body': 'Add JWT-based authentication system for user login and registration.',
            'url': 'https://github.com/example/backend/issues/456',
            'repository': {
                'name': 'api-server',
                'language': 'Python',
                'stars': 1200
            },
            'labels': ['enhancement', 'backend', 'security'],
            'comments': 12,
            'difficulty': 'medium',
            'ai_score': 7.2,
            'ai_summary': 'Intermediate level issue requiring knowledge of authentication patterns and security best practices.',
            'updated_at': '2025-09-28T15:30:00Z'
        }
    ]

if __name__ == "__main__":
    main()
