
import os
import sys

# Ensure we can import from ModelChecker package
sys.path.append(os.getcwd())

from ModelChecker.core import extract_api_keys
import requests

def test_logic():
    print("--- Starting Headless Test ---")
    
    # 1. Read cURL.txt
    try:
        with open('cURL.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"Read cURL.txt: {len(content)} bytes")
    except Exception as e:
        print(f"Error reading cURL.txt: {e}")
        return

    # 2. Extract Keys
    keys = extract_api_keys(content)
    print(f"Found {len(keys)} keys: {keys}")
    
    if not keys:
        print("No keys found! Check regex.")
        return

    # 3. Test first key
    api_key = keys[0]
    print(f"Testing key: {api_key[:6]}...")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    try:
        print(f"Sending GET request to {url}...")
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            models = [m['name'] for m in data.get('models', [])]
            print(f"Success! Found {len(models)} models.")
            for m in models[:5]:
                print(f" - {m}")
            if len(models) > 5:
                print(" ...")
        else:
            print(f"Failed: {response.text}")
            
    except Exception as e:
        print(f"Exception during request: {e}")

if __name__ == "__main__":
    test_logic()
