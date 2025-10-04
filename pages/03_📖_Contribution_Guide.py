import streamlit as st
from utils.styling import apply_custom_css
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

st.title("📖 Contribution Guide")

def main():
    # Check if coming from a specific issue
    selected_issue = st.session_state.get('selected_issue')
    experience_level = 'beginner'
    
    if st.session_state.profile:
        experience_level = st.session_state.profile.get('experience_level', 'beginner')
    
    if selected_issue:
        st.success(f"📌 **Selected Issue:** {selected_issue['title']}")
        st.markdown(f"[View Issue on GitHub]({selected_issue['url']})")
        st.markdown("---")
    
    # Experience level selector
    col1, col2 = st.columns([1, 2])
    with col1:
        guide_level = st.selectbox(
            "Guide Level:",
            ['beginner', 'intermediate', 'advanced'],
            index=['beginner', 'intermediate', 'advanced'].index(experience_level)
        )
    
    # Display appropriate guide
    if guide_level == 'beginner':
        display_beginner_guide()
    elif guide_level == 'intermediate':
        display_intermediate_guide()
    else:
        display_advanced_guide()
    
    # Additional resources
    display_resources()

def display_beginner_guide():
    st.markdown("## 🌱 Beginner's Guide to Open Source")
    
    # Progress tracker
    st.markdown("### 🎯 Step-by-Step Process")
    
    # Use native Streamlit components instead of complex visualizations
    progress_steps = [
        "Fork Repository", "Clone Fork", "Create Branch", 
        "Make Changes", "Commit Changes", "Push Changes", "Create PR"
    ]
    
    # Show progress as metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Steps", "7", help="Complete process steps")
    with col2:
        st.metric("Time Needed", "1-2 hours", help="For first contribution")
    with col3:
        st.metric("Difficulty", "⭐⭐", help="Beginner friendly")
    
    steps = [
        {
            'title': '1. Fork the Repository',
            'description': 'Click the "Fork" button on GitHub to create your own copy',
            'command': None,
            'tip': 'This creates a personal copy you can modify without affecting the original'
        },
        {
            'title': '2. Clone Your Fork',
            'description': 'Download the repository to your computer',
            'command': '''git clone https://github.com/YOUR_USERNAME/REPO_NAME.git
cd REPO_NAME''',
            'tip': 'Replace YOUR_USERNAME and REPO_NAME with actual values'
        },
        {
            'title': '3. Create a New Branch',
            'description': 'Create a separate branch for your changes',
            'command': 'git checkout -b fix-issue-name',
            'tip': 'Use descriptive names like "add-dark-mode" or "fix-login-bug"'
        },
        {
            'title': '4. Make Your Changes',
            'description': 'Edit the files to solve the issue',
            'command': None,
            'tip': 'Read the issue description carefully and test your changes'
        },
        {
            'title': '5. Commit Your Changes',
            'description': 'Save your changes with a clear message',
            'command': '''git add .
git commit -m "Fix: Add description of your fix"''',
            'tip': 'Write clear commit messages explaining what you changed'
        },
        {
            'title': '6. Push to GitHub',
            'description': 'Upload your changes to your fork',
            'command': 'git push origin fix-issue-name',
            'tip': 'This makes your changes available on GitHub'
        },
        {
            'title': '7. Create Pull Request',
            'description': 'Submit your changes for review',
            'command': None,
            'tip': 'Go to the original repository and click "Compare & pull request"'
        }
    ]
    
    for i, step in enumerate(steps):
        with st.expander(step['title'], expanded=(i == 0)):
            st.write(step['description'])
            if step['command']:
                st.code(step['command'], language='bash')
            if step['tip']:
                st.info(f"💡 **Tip:** {step['tip']}")

