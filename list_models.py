#!/usr/bin/env python3
import os
import requests

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print("Please set GEMINI_API_KEY environment variable")
    exit(1)

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
response = requests.get(url)

if response.status_code == 200:
    models = response.json()
    print("Available models:")
    for model in models.get('models', []):
        name = model.get('name', '')
        display_name = model.get('displayName', '')
        supported_methods = model.get('supportedGenerationMethods', [])
        
        if 'generateContent' in supported_methods:
            print(f"✅ {name} - {display_name}")
        else:
            print(f"❌ {name} - {display_name} (not supported for generateContent)")
else:
    print(f"Error: {response.status_code} - {response.text}")
