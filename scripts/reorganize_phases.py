import json
import os

project_path = r'd:\Projects\spec-wizard\data\projects\model_finansowy_cryptobot'
index_path = os.path.join(project_path, 'index.json')

with open(index_path, 'r', encoding='utf-8') as f:
    index = json.load(f)

# Load helper questions
with open(r'd:\Projects\spec-wizard\scripts\new_questions.json', 'r', encoding='utf-8') as f:
    new_qs = json.load(f)

def get_phase_data(path):
    with open(os.path.join(project_path, path), 'r', encoding='utf-8') as f:
        return json.load(f)

def save_phase_data(path, data):
    with open(os.path.join(project_path, path), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# 1. Merge P2 and P3 -> New P2 (Product & UX)
p2 = get_phase_data('module_financial_engine/phase_2.json')
p3 = get_phase_data('module_financial_engine/phase_3.json')
p2['id'] = 2
p2['name'] = "Faza 2: Produkt, Funkcje & UX"
p2['questions'].extend(p3['questions'])
p2['status'] = 'completed'
p2['contextSummary'] = "Zdefiniowano listę funkcji oraz szczegóły interfejsu (UX/UI)."
save_phase_data('module_financial_engine/phase_2.json', p2)

# 2. Merge P4 and P5 -> New P3 (Finances & Growth)
p4 = get_phase_data('module_financial_engine/phase_4.json')
p5 = get_phase_data('module_financial_engine/phase_5.json')
p4['id'] = 3
p4['name'] = "Faza 3: Logika Biznesowa, Dynamika Wzrostu & Dźwignia"
p4['questions'].extend(p5['questions'])
# Add new questions
p4['questions'].append(new_qs['q16c_leverage_logic'])
p4['questions'].append(new_qs['q20b_client_growth'])
p4['questions'].append(new_qs['q20c_capital_injection'])
p4['status'] = 'active' # Revert to active because new questions added
p4['contextSummary'] = "Pobrane parametry tradingu i koszty. Dodano logikę dźwigni oraz wzrostu bazy klientów."
save_phase_data('module_financial_engine/phase_3.json', p4)

# 3. Rename P8 -> New P4 (Scenarios & Risk)
p8 = get_phase_data('module_financial_engine/phase_8.json')
p8['id'] = 4
p8['name'] = "Faza 4: Scenariusze Inwestorskie & Analiza Ryzyka"
save_phase_data('module_financial_engine/phase_4.json', p8)

# 4. Merge P6 and P7 -> New P5 (Architecture & Finalization)
p6 = get_phase_data('module_financial_engine/phase_6.json')
p7 = get_phase_data('module_financial_engine/phase_7.json')
p6['id'] = 5
p6['name'] = "Faza 5: Architektura & Dostarczenie Dokumentacji"
p6['questions'].extend(p7['questions'])
p6['status'] = 'active'
p6['contextSummary'] = "Architektura techniczna połączona z planem wdrożenia i eksportem."
save_phase_data('module_financial_engine/phase_5.json', p6)

# Update index.json
index['modules'][0]['phases'] = [
    "module_financial_engine/phase_1.json",
    "module_financial_engine/phase_2.json",
    "module_financial_engine/phase_3.json",
    "module_financial_engine/phase_4.json",
    "module_financial_engine/phase_5.json"
]

with open(index_path, 'w', encoding='utf-8') as f:
    json.dump(index, f, indent=2, ensure_ascii=False)

# Cleanup old files
files_to_remove = [
    os.path.join(project_path, 'module_financial_engine/phase_6.json'),
    os.path.join(project_path, 'module_financial_engine/phase_7.json'),
    os.path.join(project_path, 'module_financial_engine/phase_8.json')
]
for f in files_to_remove:
    if os.path.exists(f):
        os.remove(f)

print("Reorganization successful.")
