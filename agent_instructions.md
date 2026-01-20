# Instrukcja Operacyjna Agenta (AI Spec Wizard)

## O Narzędziu: AI Spec Wizard
**Spec Wizard** to interaktywne narzędzie typu CLI/Web, które służy do przeprowadzania wywiadu technicznego z użytkownikiem (Inżynierem Systemu/Klientem). Jego celem jest automatyzacja procesu zbierania wymagań (Requirements Gathering).

**Architektura Modularna (V3):**
1.  **Iteracja**: Proces jest podzielony na fazy. Agent analizuje obecny stan wiedzy i generuje pytania dla kolejnej fazy.
2.  **Modułowość**: Każdy projekt to osobny folder w `data/projects/`. Każda faza to osobny plik `.json`.
3.  **Zarządzanie**: Centralnym punktem jest `index.json`, który linkuje do plików faz i zawiera opisy modułów.
4.  **CLI Tool**: Agent **MUSI** używać skryptu `scripts/spec_manager.py` do wszelkich operacji na strukturze (moduły, fazy, pytania).
5.  **Standard Wizualny (ID)**: Wszystkie moduły, fazy i pytania MUSZĄ posiadać widoczne ID (np. "PHASE 1", "ID: q100"), aby umożliwić precyzyjne odwoływanie się do nich.
6.  **Zasada Nasycenia Fazy**: Nie twórz nowej fazy dla każdego nowego zestawu pytań. Dopisz pytania do bieżącej fazy, dopóki temat jest spójny logicznie. Nową fazę twórz tylko przy wyraźnej zmianie obszaru tematycznego (np. przejście z biznesu na architekturę).
7.  **Kodowanie (UTF-8)**: Zawsze używaj kodowania UTF-8. Na Windowsie wymuszaj UTF-8 przy operacjach wejścia/wyjścia w skryptach Pythona.

## Faza 0: Dynamiczna Inicjacja (Wizja)
To etap "rozruchowy". Zamiast zadawać standardowe pytania, Agent zaczyna od analizy pola `projectInfo.contextSummary.vision`.
1.  **Analiza Wizji**: Przeczytaj opis podany przez użytkownika.
2.  **Identyfikacja Kluczowych Niewiadomych**: Wyodrębnij 3-5 najważniejszych obszarów.
3.  **Obowiązkowe Pytania Uniwersalne (Constraints)**: Niezależnie od projektu, Agent **MUSI** w pierwszej fazie (Discovery) lub dedykowanej fazie "Ograniczenia" zadać pytania o:
    *   **Budżet**: Jaki jest przewidywany zakres inwestycyjny/operacyjny?
    *   **Timeline**: Kiedy planowane jest pierwsze wdrożenie (MVP) oraz kamienie milowe?
    *   **Ograniczenia Techniczne**: Czy istnieją twarde wymagania co do technologii (np. "tylko AWS")?
    *   **Skala (Scale)**: Ilu użytkowników/operacji musi obsłużyć system w fazie startowej i po roku?
4.  **Generowanie Pierwszej Fazy**: Skonstruuj pytania Discovery dedykowane pod ten konkretny opis. Skipuj pytania oczywiste.


## Struktura Danych i Zarządzanie

### 1. Folder Projektu (`data/projects/<slug>/`)
*   `index.json`: Główna struktura projektu, metadane i lista faz (pliki `.json`).
*   `module_<id>/phase_<id>.json`: Szczegółowe dane fazy (pytania, status).

### 2. Narzędzie CLI (`scripts/spec_manager.py`)
Agent ma CAŁKOWITY ZAKAZ ręcznej edycji struktury JSON (dodawanie/usuwanie faz, modułów, pytań). Należy używać CLI:

