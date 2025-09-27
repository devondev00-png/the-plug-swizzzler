import jwt
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from database.models import UserSession, Company
from sqlalchemy.orm import Session
import requests
import os

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.secret_key = os.getenv("SECRET_KEY", "your-secret-key-here")
        self.main_app_auth_url = os.getenv("MAIN_APP_AUTH_URL", "https://your-main-app.com/api/auth")
        self.main_app_api_key = os.getenv("MAIN_APP_API_KEY", "")
    
    def validate_user_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Validate user token with your main app"""
        try:
            # Call your main app's auth endpoint
            headers = {
                "Authorization": f"Bearer {token}",
                "X-API-Key": self.main_app_api_key
            }
            
            response = requests.get(
                f"{self.main_app_auth_url}/validate",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                user_data = response.json()
                return {
                    "user_id": user_data.get("user_id"),
                    "email": user_data.get("email"),
                    "name": user_data.get("name"),
                    "is_active": user_data.get("is_active", True)
                }
            return None
            
        except Exception as e:
            print(f"Auth validation error: {e}")
            return None
    
    def create_session(self, user_id: str, token: str) -> str:
        """Create a session for the user"""
        # Generate session token
        session_token = secrets.token_urlsafe(32)
        
        # Create session record
        session = UserSession(
            user_id=user_id,
            session_token=session_token,
            expires_at=datetime.utcnow() + timedelta(hours=24)
        )
        
        self.db.add(session)
        self.db.commit()
        
        return session_token
    
    def validate_session(self, session_token: str) -> Optional[Dict[str, Any]]:
        """Validate session token"""
        session = self.db.query(UserSession).filter(
            UserSession.session_token == session_token,
            UserSession.is_active == True,
            UserSession.expires_at > datetime.utcnow()
        ).first()
        
        if session:
            return {
                "user_id": session.user_id,
                "session_id": session.id
            }
        return None
    
    def get_user_companies(self, user_id: str) -> list:
        """Get all companies for a user"""
        companies = self.db.query(Company).filter(
            Company.user_id == user_id
        ).all()
        
        return [
            {
                "id": company.id,
                "name": company.name,
                "created_at": company.created_at
            }
            for company in companies
        ]
    
    def create_company_for_user(self, user_id: str, company_name: str) -> Company:
        """Create a company for a user"""
        company = Company(
            name=company_name,
            user_id=user_id
        )
        
        self.db.add(company)
        self.db.commit()
        
        return company
    
    def logout_session(self, session_token: str) -> bool:
        """Logout a session"""
        session = self.db.query(UserSession).filter(
            UserSession.session_token == session_token
        ).first()
        
        if session:
            session.is_active = False
            self.db.commit()
            return True
        return False
    
    def cleanup_expired_sessions(self):
        """Clean up expired sessions"""
        expired_sessions = self.db.query(UserSession).filter(
            UserSession.expires_at < datetime.utcnow()
        ).all()
        
        for session in expired_sessions:
            session.is_active = False
        
        self.db.commit()
        return len(expired_sessions)
