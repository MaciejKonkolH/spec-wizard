import json
import sys
import os

def validate_spec(file_path):
    print(f"Validating: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"ERROR: File not found: {file_path}")
        return False

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON syntax: {e}")
        return False
    except Exception as e:
        print(f"ERROR: Failed to read file: {e}")
        return False

    # 1. Check Top-Level Structure
    required_top = ['projectInfo', 'modules']
    for key in required_top:
        if key not in data:
            print(f"ERROR: Missing top-level key: '{key}'")
            return False

    # 2. Check projectInfo
    info = data['projectInfo']
    if not isinstance(info, dict) or 'name' not in info:
        print("ERROR: 'projectInfo' must be an object and contains at least 'name'")
        return False

    # 3. Check Modules
    if not isinstance(data['modules'], list):
        print("ERROR: 'modules' must be a list")
        return False

    for m_idx, module in enumerate(data['modules']):
        m_path = f"modules[{m_idx}]"
        if 'id' not in module or 'name' not in module or 'phases' not in module:
            print(f"ERROR: Module at {m_path} missing required keys (id, name, phases)")
            return False

        # 4. Check Phases
        if not isinstance(module['phases'], list):
            print(f"ERROR: {m_path}.phases must be a list")
            return False

        for p_idx, phase in enumerate(module['phases']):
            p_path = f"{m_path}.phases[{p_idx}]"
            required_phase = ['id', 'name', 'status', 'questions']
            for key in required_phase:
                if key not in phase:
                    print(f"ERROR: Phase at {p_path} missing key: '{key}'")
                    return False

            # 5. Check Questions
            if not isinstance(phase['questions'], list):
                print(f"ERROR: {p_path}.questions must be a list")
                return False

            for q_idx, q in enumerate(phase['questions']):
                q_path = f"{p_path}.questions[{q_idx}] (ID: {q.get('id', 'N/A')})"
                required_q = ['id', 'text', 'type', 'userResponse']
                for key in required_q:
                    if key not in q:
                        print(f"ERROR: Question at {q_path} missing key: '{key}'")
                        return False

                # 6. Check Options for choice types
                if q['type'] in ['single_choice', 'multi_choice']:
                    if 'options' not in q or not isinstance(q['options'], list):
                        print(f"ERROR: Question at {q_path} is choice-type but missing 'options' list")
                        return False
                    
                    for o_idx, opt in enumerate(q['options']):
                        if isinstance(opt, dict):
                            if 'id' not in opt or 'label' not in opt:
                                print(f"ERROR: Option at {q_path}.options[{o_idx}] missing id/label")
                                return False

                # 7. Check userResponse structure
                ur = q['userResponse']
                if not isinstance(ur, dict):
                    print(f"ERROR: {q_path}.userResponse must be an object")
                    return False
                
                if 'selected' not in ur:
                    print(f"ERROR: {q_path}.userResponse missing 'selected' field")
                    return False

    print("SUCCESS: Specification format is valid.")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_spec.py <path_to_spec.json>")
        sys.exit(1)
    
    success = validate_spec(sys.argv[1])
    sys.exit(0 if success else 1)
