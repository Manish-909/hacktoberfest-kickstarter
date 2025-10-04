import json
from typing import Dict, Optional
import streamlit as st

class ProfileService:
    """Handle user profile management"""
    
    @staticmethod
    def save_profile(profile_data: Dict) -> bool:
        """Save user profile to session state"""
        try:
            st.session_state.profile = profile_data
            return True
        except Exception as e:
            st.error(f"Error saving profile: {str(e)}")
            return False
    
    @staticmethod
    def load_profile() -> Optional[Dict]:
        """Load user profile from session state"""
        return st.session_state.get('profile')
    
    @staticmethod
    def clear_profile() -> bool:
        """Clear user profile"""
        try:
            if 'profile' in st.session_state:
                del st.session_state.profile
            return True
        except Exception as e:
            st.error(f"Error clearing profile: {str(e)}")
            return False
    
    @staticmethod
    def get_github_labels(profile: Dict) -> list:
        """Generate appropriate GitHub search labels based on profile"""
        
        labels = ['hacktoberfest']
        experience = profile.get('experience_level', 'beginner')
        
        if experience == 'beginner':
            labels.extend(['good first issue', 'beginner-friendly', 'easy'])
        elif experience == 'intermediate':
            labels.extend(['help wanted', 'enhancement'])
        else:  # advanced
            labels.extend(['help wanted', 'feature', 'enhancement'])
        
        return labels
    
    @staticmethod
    def validate_profile(profile: Dict) -> tuple:
        """Validate profile data"""
        
        errors = []
        
        if not profile.get('experience_level'):
            errors.append('Experience level is required')
        
        if not profile.get('skills') or len(profile['skills']) == 0:
            errors.append('At least one skill is required')
        
        if not profile.get('interests') or len(profile['interests']) == 0:
            errors.append('At least one interest is required')
        
        return len(errors) == 0, errors
