# FINAL PRODUCT REQUIREMENTS DOCUMENT (PRD) v2.0
## Projekt: CryptoBot Financial Simulator (Interactive MVP)

**Wersja:** 2.0 (Engineering Ready)  
**Status:** ZATWIERDZONY DO IMPLEMENTACJI  
**Cel:** Narzędzie inwestorskie (HTML/JS) udowadniające skalowalność modelu biznesowego opartego na tradingu HFT i poleceniach.

---

## 1. Architektura Systemu (System Design)

### 1.1. Technology Stack
*   **Core**: Vanilla JS (ES6+) lub React (Vite).
*   **Wizualizacja**: Chart.js (lekki, wydajny) lub Recharts.
*   **Stylizacja**: TailwindCSS (Dark Mode, Financial Dashboard aesthetics).
*   **Baza Danych**: BRAK.
    *   *Persistence*: Stan aplikacji zserializowany do Base64 i przechowywany w URL (Shareable Links).
    *   *Historia*: Statyczny plik JSON z 5-miesięcznym 'Sample Data'.

### 1.2. Struktura Danych (State Model)
Stan aplikacji (`AppState`) musi zawierać następujące obiekty:

```json
{
  "config": {
    "simulation_months": 24,
    "yield_seed": 12345, // Ziarno dla generatora losowego
    "history_data": [3.5, 4.2, 5.1, -8.5, 2.9] // Realne wyniki
  },
  "user_params": {
    "initial_client_aum": 100000,
    "initial_runway": 70000, // PLN przeliczone na walute bazową lub display as is
    "initial_client_count": 5,
    "avg_deposit_per_user": 20000, // Calculated or Input
    "fees": {
      "success_fee_percent": 20.0,
      "management_fee_percent": 2.0, // Rocznie
      "trading_cost_bps": 5 // Koszt transakcyjny
    },
    "growth": {
      "marketing_budget_fixed": 2000, // USD
      "marketing_reinvest_rate": 0.3, // 30% zysku reinwestowane
      "cac_fixed": 50, // Koszt pozyskania $1 AUM lub per Client
      "referral_fee_share": 3.0, // % Success Fee dla partnera
      "referral_penetration": 0.2 // 20% klientów jest z polecenia
    },
    "risk_churn": {
      "leverage_avg": 1.0,
      "churn_base_monthly": 2.0, // %
      "churn_panic_multiplier": 3.0 // x3 przy stratach
    }
  }
}
```

---

## 2. Silnik Matematyczny (Core Logic)

Silnik działa w pętli miesięcznej `(Month 1 to Month N)`. Każdy miesiąc musi być obliczany sekwencyjnie, ponieważ wynik Month X jest wejściem dla Month X+1.

### 2.1. Inicjalizacja (Miesiąc 0)
*   `CurrentAUM` = `initial_client_aum`
*   `CurrentClients` = `initial_client_count`
*   `CompanyCash` = `initial_runway`
*   `HighWaterMark` (Global) = `CurrentAUM` (Uproszczenie: Startujemy z punktu zero).
*   `CumProfit` = 0

### 2.2. Algorytm Miesięczny (Step-by-Step Logic)

Dla każdego miesiąca `m` wykonaj:

#### KROK 1: Wyznaczanie Wyniku Tradingu (Yield Generation)
Używamy **Deterministycznego Generatora Pseudo-Losowego (PRNG)** opartego na `yield_seed`.
*   Algorytm nie może być czystym `Math.random()`. Musi zwracać ten sam ciąg dla tego samego Seeda.
*   Logika: `SelectedYield = history_data[ (Seed + m) % 5 ]` + (mikro_szum losowy +/- 0.5% dla wariancji).
*   **Wynik Brutto**: `TradingResult = CurrentAUM * (SelectedYield / 100) * leverage_avg`.

#### KROK 2: Aktualizacja AUM (Przed Opłatami)
*   `PreFeeAUM = CurrentAUM + TradingResult`

#### KROK 3: Naliczenie Opłat (Fee Logic)
*   **Management Fee**:
    *   `MgmtFeeAmount = CurrentAUM * (management_fee_percent / 100) / 12`
    *   Pobierane zawsze, niezależnie od wyniku.