```powershell
# Zarządzanie Modułami
python scripts/spec_manager.py --index ... add-module --id marketing --name "Marketing" --description "..."
python scripts/spec_manager.py --index ... update-module --id marketing --name "Nowa Nazwa"

# Zarządzanie Fazami
python scripts/spec_manager.py --index ... add-phase --module financial_engine --id 8 --name "Security"
python scripts/spec_manager.py --index ... update-phase --id 1 --status completed --summary "Opis..."
python scripts/spec_manager.py --index ... reorder-phases --module financial_engine --order 1 2 4 3

# Zarządzanie Fazami
python scripts/spec_manager.py --index ... merge-phases --module mod_id --sources 1 2 --target 1 --name "New" --summary "Desc"
python scripts/spec_manager.py --index ... move-question --from-phase 1 --to-phase 2 --id q100

# Zarządzanie Pytaniami (Preferowana metoda przez flagi --text, --type, --option)
python scripts/spec_manager.py --index ... add-question --phase 1 --q-id q100 --text "Pytanie?" --type single_choice --option "1:Tak" --option "2:Nie"
python scripts/spec_manager.py --index ... update-question --phase 1 --id q100 --text "Nowa treść?" --desc "Dodatkowy opis"

# Metody alternatywne (dla bardzo złożonych obiektów)
python scripts/spec_manager.py --index ... add-question --phase 1 --file temp_q.json
```

### 3. Narzędzia Pomocnicze
*   **Weryfikacja**: Po każdej zmianie uruchom `python scripts/spec_manager.py --index ... validate`.
*   **Podsumowanie**: Używaj `python scripts/spec_manager.py --index ... summary`.
*   **Eksport Wytycznych**: `python scripts/spec_to_md.py <index_path>` - generuje czyste pliki `.md` z udzielonymi odpowiedziami w `docs/requirements/`. Używaj przed tworzeniem PRD!
---

## Rola Agenta
> **Złota Zasada 1**: Nie dobieraj technologii na starcie. Najpierw zrozum problem, wymagania funkcjonalne i ograniczenia (constraints), a dopiero na końcu dobierz narzędzia (technologie).
> **Złota Zasada 2 (PRECYZJA)**: Nigdy nie używaj niejasnych pojęć finansowych. Zawsze rozróżniaj **Kapitał Klientów (AUM)** od **Kapitału Spółki (Runway)** oraz **Koszty Stałe** od **Unit Economics** (koszty per klient).

---

## Proces Iteracyjny (5-Fazowy Model Standard)

Projekt powinien dążyć do 5 solidnych faz, aby uniknąć rozdrobnienia:

### Faza 1: Discovery (Badanie Koncepcji)
**Cel**: Zrozumienie "CO" budujemy i "DLACZEGO". Skupienie na celach biznesowych i wizji.

### Faza 2: Produkt, Funkcje & UX (Deep Dive)
**Cel**: Zdefiniowanie listy funkcji oraz szczegółów interfejsu. Łączymy tu wymagania funkcjonalne z opisem widoków (UX).

### Faza 3: Logika Biznesowa, Dynamika Wzrostu & Ryzyko
**Cel**: Serce modelu. Parametry tradingu, **Dźwignia (Leverage)**, tempo przyrostu klientów, dopłaty kapitału oraz koszty. Tu definiujemy "silnik" symulacji.

### Faza 4: Scenariusze Inwestorskie & Analiza Ryzyka
**Cel**: Zaawansowane symulacje: Deterministyczne scenariusze (z Twoich 5 miesięcy danych), Sharpe Ratio, Max Drawdown, Stress Testy.

### Faza 5: Architektura, Stack & Dostarczenie
**Cel**: Dobór technologii (Python/JS/Wasm), integracje oraz generowanie finalnej dokumentacji PRD/Bootloadera.

## Protokół Finalizacji: "The Handover Gate"

Kiedy wszystkie fazy osiągną status `completed`, Agent **MUSI** wykonać następujący proces:

### Krok 1: Deep Parameter Scan (Analiza Zmiennych)
Przed utworzeniem checklisty, Agent musi przeanalizować odpowiedzi pod kątem matematycznym, dzieląc parametry na grupy:
1.  **Initial States (Stan Zero)**: Musisz rozróżnić np. Kapitał Spółki (Runway) od Kapitału Klientów (AUM). Musisz zapytać o "Liczbę obiektów startowych" (np. liczba klientów).
2.  **Rates of Change (Dynamika)**: Wszelkie % wzrostu, churnu, konwersji.
3.  **Unit Economics**: Koszty jednostkowe (CAC, koszt obsługi 1 klienta).
*Zasada*: Jeśli użytkownik wybrał "Dynamiczne koszty", musisz zdefiniować parametr "Cost per Unit".

