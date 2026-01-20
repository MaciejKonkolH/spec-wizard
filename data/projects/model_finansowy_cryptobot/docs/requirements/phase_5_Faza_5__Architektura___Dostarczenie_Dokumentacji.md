# Faza 5: Architektura & Dostarczenie Dokumentacji (ID: 5)

**Status:** completed

**Context Summary:** Ustalono architekturę techniczną i stack technologiczny.

---

### [ID: q21_tech_stack] W jakiej technologii powinien zostać zbudowany silnik symulatora?

*Opis: Determinuje wydajność oraz łatwość osadzenia modelu na stronie internetowej.*

**Wybrane opcje:**
- React + Chart.js / Recharts (Standard nowoczesny) (ID: react_charts)

---
### [ID: q22_data_flow] Jak silnik powinien zarządzać stanem parametrów (suwaków)?

*Opis: Architektura przepływu danych przy zmianach użytkownika.*

**Wybrane opcje:**
- Centralny stan (Redux/Context API) (ID: central_store)

---
### [ID: q23_component_library] Jakie komponenty UI będą potrzebne do obsługi suwaków?

*Opis: Wybór estetyki i funkcjonalności elementów sterujących.*

**Wybrane opcje:**
- Suwaki sparowane z polem liczbowym (ID: input_sync)
- Suwaki z wyborem zakresu (Min/Max) (ID: dual_range)

---
### [ID: q24_worker_calc] Gdzie powinny odbywać się obliczenia symulacji?

*Opis: Wpływa na płynność (framerate) interfejsu przy dużej ilości punktów danych.*

**Wybrane opcje:**
- Główny wątek (proste i szybkie) (ID: main_thread)

---
### [ID: q25_persistence] Gdzie powinny być zapisywane wyniki symulacji?

*Opis: Decyduje o tym, czy użytkownik może wrócić do swojej sesji później.*

**Wybrane opcje:**
- Unikalny link (Serializacja do URL) (ID: sharelink)

---
### [ID: q26_reporting_quality] Jaki poziom szczegółowości powinien mieć raport PDF?

*Opis: Eksport danych do formatu dokumentu.*

**Wybrane opcje:**
- Pełny audyt (kilka stron) (ID: full_audit)

---
### [ID: q27_hft_aggregation] W jaki sposób silnik powinien generować wyniki handlowe (Yield) na osi czasu?

*Opis: Skoro masz 5 miesięcy realnych danych (w tym jeden drawdown), możemy je wykorzystać jako fundament. Wyniki muszą być powtarzalne (deterministyczne) po odświeżeniu strony.*

**Wybrane opcje:**
- Model ‘Fixed Scenarios’ (Archetypy) (ID: deterministic_scenarios)

**Komentarz użytkownika:**
> Nie chciałbym takiej sytuacji że przy kazdym otwarciu symulacji otrzymujemy wynik. Więc losowość może być ale generowana jakoś jednorazowo. Przemyśl jeszcze raz to pytania i zaproponuj coś co uwzględni moją sugestię. Obecnie  mam wyniki symulacji z okresu mniej więcej 5 miesięcy i jest tam jeden miesiąc dropdown. Więc nie wiem czy jakoś wykorzystać te 5 miesięcy i w jakiś sposób je ekstrapolować czy może uśrednić zysk z całości i dodać jakąś losowość. Proszę o jakieś sensowne propozycje z dobrym objaśnieniem

---
### [ID: q28_spec_delivery] W jakiej formie ma zostać wygenerowana finalna specyfikacja techniczna?

*Opis: Zwieńczenie pracy ze Spec Wizardem.*

**Wybrane opcje:**
- Markdown Strukturany (zoptymalizowany pod AI) (ID: markdown_ai)

**Komentarz użytkownika:**
> PRD w formie pliku md, yaml lub tym podobnego łatwego do odczytu przez agentów AI

---