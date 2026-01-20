# Faza 3: Logika Biznesowa, Dynamika Wzrostu & Dźwignia (ID: 3)

**Status:** completed

**Context Summary:** Ustalono logikę biznesową, system poleceń i parametry wzrostu.

---

### [ID: q13_fee_logic] Z jaką częstotliwością model powinien naliczać Success Fee?

*Opis: Opłata od zysku (prowizja) jest odejmowana od kapitału użytkownika i staje się przychodem firmy.*

**Wybrane opcje:**
- Miesięcznie (ID: monthly)

---
### [ID: q14_tax_logic] Jak model powinien traktować podatki od zysku?

*Opis: Zysk brutto vs zysk netto po opodatkowaniu.*

**Wybrane opcje:**
- Uwzględnienie VAT w kosztach operacyjnych (ID: vat_inc)

---
### [ID: q15_precision] Jaka powinna być precyzja obliczeń?

*Opis: Liczba miejsc po przecinku w obliczeniach wewnętrznych i wyświetlanych.*

**Wybrane opcje:**
- Dwa miejsca po przecinku ($1,250.45) (ID: standard)

---
### [ID: q16_currency] Jaką walutę bazową powinien obsługiwać model?

*Opis: Wpływa na symbole widoczne na dashboardzie i ewentualne przeliczniki.*

**Wybrane opcje:**
- USD (Dolar amerykański) (ID: usd)

---
### [ID: q16b_trading_costs] Jak model powinien szacować koszty transakcyjne (Giełda & Slippage)?

*Opis: Zamiast liczyć koszt każdej transakcji, przyjmiemy uśredniony narzut na miesięczny obrót.*

**Wybrane opcje:**
- Stały narzut w Punktach Bazowych (bps) (ID: bps_fixed)

---
### [ID: q17_initial_aum] Jaki jest łączny początkowy kapitał KLIENTÓW (Initial Client AUM)?

*Opis: Kwota, którą bot zaczyna zarządzać w miesiącu 0.*

**Wybrane opcje:**
- $100k - $500k (Model garażowy) (ID: small)

---
### [ID: q18_fee_rates] Jakie poziomy prowizji chcesz przyjąć jako domyślne?

*Opis: Główne parametry przychodowe modelu.*

**Wybrane opcje:**
- Agresywne Success Fee (np. 30-40%) (ID: performance_higher)

---
### [ID: q19_churn_model] Jak model powinien symulować odpływ kapitału (Churn Rate)?

*Opis: Procent kapitału, który co miesiąc jest wypłacany lub zabierany przez klientów odchodzących z platformy.*

**Wybrane opcje:**
- Umiarkowany (5% miesięcznie) (ID: medium)

**Komentarz użytkownika:**
> Chce żeby ten parametr był łatwo modyfikowalny jakimś przesuwakiem lub tym podobnym

---
### [ID: q19b_capacity_cap] Czy model powinien symulować spadek rentowności (Alpha Decay) przy wzroście AUM?

*Opis: W HFT płynność rynku jest ograniczona. Powyżej pewnej kwoty (np. $50M) strategia zaczyna mieć zbyt duży wpływ na rynek i jej zyskowność % spada.*

**Wybrane opcje:**
- Pomiń (Nieskończona płynność) (ID: infinite)

**Komentarz użytkownika:**
> Na pierwsze dwa lata nie ma sensu zakładać że osiągniemy taki kapitał który realnie będzie wpływał na rynek. Tym bardziej że nie handlujemy na jednej walucie.

---
### [ID: q20_cac_efficiency] Jak definiujemy efektywność marketingu?

*Opis: Stosunek wydanych pieniędzy na reklamę do pozyskanego kapitału (AUM).*

**Wybrane opcje:**
- Stały koszt pozyskania (np. $1 spend = $50 AUM) (ID: linear)

---
### [ID: q16c_leverage_logic] Jak model powinien uwzględniać dźwignię finansową (Leverage) wybraną przez klientów?

*Opis: Wyniki historyczne są 1x (bez dźwigni). Dźwignia mnoży zysk, ale i ryzyko drawdownu.*

**Wybrane opcje:**
- Średnia Dźwignia (Globalny Suwak) (ID: avg_leverage_slider)

---
### [ID: q20b_client_growth] W jakim tempie powinna rosnąć baza klientów?

*Opis: Pozwala oszacować tempo przyrostu AUM niezależnie od wyniku tradingu.*

