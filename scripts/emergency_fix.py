import json
import os

path = 'data/cryptobot_model.json'
try:
    with open(path, 'r', encoding='utf-8') as f:
        # We read as much as possible, if it fails as JSON, we trim manually
        content = f.read()

    # Try to find the last valid closure
    # The structure is: { "projectInfo": ..., "modules": [ { "phases": [ ..., { "id": 7, ... } ] } ] }
    # So we need one }, one ], one }, one ], one }
    
    # Actually, let's just use json.loads on a substring if it fails
    # But wait, I can just write the correct content if I have it.
    
    # Let's try to parse it. If it fails, it's probably the extra brackets.
    try:
        data = json.loads(content)
        print("JSON is already valid.")
    except json.JSONDecodeError as e:
        print(f"JSON Error: {e}")
        # The error is likely at the end.
        lines = content.splitlines()
        # My view_file showed 1032 lines. Valid end is at 1028.
        fixed_content = "\n".join(lines[:1028])
        try:
            json.loads(fixed_content)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(fixed_content)
            print("Fixed JSON saved.")
        except json.JSONDecodeError as e2:
            print(f"Failed to fix even after trimming: {e2}")

except Exception as e:
    print(f"Error: {e}")