def display_intermediate_guide():
    st.markdown("## 💻 Intermediate Guide")
    
    # Show stats for intermediate contributors
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Recommended PRs", "2-5", help="Per month for skill building")
    with col2:
        st.metric("Success Rate", "85%", help="Typical acceptance rate")
    with col3:
        st.metric("Review Time", "3-7 days", help="Average response time")
    
    tabs = st.tabs(['🔧 Setup', '⚡ Best Practices', '📝 Review Process'])
    
    with tabs[0]:
        st.markdown("""
        ### Development Environment Setup
        
        **1. Read Contributing Guidelines**
        - Check CONTRIBUTING.md
        - Review CODE_OF_CONDUCT.md
        - Understand project structure
        
        **2. Set Up Development Environment**
        """)
        
        st.code("""
# Install dependencies
npm install  # or yarn, pip install -r requirements.txt

# Run tests to ensure everything works
npm test

# Start development server
npm run dev
        """, language='bash')
        
        st.markdown("""
        **3. Create Feature Branch**
        """)
        
        st.code("""
git checkout -b feature/issue-123-description
git push -u origin feature/issue-123-description
        """, language='bash')
    
    with tabs[1]:
        st.markdown("""
        ### Best Practices
        
        ✅ **Do:**
        - Write tests for new functionality
        - Follow project coding standards
        - Update documentation
        - Make atomic commits
        - Reference issue numbers in commits
        
        ❌ **Don't:**
        - Mix unrelated changes in one PR
        - Submit without testing
        - Ignore linting errors
        - Force push to shared branches
        """)
        
        # Show a checklist
        st.markdown("#### 📋 Pre-submission Checklist")
        with st.form("checklist_form"):
            check1 = st.checkbox("All tests pass locally")
            check2 = st.checkbox("Code follows project style")
            check3 = st.checkbox("Documentation updated")
            check4 = st.checkbox("Commit messages are clear")
            check5 = st.checkbox("PR description is complete")
            
            if st.form_submit_button("✅ Ready to Submit"):
                if all([check1, check2, check3, check4, check5]):
                    st.success("🎉 Your PR is ready to submit!")
                else:
                    st.warning("⚠️ Please complete all checklist items first")
    
    with tabs[2]:
        st.markdown("""
        ### Code Review Process
        
        **1. Self-Review First**
        - Check your own code before submitting
        - Ensure all tests pass
        - Verify documentation is updated
        
        **2. Respond to Feedback**
        - Address all review comments
        - Ask questions if unclear
        - Make requested changes promptly
        
        **3. Be Patient**
        - Maintainers review in their free time
        - Follow up politely if no response after a week
        """)

def display_advanced_guide():
    st.markdown("## 🚀 Advanced Contributor Guide")
    
    # Advanced metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Leadership Level", "Mentor", help="Help guide other contributors")
    with col2:
        st.metric("Complex PRs", "5-10", help="Major features per quarter")
    with col3:
        st.metric("Review Participation", "Active", help="Review others' PRs")
    
    tabs = st.tabs(['🗃️ Architecture', '📄 Complex Changes', '👥 Community'])
    
    with tabs[0]:
        st.markdown("""
        ### Understanding Project Architecture
        
        - Study codebase structure and patterns
        - Understand build and deployment processes  
        - Review existing tests and documentation
        - Identify areas for improvement
        """)
        
        # Architecture analysis checklist
        with st.expander("📊 Architecture Analysis Checklist"):
            st.markdown("""
            - [ ] Understand the main data flow
            - [ ] Identify key abstractions and interfaces
            - [ ] Map out dependencies between modules
            - [ ] Review error handling patterns
            - [ ] Understand testing strategies
            """)
    
    with tabs[1]:
        st.markdown("""
        ### Making Complex Changes
        
        **1. Design Document**
        - Create RFC for major changes
        - Discuss approach with maintainers
        - Get consensus before implementation
        
        **2. Implementation Strategy**
        - Break down into smaller commits
        - Maintain backwards compatibility
        - Add comprehensive tests
        - Update all relevant documentation
        
        **3. Performance Considerations**
        - Profile before and after changes
        - Consider memory and CPU impact
        - Test with realistic data sets
        """)
        
        # Performance tracking
        with st.expander("⚡ Performance Impact Tracker"):
            perf_col1, perf_col2 = st.columns(2)
            with perf_col1:
                st.metric("Build Time", "Before: 2.3s", delta="After: 2.1s")
                st.metric("Bundle Size", "Before: 245KB", delta="After: 238KB")
            with perf_col2:
                st.metric("Test Suite", "Before: 45s", delta="After: 42s")
                st.metric("Memory Usage", "Before: 85MB", delta="After: 82MB")
    
    with tabs[2]:
        st.markdown("""
        ### Community Leadership
        
        - Help review other contributors' PRs
        - Answer questions in issues and discussions
        - Mentor new contributors
        - Propose and lead initiatives
        - Maintain project standards
        """)
        
        # Community impact metrics
        with st.expander("🌟 Community Impact"):
            impact_col1, impact_col2 = st.columns(2)
            with impact_col1:
                st.metric("PRs Reviewed", "15", help="This month")
                st.metric("Issues Helped", "8", help="Questions answered")
            with impact_col2:
                st.metric("Contributors Mentored", "3", help="New people helped")
                st.metric("Discussions Led", "5", help="Technical discussions")

