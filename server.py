import http.server
import socketserver
import json
import os
import sys

PORT = 8000
DATA_FILE = 'spec_data.json'
CONFIG_FILE = 'config.json'

class WizardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        from urllib.parse import urlparse
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == '/api/data':
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    content = f.read().encode('utf-8')
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Content-Length', len(content))
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                self.send_error(500, str(e))
            return
        
        if path == '/api/config':
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    content = f.read().encode('utf-8')
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Content-Length', len(content))
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                self.send_error(500, str(e))
            return

        # Serve static files
        if path == '/' or path == '/index.html':
            self.path = '/public/index.html'
        elif not path.startswith('/public/'):
             # If it doesn't start with /public/, try to find it there
             if os.path.exists('public' + path):
                 self.path = '/public' + path
             else:
                 self.path = path # Fallback to root or 404

        return super().do_GET()

    def do_POST(self):
        import shutil

        if self.path == '/api/save':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # 1. Validate JSON before doing anything
                data = json.loads(post_data.decode('utf-8'))
                
                # 2. Backup existing file if it exists
                if os.path.exists(DATA_FILE):
                    shutil.copy2(DATA_FILE, DATA_FILE + '.bak')
                    print(f"Backup created: {DATA_FILE}.bak")

                # 3. Save new data
                with open(DATA_FILE, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok", "message": "Data saved and backed up"}).encode('utf-8'))
            except Exception as e:
                print(f"Save error: {e}")
                self.send_response(400) # Bad Request if JSON is invalid
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": f"Invalid data or write error: {str(e)}"}).encode('utf-8'))
            return
        
        if self.path == '/api/config':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                # 1. Validate
                new_config = json.loads(post_data.decode('utf-8'))
                
                # 2. Backup
                if os.path.exists(CONFIG_FILE):
                    shutil.copy2(CONFIG_FILE, CONFIG_FILE + '.bak')

                # 3. Save
                with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                    json.dump(new_config, f, indent=2)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok", "message": "Config updated and backed up"}).encode('utf-8'))
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
            return

        if self.path == '/api/generate':
            # Verification for API Mode would go here
            # For MVP Agent Mode, we just return a message
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Check if API mode is on
            try:
                with open(CONFIG_FILE, 'r') as f:
                    config = json.load(f)
            except:
                config = {}

            if config.get("api_mode") and config.get("api_key"):
                 # TODO: Implement OpenAI Call here in future step
                 self.wfile.write(json.dumps({
                     "status": "simulated", 
                     "message": "API Mode active (Mock). In real version, I would call OpenAI here."
                 }).encode('utf-8'))
            else:
                 self.wfile.write(json.dumps({
                     "status": "agent_mode", 
                     "message": "Data saved. Please ask your AI Agent to review the 'spec_data.json' file now."
                 }).encode('utf-8'))
            return

        self.send_error(404, "Endpoint not found")

if __name__ == '__main__':
    # Ensure public dir exists
    if not os.path.exists('public'):
        os.makedirs('public')
    
    # Change dir to script location to ensure relative paths work
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    with socketserver.TCPServer(("", PORT), WizardHandler) as httpd:
        print(f"Spec Wizard Server running at http://localhost:{PORT}")
        print(f"Data File: {os.path.abspath(DATA_FILE)}")
        print("Press Ctrl+C to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
