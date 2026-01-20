import json
import os
import sys

def spec_to_markdown(index_path):
    base_dir = os.path.dirname(index_path)
    with open(index_path, 'r', encoding='utf-8') as f:
        index = json.load(f)

    project_slug = os.path.basename(base_dir)
    # Output directory: data/projects/<slug>/docs/requirements/
    out_dir = os.path.join(base_dir, 'docs', 'requirements')
    os.makedirs(out_dir, exist_ok=True)

    print(f"Generating requirements documentation for project: {index['projectInfo']['name']}")

    # Create 00_project_info.md
    info = index['projectInfo']
    info_md = []
    info_md.append(f"# Project Info: {info.get('name', 'Unnamed Project')}")
    info_md.append(f"\n**Description:** {info.get('description', 'N/A')}")
    info_md.append(f"\n**Version:** {info.get('version', 'N/A')}")
    
    ctx = info.get('contextSummary', {})
    if isinstance(ctx, dict):
        if 'vision' in ctx:
            info_md.append(f"\n## Vision\n{ctx['vision']}")
        for k, v in ctx.items():
            if k != 'vision':
                info_md.append(f"\n### {k.capitalize()}\n{v}")
    elif ctx:
        info_md.append(f"\n## Context\n{ctx}")

    with open(os.path.join(out_dir, '00_project_info.md'), 'w', encoding='utf-8') as f:
        f.write("\n".join(info_md))
    print("Created: 00_project_info.md")

    total_questions = 0
    covered_questions = 0

    for mod in index['modules']:
        for phase_ref in mod['phases']:
            phase_path = os.path.join(base_dir, phase_ref)
            if not os.path.exists(phase_path):
                print(f"Warning: Phase file {phase_ref} not found.")
                continue

            with open(phase_path, 'r', encoding='utf-8') as f:
                phase = json.load(f)

            phase_id = phase.get('id', 'unknown')
            phase_name = phase.get('name', 'unnamed_phase')
            
            # Sanitize filename
            safe_name = "".join([c if c.isalnum() or c in '._-' else '_' for c in phase_name])
            md_filename = f"phase_{phase_id}_{safe_name}.md"
            md_path = os.path.join(out_dir, md_filename)

            md_content = []
            md_content.append(f"# {phase_name} (ID: {phase_id})")
            md_content.append(f"\n**Status:** {phase.get('status', 'N/A')}")
            md_content.append(f"\n**Context Summary:** {phase.get('contextSummary', 'N/A')}")
            md_content.append("\n---\n")

            has_answers = False
            for q in phase.get('questions', []):
                total_questions += 1
                res = q.get('userResponse', {})
                selected = res.get('selected', [])
                custom = res.get('customText', '')
                comment = res.get('comment', '')

                # We only want questions with ACTUAL answers
                if not selected and not custom and not comment:
                    continue
                
                has_answers = True
                covered_questions += 1
                md_content.append(f"### [ID: {q['id']}] {q['text']}")
                
                if q.get('description'):
                    md_content.append(f"\n*Opis: {q['description']}*")

                if selected:
                    md_content.append("\n**Wybrane opcje:**")
                    for opt_id in selected:
                        # Find label for this ID
                        opt_label = opt_id
                        for o in q.get('options', []):
                            if str(o.get('id')) == str(opt_id):
                                opt_label = o.get('label')
                                break
                        md_content.append(f"- {opt_label} (ID: {opt_id})")

                if custom:
                    md_content.append(f"\n**Odpowiedź własna:**\n> {custom}")

                if comment:
                    md_content.append(f"\n**Komentarz użytkownika:**\n> {comment}")

                md_content.append("\n---")

            if has_answers:
                with open(md_path, 'w', encoding='utf-8') as f:
                    f.write("\n".join(md_content))
                print(f"Created: {md_filename}")
            else:
                print(f"Skipped {phase_name}: No answers found.")

    print(f"\nDone! Coverage: {covered_questions}/{total_questions} questions extracted to {out_dir}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/spec_to_md.py <path_to_index.json>")
    else:
        spec_to_markdown(sys.argv[1])
