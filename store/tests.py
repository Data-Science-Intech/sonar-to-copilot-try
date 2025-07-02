import os
from django.test import TestCase
from django.conf import settings


class SettingsSecurityTestCase(TestCase):
    """Test security-related settings configuration"""

    def test_secret_key_uses_environment_variable(self):
        """Test that SECRET_KEY is loaded from environment variable"""
        # Test that SECRET_KEY is not the old hardcoded value
        old_hardcoded_key = 'django-insecure-_m)h73)&-!8sn$(ov6$z@*me7b0dr%0mjyej6x#yy7we5rpcf7'
        self.assertNotEqual(settings.SECRET_KEY, old_hardcoded_key, 
                           "SECRET_KEY should not use the old hardcoded value")
        
        # Test that SECRET_KEY is configured
        self.assertIsNotNone(settings.SECRET_KEY, "SECRET_KEY should be configured")
        self.assertTrue(len(settings.SECRET_KEY) > 0, "SECRET_KEY should not be empty")

    def test_secret_key_with_custom_environment_variable(self):
        """Test that SECRET_KEY respects DJANGO_SECRET_KEY environment variable"""
        test_key = 'test-secret-key-from-environment'
        
        # Save original value
        original_key = os.environ.get('DJANGO_SECRET_KEY')
        
        try:
            # Set test environment variable
            os.environ['DJANGO_SECRET_KEY'] = test_key
            
            # Reload settings to pick up the new environment variable
            from importlib import reload
            from django.conf import settings as django_settings
            from try_cursor import settings as project_settings
            reload(project_settings)
            
            self.assertEqual(project_settings.SECRET_KEY, test_key, 
                           "SECRET_KEY should use value from DJANGO_SECRET_KEY environment variable")
        finally:
            # Restore original environment
            if original_key is not None:
                os.environ['DJANGO_SECRET_KEY'] = original_key
            elif 'DJANGO_SECRET_KEY' in os.environ:
                del os.environ['DJANGO_SECRET_KEY']