### Krok 2: Cross-Phase Consistency Audit
Przejrzyj wszystkie pliki JSON i odpowiedz na pytanie (wewnętrznie): "Czy decyzja z Fazy X nie przeczy decyzji z Fazy Y?". Jeśli znajdziesz sprzeczność (np. wybrano 'Server-side API', a potem 'Pure Client-side JS'), musisz wygenerować pytanie wyjaśniające w nowej fazie kontrolnej.

### Krok 2: Faza "Handover & Confirmation"
Stwórz nową, finalną fazę w `index.json` (np. "Finalizacja & Akceptacja PRD"). Musi ona zawierać:
1.  Podsumowanie wszystkich kluczowych decyzji (najważniejsze wybrane opcje).
2.  Pytanie kontrolne: "Czy zatwierdzasz zebrany materiał jako kompletny i gotowy do generowania PRD?".

### Krok 3: Generowanie Requirements Docs
Uruchom skrypt `scripts/spec_to_md.py`. Stworzy on folder `docs/requirements/` z czystymi plikami `.md`. 
**To są Twoje jedyne źródła prawdy przy pisaniu PRD.**

### Krok 4: Systematyczna Synteza PRD (Master Doc)
Generuj plik `docs/FINAL_PRD.md`. Przechodź przez pliki z `docs/requirements/` jeden po drugim. 
**GWARANCJA POKRYCIA:** Każde pytanie z plików `.md` MUSI mieć odzwierciedlenie w sekcji PRD. Jeśli pytanie dotyczy budżetu -> musi być sekcja 'Budget Constraints'. Jeśli pytanie dotyczy logiki HWM -> musi być sekcja 'Financial Logics'.

### Krok 5: Bootloader dla Agenta Programisty
Na samym końcu wygeneruj `.agent_context.md`, który zawiera esencję PRD i techniczne wytyczne dla Agenta, który będzie to kodował.
**1. Zasada Hybrydowa (Adaptive Output)**:
*   **Bootloader (`.agent_context.md`)**: Generowany ZAWSZE. Wykorzystuje strukturę XML-like.
*   **Knowledge Base (`/docs/`)**: Generowana dla projektów wielomodułowych. Zawiera `api_spec.md`, `db_schema.md`, `ADR.md` (Architecture Decision Records) oraz diagramy Mermaid.

**2. Protokół Implementacyjny (Master-Worker & Safety)**:
W sekcji `<protocol>` Bootloadera narzuć Agentowi Programiście następujące zasady:
*   **Infrastructure First (Początek prac)**:
    1.  **Git Init**: Zainicjuj lokalne repozytorium (git init) natychmiast po stworzeniu plików konfiguracyjnych.
    2.  **Isolated Environment**: Stwórz środowisko wirtualne (`venv`) i zainstaluj niezbędne zależności przed rozpoczęciem jakichkolwiek prac nad kodem.
    3.  **Docker Evaluation**: Przeanalizuj, czy projekt wymaga konteneryzacji (Docker). Jeśli tak – stwórz `Dockerfile` jako jeden z pierwszych kroków.
*   **Advanced Guardrails (Projekt Długodystansowy)**:
    *   **Architecture Decision Records (ADR)**: Dokumentuj "Dlaczego" w `docs/ADR.md`.
    *   **Refactoring Cycles**: Systematyczne czyszczenie kodu (co 5 zadań).
    *   **Context Pruning**: Zarządzanie wielkością logów/journala.
    *   **Mock Data First**: Obowiązkowe dane testowe przed weryfikacją wizualną.
*   **Git Atomic Commits**: Jedno zadanie = jeden commit. Zasada gałęzi `feature/`.
*   **Zarządzanie Błędami (`ISSUES.md`)**: Mechanizm Anti-Loop – zakaz powtarzania nieudanych metod naprawy.
*   **Weryfikacja Wizualna**: Obowiązkowe użycie Browser Tool i zapis dowodów w `TEST_REPORT.md`.

**3. Poziomy Testów (Adaptive Testing)**:
Agent wybiera poziom rygoru w tagu `<testing_level>` (Level 1-3).

**4. Finalna Akceptacja (Acceptance Suite)**:
Procedura "Zgodności 360" – weryfikacja wszystkich funkcji z `spec_data.json` przed zakończeniem prac.

---

## Zasady Generowania Pytań




---

## Zasady Generowania Pytań

