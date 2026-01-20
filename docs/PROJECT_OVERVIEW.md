# Projekt: CryptoBot - Przegląd Systemu

## Czym jest CryptoBot?
CryptoBot to kompleksowy, w pełni zautomatyzowany system do tradingu wysokiej częstotliwości (HFT) na rynku Binance Futures. System wykorzystuje uczenie maszynowe (Machine Learning) do przewidywania krótkoterminowych ruchów cenowych i automatycznej egzekucji zleceń. Przeznaczony jest do obsługi dużej skali (ponad 100 symboli jednocześnie) przy zachowaniu wysokiej precyzji danych i odporności na awarie.

## Jak działa system (Pipeline)?
System składa się z niezależnych modułów (daemonów), które komunikują się ze sobą poprzez pliki danych (Parquet), co zapewnia niespotykaną stabilność (restart jednego modułu nie przerywa pracy pozostałych):

1.  **Gromadzenie Danych (`live_download`)**: Pobiera dane o cenie (OHLCV) oraz arkuszu zleceń (Orderbook) bezpośrednio z giełdy w czasie rzeczywistym.
2.  **Obliczanie Cech (`live_feature_calculator`)**: Przetwarza surowe dane na setki wskaźników technicznych (cech), które "rozumie" model AI.
3.  **Etykietowanie (`live_labeler`)**: Analizuje historię, aby sprawdzić, które sytuacje na rynku rzeczywiście doprowadziły do zysku (TP) lub straty (SL).
4.  **Trening AI (`live_trainer`)**: Co tydzień trenuje nowe modele XGBoost, aby system zawsze był dostosowany do aktualnej zmienności rynku.
5.  **Predykcja (`live_predictor`)**: Na podstawie najświeższych danych z rynku generuje prognozy (LONG/SHORT) dla każdego symbolu w każdej minucie.
6.  **Egzekucja (`live_trading/Freqtrade`)**: Silnik handlowy, który wysyła konkretne zlecenia kupna/sprzedaży na giełdę, dbając o niskie koszty transakcyjne (Maker strategy).
7.  **Monitoring (`web_data_monitor`)**: Panel graficzny dla operatora pozwalający śledzić poprawność danych i wyniki handlowe.

## Kontekst Modelu Finansowego
W Modelu Finansowym (który budujemy w Spec Wizardzie) nie skupiamy się na kodzie, ale na **biznesowej stronie przedsięwzięcia**:
*   **Skalowalność**: Jak wzrost kapitału (AUM) wpływa na zyski, biorąc pod uwagę ograniczenia płynności giełdy.
*   **Koszty**: Ile kosztuje utrzymanie infrastruktury (Cloud, GPU) oraz jakie prowizje pobiera giełda.
*   **Wyniki**: Symulacja miesięcznych zwrotów z inwestycji (ROI) w oparciu o zagregowane statystyki (liczba transakcji, win-rate) zamiast symulowania każdego pojedynczego ticka.
*   **Ryzyko**: Uwzględnienie Drawdownów (spadków kapitału) oraz modelu High-Water Mark (opłata pobierana tylko od nowych szczytów kapitału).

Ten opis stanowi fundament dla naszych dalszych ustaleń. Agent (AI) używa go jako stałego punktu odniesienia, aby zadawane pytania były precyzyjne i osadzone w realiach tego konkretnego projektu.
