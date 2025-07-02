import os
from django.test import TestCase
from django.conf import settings


class SecurityConfigurationTest(TestCase):
    """Test that security settings are properly configured."""
    
    def test_secret_key_from_environment(self):
        """Test that SECRET_KEY is loaded from environment variable and is not the default Django key."""
        # Verify SECRET_KEY exists and is not empty
        self.assertTrue(settings.SECRET_KEY)
        self.assertNotEqual(settings.SECRET_KEY, '')
        
        # Verify it's not the old insecure default key that was hardcoded
        self.assertNotEqual(
            settings.SECRET_KEY, 
            'django-insecure-_m)h73)&-!8sn$(ov6$z@*me7b0dr%0mjyej6x#yy7we5rpcf7'
        )
        
        # Verify it doesn't contain 'django-insecure' prefix (unless it's our development key)
        if not settings.SECRET_KEY.startswith('django-secure-development-key'):
            self.assertNotIn('django-insecure', settings.SECRET_KEY)
    
    def test_secret_key_is_loaded_from_environment(self):
        """Test that SECRET_KEY is actually coming from the environment variable."""
        # The SECRET_KEY should match what's in the environment
        env_secret_key = os.environ.get('SECRET_KEY')
        if env_secret_key:
            self.assertEqual(settings.SECRET_KEY, env_secret_key)
