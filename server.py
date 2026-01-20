import http.server
import socketserver
import json
import os
import sys
import shutil
import urllib.request
import urllib.error
import threading
import time
from datetime import datetime

PORT = 8000
DATA_DIR = 'data'
CONFIG_FILE = 'config.json'
INSTRUCTIONS_FILE = 'agent_instructions.md'
BACKUP_DIR = 'backups'

# --- LLM Client Implementation (No Dependencies) ---

class LLMClient:
    def __init__(self, config):
        self.provider = config.get('api_provider', 'openai')
        self.api_key = config.get('api_key', '')
        # Use custom model if provided, else defaults
        self.model = config.get('api_model')
        if not self.model:
            self.model = self._get_default_model()
        
    def _get_default_model(self):
        if self.provider == 'openai':
            return 'gpt-4-turbo'
        elif self.provider == 'gemini':
            # Gemini 2.0 Flash Exp (Latest usually available in v1beta)
            return 'gemini-2.0-flash-exp'
        elif self.provider == 'anthropic':
            return 'claude-3-opus-20240229'
        return 'gpt-3.5-turbo'

    def generate_response(self, system_prompt, user_data_json):
        """Generuje odpowiedź JSON na podstawie instrukcji i danych."""
        if not self.api_key:
            raise ValueError("Brak klucza API (API Key missing)")

        if self.provider == 'openai':
            return self._call_openai(system_prompt, user_data_json)
        elif self.provider == 'gemini':
            return self._call_gemini(system_prompt, user_data_json)
        elif self.provider == 'anthropic':
            return self._call_anthropic(system_prompt, user_data_json)
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    def _call_openai(self, sys_msg, user_msg):
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": sys_msg},
                {"role": "user", "content": f"Oto aktualny stan pliku spec_data.json. Wykonaj kolejne kroki zgodnie z instrukcją:\n\n{user_msg}"}
            ],
            "response_format": { "type": "json_object" }
        }
        
        req = urllib.request.Request(url, json.dumps(data).encode('utf-8'), headers)
        try:
            with urllib.request.urlopen(req) as response:
                result = json.load(response)
                content = result['choices'][0]['message']['content']
                return json.loads(content)
        except urllib.error.HTTPError as e:
            err_body = e.read().decode()
            raise Exception(f"OpenAI Error {e.code}: {err_body}")

    def _call_gemini(self, sys_msg, user_msg):
        # Use v1beta for advanced features like system_instruction and response_mime_type
        # v1 is often too restrictive or doesn't have these fields for all models yet.
        api_version = "v1beta" 
        url = f"https://generativelanguage.googleapis.com/{api_version}/models/{self.model}:generateContent?key={self.api_key}"
        headers = { "Content-Type": "application/json" }
        
        data = {
            "system_instruction": {
                "parts": [{ "text": sys_msg }]
            },
            "contents": [{
                "role": "user",
                "parts": [{ "text": f"Oto aktualny stan pliku spec_data.json. Zwróć PEŁNY zaktualizowany JSON:\n\n{user_msg}" }]
            }],
            "generation_config": {
                "response_mime_type": "application/json"
            }
        }
        
        print(f"Gemini Request URL: {url.replace(self.api_key, 'HIDDEN_KEY')}")
        
        req = urllib.request.Request(url, json.dumps(data).encode('utf-8'), headers)
        try:
            with urllib.request.urlopen(req) as response:
                result = json.load(response)
                # Check for candidates
                if 'candidates' not in result or not result['candidates']:
                    raise Exception(f"Gemini Error: No candidates returned. Raw: {result}")
                
                content = result['candidates'][0]['content']['parts'][0]['text']
                
                # Robust JSON cleaning
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()
                
                return json.loads(content)
        except urllib.error.HTTPError as e:
            err_body = e.read().decode()
            raise Exception(f"Gemini Error {e.code}: {err_body}")
        except Exception as e:
            raise Exception(f"Gemini Processing Error: {str(e)}")


    def list_models(self, provider=None):
        """Listuje dostępne modele dla danego dostawcy."""
        p = provider or self.provider
        
        if p == 'gemini':
            # Existing Gemini logic
            url = f"https://generativelanguage.googleapis.com/v1/models?key={self.api_key}"
            try:
                req = urllib.request.Request(url)
                with urllib.request.urlopen(req) as response:
                    return json.load(response)
            except Exception:
                url = f"https://generativelanguage.googleapis.com/v1beta/models?key={self.api_key}"
                req = urllib.request.Request(url)
                with urllib.request.urlopen(req) as response:
                    return json.load(response)
        
        elif p == 'openai':
            # Hardcoded core models as fallback/base
            core_models = [
                {"name": "gpt-4o", "id": "gpt-4o"},
                {"name": "gpt-4-turbo", "id": "gpt-4-turbo"},
                {"name": "gpt-3.5-turbo", "id": "gpt-3.5-turbo"},
                {"name": "o1-preview", "id": "o1-preview"},
                {"name": "o3-mini", "id": "o3-mini"}
            ]
            
            if not self.api_key or not self.api_key.startswith('sk-'):
                return {"models": core_models}

            url = "https://api.openai.com/v1/models"
            headers = { "Authorization": f"Bearer {self.api_key}" }
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req) as response:
                    data = json.load(response)
                    # Merge fetched with core, avoid duplicates
                    fetched = [m for m in data.get('data', []) if m['id'].startswith(('gpt-', 'o1-', 'o3-'))]
                    ids = {m['id'] for m in core_models}
                    for f in fetched:
                        if f['id'] not in ids:
                            core_models.append({"name": f['id'], "id": f['id']})
                    return {"models": core_models}
            except Exception:
                # On 401 or any other error, just return core models
                return {"models": core_models}
        
        elif p == 'anthropic':
            # Anthropic doesn't have a public "list models" without specific perms.
            # Return high-tier standard models.
            return {
                "models": [
                    {"name": "models/claude-3-5-sonnet-20241022", "id": "claude-3-5-sonnet-20241022"},
                    {"name": "models/claude-3-5-haiku-20241022", "id": "claude-3-5-haiku-20241022"},
                    {"name": "models/claude-3-opus-20240229", "id": "claude-3-opus-20240229"}
                ]
            }
            
        return {"models": []}

    def _call_anthropic(self, sys_msg, user_msg):
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01"
        }
        data = {
            "model": self.model,
            "max_tokens": 8192,
            "system": sys_msg,
            "messages": [
                {"role": "user", "content": f"Oto aktualny stan pliku spec_data.json. Wykonaj kolejne kroki zgodnie z instrukcją. Zwróć TYLKO JSON:\n\n{user_msg}"}
            ]
        }
        
        req = urllib.request.Request(url, json.dumps(data).encode('utf-8'), headers)
        try:
            with urllib.request.urlopen(req) as response:
                result = json.load(response)
                content = result['content'][0]['text']
                # Clean possible markdown block
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0].strip()
                return json.loads(content)
        except urllib.error.HTTPError as e:
            err_body = e.read().decode()
            raise Exception(f"Anthropic Error {e.code}: {err_body}")


