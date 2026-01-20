import json
import os
import re

def slugify(text):
    return re.sub(r'[^a-zA-Z0-9]', '_', text.lower()).strip('_')

def migrate(monolith_path):
    print(f"Migrating {monolith_path}...")
    with open(monolith_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    project_name = data.get('projectInfo', {}).get('name', 'Unknown Project')
    project_slug = slugify(project_name)
    base_dir = f"data/projects/{project_slug}"
    os.makedirs(base_dir, exist_ok=True)

    index_data = {
        "projectInfo": data.get('projectInfo', {}),
        "modules": []
    }

    for mod in data.get('modules', []):
        mod_id = mod['id']
        os.makedirs(f"{base_dir}/module_{mod_id}", exist_ok=True)
        
        # Create a stub that includes everything EXCEPT phases
        mod_stub = {k: v for k, v in mod.items() if k != 'phases'}
        mod_stub['phases'] = []
        
        for phase in mod.get('phases', []):
            phase_id = phase['id']
            phase_filename = f"module_{mod_id}/phase_{phase_id}.json"
            phase_path = f"{base_dir}/{phase_filename}"
            
            # Save phase file
            with open(phase_path, 'w', encoding='utf-8') as pf:
                json.dump(phase, pf, indent=2, ensure_ascii=False)
            
            # Add reference to index
            mod_stub['phases'].append(phase_filename)
        
        index_data['modules'].append(mod_stub)

    # Save index.json
    with open(f"{base_dir}/index.json", 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)

    print(f"Migration completed! New project structure in: {base_dir}")
    return f"{base_dir}/index.json"

if __name__ == "__main__":
    monolith = "data/cryptobot_model.json"
    if os.path.exists(monolith):
        new_index = migrate(monolith)
        # Update config to point to the new index
        config_path = "config.json"
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            config['active_project'] = new_index
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            print("Updated config.json to point to the new modular index.")
