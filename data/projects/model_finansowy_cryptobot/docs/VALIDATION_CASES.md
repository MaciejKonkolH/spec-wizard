# VALIDATION CASES: CryptoBot Financial Simulator

Służy do ręcznej weryfikacji poprawności algorytmu finansowego. Jeśli symulator podaje inne liczby niż poniżej (przy tych samych parametrach), oznacza to błąd w logice HWM lub Churnu.

## Case 1: Czysty Wzrost (Bez Odpływu i Opłat)
*   **Input**: AUM=$100k, Yield=+10%, SF=0%, MF=0%, Churn=0%.
*   **Output (Miesiąc 1)**: AUM=$110,000.
*   **Output (Miesiąc 2)**: AUM=$121,000.

## Case 2: High-Water Mark & Success Fee
*   **Input**: AUM=$100k, SF=20%, MF=0%, Churn=0%.
*   **Scenariusz**:
    *   Miesiąc 1: Yield=+10% -> AUM przed fee=$110k -> Fee=$2k -> **Final AUM=$108k** (HWM=$110k).
    *   Miesiąc 2: Yield=-5% -> AUM przed fee=$102.6k -> Fee=$0 -> **Final AUM=$102.6k** (HWM=$110k).
    *   Miesiąc 3: Yield=+10% -> AUM przed fee=$112.86k -> **Fee od nadwyżki nad HWM ($2.86k)** = $0.572k -> **Final AUM=$112.288k**.

## Case 3: Mechanizm Paniki (Panic Churn)
*   **Input**: BaseChurn=2%, PanicMultiplier=5x.
*   **Scenariusz**:
    *   Miesiąc 1 (Zysk): Odpływ = 2% AUM.
    *   Miesiąc 2 (Strata): Odpływ = **10%** AUM (2% * 5).

## Case 4: System Poleceń (Referral)
*   **Input**: Success Fee Revenue=$1000, ReferralShare=3%, Penetration=100%.
*   **Output**: Przychód Firmy=$970, Wypłata dla Partnerów=$30.
