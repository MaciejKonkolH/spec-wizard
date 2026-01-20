# Faza 4: Scenariusze Inwestorskie & Analiza Ryzyka (ID: 4)

**Status:** completed

**Context Summary:** Zdefiniowano scenariusze inwestorskie i wskaźniki ryzyka.

---

### [ID: q29_sim_locking] Jak system powinien zarządzać "losowości" wygenerowanego scenariusza?

*Opis: Ustaliliśmy, że wynik ma by? sta?y, ale musi istnie? sposób na zmianę symulacji.*

**Wybrane opcje:**
- URL Seed (Zakodowane w linku) (ID: url_seed)

---
### [ID: q30_data_extrapolation] Jak najlepiej wykorzystać Twoje 5 miesięcy realnych danych w modelu?

*Opis: Mamy 4 miesi?ce zysku i 1 miesi?c straty (drawdown).*

**Wybrane opcje:**
- P?tla Blokowa (Loop) (ID: block_loop)

**Odpowiedź własna:**
> Uważam powinno być losowanie miesiąca. A nie zawsze po kolei M1, M2 .... Czyli będziemy mieli bazowe wyniki dla 5 miesięcy i dla raportu 24 będziemy losować (ziarno, seed) 24 razy. Dzięki temu dane będą bardziej zróżnicowane. Inaczej będziemy mieli powtarzający się pięciomiesięczny schemat

---
### [ID: q31_kpi_set] Jakie zaawansowane wskaźniki (KPI) model powinien wyliczać automatycznie?

*Opis: Sam zysk to za mało dla profesjonalnego funduszu.*

**Wybrane opcje:**
- Max Drawdown & Recovery Time (ID: max_dd)
- Sharpe / Sortino Ratio (ID: sharpe)
- Daily Volatility (Aproksymacja) (ID: daily_vol)

---
### [ID: q32_stress_testing] Czy model powinien posiadać funkcję "Stress Test" (Czarny Łabędź)?

*Opis: Symulacja ekstremalnych warunków rynkowych.*

**Wybrane opcje:**
- Wiersz Scenariusza Pesymistycznego (ID: worst_case_row)

---
### [ID: q33_architecture_type] Jaki model architektury backendowej najlepiej pasuje do symulacji?

*Opis: Deterministyczne generowanie danych wymaga stabilnej logiki po stronie serwera lub silnika JS.*

**Wybrane opcje:**
- Pure Client-Side (JS) (ID: client_side)

---
### [ID: q34_data_format] W jakim formacie system powinien przechowywać Twoje dane historyczne (te 5 miesięcy)?

*Opis: Dane muszą być wczytywane błyskawicznie przy starcie symulacji.*

**Wybrane opcje:**
- Statyczny JSON (Embedded) (ID: json_static)

---