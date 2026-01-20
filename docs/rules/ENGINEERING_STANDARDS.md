# Engineering Standards: Code & Quality

## 1. Testing Standards
**Philosophy**: "Trust, but Verify". Agent code must be proven to work.

### A. Test Structure
*   **Location**: Mirrors source structure.
    *   Source: `src/auth/login.py`
    *   Test: `tests/auth/test_login.py` (or `src/auth/login.test.ts` for JS/TS)
*   **Frameworks**:
    *   Python: `pytest`
    *   Node/JS: `jest` or `vitest`

### B. The "Green-Gate" Rule
*   Agent **CANNOT** mark a task as complete if tests are failing.
*   If no tests exist for the feature, Agent **MUST** create a minimal reproduction/verification script (`scratchpad.py`) to prove logic works.

### C. Test Quality
*   **Descriptive Names**: `test_should_reject_invalid_email` instead of `test_email`.
*   **Isolation**: Tests should not depend on external live APIs (use Mocks).

## 2. Code Style
*   **Linting**: Follow project's `.editorconfig`, `.flake8` or `.eslintrc`.
*   **Readability**: Prefer clear variable names over short ones (`user_authentication_token` > `uat`).
*   **Comments**: Comment "Why", not "What".

## 3. Git Commit Convention (Semantic)
**Format**: `type(scope): subject`

**Types**:
*   `feat`: New feature
*   `fix`: Bug fix
*   `docs`: Documentation only
*   `style`: Formatting (whitespace, etc)
*   `refactor`: Code change that neither fixes a bug nor adds a feature
*   `test`: Adding missing tests or correcting existing tests
*   `chore`: Build process, aux tools

**Examples**:
*   `feat(auth): implement jwt token generation`
*   `fix(db): resolve connection timeout issue`
*   `docs(readme): update installation steps`

## 4. Git Protocol: The Safe Merge Flow
**Strategy**: Feature Branch Workflow (1 Directory Scope = 1 Branch).

### A. Protocol: Branch Safety Check (MANDATORY PRE-FLIGHT)
Przed jakąkolwiek edycją kodu, Agent **MUSI** wykonać:
1.  **Identity Check**: Uruchom `git status`.
    *   *Verify*: Czy jestem na gałęzi `feature/xxx`?
    *   *Alert*: Jeśli jestem na `main` -> **STOP**. Stwórz nową gałąź.
2.  **Context Check**: Uruchom `ls` (lub `dir`) w katalogu roboczym.
    *   *Verify*: Czy widzę pliki, których się spodziewam?

### B. Protocol: The Clean Merge
Scalanie kodu do `main` odbywa się **tylko** po spełnieniu `[x] DoD`.
1.  **Pre-Merge**:
    *   `pytest` (na gałęzi feature) -> **MUST PASS**.
2.  **Sync**:
    *   `git checkout main`
    *   `git pull` (Pobierz zmiany zdalne).
3.  **Merge**:
    *   `git merge --no-ff feature/name` (Zachowaj grupę commitów).
4.  **Post-Merge Verification**:
    *   `pytest` (na gałęzi main) -> **MUST PASS**.
5.  **Cleanup**:
    *   `git branch -d feature/name` (Tylko jeśli sukces).

### C. Protocol: Conflict & Recovery (Ad-Hoc Handling)
W przypadku wystąpienia konfliktu (`Merge Conflict`) lub błędu infrastruktury:
1.  **Register First**: Nie naprawiaj problemu "po cichu".
    *   Zgodnie z `TASK_MANAGEMENT.md`, dodaj zadanie `- [ ] [ADHOC] Merge Conflict Resolution` do planu.
2.  **Resolve**: Rozwiąż konflikt manualnie (zachowując logikę obu stron).
3.  **Verify**: Uruchom testy (muszą przejść po rozwiązaniu konfliktu).
4.  **Commit**: Użyj typu `fix(merge)` lub `chore(merge)`.

## 5. Workspace Hygiene (Filesystem Rules)
**Rule**: Keep the root clean. No temp files in production zones.

### Designated Zones
1.  `tools/` (or `scripts/`):
    *   Miejsce na **użyteczne** skrypty pomocnicze (np. `setup_db.py`, `generate_mock_data.js`).
    *   Te pliki są wersjonowane (Git).
2.  `scratchpad/`:
    *   Miejsce na **śmieci** (brudnopisy): jednorazowe testy, zrzuty JSON, skrypty debugujące.
    *   To miejsce **MUSI** być ignorowane przez Gita (`.gitignore`).
    *   Agent może tu pisać dowolny bałagan bez konsekwencji.

### Prohibition
*   **ZAKAZ**: Tworzenia plików `test.py`, `temp.txt` w katalogu głównym projektu lub wewnątrz `src/`.

## 6. Code Craftsmanship (Senior Habits)
Wymagane "miękkie" nawyki przy każdej edycji kodu:

1.  **The Boy Scout Rule**:
    *   *"Zostaw kod czystszym niż go zastałeś"*.
    *   Widzisz nieużywany import obok swojej zmiany? Usuń go.
    *   Widzisz literówkę w komentarzu? Popraw ją.
2.  **YAGNI (You Ain't Gonna Need It)**:
    *   Nie pisz kodu "na przyszłość". Implementuj tylko to, co jest w `feature.md`.
    *   Zakaz over-engineeringu (np. tworzenia fabryk dla jednej klasy).
3.  **Docs-Code Parity**:
    *   Zmiana w kodzie = Zmiana w dokumentacji.
    *   Jeśli zmieniasz argumenty funkcji -> Zaktualizuj Docstring.
    *   Jeśli zmieniasz Config -> Zaktualizuj `README.md`.
4.  **Secrets Safety (Zero Trust)**:
    *   **CRITICAL**: Nigdy nie wpisuj haseł/kluczy API do kodu ("hardcoding").
    *   Zawsze używaj zmiennych środowiskowych (`os.getenv`, `.env`).
