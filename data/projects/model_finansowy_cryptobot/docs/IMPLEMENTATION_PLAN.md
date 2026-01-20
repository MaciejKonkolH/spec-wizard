# IMPLEMENTATION PLAN: CryptoBot Financial Simulator

Ten dokument dzieli budowę symulatora na 4 krytyczne fazy (sprinty), aby zapewnić poprawność matematyczną przed nałożeniem warstwy wizualnej.

## Faza 1: Silnik Matematyczny (Headless Core)
**Cel**: Stworzenie funkcji `calculateSimulation()`, która przyjmuje parametry i zwraca tablicę obiektów z wynikami miesiąc po miesiącu.
*   Implementacja PRNG (Seeded Random).
*   Implementacja pętli finansowej: Trading -> Management Fee -> Success Fee (HWM) -> Churn -> Growth.
*   **Weryfikacja**: Porównanie wyników z plikiem `VALIDATION_CASES.md`. Dopóki liczby się nie zgadzają, nie przechodzimy do UI.

## Faza 2: Zarządzanie Stanem i Integracja URL
**Cel**: Połączenie suwaków z silnikiem i umożliwienie udostępniania wyników.
*   Stworzenie centralnego stanu (np. React Context).
*   Implementacja dwukierunkowej synchronizacji z adresem URL (Base64 hash).
*   Zapewnienie "Live Update" – każda zmiana suwaka natychmiast wywołuje `calculateSimulation()`.

## Faza 3: Dashboard i Wizualizacje
**Cel**: Prezentacja danych w formie "Inwestorskiej".
*   Konfiguracja Chart.js/Recharts.
*   Wdrożenie wykresu AUM (Area) oraz Cashflow (Bar).
*   Dodanie kart KPI z kluczowymi wynikami (ROI, BEP, Valuation).

## Faza 4: Polish & Refinement (Premium Look)
**Cel**: Estetyka "Wow Effect".
*   Wdrożenie Dark Mode (tło: `#0a0a0a`).
*   Efekty Glassmorphism na kartach.
*   Animacje wejścia dla wykresów.
*   Dodanie przycisku "Export to PDF/Report".