# --- Server Handler ---

class WizardHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Opcjonalnie: minimalizacja logów konsoli
        sys.stderr.write("%s - - [%s] %s\n" %
                         (self.client_address[0],
                          self.log_date_time_string(),
                          format%args))

    def do_GET(self):
        from urllib.parse import urlparse
        path = urlparse(self.path).path
        
        if path == '/api/data':
            return self._serve_file(self._get_data_file())
        if path == '/api/config':
            return self._serve_file(CONFIG_FILE)
        if path == '/api/models':
            return self._handle_models()
        if path == '/api/projects':
            return self._handle_list_projects()
            
        # Serve static files
        if path == '/' or path == '/index.html':
            self.path = '/public/index.html'
        elif not path.startswith('/public/'):
            if os.path.exists('public' + path):
                self.path = '/public' + path
        
        return super().do_GET()

    def do_POST(self):
        if self.path == '/api/save':
            self._handle_save()
            return
        if self.path == '/api/config':
            self._handle_config()
            return
        if self.path == '/api/generate':
            self._handle_generate()
            return
        if self.path == '/api/projects/select':
            self._handle_select_project()
            return

        self.send_error(404, "Endpoint not found")

    def _get_data_file(self):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
            return config.get('active_project', 'spec_data.json')
        except:
            return 'spec_data.json'

    def _serve_file(self, filename):
        try:
            if not os.path.exists(filename):
                 ensure_files()
            
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # If it's an index.json (modular project), merge phases
            norm_filename = filename.replace('\\', '/').lower()
            if norm_filename.endswith('index.json'):
                base_dir = os.path.dirname(filename)
                for mod in data.get('modules', []):
                    full_phases = []
                    for phase_ref in mod.get('phases', []):
                        phase_path = os.path.join(base_dir, phase_ref)
                        if os.path.exists(phase_path):
                            with open(phase_path, 'r', encoding='utf-8') as pf:
                                full_phases.append(json.load(pf))
                        else:
                            print(f"Warning: Phase file not found: {phase_path}")
                    mod['phases'] = full_phases

            content = json.dumps(data, indent=2, ensure_ascii=False).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            print(f"Serve Error: {e}")
            self.send_error(500, str(e))

    def _handle_models(self):
        try:
            from urllib.parse import urlparse, parse_qs
            query = parse_qs(urlparse(self.path).query)
            provider = query.get('provider', [None])[0]
            provided_key = query.get('key', [None])[0]

            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Use provided data or fall back to config
            if provider:
                config['api_provider'] = provider
            if provided_key:
                config['api_key'] = provided_key

            # We don't raise error anymore, list_models will return fallbacks if key is missing
            client = LLMClient(config)
            models = client.list_models(provider=provider)
            self._send_json(200, models)
        except Exception as e:
            self._send_json(500, {"error": str(e)})

    def _handle_save(self):
        try:
            length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(length).decode('utf-8'))
            
            data_file = self._get_data_file()
            self._backup_file(data_file)
            
            if data_file.endswith('index.json'):
                # Modular save
                base_dir = os.path.dirname(data_file)
                # 1. Update index (metadata, module/phase structure)
                index_to_save = {
                    "projectInfo": data.get("projectInfo", {}),
                    "modules": []
                }
                for mod in data.get('modules', []):
                    mod_stub = {
                        "id": mod['id'],
                        "name": mod['name'],
                        "phases": []
                    }
                    for phase in mod.get('phases', []):
                        # Save individual phase file
                        phase_rel_path = f"module_{mod['id']}/phase_{phase['id']}.json"
                        phase_abs_path = os.path.join(base_dir, phase_rel_path)
                        os.makedirs(os.path.dirname(phase_abs_path), exist_ok=True)
                        
                        self._backup_file(phase_abs_path)
                        with open(phase_abs_path, 'w', encoding='utf-8') as pf:
                            json.dump(phase, pf, indent=2, ensure_ascii=False)
                        
                        mod_stub['phases'].append(phase_rel_path)
                    index_to_save['modules'].append(mod_stub)
                
                with open(data_file, 'w', encoding='utf-8') as f:
                    json.dump(index_to_save, f, indent=2, ensure_ascii=False)
            else:
                # Legacy monolith save
                with open(data_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
            self._send_json(200, {"status": "ok"})
        except Exception as e:
            print(f"Save Error: {e}")
            self._send_json(400, {"status": "error", "message": str(e)})

    def _handle_config(self):
        try:
            length = int(self.headers['Content-Length'])
            new_config = json.loads(self.rfile.read(length).decode('utf-8'))
            
            # Preserve active_project if not provided
            if 'active_project' not in new_config:
                old_data_file = self._get_data_file()
                new_config['active_project'] = old_data_file

            self._backup_file(CONFIG_FILE)
            
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(new_config, f, indent=2)
                
            self._send_json(200, {"status": "ok"})
        except Exception as e:
            self._send_json(400, {"status": "error", "message": str(e)})

    def _handle_generate(self):
        try:
            # 1. Load Config & Verify Mode
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            if not config.get('api_mode') or not config.get('api_key'):
                self._send_json(200, {
                    "status": "agent_mode", 
                    "message": "Manual Mode Active. Please ask the AI Agent to proceed."
                })
                return

            print(f"Generowanie z użyciem API: {config.get('api_provider')}")
            
            # 2. Load Instructions & Data
            if not os.path.exists(INSTRUCTIONS_FILE):
                raise FileNotFoundError("Brak pliku instrukcji (agent_instructions.md)!")
                
            with open(INSTRUCTIONS_FILE, 'r', encoding='utf-8') as f:
                system_prompt = f.read()
            
            data_file = self._get_data_file()
            with open(data_file, 'r', encoding='utf-8') as f:
                current_data = f.read() # Send as string

            # 3. Call LLM
            client = LLMClient(config)
            new_data_json = client.generate_response(system_prompt, current_data)
            
            # 4. Save Result (Main Data)
            self._backup_file(data_file)
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(new_data_json, f, indent=2, ensure_ascii=False)

            # 5. Handle Generated Artifacts (if any)
            # Support for Phase 7 where Agent creates external files (e.g. docs/*.md)
            if 'generated_files' in new_data_json:
                files = new_data_json['generated_files']
                for filename, content in files.items():
                    # Security check: prevent traversing up
                    if ".." in filename or filename.startswith("/") or ":" in filename:
                        print(f"Skipping unsafe filename: {filename}")
                        continue
                    
                    # Create directory if needed
                    file_path = os.path.join(os.getcwd(), filename)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Generated file saved: {filename}")

            self._send_json(200, {
                "status": "simulated", # Keeps frontend logic happy (reloads data)
                "message": "AI generated new phases successfully."
            })

        except Exception as e:
            print(f"Generate Error: {e}")
            self._send_json(500, {"status": "error", "message": str(e)})

    def _handle_list_projects(self):
        try:
            if not os.path.exists(DATA_DIR):
                os.makedirs(DATA_DIR)
            
            projects = []
            
            # Legacy monoliths in data/*.json
            legacy_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.json') and f != 'index.json']
            for f in legacy_files:
                path = os.path.join(DATA_DIR, f)
                try:
                    with open(path, 'r', encoding='utf-8') as pj:
                        d = json.load(pj)
                        projects.append({
                            "id": path,
                            "name": d.get('projectInfo', {}).get('name', f),
                            "description": d.get('projectInfo', {}).get('description', '')
                        })
                except: pass

            # Modular projects in data/projects/*/index.json
            projects_root = os.path.join(DATA_DIR, 'projects')
            if os.path.exists(projects_root):
                for dname in os.listdir(projects_root):
                    idx_path = os.path.join(projects_root, dname, 'index.json')
                    if os.path.exists(idx_path):
                        try:
                            with open(idx_path, 'r', encoding='utf-8') as pj:
                                d = json.load(pj)
                                projects.append({
                                    "id": idx_path,
                                    "name": f"📦 {d.get('projectInfo',{}).get('name', dname)}",
                                    "description": d.get('projectInfo',{}).get('description', 'Modular Project')
                                })
                        except: pass
            
            active = self._get_data_file()
            self._send_json(200, {"projects": projects, "active": active})
        except Exception as e:
            self._send_json(500, {"error": str(e)})

    def _handle_select_project(self):
        try:
            length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(length).decode('utf-8'))
            project_id = data.get('id')
            
            if not project_id or not os.path.exists(project_id):
                raise ValueError("Błędny ID projektu (Invalid project ID)")

            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            config['active_project'] = project_id
            
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            
            self._send_json(200, {"status": "ok", "active": project_id})
        except Exception as e:
            self._send_json(400, {"error": str(e)})

    def _backup_file(self, filename):
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)
        if os.path.exists(filename):
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            # Flatten path separators to avoid "directory not found" in backup dir
            safe_name = filename.replace('/', '_').replace('\\', '_')
            shutil.copy2(filename, os.path.join(BACKUP_DIR, f"{safe_name}_{ts}.bak"))

    def _send_json(self, code, data):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