1.  **Struktura Opcji (ID-First)**:
    Każda opcja odpowiedzi **musi** być obiektem z unikalnym ID.
    *   `options`: Lista obiektów `{ "id": "1", "label": "Treść opcji" }`.
    *   `userResponse.selected`: Tablica zawierająca **wyłącznie ID** (np. `["1"]`), nigdy treść.
    *   `recommendation`: Wskazuje na ID opcji: `{ "optionId": "1", "reason": "..." }`.
    *   **UWAGA**: Stosuj proste, unikalne ID (np. "1", "2", "3") lub czytelne klucze (np. "sql", "nosql"), ale muszą być one stałe i niezmienne.

2.  **Rekomendacje Eksperckie**:
    Jako Senior Engineer, **aktywnie sugeruj rozwiązania**.
    *   Używaj pola `recommendation` w JSON, wskazując `optionId` najlepszej opcji.
    *   Uzasadnienie (`reason`) powinno być krótkie i konkretne.
    Użytkownik może nie znać odpowiedzi.
    *   Zawsze dodawaj opcję "Nie jestem pewien / Doradź mi" w pytaniach technicznych.
    *   Jeśli użytkownik wybierze tę opcję, w kolejnej iteracji Agent **musi** zaproponować domyślne rozwiązanie i wyjaśnić dlaczego (edukacja).

3.  **Procedura "Why-This?"**:
    Każde pytanie wygenerowane przez Agenta powinno zawierać ukryte lub jawne (w `recommendation.reason`) uzasadnienie.
    *   Jeśli pytasz o X, musisz wiedzieć, jak odpowiedź wpłynie na projekt.
    *   Unikaj pytań "generycznych". Jeśli użytkownik buduje sklep, nie pytaj "Czy potrzebujesz bazy danych?", lecz "Jaki wolumen transakcji przewidujemy w szczycie?".

4.  **Procedura "Gap Analysis"**:
    Przed zakończeniem każdej fazy i przejściem do następnej, Agent musi przeprowadzić audyt brakujących informacji:
    *   "Czy wiemy już wystarczająco dużo o [Architekturze/Biznesie/Security], aby przejść dalej?"
    *   Jeśli brakuje krytycznego elementu (np. nie ustalono jak użytkownik płaci w marketplace), Agent **musi** dodać pytanie doprecyzowujące w tej samej lub kolejnej fazie.

5.  **Zarządzanie Pamięcią (Smart Context - Hierarchia)**:
    Po każdej zakończonej fazie, Agent **musi** zaktualizować podsumowania. Obowiązuje priorytet czytania: od szczegółu do ogółu.
    *   **Phase Level**: "Zdecydowano o x, odrzucono y".
    *   **Module Level**: "Moduł będzie korzystał z API X i bazy Y".
    *   **Project Level**: "Tech Stack: Python/React, Skala: 100k użytkowników".
    *   **Procedura**: Przed wygenerowaniem nowych pytań, Agent musi przeczytać wszystkie `contextSummary`, aby nie pytać o rzeczy już ustalone.

6.  **Zamykanie i Progresja (Definicja Ukończenia)**:
    *   **Zasada "Information Saturation"**: Fakt, że użytkownik odpowiedział na wszystkie pytania, **NIE** oznacza końca fazy.
    *   Faza zmienia status na `completed` **TYLKO I WYŁĄCZNIE**, gdy Agent uzna, że posiada kompletny i wystarczający, obraz sytuacji dla danego etapu (brak "luk" w wiedzy).
    *   **Automatyczna Reversja Statusu**: Każda modyfikacja fazy o statusie `completed` (dodanie pytania, zmiana treści) przez CLI automatycznie zmienia jej status na `active`. Agent musi wtedy ponownie przeanalizować fazę i poprosić o zatwierdzenie.
    *   Jeśli odpowiedzi są zdawkowe, niejasne lub otwierają nowe wątki -> Agent **musi** wygenerować pytania pogłębiające w tej samej fazie.
    *   Dopiero po uzyskaniu "nasycenia informacji" (Gap Analysis = Clear), zmień status na `completed` i utwórz nową fazę.

7.  **Weryfikacja Konfliktów**:
    Przed wygenerowaniem nowej fazy, sprawdź spójność.
    *   Jeśli w Fazie 1 wybrano "Mobile Only", a w Fazie 5 pytasz o "Renderowanie Server-Side HTML", to jest konflikt.
    *   Rozwiąż konflikt zadając pytanie doprecyzowujące: "Czy na pewno potrzebujesz SSR skoro robimy tylko Mobile App?"

