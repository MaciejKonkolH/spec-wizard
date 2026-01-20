# Plan Rozwoju (Roadmap) - AI Spec Wizard

Na podstawie "Analizy Projektu" przygotowano plan działań mający na celu przekształcenie wersji MVP w stabilne, profesjonalne narzędzie inżynierskie.

## Faza 1: Stabilizacja (Hardening)
**Cel**: Eliminacja błędów krytycznych i zabezpieczenie danych przed utratą.

1.  **Implementacja Auto-Backup w `server.py`** [DONE]:
    *   Przed każdym zapisem `spec_data.json` tworzona jest kopia z timestampem.
    *   Chroni przed utratą danych i pozwala na przywrócenie dowolnej wersji historycznej.
2.  **Walidacja JSON (Schema Check)**:
    *   Serwer nie powinien pozwolić na zapisanie pliku, jeśli nie jest poprawnym JSON-em.
    *   Dodatkowo: Sprawdzenie kluczowych pól (czy istnieje `modules`, `phases`).
3.  **Obsługa Błędów Frontend**:
    *   Rozbudowa mechanizmu `window.onerror` w UI o ładny komunikat dla użytkownika ("Wystąpił błąd, odśwież stronę") zamiast "wiszącego" Loading.

## Faza 2: Inteligentny Kontekst (Smart Context)
**Cel**: Rozwiązanie problemu "krótkiej pamięci" Agenta i usprawnienie generowania pytań.

1.  **Rozszerzenie struktury `spec_data.json`**:
    *   Dodanie sekcji `contextSummary` na poziomie projektu i modułu.
    *   Przykład: `contextSummary: { "techStack": ["Python", "PostgreSQL"], "constraints": ["High Availability"] }`.
2.  **Aktualizacja Instrukcji Agenta**:
    *   Wymuszenie aktualizacji `contextSummary` po każdej zakończonej fazie.
    *   Nakaz czytania `contextSummary` przed generowaniem nowych pytań, zamiast parsowania całego JSONa.

## Faza 3: Użyteczność i Eksport (Usability)
**Cel**: Zwiększenie wartości biznesowej narzędzia (output).

1.  **Generator Dokumentacji (`specification.md`)**:
    *   Skrypt (lub funkcja Agenta), który na żądanie zamienia `spec_data.json` w czytelny dokument Markdown z podziałem na rozdziały.
    *   To jest "produkt końcowy" dla klienta.
2.  **Wskaźnik Postępu UI**:
    *   Wizualizacja, na jakim etapie jest użytkownik (Pasek postępu per moduł i globalny).

3.  **Manualna Edycja Schematu ("Safety Hatch")**:
    *   Przycisk "Edytuj Pytanie" w UI, pozwalający użytkownikowi poprawić błąd Agenta (zły tekst, brak opcji). Kluczowe dla frustracji użytkownika.

## Faza 4: Funkcje Zaawansowane (Next-Gen)
**Cel**: Innowacyjność.

1.  **Tryb "Devil's Advocate"**:
    *   Przycisk "Challenge Me" – Agent analizuje odpowiedzi i szuka dziur w logicznym rozumowaniu użytkownika.
2.  **Integracja z Git**:
    *   Automatyczny commit `spec_data.json` po każdej fazie (wersjonowanie decyzji).

3.  **Procedura "Dynamicznej Inicjacji" (Faza 0)**:
    *   Opracowanie mechanizmu "rozruchu" projektu na podstawie pola tekstowego "Wizja Projektu".

---

## Harmonogram Wdrożenia

### Tydzień 1 (Priorytet: Stabilność)
- [x] Auto-Backup w `server.py` (z timestampami)
- [ ] Walidacja JSON przy zapisie (rozszerzona strukturalna)
- [ ] Poprawa Instrukcji (Context Summary - definicja)

### Tydzień 2 (Priorytet: Kontekst & Logika)
- [ ] Aktualizacja schematu danych o `contextSummary`
- [ ] Implementacja "Fazy 0" (Wizja -> Pytania Discovery)
- [ ] Przepisanie Instrukcji Agenta (Procedury "Why-This" i "Gap Analysis")

### Tydzień 3 (Priorytet: Output & Control)
- [ ] Generator raportu PDF/MD
- [ ] Implementacja "Manual Edit Mode" w UI
