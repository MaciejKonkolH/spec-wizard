# Faza 2: Produkt, Funkcje & UX (ID: 2)

**Status:** completed

**Context Summary:** Zdefiniowano funkcje produktu i UX.

---

### [ID: q5_features] Jakie interaktywne funkcje powinny znaleźć się w panelu symulacji?

*Opis: Funkcjonalności dashboardu, które pozwalają na głębszą analizę danych i interakcję z modelem.*

**Wybrane opcje:**
- Suwaki parametrów (zmiana 'w locie' yield'u, churnu, kosztów) (ID: sliders)
- Panel edycji kosztów (dodawanie/usuwanie konkretnych pozycji budżetowych) (ID: cost_deepdive)
- System scenariuszy (zapisywanie i porównywanie Bull/Bear/Base) (ID: scenarios)

---
### [ID: q6_kpis] Które wskaźniki (KPI) powinny być najbardziej widoczne na dashboardzie?

*Opis: KPI (Key Performance Indicators) to kluczowe mierniki sukcesu, które inwestor chce widzieć jako pierwsze.*

**Wybrane opcje:**
- Miesięczny Zysk Netto (po kosztach i podatkach) (ID: net_profit)
- Dynamika wzrostu AUM (Assets Under Management) (ID: aum_growth)
- Czas do osiągnięcia Break-Even Point (ID: bep_time)
- Aktualny stan HWM i rezerwa na Drawdown (ID: hwm_status)
- Relacja CLV do CAC (opłacalność pozyskania klienta) (ID: clv_cac)

---
### [ID: q7_sampling] Z jaką częstotliwością model powinien przeliczać kapitał i koszty?

*Opis: Określa 'gęstość' danych na wykresach. Więcej punktów to ładniejsze wykresy, ale większy szum informacyjny.*

**Wybrane opcje:**
- Miesięcznie (najbardziej czytelne dla finansów) (ID: monthly)

---
### [ID: q8_market_data] Skąd model powinien brać parametry zmienności rynkowej (do testów HWM)?

*Opis: Sposób, w jaki symulator generuje spadki i wzrosty kapitału.*

**Wybrane opcje:**
- Ręczny suwak % drawdown (uproszczone) (ID: fixed_input)

---
### [ID: q9_layout] Jaki układ interfejsu preferujesz dla dashboardu?

*Opis: Sposób rozmieszczenia paneli sterowania (suwaków) względem wyników (wykresów).*

**Wybrane opcje:**
- Panel sterowania z lewej, wykresy z prawej (klasyczny SaaS) (ID: split_sidebar)

---
### [ID: q10_chart_types] Ktöre typy wizualizacji są kluczowe dla Twojej prezentacji?

*Opis: Wybór sposobu prezentowania danych liczbowych na ekranie.*

**Wybrane opcje:**
- Pole powierzchni (Cumulative Growth) dla AUM (ID: area_cumulative)
- Słupki dla miesięcznych przychodów i kosztów (ID: bar_monthly)
- Wykres kaskadowy (Waterfall) dla marży (ID: waterfall)
- Duże karty numerów (Big Numbers) dla KPI (ID: status_cards)

---
### [ID: q11_interaction_flow] Jak model ma reagować na zmianę parametrów?

*Opis: Decyduje o poczuciu 'życia' aplikacji.*

**Wybrane opcje:**
- Auto-reobliczanie w czasie rzeczywistym (Live Update) (ID: realtime)

---
### [ID: q12_scenarios_viz] Jak chcesz porównywać scenariusze (Bull/Bear/Base)?

*Opis: Sposób prezentacji różnic między założeniami rynkowymi.*

**Wybrane opcje:**
- Nałożenie na jeden wykres (różne kolory linii) (ID: overlay)

---