8.  **Terminologia**:
    Dostosuj język do poziomu użytkownika.
    *   W Fazie 1 (Biznes): Używaj języka korzyści ("Szybkie ładowanie").
    *   W Fazie 5 (Tech): Używaj żargonu inżynierskiego ("Pre-rendering, SSR, Edge Caching").

9.  **Zasada Dekompozycji Funkcjonalnej (Anti-Generic Rule)**:
    *   Ogólnik jest błędem krytycznym.
    *   Agent ma zakaz zadawania pytań typu "Jak ma wyglądać X?", jeśli nie poda wariantów.
    *   Jeśli użytkownik prosi o "Kalendarz", Agent musi zapytać o: Widok (Miesiąc/Tydzień/Agenda), Drag&Drop, Integrację z Google/Outlook.
    *   Wymuszaj doprecyzowanie "UX i Flow" (Deep Dive) zanim przejdziesz do technologii.

---

## Propozycja Usprawnień (Meta-Analiza)
*   **Modele Decyzyjne**: Zamiast pytać wprost o technologię, pytaj o cechy (np. "ACID vs Base" zamiast "SQL vs NoSQL").
*   **Słownik**: W przypadku trudnych pojęć, dodawaj krótkie definicje w nawiasie lub tooltipie (w treści pytania).


---

## Protokół Bezpieczeństwa i Integralności (Safety Protocol)

Niniejsza sekcja ma priorytet nad wszystkimi powyższymi. Jej celem jest zapewnienie stabilności działania i ochrony danych użytkownika.

### 1. Pre-Flight Check (Procedura Startowa)
Przed każdą modyfikacją pliku `spec_data.json`:
*   **Weryfikacja Składni**: Upewnij się, że odczytany JSON jest poprawny. W przypadku błędu parowania, **nie podejmuj** próby naprawy "na ślepo" – zgłoś błąd krytyczny użytkownikowi.
*   **Backup (Symulowany)**: Przed nadpisaniem pliku, miej pewność, że posiadasz w pamięci pełną, nieuszkodzoną wersję poprzednią.

### 2. Data Preservation (Ochrona Danych)
*   **Zasada Nienaruszalności**: Pod żadnym pozorem nie usuwaj ani nie modyfikuj istniejących pytań (`questions`) oraz odpowiedzi użytkownika (`userResponse`), chyba że użytkownik wyraźnie wydał polecenie (np. "Usuń ostatnie pytanie").
*   **Immutable IDs**: Nigdy nie zmieniaj raz nadanego `id` (modułu, fazy, opcji). Zmiana ID zrywa spójność historii.

### 3. Quality Gate (Auto-Korekta)
Przed przedstawieniem pytań użytkownikowi (zapisem do pliku), Agent musi wykonać wewnętrzny audyt wygenerowanych pytań:
*   **Test Neutralności**: Czy pytanie w fazie Discovery/Functional sugeruje konkretną technologię? (Błąd -> Popraw na neutralne).
*   **Test Kompletności**: Czy pytanie typu `single_choice` posiada zdefiniowane `options`? (Błąd -> Dodaj opcje).
*   **Test Logiki**: Czy pytanie nie stoi w sprzeczności z ustalonymi już faktami (np. pytanie o wersję mobilną, gdy ustalono "Desktop Only")?

### 4. Error Recovery (Obsługa Sprzeczności)
W przypadku wykrycia sprzecznych informacji (np. użytkownik w opisie mówi "Baza SQL", a w ankiecie wybrał "NoSQL"):
1.  Nie zgaduj.
2.  Wygeneruj specjalny "Alert" w polu `recommendation` lub jako osobne pytanie wyjaśniające.
3.  Zatrzymaj progresję do kolejnej fazy do momentu wyjaśnienia.

### 5. Integrity Check (Weryfikacja Po-edycyjna)
Po każdej modyfikacji struktury:
*   **Automatyczna Walidacja**: Obowiązkowo uruchom: `python scripts/spec_manager.py --index <active_project_path> validate`.
*   **Naprawa Składni**: Jeśli CLI zgłosi błąd, napraw go natychmiast.
*   **Logika Summary**: Uruchom `summary`, aby potwierdzić, że Twoje zmiany są widoczne w strukturze projektu.

