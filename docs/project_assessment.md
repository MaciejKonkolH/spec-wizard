# Ocena i Analiza Projektu "AI Spec Wizard"

## 1. Ocena Ogólna (Current State Assessment)

Projekt **"Spec Wizard"** w obecnej fazie (MVP) jest funkcjonalnym narzędziem do zbierania wymagań, ale posiada typowe cechy wczesnego prototypu – solidne fundamenty koncepcyjne, ale kruche fundamenty techniczne i operacyjne.

### MOCNE STRONY (Strengths):
*   **Logika ID-First**: Przejście na obiekty `{id, label}` w schemacie JSON to strzał w dziesiątkę. Zapewnia to odporność na zmiany językowe i literówki.
*   **Czysty UI**: Interfejs jest estetyczny, nowoczesny (ciemny motyw) i czytelny dla inżyniera. Brak zbędnych "rozpraszaczy".
*   **Prostota Danych**: Plik `spec_data.json` jest czytelny dla człowieka i maszyny. Łatwo go wersjonować w Git.
*   **Model Hybrydowy**: Koncepcja przełączania między trybem manualnym (Agent) a automatycznym (API) jest bardzo elastyczna.

### SŁABE STRONY (Weaknesses):
*   **Kruchy Backend**: Serwer w Pythonie (`http.server`) jest bardzo prosty. Brakuje mu obsługi błędów (co pokazała awaria z "Loading..."), logowania zdarzeń i zabezpieczeń.
*   **Brak Walidacji**: Aplikacja ufa, że `spec_data.json` jest poprawny. Uszkodzenie pliku (nawet jeden znak) kładzie cały UI.
*   **Rozmyta Instrukcja**: Instrukcje dla Agenta są poprawne, ale brakuje im precyzji w obszarze "kontekstu między-modułowego".

---

## 2. Krytyczna Analiza Instrukcji Agenta (`agent_instructions.md`)

Instrukcja w obecnej formie jest **dobra na start, ale niewystarczająca na skalę**.

### Zidentyfikowane Problemy:
1.  **Brak Definicji "Pamięci Długoterminowej"**:
    *   Instrukcja mówi: *"Agent analizuje obecny stan wiedzy"*, ale nie definiuje **jak** ma to robić. Czy Agent ma czytać wszystkie poprzednie fazy przy każdym nowym pytaniu? Przy dużym projekcie (5 modułów po 10 pytań) Agent zgubi kontekst (context window).
    *   **Ryzyko**: Agent zacznie zadawać pytania sprzeczne z ustaleniami z Modułu 1 w Module 5.

2.  **Niejasny Proces "Backfillu"**:
    *   Zasada "Backtracking" jest wspomniana, ale technicznie trudna do wykonania manualnie. Instrukcja każe *"oflagować pytania jako do regeneracji"*, ale w JSON nie ma pola `flags` ani `status: "dirty"`.
    *   **Ryzyko**: Użytkownik zmieni kluczową decyzję (np. "Mobile" na "Desktop"), a stare pytania o "App Store" zostaną w JSON.

3.  **Brak Standardu "Rekomendacji"**:
    *   Pole `recommendation` jest opcjonalne. W praktyce, Agent powinien mieć **obowiązek** uzasadnienia każdej decyzji architektonicznej.

4.  **Zbyt Ogólna Faza "Techniczna"**:
    *   Faza 4 jest workiem na wszystko. Powinna być rozbita na: "Architektura Danych", "API & Interface", "Security".

5.  **Brak Procedury "Inicjacji" (Dynamic Start)**:
    *   Agent obecnie oczekuje gotowego schematu zamiast go budować. Brakuje mechanizmu "Fazy 0", w której na podstawie krótkiego opisu użytkownika Agent sam decyduje, o co zapytać w Fazie 1.

6.  **Brak Metadanych o Celowości Pytań (Why-This)**:
    *   Agent zadaje pytania, ale nie "tłumaczy się" z nich. Brakuje procedury, która wymusza na Agencie uzasadnienie: "Pytam o X, ponieważ wspomniałeś o Y".

---

## 3. Sugestie i Pomysły na Ulepszenia (Roadmap)

### A. Usprawnienia Natychmiastowe (Quick Wins):
1.  **Schema Validation**: Dodać w `server.py` (lub w Agencie) walidację JSON Schema przed zapisem/odczytem. Nie pozwól zapisać uszkodzonego pliku.
2.  **Auto-Backup**: Serwer powinien robić kopię `spec_data.json.bak` przed każdym nadpisaniem. To uratowałoby nas przed awarią sprzed chwili.
3.  **Wskaźnik Postępu**: Dodać pasek postępu (np. "Faza 1/4" lub "25% Ukończono") w UI.

### B. Rozwój Logiki Agenta (Agent Logic):
1.  **Context Summary (Nowa sekcja w JSON)**:
    *   Wprowadzić pole `projectSummary` w JSON, które jest aktualizowane przez Agenta po każdej fazie.
    *   Zamiast czytać surowe Q&A, Agent czyta skrót: *"Ustalono: Backend w Pythonie, Baza SQL, Ruch wysoki"*. To oszczędza tokeny i poprawia spójność.
2.  **Wykrywanie Konfliktów**:
    *   Dodać krok w instrukcji: *"Przed wygenerowaniem pytań, uruchom procedurę Conflict Check"*. Agent musi explicite napisać: "Nie wykryto sprzeczności z Modułem 1".

### C. Koncepcje Rozwoju (Future Concepts):
1.  **Eksport do PDF/Confluence**:
    *   Specyfikacja w JSON nikogo nie obchodzi biznesowo. Dodanie generatora ładnego dokumentu PDF/Markdown ("Końcowa Specyfikacja") jest kluczowe.
2.  **Tryb "Devil's Advocate"**:
    *   Specjalny tryb, w którym Agent nie zadaje pytań, ale **krytykuje** obecne odpowiedzi użytkownika (np. "Wybrałeś SQL, ale przy tym ruchu bazy relacyjne będą wąskim gardłem. Czy na pewno?").
3.  **Multi-User / WebSocket**:
    *   Współpraca na żywo – Product Owner i Architekt wypełniają ankietę jednocześnie.

4.  **Dynamiczna Inicjacja (Faza 0)**:
    *   Mechanizm, w którym użytkownik podaje 2-3 zdania opisu wizji, a Agent na tej podstawie "sieje" pierwsze pytania Discovery, zamiast używać sztywnych ankiet.

5.  **Procedura "Gap Analysis"**:
    *   Zasada, według której Agent po każdej fazie sprawdza, jakie kluczowe informacje dla danego typu projektu są nadal nieobecne.

6.  **Edytor Schematu ("God Mode")**:
    *   Panel administracyjny (Satefy Hatch) pozwalający użytkownikowi ręcznie poprawić JSON, jeśli AI wygeneruje błędne pytania.

---

## 4. Wnioski Końcowe

Projekt ma potencjał, by stać się standardowym narzędziem startowym w Antigravity. Aby to osiągnąć, musimy przejść z myślenia "plik tekstowy" na myślenie "baza wiedzy". Agent musi stać się strażnikiem spójności tej bazy, a nie tylko generatorem pytań.

**Rekomendacja**: Skupić się teraz na uszczelnieniu **Backendu** (Backup/Walidacja) i doprecyzowaniu **Instrukcji** (Pamięć kontekstu), zanim rozbudujemy UI.
