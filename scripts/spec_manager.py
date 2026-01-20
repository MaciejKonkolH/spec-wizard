import json
import os
import argparse
import sys
import shutil

class SpecManager:
    def __init__(self, index_path):
        self.index_path = index_path
        self.base_dir = os.path.dirname(index_path)
        self.load_index()

    def load_index(self):
        with open(self.index_path, 'r', encoding='utf-8') as f:
            self.index = json.load(f)

    def save_index(self):
        with open(self.index_path, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, indent=2, ensure_ascii=False)

    def get_phase_path(self, phase_ref):
        return os.path.join(self.base_dir, phase_ref)

    # --- Module Management ---

    def add_module(self, module_id, name, description=""):
        if any(m['id'] == module_id for m in self.index['modules']):
            print(f"Error: Module {module_id} already exists.")
            return
        
        module_dir = f"module_{module_id}"
        os.makedirs(os.path.join(self.base_dir, module_dir), exist_ok=True)
        
        new_module = {
            "id": module_id,
            "name": name,
            "description": description,
            "phases": []
        }
        self.index['modules'].append(new_module)
        self.save_index()
        print(f"Module {module_id} added and folder created.")

    def remove_module(self, module_id, delete_files=False):
        module = next((m for m in self.index['modules'] if m['id'] == module_id), None)
        if not module:
            print(f"Error: Module {module_id} not found.")
            return

        if delete_files:
            module_dir = os.path.join(self.base_dir, f"module_{module_id}")
            if os.path.exists(module_dir):
                shutil.rmtree(module_dir)
                print(f"Directory {module_dir} deleted.")

        self.index['modules'] = [m for m in self.index['modules'] if m['id'] != module_id]
        self.save_index()
        print(f"Module {module_id} removed from index.")

    def rename_module(self, module_id, new_name=None, new_description=None):
        module = next((m for m in self.index['modules'] if m['id'] == module_id), None)
        if not module:
            print(f"Error: Module {module_id} not found.")
            return
        if new_name:
            module['name'] = new_name
        if new_description:
            module['description'] = new_description
        self.save_index()
        print(f"Module {module_id} updated.")

    # --- Phase Management ---

    def add_phase(self, module_id, phase_id, name, status="active", summary=""):
        module = next((m for m in self.index['modules'] if m['id'] == module_id), None)
        if not module:
            print(f"Error: Module {module_id} not found.")
            return

        phase_filename = f"module_{module_id}/phase_{phase_id}.json"
        full_path = self.get_phase_path(phase_filename)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        phase_data = {
            "id": phase_id,
            "name": name,
            "status": status,
            "contextSummary": summary,
            "questions": []
        }

        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(phase_data, f, indent=2, ensure_ascii=False)

        if phase_filename not in module['phases']:
            module['phases'].append(phase_filename)
            self.save_index()
            print(f"Phase {phase_id} added and linked.")
        else:
            print(f"Phase {phase_id} file updated.")

    def update_phase_status(self, phase_id, status, summary=None):
        found = False
        for mod in self.index['modules']:
            for phase_ref in mod['phases']:
                if f"phase_{phase_id}.json" in phase_ref:
                    path = self.get_phase_path(phase_ref)
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    data['status'] = status
                    if summary:
                        data['contextSummary'] = summary
                    with open(path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    print(f"Phase {phase_id} updated to {status}.")
                    found = True
        if not found:
            print(f"Error: Phase {phase_id} not found.")

    def remove_phase(self, phase_id, delete_file=False):
        found = False
        for mod in self.index['modules']:
            new_phases = []
            for phase_ref in mod['phases']:
                if f"phase_{phase_id}.json" in phase_ref:
                    if delete_file:
                        path = self.get_phase_path(phase_ref)
                        if os.path.exists(path):
                            os.remove(path)
                            print(f"File {path} deleted.")
                    found = True
                else:
                    new_phases.append(phase_ref)
            mod['phases'] = new_phases
        
        if found:
            self.save_index()
            print(f"Phase {phase_id} unlinked from index.")
        else:
            print(f"Error: Phase {phase_id} not found.")

    def merge_phases(self, module_id, source_ids, target_id, new_name, new_summary, delete_sources=False):
        module = next((m for m in self.index['modules'] if m['id'] == module_id), None)
        if not module:
            print(f"Error: Module {module_id} not found.")
            return

        all_questions = []
        source_paths = []
        
        for pid in source_ids:
            path = self._find_phase(pid)
            if path and os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    p_data = json.load(f)
                    all_questions.extend(p_data.get('questions', []))
                source_paths.append(path)
            else:
                print(f"Warning: Phase {pid} not found. Skipping.")

        # Create/Update target phase
        target_path = self._find_phase(target_id)
        if not target_path:
            # Create new if target doesn't exist
            target_filename = f"module_{module_id}/phase_{target_id}.json"
            target_path = self.get_phase_path(target_filename)
        
        target_data = {
            "id": target_id,
            "name": new_name,
            "status": "active",
            "contextSummary": new_summary,
            "questions": all_questions
        }

        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with open(target_path, 'w', encoding='utf-8') as f:
            json.dump(target_data, f, indent=2, ensure_ascii=False)

        # Update index
        new_refs = []
        target_ref = f"module_{module_id}/phase_{target_id}.json"
        
        added_target = False
        for ref in module['phases']:
            is_source = any(f"phase_{sid}.json" in ref for sid in source_ids)
            is_target = f"phase_{target_id}.json" in ref
            
            if is_target:
                new_refs.append(ref)
                added_target = True
            elif not is_source:
                new_refs.append(ref)
        
        if not added_target:
            new_refs.append(target_ref)
        
        module['phases'] = new_refs
        self.save_index()

        if delete_sources:
            for sp in source_paths:
                if sp != target_path and os.path.exists(sp):
                    os.remove(sp)
                    print(f"Deleted source phase file: {sp}")

        print(f"Merged phases {source_ids} into phase {target_id} in module {module_id}.")

    def reorder_phases(self, module_id, order_list):
        module = next((m for m in self.index['modules'] if m['id'] == module_id), None)
        if not module:
            print(f"Error: Module {module_id} not found.")
            return
        
        new_phases = []
        for pid in order_list:
            match = next((ref for ref in module['phases'] if f"phase_{pid}.json" in ref), None)
            if match:
                new_phases.append(match)
            else:
                print(f"Warning: Phase ID {pid} not found in module {module_id}. Skipping.")
        
        module['phases'] = new_phases
        self.save_index()
        print(f"Phases reordered in module {module_id}.")

    # --- Question Management ---

    def _find_phase(self, phase_id):
        for mod in self.index['modules']:
            for phase_ref in mod['phases']:
                if f"phase_{phase_id}.json" in phase_ref:
                    return self.get_phase_path(phase_ref)
        return None

    def add_question(self, phase_id, q_data):
        path = self._find_phase(phase_id)
        if not path:
            print(f"Error: Phase {phase_id} not found.")
            return

        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'userResponse' not in q_data:
            q_data['userResponse'] = {"selected": [], "customText": "", "comment": ""}
        
        data['questions'].append(q_data)
        
        # Auto-revert status if question added
        if data.get('status') == 'completed':
            data['status'] = 'active'
            print(f"Phase {phase_id} status auto-reverted to 'active' due to new question.")

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Question {q_data.get('id')} added to phase {phase_id}.")

    def update_question(self, phase_id, q_id, q_update):
        path = self._find_phase(phase_id)
        if not path:
            print(f"Error: Phase {phase_id} not found.")
            return

        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        found = False
        for i, q in enumerate(data['questions']):
            if q['id'] == q_id:
                data['questions'][i].update(q_update)
                found = True
                break
        
        if found:
            # If we update a question and it becomes unanswered, might want to revert status
            # For now, let's just ensure if user adds new options or clears response, 
            # we consider it active. Simple rule: any update to a COMPLETED phase 
            # triggers a warning or reversion.
            if data.get('status') == 'completed':
                data['status'] = 'active'
                print(f"Phase {phase_id} status auto-reverted to 'active' due to update.")

            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Question {q_id} updated.")
        else:
            print(f"Error: Question {q_id} not found.")

    def remove_question(self, phase_id, q_id):
        path = self._find_phase(phase_id)
        if not path:
            print(f"Error: Phase {phase_id} not found.")
            return

        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        orig_len = len(data['questions'])
        data['questions'] = [q for q in data['questions'] if q['id'] != q_id]
        
        if len(data['questions']) < orig_len:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Question {q_id} removed.")
        else:
            print(f"Error: Question {q_id} not found.")

    def move_question(self, from_phase_id, to_phase_id, q_id):
        from_path = self._find_phase(from_phase_id)
        to_path = self._find_phase(to_phase_id)
        if not from_path or not to_path:
            print(f"Error: One of the phases ({from_phase_id} -> {to_phase_id}) not found.")
            return

        # Get question
        with open(from_path, 'r', encoding='utf-8') as f:
            from_data = json.load(f)
        
        q_to_move = next((q for q in from_data['questions'] if q['id'] == q_id), None)
        if not q_to_move:
            print(f"Error: Question {q_id} not found in phase {from_phase_id}.")
            return
        
        # Remove from source
        from_data['questions'] = [q for q in from_data['questions'] if q['id'] != q_id]
        
        # Add to dest
        with open(to_path, 'r', encoding='utf-8') as f:
            to_data = json.load(f)
        to_data['questions'].append(q_to_move)

        # Save both
        with open(from_path, 'w', encoding='utf-8') as f:
            json.dump(from_data, f, indent=2, ensure_ascii=False)
        with open(to_path, 'w', encoding='utf-8') as f:
            json.dump(to_data, f, indent=2, ensure_ascii=False)
        print(f"Question {q_id} moved from {from_phase_id} to {to_phase_id}.")

    def reorder_questions(self, phase_id, order_list):
        path = self._find_phase(phase_id)
        if not path:
            print(f"Error: Phase {phase_id} not found.")
            return

        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        new_qs = []
        for qid in order_list:
            match = next((q for q in data['questions'] if q['id'] == qid), None)
            if match:
                new_qs.append(match)
            else:
                print(f"Warning: Question ID {qid} not found. Skipping.")
        
        # Add any missing questions at the end? (Safety)
        existing_ids = [q['id'] for q in new_qs]
        for q in data['questions']:
            if q['id'] not in existing_ids:
                new_qs.append(q)

        data['questions'] = new_qs
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Questions in phase {phase_id} reordered.")

    # --- Diagnostics ---

    def validate(self):
        print("=== Validation Report ===")
        errors = 0
        all_q_ids = set()
        
        for mod in self.index['modules']:
            print(f"Module: {mod['id']} ({mod['name']})")
            for ref in mod['phases']:
                path = self.get_phase_path(ref)
                if not os.path.exists(path):
                    print(f"  [ERROR] Phase file missing: {ref}")
                    errors += 1
                    continue
                
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        p_data = json.load(f)
                    print(f"  Phase {p_data.get('id')}: {p_data.get('name')} ({len(p_data.get('questions', []))} qs)")
                    for q in p_data.get('questions', []):
                        if q['id'] in all_q_ids:
                            print(f"    [WARNING] Duplicate Question ID found: {q['id']}")
                        all_q_ids.add(q['id'])
                except Exception as e:
                    print(f"  [ERROR] JSON Error in {ref}: {e}")
                    errors += 1
        
        if errors == 0:
            print("SUCCESS: Structure is valid.")
        else:
            print(f"FINISHED: Found {errors} errors.")

    def summary(self):
        print(f"Project: {self.index['projectInfo']['name']} v{self.index['projectInfo']['version']}")
        print("-" * 50)
        for mod in self.index['modules']:
            done = 0
            total = len(mod['phases'])
            print(f"[{mod['id']}] {mod['name']}")
            if mod.get('description'):
                print(f"    Desc: {mod['description']}")
            for ref in mod['phases']:
                path = self.get_phase_path(ref)
                if os.path.exists(path):
                    with open(path, 'r', encoding='utf-8') as f:
                        p = json.load(f)
                        status_char = "✅" if p['status'] == 'completed' else "▶️" 
                        print(f"    {status_char} Phase {p['id']}: {p['name']} ({len(p['questions'])} questions)")
        print("-" * 50)

def main():
    parser = argparse.ArgumentParser(description="Spec Wizard Manager CLI - Advanced Project Guardian")
    parser.add_argument("--index", help="Path to index.json", required=True)
    subparsers = parser.add_subparsers(dest="command")

    # Module Commands
    m_add = subparsers.add_parser("add-module", help="Create new module and folder")
    m_add.add_argument("--id", required=True)
    m_add.add_argument("--name", required=True)
    m_add.add_argument("--description", default="")

    m_rem = subparsers.add_parser("remove-module", help="Remove module from index")
    m_rem.add_argument("--id", required=True)
    m_rem.add_argument("--delete-files", action="store_true", help="Physically delete module folder!")

    m_upd = subparsers.add_parser("update-module", help="Update module info")
    m_upd.add_argument("--id", required=True)
    m_upd.add_argument("--name")
    m_upd.add_argument("--description")

    # Phase Commands
    p_add = subparsers.add_parser("add-phase", help="Add new phase to module")
    p_add.add_argument("--module", required=True)
    p_add.add_argument("--id", type=int, required=True)
    p_add.add_argument("--name", required=True)
    p_add.add_argument("--summary", default="")

    p_upd = subparsers.add_parser("update-phase", help="Update phase status/summary")
    p_upd.add_argument("--id", type=int, required=True)
    p_upd.add_argument("--status", choices=["active", "completed", "locked"])
    p_upd.add_argument("--summary")

    p_rem = subparsers.add_parser("remove-phase", help="Unlink phase from module")
    p_rem.add_argument("--id", type=int, required=True)
    p_rem.add_argument("--delete-file", action="store_true")

    p_ord = subparsers.add_parser("reorder-phases", help="Change phases order in module")
    p_ord.add_argument("--module", required=True)
    p_ord.add_argument("--order", nargs="+", type=int, help="List of Phase IDs in new order", required=True)

    p_mrg = subparsers.add_parser("merge-phases", help="Merge multiple phases into one")
    p_mrg.add_argument("--module", required=True)
    p_mrg.add_argument("--sources", nargs="+", type=int, required=True, help="IDs of phases to merge")
    p_mrg.add_argument("--target", type=int, required=True, help="ID of the resulting phase")
    p_mrg.add_argument("--name", required=True, help="New phase name")
    p_mrg.add_argument("--summary", required=True, help="New phase summary")
    p_mrg.add_argument("--delete-sources", action="store_true")

    # Question Commands
    q_add = subparsers.add_parser("add-question", help="Add question")
    q_add.add_argument("--phase", type=int, required=True)
    q_add.add_argument("--q-id", help="Question ID (replaces 'id' in JSON)")
    q_add.add_argument("--text", help="Question text")
    q_add.add_argument("--type", choices=["single_choice", "multi_choice", "text", "number"], default="single_choice")
    q_add.add_argument("--desc", help="Description")
    q_add.add_argument("--option", action="append", help="Option in format 'id:label' or 'id:label:description' (can be used multiple times)")
    q_add.add_argument("--rec-id", help="Recommended option ID")
    q_add.add_argument("--rec-reason", help="Recommendation reason")
    q_add.add_argument('--file', help="Path to JSON file (legacy/complex)")
    q_add.add_argument('--json', help="Question data as JSON string (legacy/complex)")

    q_upd = subparsers.add_parser("update-question", help="Update question")
    q_upd.add_argument("--phase", type=int, required=True)
    q_upd.add_argument("--id", required=True)
    q_upd.add_argument("--text", help="Update question text")
    q_upd.add_argument("--type", choices=["single_choice", "multi_choice", "text", "number"])
    q_upd.add_argument("--desc", help="Update description")
    q_upd.add_argument("--option", action="append", help="Replace options: 'id:label' or 'id:label:description'")
    q_upd.add_argument("--rec-id", help="Update recommended option ID")
    q_upd.add_argument("--rec-reason", help="Update recommendation reason")
    q_upd.add_argument('--file', help="Path to JSON file with update data")
    q_upd.add_argument('--json', help="Update data as JSON string")

    q_rem = subparsers.add_parser("remove-question", help="Delete question")
    q_rem.add_argument("--phase", type=int, required=True)
    q_rem.add_argument("--id", required=True)

    q_mov = subparsers.add_parser("move-question", help="Move question between phases")
    q_mov.add_argument("--from-phase", type=int, required=True)
    q_mov.add_argument("--to-phase", type=int, required=True)
    q_mov.add_argument("--id", required=True)

    q_ord = subparsers.add_parser("reorder-questions", help="Reorder questions in phase")
    q_ord.add_argument("--phase", type=int, required=True)
    q_ord.add_argument("--order", nargs="+", help="List of Question IDs in new order", required=True)

    # Diagnostic Commands
    subparsers.add_parser("validate", help="Check everything for errors")
    subparsers.add_parser("summary", help="Project overview")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    manager = SpecManager(args.index)

    def parse_options(opt_list):
        if not opt_list: return None
        parsed = []
        for o in opt_list:
            parts = o.split(':', 2)
            opt = {"id": parts[0], "label": parts[1] if len(parts) > 1 else parts[0]}
            if len(parts) > 2:
                opt["description"] = parts[2]
            parsed.append(opt)
        return parsed

    if args.command == "add-module":
        manager.add_module(args.id, args.name, args.description)
    elif args.command == "remove-module":
        manager.remove_module(args.id, args.delete_files)
    elif args.command == "update-module":
        manager.rename_module(args.id, args.name, args.description)
    elif args.command == "add-phase":
        manager.add_phase(args.module, args.id, args.name, summary=args.summary)
    elif args.command == "update-phase":
        manager.update_phase_status(args.id, args.status, args.summary)
    elif args.command == "remove-phase":
        manager.remove_phase(args.id, args.delete_file)
    elif args.command == "reorder-phases":
        manager.reorder_phases(args.module, args.order)
    elif args.command == "merge-phases":
        manager.merge_phases(args.module, args.sources, args.target, args.name, args.summary, args.delete_sources)
    elif args.command == 'add-question':
        q_data = None
        if args.q_id: # Use flags if ID is provided
            q_data = {
                "id": args.q_id,
                "text": args.text or "Placeholder text",
                "type": args.type,
                "description": args.desc or "",
                "options": parse_options(args.option) or []
            }
            if args.rec_id:
                q_data["recommendation"] = {"optionId": args.rec_id, "reason": args.rec_reason or ""}
        elif args.json:
            q_data = json.loads(args.json)
        elif args.file:
            with open(args.file, 'r', encoding='utf-8') as f:
                q_data = json.load(f)
        else:
            q_data = json.load(sys.stdin)
        manager.add_question(args.phase, q_data)
    elif args.command == 'update-question':
        update_data = {}
        if args.text: update_data["text"] = args.text
        if args.type: update_data["type"] = args.type
        if args.desc: update_data["description"] = args.desc
        opts = parse_options(args.option)
        if opts: update_data["options"] = opts
        
        if args.rec_id:
            update_data["recommendation"] = update_data.get("recommendation", {})
            update_data["recommendation"]["optionId"] = args.rec_id
            if args.rec_reason: update_data["recommendation"]["reason"] = args.rec_reason
        elif args.rec_reason:
             update_data["recommendation"] = update_data.get("recommendation", {})
             update_data["recommendation"]["reason"] = args.rec_reason

        if args.json:
            update_data.update(json.loads(args.json))
        elif args.file:
            with open(args.file, 'r', encoding='utf-8') as f:
                update_data.update(json.load(f))
        
        if not update_data and not (args.json or args.file):
            print("Error: No update data provided.")
            return
            
        manager.update_question(args.phase, args.id, update_data)
    elif args.command == "remove-question":
        manager.remove_question(args.phase, args.id)
    elif args.command == "move-question":
        manager.move_question(args.from_phase, args.to_phase, args.id)
    elif args.command == "reorder-questions":
        manager.reorder_questions(args.phase, args.order)
    elif args.command == "validate":
        manager.validate()
    elif args.command == "summary":
        manager.summary()

if __name__ == "__main__":
    # Force UTF-8 for stdin/stdout on Windows
    if sys.platform == "win32":
        import io
        sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    main()
