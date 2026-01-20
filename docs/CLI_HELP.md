# Spec Wizard Manager CLI - Manual

Narzędzie `scripts/spec_manager.py` służy do bezpiecznego zarządzania strukturą projektów Spec Wizarda bez konieczności ręcznej edycji plików JSON.

## Podstawowe Użycie
Wszystkie komendy wymagają wskazania pliku `index.json` projektu:
```bash
python scripts/spec_manager.py --index data/projects/model_finansowy_cryptobot/index.json <komenda> [opcje]
```

## Komendy

### 1. Zarządzanie Modułami
*   **Dodawanie Modułu**: Tworzy wpis w indeksie oraz fizyczny folder.
    ```bash
    python scripts/spec_manager.py --index ... add-module --id marketing --name "Marketing i PR" --description "Plan pozyskiwania użytkowników."
    ```
*   **Usuwanie Modułu**:
    ```bash
    python scripts/spec_manager.py --index ... remove-module --id marketing [--delete-files]
    ```
*   **Aktualizacja Modułu**:
    ```bash
    python scripts/spec_manager.py --index ... update-module --id financial_engine --name "Nowa Nazwa" --description "Nowy Opis"
    ```

### 2. Zarządzanie Fazami
*   **Dodawanie Fazy**: Tworzy plik `.json` fazy w folderze modułu i linkuje go.
    ```bash
    python scripts/spec_manager.py --index ... add-phase --module financial_engine --id 8 --name "Faza Dodatkowa"
    ```
*   **Usuwanie Fazy**:
    ```bash
    python scripts/spec_manager.py --index ... remove-phase --id 8 [--delete-file]
    ```
*   **Aktualizacja Statusu**:
    ```bash
    python scripts/spec_manager.py --index ... update-phase --id 1 --status completed --summary "Opis co ustalono..."
    ```
*   **Zmiana Kolejności**:
    ```bash
    python scripts/spec_manager.py --index ... reorder-phases --module financial_engine --order 1 2 4 3 5 6 7
    ```
*   **Łączenie Faz**: Konsoliduje pytania z wielu faz w jedną.
    ```bash
    python scripts/spec_manager.py --index ... merge-phases --module financial_engine --sources 2 3 --target 2 --name "Nowa Nazwa" --summary "Nowy opis..." [--delete-sources]
    ```

### 3. Zarządzanie Pytaniami
*   **Dodawanie Pytania**: Przyjmuje JSON z potoku (stdin).
    ```bash
    echo '{"id": "q100", "text": "Pytanie?", "type": "text"}' | python scripts/spec_manager.py --index ... add-question --phase 1
    ```
*   **Aktualizacja Pytania**:
    ```bash
    python scripts/spec_manager.py --index ... update-question --phase 1 --id q100 --json '{"text": "Zmieniona tresć"}'
    ```
*   **Przenoszenie Pytania**:
    ```bash
    python scripts/spec_manager.py --index ... move-question --from-phase 1 --to-phase 2 --id q100
    ```
*   **Zmiana Kolejności Pytań**:
    ```bash
    python scripts/spec_manager.py --index ... reorder-questions --phase 1 --order q101 q100 q102
    ```

### 4. Diagnostyka
*   **Walidacja Projektu**: Sprawdza spójność plików i ID.
    ```bash
    python scripts/spec_manager.py --index ... validate
    ```
*   **Podsumowanie Projektu**: Wyświetla postęp prac w konsoli.
    ```bash
    python scripts/spec_manager.py --index ... summary
    ```

---
*Uwaga: Zawsze używaj CLI do zmian w strukturze, aby uniknąć błędów składni JSON.*
