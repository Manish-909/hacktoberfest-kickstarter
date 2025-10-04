#!/usr/bin/env python3
"""
Working Resume Processor with AI Analysis
Analyzes uploaded resumes and creates structured profiles
"""

import os
import json
import sys
import re
from pathlib import Path
from typing import Dict, Optional, List

class WorkingResumeProcessor:
    """Working service for processing resume files with intelligent analysis"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        
        # Predefined lists for skills and interests
        self.SKILLS_LIST = [
            'JavaScript', 'Python', 'Java', 'TypeScript', 'React', 'Vue.js', 'Angular',
            'Node.js', 'Express', 'Django', 'Flask', 'Spring Boot', 'PHP', 'Laravel',
            'Ruby', 'Rails', 'Go', 'Rust', 'C++', 'C#', '.NET', 'Swift', 'Kotlin',
            'HTML', 'CSS', 'SCSS', 'Tailwind', 'Bootstrap', 'jQuery', 'Redux',
            'GraphQL', 'REST API', 'MongoDB', 'PostgreSQL', 'MySQL', 'SQLite',
            'Docker', 'Kubernetes', 'AWS', 'Azure', 'GCP', 'Git', 'Linux', 'Bash',
            'TensorFlow', 'PyTorch', 'Pandas', 'NumPy', 'Scikit-learn', 'OpenCV'
        ]
        
        self.INTERESTS_LIST = [
            'frontend', 'backend', 'fullstack', 'mobile', 'web', 'api', 'database',
            'devops', 'cloud', 'ai', 'machine-learning', 'data-science', 'blockchain',
            'security', 'testing', 'documentation', 'ui-ux', 'performance', 'accessibility',
            'open-source', 'beginner-friendly', 'hacktoberfest', 'help-wanted', 'bug',
            'feature', 'enhancement', 'refactor', 'optimization', 'tutorial', 'automation',
            'microservices', 'analytics', 'visualization', 'cybersecurity', 'quality-assurance'
        ]

    def extract_text_from_txt(self, file_path: str) -> str:
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()

    def determine_experience_level(self, resume_text: str) -> str:
        """Determine experience level based on resume content"""
        text_lower = resume_text.lower()
        
        # Advanced indicators
        advanced_keywords = [
            'senior', 'lead', 'architect', 'principal', 'manager', 'director',
            'team lead', 'technical lead', '6+ years', '7+ years', '8+ years', 
            '9+ years', '10+ years', 'mentoring', 'mentored'
        ]
        
        # Beginner indicators
        beginner_keywords = [
            'junior', 'entry', 'intern', 'recent graduate', 'new grad',
            '1 year', '2 years', 'entry-level', 'fresher'
        ]
        
        # Count matches
        advanced_count = sum(1 for keyword in advanced_keywords if keyword in text_lower)
        beginner_count = sum(1 for keyword in beginner_keywords if keyword in text_lower)
        
        # Check for years of experience patterns
        years_pattern = r'(\d+)[\+\s]*years?\s+(?:of\s+)?experience'
        years_matches = re.findall(years_pattern, text_lower)
        
        max_years = 0
        if years_matches:
            max_years = max(int(year) for year in years_matches)
        
        # Determine level
        if advanced_count >= 2 or max_years >= 6:
            return "advanced"
        elif beginner_count >= 1 or max_years <= 2:
            return "beginner"
        else:
            return "intermediate"

    def extract_skills(self, resume_text: str) -> List[str]:
        """Extract programming skills from resume text"""
        found_skills = []
        text_lower = resume_text.lower()
        
        for skill in self.SKILLS_LIST:
            # Create pattern that matches the skill as a whole word
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill)
        
        return found_skills

    def extract_interests(self, resume_text: str, found_skills: List[str]) -> List[str]:
        """Extract areas of interest from resume text and skills"""
        found_interests = []
        text_lower = resume_text.lower()
        
        # Direct keyword matching
        for interest in self.INTERESTS_LIST:
            pattern = r'\b' + re.escape(interest.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found_interests.append(interest)
        
        # Infer interests from skills
        skill_to_interest_mapping = {
            'React': ['frontend', 'web'],
            'Angular': ['frontend', 'web'],
            'Vue.js': ['frontend', 'web'],
            'Node.js': ['backend', 'web', 'api'],
            'Express': ['backend', 'web', 'api'],
            'Django': ['backend', 'web', 'api'],
            'Flask': ['backend', 'web', 'api'],
            'MongoDB': ['database'],
            'PostgreSQL': ['database'],
            'MySQL': ['database'],
            'Docker': ['devops', 'cloud'],
            'Kubernetes': ['devops', 'cloud'],
            'AWS': ['cloud', 'devops'],
            'Azure': ['cloud', 'devops'],
            'GCP': ['cloud', 'devops'],
            'TensorFlow': ['ai', 'machine-learning'],
            'PyTorch': ['ai', 'machine-learning'],
            'HTML': ['frontend', 'web'],
            'CSS': ['frontend', 'web'],
            'JavaScript': ['web', 'frontend'],
            'Python': ['backend', 'ai', 'data-science'],
            'Git': ['open-source'],
        }
        
        for skill in found_skills:
            if skill in skill_to_interest_mapping:
                for interest in skill_to_interest_mapping[skill]:
                    if interest not in found_interests:
                        found_interests.append(interest)
        
        # Check for fullstack indicators
        frontend_skills = ['React', 'Angular', 'Vue.js', 'HTML', 'CSS', 'JavaScript']
        backend_skills = ['Node.js', 'Express', 'Django', 'Flask', 'Python', 'Java', 'PHP']
        
        has_frontend = any(skill in found_skills for skill in frontend_skills)
        has_backend = any(skill in found_skills for skill in backend_skills)
        
        if has_frontend and has_backend and 'fullstack' not in found_interests:
            found_interests.append('fullstack')
        
        # Check for open source involvement
        if re.search(r'\b(open\s*source|github|hacktoberfest|contribution)\b', text_lower):
            if 'open-source' not in found_interests:
                found_interests.append('open-source')
        
        return found_interests

    def analyze_resume_intelligent(self, resume_text: str) -> Dict:
        """Analyze resume text using intelligent keyword extraction and pattern matching"""
        
        try:
            print("🧠 Analyzing resume using intelligent pattern matching...")
            
            # Determine experience level
            experience_level = self.determine_experience_level(resume_text)
            print(f"   Experience level detected: {experience_level}")
            
            # Extract skills
            programming_skills = self.extract_skills(resume_text)
            print(f"   Skills detected: {len(programming_skills)} skills")
            
            # Extract interests
            areas_of_interest = self.extract_interests(resume_text, programming_skills)
            print(f"   Interests inferred: {len(areas_of_interest)} interests")
            
            return {
                "experienceLevel": experience_level,
                "programmingSkills": programming_skills,
                "areasOfInterest": areas_of_interest
            }
            
        except Exception as e:
            print(f"Analysis error: {e}")
            return self.get_default_profile()

    def get_default_profile(self) -> Dict:
        """Return a default profile when analysis fails"""
        return {
            "experienceLevel": "intermediate",
            "programmingSkills": [],
            "areasOfInterest": []
        }

    def process_resume(self, file_path: str) -> Dict:
        """Complete resume processing pipeline"""
        try:
            if not os.path.exists(file_path):
                return {
                    "success": False,
                    "error": f"File not found: {file_path}",
                    "profile": None,
                    "resume_text_preview": None
                }
            
            print(f"📄 Processing resume: {file_path}")
            
            file_path_obj = Path(file_path)
            if file_path_obj.suffix.lower() != '.txt':
                return {
                    "success": False,
                    "error": f"Unsupported file type: {file_path_obj.suffix}. Currently only .txt files are supported.",
                    "profile": None,
                    "resume_text_preview": None
                }
            
            resume_text = self.extract_text_from_txt(file_path)
            
            if not resume_text.strip():
                return {
                    "success": False,
                    "error": "No text could be extracted from the resume file",
                    "profile": None,
                    "resume_text_preview": None
                }
            
            print(f"📝 Extracted {len(resume_text)} characters from resume")
            
            # Analyze resume
            profile_data = self.analyze_resume_intelligent(resume_text)
            
            return {
                "success": True,
                "profile": profile_data,
                "resume_text_preview": resume_text[:500] + "..." if len(resume_text) > 500 else resume_text,
                "resume_text_length": len(resume_text),
                "analysis_method": "intelligent_pattern_matching"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "profile": None,
                "resume_text_preview": None
            }

    def create_profile_summary(self, profile_data: Dict) -> str:
        """Create a formatted summary of the extracted profile"""
        if not profile_data:
            return "❌ No profile data available"
        
        summary = []
        summary.append("🎯 **PROFILE ANALYSIS SUMMARY**")
        summary.append("=" * 40)
        
        # Experience Level
        exp_level = profile_data.get("experienceLevel", "unknown")
        exp_emoji = {"beginner": "🌱", "intermediate": "🚀", "advanced": "⭐"}.get(exp_level, "❓")
        summary.append(f"\n{exp_emoji} **Experience Level:** {exp_level.title()}")
        
        # Programming Skills
        skills = profile_data.get("programmingSkills", [])
        summary.append(f"\n💻 **Programming Skills:** ({len(skills)} found)")
        if skills:
            # Group skills for better display
            skills_text = ", ".join(skills)
            if len(skills_text) > 80:
                # Break into lines for readability
                skill_chunks = []
                current_chunk = []
                current_length = 0
                
                for skill in skills:
                    if current_length + len(skill) + 2 > 80 and current_chunk:
                        skill_chunks.append(", ".join(current_chunk))
                        current_chunk = [skill]
                        current_length = len(skill)
                    else:
                        current_chunk.append(skill)
                        current_length += len(skill) + 2
                
                if current_chunk:
                    skill_chunks.append(", ".join(current_chunk))
                
                for chunk in skill_chunks:
                    summary.append(f"   {chunk}")
            else:
                summary.append(f"   {skills_text}")
        else:
            summary.append("   None detected")
        
        # Areas of Interest
        interests = profile_data.get("areasOfInterest", [])
        summary.append(f"\n🎯 **Areas of Interest:** ({len(interests)} found)")
        if interests:
            interests_text = ", ".join(interests)
            summary.append(f"   {interests_text}")
        else:
            summary.append("   None detected")
        
        return "\n".join(summary)


def main():
    """Main function to run the resume processor"""
    if len(sys.argv) < 2:
        print("Usage: python working_resume_processor.py <resume_file_path>")
        print("Supported formats: .txt")
        return
    
    file_path = sys.argv[1]
    
    try:
        # Initialize the processor
        processor = WorkingResumeProcessor()
        
        # Process the resume
        result = processor.process_resume(file_path)
        
        if result["success"]:
            print("✅ Resume processing completed successfully!")
            print("\n" + processor.create_profile_summary(result["profile"]))
            
            # Save results to JSON file
            output_file = Path(file_path).stem + "_profile.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"\n📁 Results saved to: {output_file}")
            print(f"📊 Analysis method: {result.get('analysis_method', 'unknown')}")
            
        else:
            print(f"❌ Resume processing failed: {result['error']}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
