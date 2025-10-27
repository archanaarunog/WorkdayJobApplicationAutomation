#!/usr/bin/env python3
"""
Phase 7 Testing Script - Email & File Upload Systems
Comprehensive testing of implemented backend functionality
"""

import requests
import json
import sys
from datetime import datetime

class Phase7Tester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.auth_token = None
        
    def log(self, message, status="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {status}: {message}")
    
    def test_server_health(self):
        """Test if server is running"""
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                self.log("✅ Server is running", "SUCCESS")
                return True
            else:
                self.log(f"❌ Server returned {response.status_code}", "ERROR")
                return False
        except requests.exceptions.RequestException as e:
            self.log(f"❌ Server connection failed: {e}", "ERROR")
            return False
    
    def test_api_documentation(self):
        """Test API documentation endpoints"""
        try:
            # Test OpenAPI spec
            response = self.session.get(f"{self.base_url}/openapi.json")
            if response.status_code == 200:
                openapi_spec = response.json()
                paths = openapi_spec.get("paths", {})
                
                # Count email endpoints
                email_endpoints = [path for path in paths.keys() if "/email" in path]
                file_endpoints = [path for path in paths.keys() if "/file" in path or "/resume" in path]
                
                self.log(f"✅ API Documentation available", "SUCCESS")
                self.log(f"📧 Email endpoints: {len(email_endpoints)}", "INFO")
                self.log(f"📁 File endpoints: {len(file_endpoints)}", "INFO")
                
                return True
            else:
                self.log("❌ API documentation not accessible", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Error accessing API docs: {e}", "ERROR")
            return False
    
    def authenticate_test_user(self):
        """Authenticate with a test user"""
        try:
            # First, try to register a test user
            register_data = {
                "email": "test@example.com",
                "password": "testpassword123",
                "first_name": "Test",
                "last_name": "User",
                "phone": "555-0123"
            }
            
            # Try registration (might fail if user exists)
            register_response = self.session.post(
                f"{self.base_url}/api/users/register",
                json=register_data
            )
            
            # Login attempt
            login_data = {
                "email": "test@example.com",
                "password": "testpassword123"
            }
            
            login_response = self.session.post(
                f"{self.base_url}/api/users/login",
                json=login_data
            )
            
            if login_response.status_code == 200:
                login_result = login_response.json()
                self.auth_token = login_result.get("access_token")
                self.session.headers.update({
                    "Authorization": f"Bearer {self.auth_token}"
                })
                self.log("✅ User authentication successful", "SUCCESS")
                return True
            else:
                self.log(f"❌ Login failed: {login_response.status_code}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Authentication error: {e}", "ERROR")
            return False
    
    def test_email_templates(self):
        """Test email template functionality"""
        try:
            # Get email templates
            response = self.session.get(f"{self.base_url}/api/admin/email-templates")
            
            if response.status_code == 200:
                templates = response.json()
                self.log(f"✅ Email templates loaded: {len(templates)} templates", "SUCCESS")
                
                # Show template names
                for template in templates:
                    self.log(f"  📧 Template: {template.get('name')} - {template.get('display_name')}", "INFO")
                
                return True
            elif response.status_code == 403:
                self.log("⚠️  Email templates require admin access", "WARNING")
                return False
            else:
                self.log(f"❌ Email templates error: {response.status_code}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Email templates test failed: {e}", "ERROR")
            return False
    
    def test_email_preferences(self):
        """Test user email preferences"""
        try:
            # Get user email preferences
            response = self.session.get(f"{self.base_url}/api/user/email-preferences")
            
            if response.status_code == 200:
                preferences = response.json()
                self.log("✅ Email preferences accessible", "SUCCESS")
                self.log(f"  📧 Digest frequency: {preferences.get('digest_frequency')}", "INFO")
                self.log(f"  📧 Job notifications: {preferences.get('job_application_confirmations')}", "INFO")
                return True
            else:
                self.log(f"❌ Email preferences error: {response.status_code}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Email preferences test failed: {e}", "ERROR")
            return False
    
    def test_file_upload_endpoints(self):
        """Test file upload endpoint accessibility"""
        try:
            # Test resume list endpoint
            response = self.session.get(f"{self.base_url}/api/resumes")
            
            if response.status_code == 200:
                resumes = response.json()
                self.log(f"✅ Resume endpoints accessible: {len(resumes)} resumes", "SUCCESS")
                return True
            else:
                self.log(f"❌ Resume endpoints error: {response.status_code}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ File upload endpoints test failed: {e}", "ERROR")
            return False
    
    def test_database_models(self):
        """Test database model integration"""
        try:
            # This tests if models are properly integrated by checking endpoints that query them
            endpoints_to_test = [
                ("/api/user/email-preferences", "Email models"),
                ("/api/resumes", "File upload models"),
            ]
            
            all_passed = True
            for endpoint, model_name in endpoints_to_test:
                response = self.session.get(f"{self.base_url}{endpoint}")
                if response.status_code in [200, 404]:  # 200 = data exists, 404 = no data but model works
                    self.log(f"✅ {model_name} database integration working", "SUCCESS")
                else:
                    self.log(f"❌ {model_name} database integration failed: {response.status_code}", "ERROR")
                    all_passed = False
            
            return all_passed
            
        except Exception as e:
            self.log(f"❌ Database models test failed: {e}", "ERROR")
            return False
    
    def run_comprehensive_test(self):
        """Run all tests"""
        self.log("🚀 Starting Phase 7 Comprehensive Testing", "INFO")
        self.log("=" * 50, "INFO")
        
        test_results = []
        
        # Test 1: Server Health
        test_results.append(("Server Health", self.test_server_health()))
        
        # Test 2: API Documentation
        test_results.append(("API Documentation", self.test_api_documentation()))
        
        # Test 3: Authentication
        test_results.append(("User Authentication", self.authenticate_test_user()))
        
        # Test 4: Email Templates (if authenticated)
        if self.auth_token:
            test_results.append(("Email Templates", self.test_email_templates()))
            test_results.append(("Email Preferences", self.test_email_preferences()))
            test_results.append(("File Upload Endpoints", self.test_file_upload_endpoints()))
            test_results.append(("Database Models", self.test_database_models()))
        
        # Results Summary
        self.log("=" * 50, "INFO")
        self.log("📊 TEST RESULTS SUMMARY", "INFO")
        self.log("=" * 50, "INFO")
        
        passed = 0
        total = len(test_results)
        
        for test_name, result in test_results:
            status = "✅ PASS" if result else "❌ FAIL"
            self.log(f"{status} - {test_name}", "RESULT")
            if result:
                passed += 1
        
        self.log("=" * 50, "INFO")
        self.log(f"TOTAL: {passed}/{total} tests passed ({passed/total*100:.1f}%)", "SUMMARY")
        
        if passed == total:
            self.log("🎉 ALL TESTS PASSED - Phase 7 backend is working perfectly!", "SUCCESS")
        elif passed > total * 0.8:
            self.log("⚠️  Most tests passed - Phase 7 backend is mostly functional", "WARNING")
        else:
            self.log("❌ Several tests failed - Phase 7 backend needs attention", "ERROR")
        
        return passed == total

if __name__ == "__main__":
    tester = Phase7Tester()
    success = tester.run_comprehensive_test()
    sys.exit(0 if success else 1)