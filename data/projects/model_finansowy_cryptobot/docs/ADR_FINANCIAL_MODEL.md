# Architecture Decision Record (ADR): Financial Model Deviations

Ten dokument rejestruje wszystkie odstępstwa implementacji od pierwotnej specyfikacji (`FINAL_PRD.md`) oraz wprowadzone nowe funkcjonalności w projekcie **CryptoBot Financial Simulator**.

---

## 1. Silnik Inicjalizacji i Parametry Domyślne

Wprowadzono nowe, bardziej realistyczne wartości bazowe dla startupu:
- **Początkowy kapitał spółki (Runway)**: 20 000 USD.
- **Liczba klientów**: 5 (suwak 1-50).
- **Średni depozyt**: 10 000 USD.
- **Koszty stałe**: 1 500 USD/msc.
- **Opłaty**: Zarządzająca (0%), Sukcesu (20%).

| Cecha | Pierwotny Plan (PRD) | Stan Faktyczny (Implementacja) | Rationale (Uzasadnienie) |
| :--- | :--- | :--- | :--- |
| **Początkowe AUM** | Parametr niezależny | `initial_client_count * avg_deposit` | **Logika biznesowa**: Wyeliminowano niespójność, gdzie AUM mogło być nieproporcjonalne do liczby klientów. |
| **High-Water Mark** | Globalny Portfel | `grossAUM - successFeeAmount` | **Precyzja**: HWM po pobraniu opłaty staje się nowym punktem odniesienia (netto). |

---

## 2. Model Generowania Wyników (Yield)

| Cecha | Pierwotny Plan (PRD) | Stan Faktyczny (Implementacja) | Rationale (Uzasadnienie) |
| :--- | :--- | :--- | :--- |
| **Wybór Wyniku** | Modulo: `(Seed + m) % 5` | **Real Sequential Data (Aktualizacja 19.01)** | **Realizm**: Zastosowano 24-miesięczną historię. Pierwsze 4 msc to realne dane bota, kolejne 20 msc to bootstrap (losowe próbkowanie z dni historycznych). |
| **Dźwignia** | Mnożnik końcowy | Stosowana bezpośrednio w `tradingResult` | **Agresywność alokacji**: Dane bazowe to alokacja 1%. Suwak Leverage to mnożnik tej alokacji (np. 5x = 5% kapitału na pozycję). |

---

## 3. Dynamiczne CPA i Nasycenie Rynku

Zoptymalizowano model wzrostu, aby zapobiec nierealistycznej "eksplozji" wykresów (Growth Saturation):
- **CPA (Cost Per Acquisition)**: Koszt pozyskania klienta.
- **CPA Scaling (Saturacja)**: Nowy parametr określający wzrost kosztu marketingu o X% na każde 10 aktywnych portfeli. 
- **Rationale**: Symuluje naturalne zjawisko drożejących kampanii reklamowych w miarę wyczerpywania się grupy docelowej.

---

## 4. Interaktywna Wizualizacja (Pan & Zoom)

Zrezygnowano z tradycyjnych pasków przewijania na rzecz nowoczesnych gestów (Trading-style UI):
- **Zoom**: Scroll kółkiem myszy nad obszarem wykresu (Zoom-In / Zoom-Out).
- **Pan (Przesuwanie)**: Kliknij i przeciągnij (Drag & Horizontal Scroll) na osi czasu.
- **Reset**: Manualny przycisk przywracania pełnego widoku (24 miesiące) w nagłówku każdego wykresu.
- **Wydajność**: Wyłączenie animacji renderowania podczas interakcji (isAnimationActive={false}) dla płynności reakcji w czasie rzeczywistym.

---

## 5. Nowa Funkcjonalność: Kapitał Własny Spółki

- **Company Trading Capital**: Subkonto firmowe u bota zwiększane przez trading własny i reinwestycję zysku.
- **Marketing Reinvestment**: Procent zysków firmy automatycznie zasilający budżet marketingowy.
- **Profit Allocation**: Model uwzględnia podatek/koszty przed reinwestycją.

---

## 6. System Dywidend i Udziałów (Investor Rewards)

Wprowadzono mechanizm dzielenia się zyskiem z inwestorami:
- **Polityka Dywidendowa**: Procent zysku netto firmy (po kosztach i marketingu), który jest wypłacany udziałowcom.
- **Udział Inwestora**: Możliwość symulacji zarobków konkretnego inwestora na podstawie jego % udziałów w spółce.
- **Wpływ na Cashflow**: Wypłacone dywidendy są odejmowane od `monthlyNetProfit`, co fizycznie pomniejsza Runway spółki (realny odpływ gotówki).
- **Zarobki Inwestora**: Nowy wykres agregujący skumulowaną sumę wypłat dywidendowych.

---

## 7. Modyfikacje UI, KPI i i18n

- **Formatowanie**: Implementacja separatorów tysięcy (spacje) w dymkach (Tooltip) i polach input (np. `2 000 000`).
- **Kontrast**: Zmiana koloru czcionki w dymkach na biały (`#fff`) dla czytelności na ciemnym tle (Dark Mode).
- **Nazewnictwo**: Ujednolicono terminologię (np. "Początkowy kapitał spółki", "Naturalny odpływ kapitału klienta").
- **Serializacja**: Cały stan symulacji jest binarnie serializowany (Base64) w URL (Share Simulation).

---
*Status Dokumentu: Aktywny / Living Document*  
*Data ostatniej aktualizacji: 2026-01-20 (v2.2)*  
