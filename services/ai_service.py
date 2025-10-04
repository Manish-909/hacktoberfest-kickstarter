import requests
import json
from typing import List, Dict
import streamlit as st
import ollama

class AIService:
    def __init__(self):
        self.ollama_model = "qwen2:0.5b "
    
    def get_recommendations(self, issues: List[Dict], profile: Dict) -> List[Dict]:
        """Get AI-powered recommendations for issues"""
        
        if not issues:
            return []
        
        try:
            # Analyze issues with AI
            scored_issues = self._analyze_issues_with_ai(issues, profile)
            
            # Sort by AI score
            scored_issues.sort(key=lambda x: x.get('ai_score', 0), reverse=True)
            
            return scored_issues
            
        except Exception as e:
            st.warning(f"AI analysis unavailable: {str(e)}")
            # Fallback to simple scoring
            return self._fallback_scoring(issues, profile)
    
    def _analyze_issues_with_ai(self, issues: List[Dict], profile: Dict) -> List[Dict]:
        """Analyze issues using Ollama"""
        
        scored_issues = []
        context = self._create_user_context(profile)
        
        # Process issues in batches to avoid overwhelming the AI
        for issue in issues[:15]:  # Limit for performance
            try:
                analysis = self._analyze_single_issue(issue, context)
                
                issue_with_analysis = issue.copy()
                issue_with_analysis.update({
                    'ai_score': analysis.get('score', 5),
                    'ai_summary': analysis.get('summary', 'AI analysis in progress...'),
                    'estimated_time': analysis.get('time', '2-4 hours'),
                    'learning_opportunity': analysis.get('learning', 'Medium')
                })
                
                scored_issues.append(issue_with_analysis)
                
            except Exception as e:
                # If AI fails for this issue, use fallback
                issue['ai_score'] = self._calculate_fallback_score(issue, profile)
                issue['ai_summary'] = f"Issue in {issue['repository']['name']}: {issue['title'][:100]}..."
                scored_issues.append(issue)
        
        return scored_issues
    
    def _analyze_single_issue(self, issue: Dict, context: str) -> Dict:
        """Analyze a single issue with AI"""
        
        prompt = self._create_analysis_prompt(issue, context)
        
        try:
            response = ollama.chat(
                model=self.ollama_model,
                messages=[
                    {
                        'role': 'system',
                        'content': 'You are an expert open source mentor. Analyze GitHub issues and provide recommendations.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                options={
                    'temperature': 0.3,
                    'top_p': 0.9
                }
            )
            
            return self._parse_ai_response(response['message']['content'])
            
        except Exception as e:
            # Fallback response
            return {
                'score': 6,
                'summary': f"Great opportunity to work on {issue.get('repository', {}).get('language', 'a')} project!",
                'time': '2-4 hours',
                'learning': 'Medium'
            }
    
    def _create_analysis_prompt(self, issue: Dict, context: str) -> str:
        """Create AI analysis prompt"""
        
        return f"""
        Analyze this GitHub issue for a developer with the following profile:
        {context}
        
        Issue: {issue['title']}
        Repository: {issue['repository']['name']}
        Language: {issue['repository'].get('language', 'Unknown')}
        Labels: {', '.join(issue['labels'])}
        Description: {issue.get('body', '')[:300]}...
        
        Provide a score (1-10) and brief analysis focusing on:
        - How well this matches their skills
        - Learning opportunity
        - Estimated time to complete
        - Why this is good for their level
        
        Respond in this format:
        Score: X/10
        Summary: Brief explanation
        Time: X hours
        Learning: High/Medium/Low
        """
    
    def _create_user_context(self, profile: Dict) -> str:
        """Create user context for AI"""
        
        return f"""
        Experience: {profile['experience_level']}
        Skills: {', '.join(profile['skills'][:10])}
        Interests: {', '.join(profile['interests'][:8])}
        Goal: Find good open source contributions for Hacktoberfest
        """
    
    def _parse_ai_response(self, response: str) -> Dict:
        """Parse AI response into structured data"""
        
        try:
            # Extract structured information from AI response
            lines = response.split('\n')
            result = {}
            
            for line in lines:
                if 'Score:' in line:
                    score_text = line.split('Score:')[1].strip()
                    result['score'] = int(score_text.split('/')[0])
                elif 'Summary:' in line:
                    result['summary'] = line.split('Summary:')[1].strip()
                elif 'Time:' in line:
                    result['time'] = line.split('Time:')[1].strip()
                elif 'Learning:' in line:
                    result['learning'] = line.split('Learning:')[1].strip()
            
            # Set defaults if parsing failed
            if 'score' not in result:
                result['score'] = 6
            if 'summary' not in result:
                result['summary'] = response[:200] + '...'
            if 'time' not in result:
                result['time'] = '2-4 hours'
            if 'learning' not in result:
                result['learning'] = 'Medium'
                
            return result
            
        except Exception:
            # Fallback parsing
            return {
                'score': 6,
                'summary': response[:150] + '...' if len(response) > 150 else response,
                'time': '2-4 hours', 
                'learning': 'Medium'
            }
    
    def _fallback_scoring(self, issues: List[Dict], profile: Dict) -> List[Dict]:
        """Simple fallback scoring when AI is unavailable"""
        
        for issue in issues:
            score = self._calculate_fallback_score(issue, profile)
            issue['ai_score'] = score
            issue['ai_summary'] = f"Good match for {profile['experience_level']} developer interested in {issue['repository'].get('language', 'programming')}!"
            issue['estimated_time'] = '2-4 hours'
            issue['learning_opportunity'] = 'Medium'
        
        issues.sort(key=lambda x: x['ai_score'], reverse=True)
        return issues
    
    def _calculate_fallback_score(self, issue: Dict, profile: Dict) -> int:
        """Calculate basic compatibility score"""
        
        score = 5
        
        # Experience matching
        difficulty = issue.get('difficulty', 'medium')
        if profile['experience_level'] == 'beginner' and difficulty == 'easy':
            score += 2
        elif profile['experience_level'] == 'intermediate' and difficulty in ['easy', 'medium']:
            score += 1
        
        # Language matching
        repo_lang = issue['repository'].get('language', '').lower()
        user_skills = [skill.lower() for skill in profile['skills']]
        if repo_lang in user_skills:
            score += 2
        
        # Label matching with interests
        labels = [label.lower() for label in issue['labels']]
        interests = [interest.lower() for interest in profile['interests']]
        common_interests = set(labels) & set(interests)
        score += min(len(common_interests), 2)
        
        # Repository activity (comments indicate engagement)
        if issue.get('comments', 0) > 0:
            score += 1
        
        return min(10, max(1, score))
