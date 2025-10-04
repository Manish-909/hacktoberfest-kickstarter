#!/usr/bin/env python3
"""
Simple test script for the ResumeService
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from services.resume_service import ResumeService

def test_gemini_api():
    """Test the Gemini API connection"""
    print("Testing ResumeService...")
    
    try:
        # Initialize service
        resume_service = ResumeService()
        print("✅ ResumeService initialized successfully")
        
        # Test with sample resume text
        sample_resume_text = """
        John Doe
        Senior Software Developer
        
        Experience:
        - 5 years of experience in full-stack web development
        - Led a team of 3 developers on React and Node.js projects
        - Built REST APIs using Python Django and Flask
        - Deployed applications on AWS using Docker
        
        Skills:
        - Programming Languages: Python, JavaScript, TypeScript, Java
        - Frontend: React, Angular, HTML, CSS
        - Backend: Node.js, Django, Flask, Express
        - Database: PostgreSQL, MongoDB
        - DevOps: Docker, AWS, Git
        
        Projects:
        - E-commerce platform using React and Node.js
        - Machine learning recommendation system with Python
        - Mobile app backend with Django REST Framework
        """
        
        print("🔄 Testing Gemini AI analysis...")
        
        try:
            # Test AI analysis
            result = resume_service.analyze_resume_with_gemini(sample_resume_text)
            print("✅ Gemini AI analysis successful!")
            print(f"📊 Results: {result}")
            
        except Exception as e:
            print(f"❌ Gemini AI analysis failed: {str(e)}")
            return False
        
        print("✅ All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_gemini_api()
    sys.exit(0 if success else 1)
