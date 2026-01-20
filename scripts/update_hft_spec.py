import json

def update_spec():
    path = 'd:/Projects/spec-wizard/data/cryptobot_model.json'
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Find modules
    modules = data.get('modules', [])
    if not modules: return
    
    # Financial Model Module
    fm = modules[0]
    phases = fm.get('phases', [])

    # Phase 4: Add q16b
    p4 = next((p for p in phases if p['id'] == 4), None)
    if p4:
        # Check if already exists
        if not any(q['id'] == 'q16b_trading_costs' for q in p4['questions']):
            q16b = {
                "id": "q16b_trading_costs",
                "text": "Jak model powinien uwzględniać koszty handlowe (Egzekucja HFT)?",
                "description": "W tradingu wysokiej częstotliwości prowizje giełdowe i slippage mogą zjeść większość zysku.",
                "type": "single_choice",
                "options": [
                    { "id": "bps_fixed", "label": "Stała stawka w punktach bazowych (bps)", "description": "Odejmujemy np. 5 bps od każdego obrotu jako średni koszt (Fee + Slippage)." },
                    { "id": "exchange_tiers", "label": "Dynamiczne Tiers (zależne od wolumenu)", "description": "Model symuluje spadek prowizji giełdowych wraz ze wzrostem AUM i obrotu." },
                    { "id": "net_yield_only", "label": "Uproszczone (Yield podawany już jako Netto)", "description": "Zakładamy, że yield na dashboardzie to już zysk 'na czysto'." }
                ],
                "recommendation": { "optionId": "exchange_tiers", "reason": "W HFT skala obrotu zmienia rentowność – model powinien pokazywać to jako przewagę skali." },
                "userResponse": { "selected": [], "customText": "", "comment": "" }
            }
            p4['questions'].append(q16b)
            p4['status'] = 'completed'
            p4['contextSummary'] = "Silnik będzie naliczał Success Fee miesięcznie, uwzględniając VAT oraz koszty egzekucji tradingowej."

    # Phase 5: Add q19b
    p5 = next((p for p in phases if p['id'] == 5), None)
    if p5:
        if not any(q['id'] == 'q19b_capacity_cap' for q in p5['questions']):
            # Find index of q19
            idx = next((i for i, q in enumerate(p5['questions']) if q['id'] == 'q19_churn_model'), len(p5['questions'])-1)
            q19b = {
                "id": "q19b_capacity_cap",
                "text": "Czy model powinien symulować spadek rentowności (Alpha Decay) przy wzroście AUM?",
                "description": "W HFT płynność rynku jest ograniczona. Powyżej pewnej kwoty (np. $50M) strategia zaczyna mieć zbyt duży wpływ na rynek i jej zyskowność % spada.",
                "type": "single_choice",
                "options": [
                    { "id": "hard_cap", "label": "Hard Cap (Stały limit kapitału)", "description": "Model przestaje przyjmować nowe środki powyżej np. $20M." },
                    { "id": "linear_decay", "label": "Liniowy spadek Yield wraz ze wzrostem AUM", "description": "Im więcej zarządzamy, tym mniejszy procent zysku wypracowujemy." },
                    { "id": "infinite", "label": "Pomiń (Nieskończona płynność)", "description": "Zakładamy, że rynek jest tak głęboki, że nasza skala nigdy nie wpłynie na zysk." }
                ],
                "recommendation": { "optionId": "linear_decay", "reason": "Realistyczne podejście buduje zaufanie zawodowych inwestorów." },
                "userResponse": { "selected": [], "customText": "", "comment": "" }
            }
            p5['questions'].insert(idx + 1, q19b)
            p5['status'] = 'completed'
            p5['contextSummary'] = "Zdefiniowano parametry startowe i mechanizmy skalowania, w tym limity pojemności strategii (Capacity Limit)."

    # Phase 7: Update q27 and q28
    p7 = next((p for p in phases if p['id'] == 7), None)
    if p7:
        p7['status'] = 'active'
        p7['contextSummary'] = "Określamy sposób agregacji wyników HFT, raportowanie oraz eksport dokumentacji AI-Ready."
        
        # Update q27
        q27 = next((q for q in p7['questions'] if q['id'] == 'q27_realtime_rates'), None)
        if q27:
            q27['id'] = 'q27_hft_aggregation'
            q27['text'] = "Jak model powinien prezentować dane z tysięcy transakcji HFT?"
            q27['description'] = "Finansowy model nie może śledzić każdej sekundy, musi agregować dane w sposób wiarygodny dla rocznego planowania."
            q27['options'] = [
                { "id": "stochastic_monthly", "label": "Agregacja statystyczna (Monthly Distribution)", "description": "Modelujemy średni zysk dzienny i jego odchylenie, agregując do wyniku miesięcznego." },
                { "id": "representative_day", "label": "Symulacja 'Dnia Referencyjnego'", "description": "Pokazujemy szczegółowy przebieg zysku z jednego dnia, resztę roku ekstrapolujemy." },
                { "id": "pure_yield_input", "label": "Czysty yield miesięczny (Uproszczony)", "description": "Ignorujemy mikro-transakcje, skupiamy się na finalnym procencie zwrotu." }
            ]
            q27['recommendation'] = { "optionId": "stochastic_monthly", "reason": "Najlepiej oddaje ryzyko drawdownu przy dużej liczbie transakcji." }
            # Preserve comment but reset selection for user to re-evaluate
            q27['userResponse'] = { "selected": [], "customText": "", "comment": "Zmieniono pytanie na adekwatne do HFT zgodnie z feedbackiem." }

        # Update q28 for AI optimization
        q28 = next((q for q in p7['questions'] if q['id'] == 'q28_spec_delivery'), None)
        if q28:
            q28['options'] = [
                { "id": "markdown_ai", "label": "Markdown Strukturany (zoptymalizowany pod AI)", "description": "Plik .md z wyraźną hierarchią i tabelami dla agentów kochających kod." },
                { "id": "yaml_spec", "label": "Struktura YAML / JSON", "description": "Czyste dane techniczne." },
                { "id": "combined_prd", "label": "Pełny PRD (Markdown + Diagramy Mermaid)", "description": "Kompletna specyfikacja z wizualizacją logiki." }
            ]

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Specification updated successfully via Python.")

if __name__ == '__main__':
    update_spec()