def display_resources():
    st.markdown("---")
    st.markdown("## 📚 Helpful Resources")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🔗 Essential Links
        - [GitHub Flow Guide](https://guides.github.com/introduction/flow/)
        - [First Contributions](https://github.com/firstcontributions/first-contributions)
        - [How to Write Good Commit Messages](https://chris.beams.io/posts/git-commit/)
        - [Open Source Guide](https://opensource.guide/)
        """)
    
    with col2:
        st.markdown("""
        ### 🛠️ Useful Tools  
        - [GitKraken](https://www.gitkraken.com/) - Git GUI
        - [VS Code](https://code.visualstudio.com/) - Code Editor
        - [GitHub CLI](https://cli.github.com/) - Command Line Tool
        - [Conventional Commits](https://www.conventionalcommits.org/) - Commit Standards
        """)
    
    # Quick reference chart using Streamlit native charting
    st.markdown("### 📊 Contribution Types Overview")
    
    contribution_data = {
        'Type': ['Bug Fix', 'Feature', 'Documentation', 'Tests', 'Refactor'],
        'Difficulty': [2, 4, 1, 3, 5],
        'Time (hours)': [1, 8, 0.5, 2, 6]
    }
    
    # Show as a simple bar chart using Streamlit
    col1, col2 = st.columns(2)
    with col1:
        st.bar_chart(
            data={contribution_data['Type'][i]: contribution_data['Difficulty'][i] 
                  for i in range(len(contribution_data['Type']))},
            use_container_width=True
        )
        st.caption("Difficulty Level by Contribution Type")
    
    with col2:
        st.bar_chart(
            data={contribution_data['Type'][i]: contribution_data['Time (hours)'][i] 
                  for i in range(len(contribution_data['Type']))},
            use_container_width=True
        )
        st.caption("Time Investment by Contribution Type")
    
    # Troubleshooting section
    with st.expander("🔧 Common Issues & Solutions"):
        st.markdown("""
        **Problem: Fork is out of sync**
        ```bash
        git remote add upstream https://github.com/ORIGINAL_OWNER/ORIGINAL_REPO.git
        git fetch upstream
        git checkout main
        git merge upstream/main
        git push origin main
        ```
        
        **Problem: Merge conflicts**
        ```bash
        # Fix conflicts in your editor
        git add .
        git commit -m "Resolve merge conflicts"
        ```
        
        **Problem: Need to update PR**
        ```bash
        # Make changes, then:
        git add .
        git commit -m "Address review feedback"
        git push origin your-branch-name
        ```
        """)
    
    # Success metrics
    st.markdown("### 🎯 Success Metrics")
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    
    with metrics_col1:
        st.metric("PR Acceptance", "95%", delta="↗️ Good practices")
    with metrics_col2:
        st.metric("Review Speed", "2 days", delta="↗️ Clear descriptions")
    with metrics_col3:
        st.metric("Community Rating", "4.8/5", delta="↗️ Helpful attitude")
    with metrics_col4:
        st.metric("Repeat Contributions", "85%", delta="↗️ Positive experience")

if __name__ == "__main__":
    main()
