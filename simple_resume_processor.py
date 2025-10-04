#!/usr/bin/env python3
"""
Simple Resume Processor using Gemini API via HTTP requests
Analyzes uploaded resumes and creates structured profiles
"""

import os
import json
import sys
import requests
from pathlib import Path
from typing import Dict, Optional

class SimpleResumeProcessor:
    """Simple service for processing resume files using Gemini API via HTTP"""
    
    def __init__(self, api_key: Optional[str] = None):
        # Use API key from environment or parameter
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key is required. Set GEMINI_API_KEY environment variable or pass api_key parameter.")
        
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
        
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
            # Try with different encoding
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()

    def analyze_resume_with_gemini(self, resume_text: str) -> Dict:
        """Analyze resume text using Gemini API to extract profile information"""
        
        prompt = f"""Act as an expert career counselor AI and resume interpreter. Your primary function is to analyze the text of a resume to extract key information about a candidate's professional profile.

Analyze the provided resume text to identify the candidate's:
1. Experience Level: Categorize their overall professional experience
2. Programming Skills: Identify all programming languages, frameworks, and technologies they know
3. Areas of Interest: Infer their professional interests based on their project descriptions, summary, and experience

You must strictly use the predefined lists for Programming Skills and Areas of Interest.

SKILLS LIST:
{json.dumps(self.SKILLS_LIST)}

INTERESTS LIST:
{json.dumps(self.INTERESTS_LIST)}

Analysis Guidelines:
1. For Experience Level, classify as: beginner, intermediate, or advanced
   - beginner: 0-2 years, junior roles, internships, entry-level positions
   - intermediate: 3-5 years, mid-level roles, some leadership experience
   - advanced: 5+ years, senior roles, team lead, architect positions

2. For Programming Skills, only include skills that are explicitly mentioned or clearly implied in the resume

3. For Areas of Interest, infer from:
   - Job responsibilities and projects
   - Technologies used
   - Industry domains worked in
   - Stated interests or objectives

Return ONLY a valid JSON object with no additional text or formatting:

{{"experienceLevel": "beginner|intermediate|advanced", "programmingSkills": ["skill1", "skill2"], "areasOfInterest": ["interest1", "interest2"]}}

Resume Text:
{resume_text[:3000]}  # Truncate to avoid token limits
"""

        headers = {
            'Content-Type': 'application/json',
        }
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.3,
                "topK": 1,
                "topP": 1,
                "maxOutputTokens": 2048,
            },
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]
        }

        try:
            url = f"{self.base_url}?key={self.api_key}"
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                
                if 'candidates' in result and len(result['candidates']) > 0:
                    content = result['candidates'][0]['content']['parts'][0]['text']
                    return self.parse_gemini_response(content)
                else:
                    print("No candidates in response")
                    return self.get_default_profile()
            else:
                print(f"HTTP Error {response.status_code}: {response.text}")
                return self.get_default_profile()
                
        except Exception as e:
            print(f"Gemini API error: {e}")
            return self.get_default_profile()

    def parse_gemini_response(self, response_text: str) -> Dict:
        """Parse Gemini response and extract profile data"""
        try:
            # Clean up the response
            if response_text.startswith("```"):
                # Remove markdown code blocks
                lines = response_text.split('\n')
                start_idx = 0
                end_idx = len(lines)
                
                for i, line in enumerate(lines):
                    if line.strip().startswith('```'):
                        if start_idx == 0:
                            start_idx = i + 1
                        else:
                            end_idx = i
                            break
                
                response_text = '\n'.join(lines[start_idx:end_idx])
            
            # Remove any "json" prefix
            if response_text.lower().startswith('json'):
                response_text = response_text[4:].strip()
            
            # Parse JSON
            profile_data = json.loads(response_text)
            
            # Validate and clean the response
            return self.validate_extracted_profile(profile_data)
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Raw response: {response_text}")
            return self.get_default_profile()

    def get_default_profile(self) -> Dict:
        """Return a default profile when analysis fails"""
        return {
            "experienceLevel": "intermediate",
            "programmingSkills": [],
            "areasOfInterest": []
        }

    def validate_extracted_profile(self, profile_data: Dict) -> Dict:
        """Validate and clean the extracted profile data"""
        cleaned_profile = self.get_default_profile()
        
        if profile_data:
            # Validate experience level
            experience = str(profile_data.get("experienceLevel", "")).lower()
            if experience in ["beginner", "intermediate", "advanced"]:
                cleaned_profile["experienceLevel"] = experience
            
            # Validate skills (only include those in our predefined list)
            skills = profile_data.get("programmingSkills", [])
            if isinstance(skills, list):
                cleaned_profile["programmingSkills"] = [
                    skill for skill in skills if skill in self.SKILLS_LIST
                ]
            
            # Validate interests (only include those in our predefined list)
            interests = profile_data.get("areasOfInterest", [])
            if isinstance(interests, list):
                cleaned_profile["areasOfInterest"] = [
                    interest for interest in interests if interest in self.INTERESTS_LIST
                ]
        
        return cleaned_profile

    def process_resume(self, file_path: str) -> Dict:
        """Complete resume processing pipeline"""
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return {
                    "success": False,
                    "error": f"File not found: {file_path}",
                    "profile": None,
                    "resume_text_preview": None
                }
            
            print(f"📄 Processing resume: {file_path}")
            
            # Extract text from file (currently only supports .txt)
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
            
            # Analyze with Gemini
            print("🤖 Analyzing resume with Gemini AI...")
            profile_data = self.analyze_resume_with_gemini(resume_text)
            
            return {
                "success": True,
                "profile": profile_data,
                "resume_text_preview": resume_text[:500] + "..." if len(resume_text) > 500 else resume_text,
                "resume_text_length": len(resume_text)
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
            skills_text = ", ".join(skills)
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
        print("Usage: python simple_resume_processor.py <resume_file_path>")
        print("Supported formats: .txt")
        return
    
    file_path = sys.argv[1]
    
    try:
        # Initialize the processor
        processor = SimpleResumeProcessor()
        
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
            
        else:
            print(f"❌ Resume processing failed: {result['error']}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
