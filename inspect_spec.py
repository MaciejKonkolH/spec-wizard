import json

try:
    with open('spec_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    print(f"Project Name: {data.get('projectInfo', {}).get('name')}")
    
    modules = data.get('modules', [])
    for m in modules:
        print(f"Module: {m.get('name')}")
        phases = m.get('phases', [])
        for p in phases:
            print(f"  Phase: {p.get('name')} (Status: {p.get('status')})")
            questions = p.get('questions', [])
            answered = 0
            for q in questions:
                resp = q.get('userResponse', {})
                is_answered = bool(resp.get('selected') or resp.get('customText'))
                print(f"    Q: {q.get('text')[:50]}... -> Answered: {is_answered}")
                if is_answered:
                    answered += 1
            print(f"  Progress: {answered}/{len(questions)}")
            
except Exception as e:
    print(f"Error: {e}")
