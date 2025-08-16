#!/usr/bin/env python3
"""Test database connection endpoint"""

import requests
import json

# Test with HTTP explicitly
base_url = "http://127.0.0.1:5000"

print("Testing Database Connection Endpoint")
print("=" * 50)

# Test 1: Check status
print("\n1. Checking database status...")
try:
    response = requests.get(f"{base_url}/api/database/status")
    print(f"   Status Code: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   Error: {e}")

# Test 2: Test database connection
print("\n2. Testing database connection...")
test_data = {
    "host": "localhost",
    "user": "root",
    "password": "your_password",  # Update this
    "database": "personal_finance_db",
    "port": 3306
}

try:
    response = requests.post(
        f"{base_url}/api/database/test",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"   Status Code: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   Error: {e}")

# Test 3: Connect to database
print("\n3. Connecting to database...")
try:
    response = requests.post(
        f"{base_url}/api/database/connect",
        json=test_data,
        headers={"Content-Type": "application/json"}
    )
    print(f"   Status Code: {response.status_code}")
    if response.status_code == 500:
        print(f"   Error Response: {response.text}")
    else:
        print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "=" * 50)
print("\nIf you see SSL/HTTPS errors, make sure:")
print("1. Frontend is using http://localhost:5000 (not https)")
print("2. No browser extensions are forcing HTTPS")
print("3. Clear browser cache and cookies")