def ensure_files():
    if not os.path.exists(CONFIG_FILE):
        default_config = {
            "language": "pl",
            "api_mode": False,
            "api_provider": "openai",
            "api_model": "",
            "api_key": ""
        }
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2)

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        
    # Check if there are any projects, if not create one
    if not os.listdir(DATA_DIR):
        default_project = os.path.join(DATA_DIR, 'default_project.json')
        with open(default_project, 'w', encoding='utf-8') as f:
             json.dump({"projectInfo": {"name": "Nowy Projekt", "description": "Opis projektu..."}, "modules": []}, f, indent=2, ensure_ascii=False)

# --- Threading Server Implementation ---
class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True # Wątki są ubijane przy zamknięciu programu

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    if not os.path.exists('public'):
        os.makedirs('public')
    ensure_files()

    # Użycie wielowątkowości zapobiega blokowaniu głównej pętli przez żądania HTTP
    server = ThreadingHTTPServer(("", PORT), WizardHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True # Pozwala zakończyć wątek gdy główny program się kończy
    server_thread.start()

    print(f"Spec Wizard Server (AI Powered with Threading) running at http://localhost:{PORT}")
    print("Naciśnij Ctrl+C, aby zatrzymać serwer.")

    try:
        while True:
            time.sleep(1) # Pętla główna tylko czeka na przerwanie
    except KeyboardInterrupt:
        print("\nZatrzymywanie serwera (Ctrl+C)...")
        server.shutdown()
        server.server_close()
        print("Serwer zatrzymany.")
        sys.exit(0)
