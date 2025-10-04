#!/usr/bin/env python3
"""
Test script to validate all imports and services
"""

def test_imports():
    """Test all imports to ensure they work"""
    try:
        print("Testing imports...")
        
        # Test utils imports
        print("✓ Testing utils...")
        from utils.styling import apply_custom_css
        from utils.helpers import format_time_ago, format_number
        
        # Test services imports
        print("✓ Testing services...")
        from services.profile_service import ProfileService
        from services.mock_resume_service import MockResumeService
        from services.resume_service import ResumeService
        
        # Test main app import
        print("✓ Testing main app...")
        import streamlit_app
        
        # Test services functionality
        print("✓ Testing ProfileService...")
        profile_service = ProfileService()
        print("ProfileService initialized successfully")
        
        print("✓ Testing MockResumeService...")
        mock_service = MockResumeService()
        print("MockResumeService initialized successfully")
        
        print("✓ Testing ResumeService...")
        resume_service = ResumeService()
        print("ResumeService initialized successfully")
        
        print("\n🎉 All imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_imports()
