import requests
import time
from typing import List, Dict, Optional
import streamlit as st

class GitHubService:
    def __init__(self, token: Optional[str] = None):
        self.base_url = "https://api.github.com"
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Hacktoberfest-Mentor-2025/1.0'
        }
        
        # Use token from session state if available
        if not token and hasattr(st.session_state, 'github_token') and st.session_state.github_token:
            token = st.session_state.github_token
            
        if token:
            self.headers['Authorization'] = f'token {token}'
            self.rate_limit = 5000  # Authenticated rate limit
        else:
            self.rate_limit = 60   # Unauthenticated rate limit
    
    def fetch_issues(self, skills: List[str], interests: List[str], 
                    experience_level: str, max_results: int = 20) -> List[Dict]:
        """Fetch Hacktoberfest 2025 issues based on user criteria"""
        
        try:
            # Build Hacktoberfest-specific search queries
            queries = self._build_hacktoberfest_queries(skills, interests, experience_level)
            
            all_issues = []
            for query in queries[:4]:  # Limit queries to avoid rate limiting
                try:
                    issues = self._search_issues(query, per_page=min(max_results // 4, 25))
                    all_issues.extend(issues)
                    time.sleep(1.2)  # Rate limiting - be respectful
                except Exception as e:
                    st.warning(f"Query failed: {str(e)}")
                    continue
            
            # Remove duplicates and limit results
            unique_issues = self._deduplicate_issues(all_issues)
            
            # Filter and prioritize Hacktoberfest issues
            hacktoberfest_issues = self._prioritize_hacktoberfest_issues(unique_issues)
            
            return hacktoberfest_issues[:max_results]
            
        except Exception as e:
            st.error(f"GitHub API Error: {str(e)}")
            return self._get_hacktoberfest_fallback_issues()
    
    def _build_hacktoberfest_queries(self, skills: List[str], interests: List[str], 
                                   experience_level: str) -> List[str]:
        """Build Hacktoberfest 2025 specific search queries"""
        
        # Base query for Hacktoberfest 2025
        base_query = 'state:open type:issue archived:false'
        
        # Hacktoberfest labels (both current and historical)
        hacktoberfest_labels = [
            'hacktoberfest',
            'hacktoberfest2025',
            'hacktoberfest-accepted',
            'hacktober',
            'october'
        ]
        
        queries = []
        
        # Experience-based queries with Hacktoberfest focus
        if experience_level == 'beginner':
            for label in hacktoberfest_labels[:3]:
                queries.extend([
                    f'{base_query} label:"{label}" label:"good first issue"',
                    f'{base_query} label:"{label}" label:"beginner-friendly"',
                    f'{base_query} label:"{label}" label:"first-timers-only"'
                ])
        elif experience_level == 'intermediate':
            for label in hacktoberfest_labels[:2]:
                queries.extend([
                    f'{base_query} label:"{label}" label:"help wanted"',
                    f'{base_query} label:"{label}" label:"enhancement"',
                    f'{base_query} label:"{label}" label:"good first issue"'
                ])
        else:  # advanced
            for label in hacktoberfest_labels[:2]:
                queries.extend([
                    f'{base_query} label:"{label}" label:"help wanted"',
                    f'{base_query} label:"{label}" label:"feature"',
                    f'{base_query} label:"{label}" label:"enhancement"'
                ])
        
        # Add language filters from skills
        programming_languages = [
            'python', 'javascript', 'typescript', 'java', 'go', 'rust', 
            'cpp', 'csharp', 'php', 'ruby', 'swift', 'kotlin', 'html', 'css'
        ]
        
        user_languages = []
        for skill in skills:
            skill_lower = skill.lower()
            if 'javascript' in skill_lower or skill_lower == 'js':
                user_languages.append('javascript')
            elif skill_lower in programming_languages:
                user_languages.append(skill_lower)
            elif skill_lower == 'c++':
                user_languages.append('cpp')
            elif skill_lower == 'c#':
                user_languages.append('csharp')
        
        # Create language-specific Hacktoberfest queries
        if user_languages:
            for lang in user_languages[:3]:  # Top 3 languages
                queries.append(f'{base_query} label:"hacktoberfest" language:{lang}')
                if experience_level == 'beginner':
                    queries.append(f'{base_query} label:"hacktoberfest" label:"good first issue" language:{lang}')
        
        # Add topic-based queries for popular Hacktoberfest repositories
        popular_hacktoberfest_topics = [
            'web-development', 'machine-learning', 'python', 'javascript', 
            'react', 'open-source', 'beginner-friendly', 'documentation'
        ]
        
        for topic in popular_hacktoberfest_topics[:3]:
            queries.append(f'{base_query} label:"hacktoberfest" topic:{topic}')
        
        return list(set(queries))[:8]  # Remove duplicates and limit
    
    def _search_issues(self, query: str, per_page: int = 25) -> List[Dict]:
        """Search GitHub issues using the Search API"""
        
        url = f"{self.base_url}/search/issues"
        params = {
            'q': query,
            'sort': 'updated',
            'order': 'desc', 
            'per_page': min(per_page, 100)  # GitHub max is 100
        }
        
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            issues = []
            
            for item in data.get('items', []):
                # Skip pull requests and focus on issues
                if 'pull_request' not in item:
                    formatted_issue = self._format_issue(item)
                    if formatted_issue and self._is_hacktoberfest_issue(formatted_issue):
                        issues.append(formatted_issue)
            
            return issues
            
        elif response.status_code == 403:
            st.error("🔒 GitHub API rate limit exceeded. Please add a GitHub token in the settings.")
            return []
        elif response.status_code == 422:
            st.warning("⚠️ Search query too complex. Trying simplified search...")
            return []
        else:
            st.warning(f"GitHub API returned status {response.status_code}")
            return []
    
    def _is_hacktoberfest_issue(self, issue: Dict) -> bool:
        """Check if issue is relevant for Hacktoberfest 2025"""
        
        labels = [label.lower() for label in issue.get('labels', [])]
        
        # Must have at least one Hacktoberfest-related label
        hacktoberfest_keywords = [
            'hacktoberfest', 'hacktoberfest2025', 'hacktoberfest-accepted',
            'hacktober', 'october', 'good first issue', 'help wanted'
        ]
        
        has_hacktoberfest_label = any(
            any(keyword in label for keyword in hacktoberfest_keywords)
            for label in labels
        )
        
        # Check if repository name suggests Hacktoberfest participation
        repo_name = issue.get('repository', {}).get('name', '').lower()
        has_hacktoberfest_repo = any(keyword in repo_name for keyword in ['hacktoberfest', '2025'])
        
        return has_hacktoberfest_label or has_hacktoberfest_repo
    
    def _prioritize_hacktoberfest_issues(self, issues: List[Dict]) -> List[Dict]:
        """Prioritize issues based on Hacktoberfest relevance"""
        
        def hacktoberfest_score(issue):
            score = 0
            labels = [label.lower() for label in issue.get('labels', [])]
            
            # High priority labels
            if any('hacktoberfest' in label for label in labels):
                score += 10
            if any('good first issue' in label for label in labels):
                score += 8
            if any('help wanted' in label for label in labels):
                score += 6
            if any('beginner' in label for label in labels):
                score += 5
            
            # Repository factors
            repo_name = issue.get('repository', {}).get('name', '').lower()
            if 'hacktoberfest' in repo_name or '2025' in repo_name:
                score += 7
            
            # Freshness factor (recent issues are better)
            try:
                from datetime import datetime, timezone
                updated = datetime.fromisoformat(issue.get('updated_at', '').replace('Z', '+00:00'))
                days_old = (datetime.now(timezone.utc) - updated).days
                if days_old < 7:
                    score += 3
                elif days_old < 30:
                    score += 1
            except:
                pass
            
            # Activity factor (issues with some engagement)
            comments = issue.get('comments', 0)
            if 1 <= comments <= 5:  # Sweet spot - has attention but not overwhelming
                score += 2
            
            return score
        
        # Sort by Hacktoberfest relevance
        issues.sort(key=hacktoberfest_score, reverse=True)
        return issues
    
    def _format_issue(self, issue: Dict) -> Optional[Dict]:
        """Format GitHub issue data for display"""
        
        try:
            # Extract repository info
            repo_info = issue.get('repository', {})
            labels = [label['name'] for label in issue.get('labels', [])]
            
            # Get repository details
            repo_url = issue.get('repository_url', '')
            repo_parts = repo_url.split('/')
            repo_owner = repo_parts[-2] if len(repo_parts) >= 2 else 'unknown'
            repo_name = repo_parts[-1] if len(repo_parts) >= 1 else 'unknown'
            
            return {
                'id': issue['id'],
                'number': issue['number'],
                'title': issue['title'],
                'body': self._clean_body(issue.get('body', '')),
                'url': issue['html_url'],
                'repository': {
                    'name': repo_name,
                    'owner': repo_owner,
                    'full_name': f"{repo_owner}/{repo_name}",
                    'language': self._extract_language(labels, issue),
                    'stars': 0,  # Would need separate API call for stars
                    'is_hacktoberfest': self._check_hacktoberfest_repo(repo_name, labels)
                },
                'labels': labels,
                'comments': issue.get('comments', 0),
                'created_at': issue['created_at'],
                'updated_at': issue['updated_at'],
                'assignee': issue.get('assignee', {}).get('login') if issue.get('assignee') else None,
                'difficulty': self._assess_difficulty(labels, issue.get('body', '')),
                'state': issue.get('state', 'open'),
                'hacktoberfest_score': self._calculate_hacktoberfest_score(labels, repo_name)
            }
            
        except Exception as e:
            return None
    
    def _check_hacktoberfest_repo(self, repo_name: str, labels: List[str]) -> bool:
        """Check if repository is participating in Hacktoberfest"""
        
        repo_keywords = ['hacktoberfest', '2025']
        label_keywords = ['hacktoberfest', 'hacktoberfest2025', 'hacktoberfest-accepted']
        
        repo_match = any(keyword in repo_name.lower() for keyword in repo_keywords)
        label_match = any(keyword in label.lower() for label in labels for keyword in label_keywords)
        
        return repo_match or label_match
    
    def _calculate_hacktoberfest_score(self, labels: List[str], repo_name: str) -> int:
        """Calculate how relevant this issue is for Hacktoberfest"""
        
        score = 0
        labels_lower = [label.lower() for label in labels]
        
        # Direct Hacktoberfest labels
        if any('hacktoberfest' in label for label in labels_lower):
            score += 10
        if 'hacktoberfest2025' in labels_lower:
            score += 15
        if 'hacktoberfest-accepted' in labels_lower:
            score += 12
        
        # Beginner-friendly labels
        if 'good first issue' in labels_lower:
            score += 8
        if any(term in labels_lower for term in ['beginner-friendly', 'easy', 'starter']):
            score += 6
        if 'first-timers-only' in labels_lower:
            score += 7
        
        # General contribution labels
        if 'help wanted' in labels_lower:
            score += 5
        if any(term in labels_lower for term in ['documentation', 'docs']):
            score += 4
        
        # Repository name bonus
        if 'hacktoberfest' in repo_name.lower():
            score += 8
        
        return min(score, 20)  # Cap at 20
    
    def _clean_body(self, body: str) -> str:
        """Clean and truncate issue body"""
        if not body:
            return "No description provided. Check the issue on GitHub for more details."
        
        # Remove excessive whitespace and markdown
        import re
        body = re.sub(r'\r\n|\r|\n', ' ', body)
        body = re.sub(r'\s+', ' ', body.strip())
        body = re.sub(r'``````', '[Code block]', body)  # Replace code blocks
        body = re.sub(r'`.*?`', '[Code]', body)  # Replace inline code
        
        # Truncate if too long
        if len(body) > 400:
            body = body[:400] + "..."
        
        return body
    
    def _extract_language(self, labels: List[str], issue: Dict) -> str:
        """Extract programming language from labels"""
        
        # Language mapping from labels
        language_indicators = {
            'python': 'Python', 'javascript': 'JavaScript', 'typescript': 'TypeScript',
            'java': 'Java', 'cpp': 'C++', 'c++': 'C++', 'csharp': 'C#', 'c#': 'C#',
            'go': 'Go', 'rust': 'Rust', 'php': 'PHP', 'ruby': 'Ruby',
            'swift': 'Swift', 'kotlin': 'Kotlin', 'html': 'HTML', 'css': 'CSS',
            'react': 'JavaScript', 'vue': 'JavaScript', 'angular': 'TypeScript',
            'node': 'JavaScript', 'django': 'Python', 'flask': 'Python'
        }
        
        # Check labels first
        for label in labels:
            label_lower = label.lower()
            for indicator, language in language_indicators.items():
                if indicator in label_lower:
                    return language
        
        return 'Multiple'  # Default when language is unclear
    
    def _assess_difficulty(self, labels: List[str], body: str) -> str:
        """Assess issue difficulty from labels and content"""
        
        label_text = ' '.join(labels).lower()
        
        # Easy indicators
        easy_indicators = [
            'good first issue', 'easy', 'beginner', 'starter', 'first-timers-only',
            'newbie-friendly', 'low-hanging-fruit', 'simple', 'trivial'
        ]
        
        # Hard indicators
        hard_indicators = [
            'expert', 'advanced', 'complex', 'difficult', 'breaking-change',
            'architecture', 'performance', 'security', 'refactor', 'critical'
        ]
        
        # Medium indicators
        medium_indicators = [
            'enhancement', 'feature', 'improvement', 'optimization'
        ]
        
        # Check for difficulty indicators
        if any(indicator in label_text for indicator in easy_indicators):
            return 'easy'
        elif any(indicator in label_text for indicator in hard_indicators):
            return 'hard'
        elif any(indicator in label_text for indicator in medium_indicators):
            return 'medium'
        else:
            # Default to easy for Hacktoberfest to encourage participation
            return 'easy'
    
    def _deduplicate_issues(self, issues: List[Dict]) -> List[Dict]:
        """Remove duplicate issues based on URL"""
        
        seen_urls = set()
        unique_issues = []
        
        for issue in issues:
            issue_url = issue.get('url', '')
            if issue_url not in seen_urls:
                seen_urls.add(issue_url)
                unique_issues.append(issue)
        
        return unique_issues
    
    def _get_hacktoberfest_fallback_issues(self) -> List[Dict]:
        """Provide fallback Hacktoberfest sample issues when API fails"""
        
        return [
            {
                'id': 1,
                'number': 123,
                'title': 'Add dark mode toggle to navigation bar [Hacktoberfest]',
                'body': 'This is a beginner-friendly issue perfect for Hacktoberfest! We need to add a dark mode toggle button to our main navigation. This involves basic CSS and JavaScript. Great for first-time contributors!',
                'url': 'https://github.com/example/hacktoberfest-web-app/issues/123',
                'repository': {
                    'name': 'hacktoberfest-web-app',
                    'owner': 'example',
                    'full_name': 'example/hacktoberfest-web-app',
                    'language': 'JavaScript',
                    'stars': 2500,
                    'is_hacktoberfest': True
                },
                'labels': ['hacktoberfest', 'good first issue', 'help wanted', 'frontend', 'css'],
                'comments': 3,
                'difficulty': 'easy',
                'created_at': '2025-10-01T10:00:00Z',
                'updated_at': '2025-10-03T15:30:00Z',
                'assignee': None,
                'state': 'open',
                'hacktoberfest_score': 18
            },
            {
                'id': 2,
                'number': 456,
                'title': 'Update documentation for new contributors [Hacktoberfest 2025]',
                'body': 'Help us improve our documentation! We need to update the CONTRIBUTING.md file with clearer instructions for new contributors. Perfect for writers and developers who want to help the community.',
                'url': 'https://github.com/example/open-source-project/issues/456',
                'repository': {
                    'name': 'open-source-project',
                    'owner': 'example',
                    'full_name': 'example/open-source-project',
                    'language': 'Python',
                    'stars': 1200,
                    'is_hacktoberfest': True
                },
                'labels': ['hacktoberfest2025', 'documentation', 'good first issue', 'help wanted'],
                'comments': 5,
                'difficulty': 'easy',
                'created_at': '2025-09-28T08:00:00Z',
                'updated_at': '2025-10-02T12:15:00Z',
                'assignee': None,
                'state': 'open',
                'hacktoberfest_score': 20
            },
            {
                'id': 3,
                'number': 789,
                'title': 'Fix bug in user profile validation',
                'body': 'There\'s a small bug in our user profile validation logic. When users enter certain special characters, the validation fails incorrectly. This is a great issue for intermediate contributors!',
                'url': 'https://github.com/example/user-management/issues/789',
                'repository': {
                    'name': 'user-management',
                    'owner': 'example',
                    'full_name': 'example/user-management',
                    'language': 'Python',
                    'stars': 800,
                    'is_hacktoberfest': True
                },
                'labels': ['hacktoberfest', 'bug', 'python', 'help wanted'],
                'comments': 8,
                'difficulty': 'medium',
                'created_at': '2025-09-25T14:20:00Z',
                'updated_at': '2025-10-01T09:45:00Z',
                'assignee': None,
                'state': 'open',
                'hacktoberfest_score': 15
            }
        ]
    
    def check_rate_limit(self) -> Dict:
        """Check current GitHub API rate limit status"""
        
        try:
            response = requests.get(f"{self.base_url}/rate_limit", headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                return {
                    'remaining': data['rate']['remaining'],
                    'limit': data['rate']['limit'],
                    'reset_time': data['rate']['reset']
                }
        except Exception:
            pass
        
        return {'remaining': 'unknown', 'limit': 'unknown', 'reset_time': 'unknown'}