*   **Success Fee (High-Water Mark)**:
    *   `GrossAUM = PreFeeAUM - MgmtFeeAmount`
    *   `IF (GrossAUM > HighWaterMark)`:
        *   `ProfitDlaDystrybucji = GrossAUM - HighWaterMark`
        *   `SuccessFeeAmount = ProfitDlaDystrybucji * (success_fee_percent / 100)`
        *   **Nowy HWM**: `HighWaterMark = GrossAUM` (Aktualizujemy rekord po pobraniu fee? NIE. Zazwyczaj HWM to poziom AUM przed fee. Tu przyjmujemy model: HWM rośnie wraz z kapitałem klienta.
        *   *Korekta HWM*: W modelu uproszczonym (pula globalna) HWM podążą za wartością portfela netto.
    *   `ELSE`: `SuccessFeeAmount = 0`

#### KROK 4: Dystrybucja Przychodów i System Poleceń (Revenue Share)
Z kwoty `SuccessFeeAmount` firma musi opłacić partnerów:
*   `ReferralCost = SuccessFeeAmount * (referral_penetration_rate) * (referral_fee_share / 100)`
    *   *Wyjaśnienie*: Płacimy prowizję tylko od tej części kapitału, która pochodzi z polecenia (np. 20% bazy), ułamkiem naszej prowizji (np. 3%).
*   **Przychód Netto Firmy**: `CompanyRevenue = SuccessFeeAmount - ReferralCost + MgmtFeeAmount`.

#### KROK 5: Marketing i Wzrost (Growth Engine)
*   `MarketingBudget = marketing_budget_fixed + (CompanyRevenue * marketing_reinvest_rate)`
*   *Zabezpieczenie*: Jeśli `CompanyRevenue < 0` (np strata operacyjna), marketing bazuje tylko na fixed_budget LUB czerpie z Runwayu.
*   **Nowy Kapitał (Acquisition)**: `NewAUM_Inflow = MarketingBudget * (efficiency_multiplier / cac_fixed)`.
    *   *Uwaga*: Użytkownik zdefiniował CAC jako "$1 spend = $X AUM".
*   **Nowi Klienci**: `NewClients = NewAUM_Inflow / avg_deposit_per_user`.

#### KROK 6: Odpływ Klientów (Churn Dynamics)
*   `IsPanicMode = (SelectedYield < 0)`
*   `EffectiveChurnRate = churn_base_monthly * (IsPanicMode ? churn_panic_multiplier : 1)`
*   `ChurnOutflow = PreFeeAUM * (EffectiveChurnRate / 100)`
*   `ClientsLost = CurrentClients * (EffectiveChurnRate / 100)`

#### KROK 7: Bilans Końcowy Miesiąca
*   `FinalAUM = PreFeeAUM - MgmtFeeAmount - SuccessFeeAmount + NewAUM_Inflow - ChurnOutflow`
*   `CurrentClients = CurrentClients + NewClients - ClientsLost`
*   `FixedCosts = 2000` (lub inna stała operacyjna zdefiniowana w kodzie).
*   `CompanyCashFlow = CompanyRevenue - FixedCosts - MarketingBudget`
*   `CompanyRunway = CompanyRunway + CompanyCashFlow`

---

## 3. UI/UX Specifications (Frontend)

### 3.1. Layout Dashboardu (Single Page)
*   **Sekcja Lewa (Input Matrix)**:
    *   Zwijane "akordeony" dla grup parametrów: [Start], [Opłaty/Fees], [Wzrost/Growth], [Ryzyko/Risk].
    *   Każdy parametr: Label + Slider + Input Number (zsynchronizowane).
*   **Sekcja Prawa (Wizualizacja)**:
    *   **Header**: Główne KPI (Big Font):
        *   `Total AUM`
        *   `Company Valuation` (np. 10x roczny zysk)
        *   `Investor ROI`
    *   **Main Chart (Area)**: Total AUM Growth (Oś X: Miesiące, Oś Y: $).
    *   **Secondary Chart (Bar)**: Monthly Company Cashflow (Green/Red bars). Przychód vs Koszty.
    *   **Tertiary Chart (Line)**: "Panic Index" (pokazuje kiedy zadziałał mnożnik churnu).

### 3.2. UX Interactions
*   **Debounce**: Przeliczanie modelu następuje max co 50-100ms podczas przesuwania suwakiem, aby zachować płynność 60fps.
*   **Hover**: Najechanie na miesiąc na wykresie pokazuje Tooltip ze szczegółami: `Yield: -5%`, `Churn: -$50k`, `Fees: $0`.

---

## 4. Scenariusze Testowe (Quality Assurance)

Implementując model, Agent musi zweryfikować poprawność na tych skrajnych przypadkach:

1.  **Test "Zero-Profit"**:
    *   Ustaw `Success Fee = 0`, `Mgmt Fee = 0`.
    *   Oczekiwane: Przychód firmy = 0. Runway spada o koszty stałe co miesiąc aż do bankructwa.
2.  **Test "Panic Spiral"**:
    *   Ustaw historyczne dane na same straty (`[-5, -5, -5]`).
    *   Ustaw `Panic Multiplier = 10x`.
    *   Oczekiwane: AUM powinno spaść do blisko zera w kilka miesięcy przez gigantyczny churn.
3.  **Test "High-Water Mark"**:
    *   Miesiąc 1: +10% (Pobierz Fee).
    *   Miesiąc 2: -5% (Brak Fee).
    *   Miesiąc 3: +4% (Brak Fee, bo nadal nie odrobiliśmy straty z M2! Suma to -1%).
    *   Miesiąc 4: +2% (Pobierz Fee tylko od nadwyżki ponad szczyt z M1).

---

## 5. Agent Instructions (Implementation Prompts)

Jeśli zlecasz to zadanie innemu LLM, użyj tego promptu jako "System Message":

> "Jesteś inżynierem FinTech. Twoim zadaniem jest zaimplementowanie symulatora inwestycyjnego w czystym JS/React. Cała logika biznesowa (Fees, HWM, Churn, Referral) musi być odwzorowana 1:1 z sekcji '2. Silnik Matematyczny' dostarczonego pliku PRD. Nie stosuj uproszczeń. Użyj danych historycznych `[3.5, 4.2, 5.1, -8.5, 2.9]` jako bazy do generowania losowości. Kod ma być czysty, modularny i gotowy do wdrożenia."

---

*Zatwierdzono do realizacji. Brak dodatkowych pytań wymaganych.*
