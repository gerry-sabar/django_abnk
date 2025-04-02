from django.test import TestCase
from .singpass import SingpassSerializer


class SingpassSerializerTest(TestCase):

    def setUp(self):
        self.valid_data = {
            'auth_code': 'test_code',
            'auth_state': 'test_state',
        }

    def test_valid_serialization(self):
        serializer = SingpassSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, self.valid_data)
        self.assertEqual(serializer.data, self.valid_data)

    def test_empty_input(self):
        serializer = SingpassSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertIn('auth_code', serializer.errors)
        self.assertIn('auth_state', serializer.errors)        

    def test_ignore_extra_fields(self):
        data = {
            'auth_code': 'test_code',
            'auth_state': 'test_state',
            'custom_field': 'test123',
        }
        serializer = SingpassSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertNotIn('extra_field', serializer.validated_data)
        self.assertNotIn('extra_field', serializer.data)
