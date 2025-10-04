#!/usr/bin/env python3
"""
Test script for the MockResumeService
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from services.mock_resume_service import MockResumeService

def test_mock_resume_service():
    """Test the MockResumeService"""
    print("Testing MockResumeService...")
    
    try:
        # Initialize service
        resume_service = MockResumeService()
        print("✅ MockResumeService initialized successfully")
        
        # Test with sample resume text
        sample_resume_text = """
        Jane Smith
        Senior Full Stack Developer
        
        Experience:
        - 6+ years of experience in full-stack web development
        - Led a team of 4 developers on React and Node.js projects
        - Built REST APIs using Python Django and Flask
        - Deployed applications on AWS using Docker and Kubernetes
        - Worked on machine learning recommendation systems
        
        Skills:
        - Programming Languages: Python, JavaScript, TypeScript, Java
        - Frontend: React, Angular, HTML, CSS, SCSS
        - Backend: Node.js, Django, Flask, Express
        - Database: PostgreSQL, MongoDB, MySQL
        - DevOps: Docker, Kubernetes, AWS, Azure, Git
        - Testing: Jest, Pytest
        
        Projects:
        - E-commerce platform using React and Node.js with microservices architecture
        - Machine learning recommendation system with Python and TensorFlow
        - Mobile app backend with Django REST Framework
        - Open source contributions to various web development projects
        """
        
        print("🔄 Testing AI analysis...")
        
        try:
            # Test AI analysis
            result = resume_service.analyze_resume_with_ai(sample_resume_text)
            print("✅ AI analysis successful!")
            print(f"📊 Experience Level: {result['experienceLevel']}")
            print(f"💻 Skills Found: {result['programmingSkills']}")
            print(f"🎯 Interests: {result['areasOfInterest']}")
            
        except Exception as e:
            print(f"❌ AI analysis failed: {str(e)}")
            return False
        
        print("✅ All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_mock_resume_service()
    sys.exit(0 if success else 1)
