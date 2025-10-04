from datetime import datetime, timedelta
import re

def format_time_ago(date_string: str) -> str:
    """Format a date string to 'X time ago' format"""
    
    try:
        date = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        now = datetime.now(date.timezone)
        
        diff = now - date
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"
            
    except Exception:
        return "Recently"

def format_number(num: int) -> str:
    """Format numbers with K/M suffixes"""
    
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    else:
        return str(num)

def extract_language_from_labels(labels: list) -> str:
    """Extract programming language from issue labels"""
    
    language_indicators = {
        'python': 'Python',
        'javascript': 'JavaScript',
        'typescript': 'TypeScript',
        'java': 'Java',
        'cpp': 'C++',
        'c++': 'C++',
        'csharp': 'C#',
        'go': 'Go',
        'rust': 'Rust',
        'php': 'PHP',
        'ruby': 'Ruby',
        'swift': 'Swift',
        'kotlin': 'Kotlin'
    }
    
    for label in labels:
        label_lower = label.lower()
        for indicator, language in language_indicators.items():
            if indicator in label_lower:
                return language
    
    return 'Unknown'

def clean_text(text: str, max_length: int = 200) -> str:
    """Clean and truncate text for display"""
    
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Truncate if too long
    if len(text) > max_length:
        text = text[:max_length] + "..."
    
    return text

def calculate_difficulty_score(labels: list, body: str = "", comments: int = 0) -> tuple:
    """Calculate difficulty level and score"""
    
    label_text = ' '.join(labels).lower()
    
    # Easy indicators
    easy_indicators = [
        'good first issue', 'easy', 'beginner', 'starter',
        'first-timers-only', 'newbie', 'simple'
    ]
    
    # Hard indicators  
    hard_indicators = [
        'expert', 'advanced', 'complex', 'difficult',
        'breaking change', 'architecture', 'performance'
    ]
    
    # Medium indicators
    medium_indicators = [
        'enhancement', 'feature', 'improvement',
        'optimization', 'refactor'
    ]
    
    # Check for difficulty indicators in labels
    if any(indicator in label_text for indicator in easy_indicators):
        return 'easy', 8
    elif any(indicator in label_text for indicator in hard_indicators):
        return 'hard', 4
    elif any(indicator in label_text for indicator in medium_indicators):
        return 'medium', 6
    
    # Fallback based on issue metrics
    if comments > 15 or (body and len(body) > 2000):
        return 'hard', 4
    elif comments > 5 or (body and len(body) > 500):
        return 'medium', 6
    else:
        return 'easy', 8

def get_skill_categories() -> dict:
    """Get categorized skills for better organization"""
    
    return {
        'Frontend': [
            'JavaScript', 'TypeScript', 'React', 'Vue.js', 'Angular',
            'HTML', 'CSS', 'SCSS', 'Tailwind', 'Bootstrap', 'jQuery'
        ],
        'Backend': [
            'Python', 'Java', 'Node.js', 'Express', 'Django', 'Flask',
            'Spring Boot', 'PHP', 'Laravel', 'Ruby', 'Rails', 'Go', 'Rust'
        ],
        'Mobile': [
            'Swift', 'Kotlin', 'React Native', 'Flutter', 'Xamarin'
        ],
        'Database': [
            'MongoDB', 'PostgreSQL', 'MySQL', 'SQLite', 'Redis'
        ],
        'DevOps': [
            'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP', 'Linux', 'Bash'
        ],
        'Other': [
            'C++', 'C#', '.NET', 'GraphQL', 'REST API', 'Git'
        ]
    }

def validate_github_url(url: str) -> bool:
    """Validate if a URL is a valid GitHub issue URL"""
    
    github_issue_pattern = r'https://github\.com/[\w\-\.]+/[\w\-\.]+/issues/\d+'
    return bool(re.match(github_issue_pattern, url))

def extract_repo_info(github_url: str) -> dict:
    """Extract repository information from GitHub URL"""
    
    pattern = r'https://github\.com/([\w\-\.]+)/([\w\-\.]+)'
    match = re.match(pattern, github_url)
    
    if match:
        return {
            'owner': match.group(1),
            'repo': match.group(2),
            'full_name': f"{match.group(1)}/{match.group(2)}"
        }
    
    return {}
