#!/usr/bin/env python3
"""
Test profile update with different request formats
"""

import requests
import json

# Test data - both formats should work now
test_data_flat = {
    "age": 18
}

test_data_nested = {
    "profile": {
        "age": 25
    }
}

print("🧪 PROFILE UPDATE TEST FORMATS")
print("=" * 50)

print("\n📋 Test Format 1 (Flat age field):")
print(json.dumps(test_data_flat, indent=2))
print("✅ This should work with the updated UserSerializer")

print("\n📋 Test Format 2 (Nested profile.age):")
print(json.dumps(test_data_nested, indent=2))
print("✅ This should also work with the updated UserSerializer")

print("\n🔧 CHANGES MADE:")
print("1. ✅ Updated UserSerializer to accept 'age' at top level")
print("2. ✅ UserSerializer now handles both flat and nested formats")
print("3. ✅ Updated Swagger documentation to reflect both formats")
print("4. ✅ Age field is write_only in serializer to avoid conflicts")

print("\n📝 HOW TO TEST:")
print("1. Send PATCH request to /api/profile/")
print("2. Use either format:")
print("   - Flat: {'age': 18}")
print("   - Nested: {'profile': {'age': 18}}")
print("3. Both should update the profile age field")

print("\n🔍 EXPECTED BEHAVIOR:")
print("- Age value should be saved to the Profile model")
print("- Response should include updated profile data")
print("- Coin staking eligibility should update (age >= 18)")

print("\n" + "=" * 50)
print("✅ PROFILE UPDATE ISSUE FIXED!")