**Wybrane opcje:**
- Wzrost napędzany budżetem (Ad-Spend) (ID: marketing_driven)

**Komentarz użytkownika:**
> Możemy zrobić wzrost klientów uzależniony od budżetu reklamowego ale chce mieć możliwość ustawiania jaki kapitał idzie na reklamę oraz jak ten kapitał będzie rósł. Trzeba obmyśleć jak to rozwiązać ponieważ na początku koszty mogą przewyższać przychody a kapitał reklamowy jakiś musi być więc nie możemy po prostu ustalić go jako procentową wartość dochodów. Liczę na twoje sugestie.

---
### [ID: q20c_capital_injection] Jak często i w jakiej skali klienci będą dopłacać kapitał?

*Opis: Symulacja 'Retention Upsell' – zadowoleni klienci dorzucają środki.*

**Wybrane opcje:**
- Regularne dopłaty (np. co kwartał +20%) (ID: periodic_injection)

**Komentarz użytkownika:**
> Chce żeby tą wartość dało się regulować. Jak dużo i jak często.

---
### [ID: q_universal_budget] Jaki jest przewidywany budżet na rozwój platformy MVP?

**Odpowiedź własna:**
> Cały MVP ma zostać zrobiony przez agenta AI więc zakładam że zrobi to w cenie poniżej 100$

---
### [ID: q_universal_timeline] Jaki jest docelowy czas na wdrożenie działającego symulatora?

**Odpowiedź własna:**
> Tydzień. Dla agenta to i tak bardzo dużo ale wiem że potrzeba nadzoru człowieka.

---
### [ID: q_universal_scale] Jaka jest zakładana liczba użytkowników końcowych (inwestorów) w roku 1?

**Wybrane opcje:**
- Do 100 (Zamknięty krąg) (ID: early)

**Odpowiedź własna:**
> Chce żeby ta wartość była regulowana

---
### [ID: q_initial_client_count] Ilu klientów posiada system w momencie startu (Miesiąc 0)?

*Opis: Liczba kont/portfeli, które są aktywne od pierwszego dnia.*

**Odpowiedź własna:**
> 5

---
### [ID: q_initial_runway] Jaki jest początkowy kapitał operacyjny SPÓŁKI (Company Runway)?

*Opis: Środki własne/inwestorskie przeznaczone na pokrycie kosztów stałych i marketingu przed osiągnięciem rentowności.*

**Odpowiedź własna:**
> 70000 zł

---
### [ID: q_parameter_checklist] Które parametry modelu finansowego mają być regulowane przez użytkownika (suwaki/inputy)?

*Opis: Zaznacz wszystkie wartości, które chcesz zmieniać dynamicznie w symulatorze. Niezaznaczone parametry zostaną przyjęte jako stałe (hardcoded) w PRD.*

**Wybrane opcje:**
- Początkowy kapitał KLIENTÓW (AUM) (ID: initial_client_aum)
- Kapitał operacyjny SPÓŁKI (Runway) (ID: initial_runway)
- Początkowa liczba klientów (ID: initial_client_count)
- Średnia wpłata na klienta (ID: avg_deposit)
- Prowizja Success Fee (%) (ID: success_fee)
- churn_rate (ID: churn_rate)
- leverage (ID: leverage)
- panic_churn (ID: panic_churn)
- marketing_fixed (ID: marketing_fixed)
- marketing_revenue_perc (ID: marketing_revenue_perc)
- injection_params (ID: injection_params)
- reserve_fund (ID: reserve_fund)
- yield_seed (ID: yield_seed)
- Opłata Management Fee (%) (ID: management_fee)
- % zysku oddawany polecającemu (ID: referral_fee_share)
- % klientów pochodzących z polecenia (ID: referral_client_ratio)
- Budżet marketingowy ($/mc) (ID: marketing_budget_start)
- % przychodu na marketing (ID: marketing_reinvest)
- Fundusz rezerwowy (%) (ID: reserve_rate)
- Średnia dźwignia (Leverage) (ID: leverage_avg)
- Panic Multiplier (x) (ID: churn_panic)
- Base Churn Rate (%) (ID: churn_base)

---
### [ID: q_referral_logic] Jak ma działać system poleceń (Affiliate)?

*Opis: System poleceń to kluczowy element obniżający koszt pozyskania klienta (CAC).*

**Wybrane opcje:**
- Revenue Share (np. oddajemy 3% z naszych 20% Success Fee) (ID: rev_share)

---