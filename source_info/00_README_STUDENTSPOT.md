# StudentSpot — pakiet wdrożeniowy

## Cel pakietu

Pakiet służy do zbudowania działającego MVP aplikacji **StudentSpot** na potrzeby projektu z przedmiotu „Podstawy systemów informatycznych zarządzania / Metodyka zarządzania informacją”.

StudentSpot jest lekkim systemem webowym wspierającym:

- rejestrację i aktywację kont studentów,
- obsługę członkostwa w kołach naukowych,
- prezentację wydarzeń i spotkań,
- wyszukiwanie sal według potrzeb,
- składanie i zatwierdzanie rezerwacji,
- uwzględnianie potrzeb dostępnościowych,
- obsługę organizacji studenckich i wybranych inicjatyw Uniwersytetu Trzeciego Wieku.

## Pliki

1. `01_STUDENTSPOT_SPECYFIKACJA_MVP.md`  
   Pełna specyfikacja funkcjonalna, architektura, role, procesy, model danych, testy akceptacyjne i wdrożenie na Mikrus Frog.

2. `02_STUDENTSPOT_DANE_I_ZRODLA.md`  
   Dane startowe o salach, kołach naukowych, dostępności, kontaktach, logotypach i mapach. Zawiera rozróżnienie danych potwierdzonych oraz roboczych.

3. `03_PROMPT_CLAUDE_CODE.md`  
   Prompt do Claude Code prowadzący przez analizę, budowę, testy i dokumentację aplikacji.

4. `04_PROMPT_CODEX.md`  
   Prompt do Codex przeznaczony do wdrożenia aplikacji w repozytorium, z naciskiem na działający kod, testy i deployment.

## Zalecana kolejność

1. Przekaż agentowi wszystkie cztery pliki.
2. Poproś o przeczytanie ich przed modyfikacją repozytorium.
3. Najpierw zbuduj wersję lokalną.
4. Uruchom testy automatyczne.
5. Zasil bazę danymi demonstracyjnymi.
6. Dopiero potem wykonaj wdrożenie na Frog.

## Najważniejsza zasada zakresu

MVP ma być **małe, kompletne i działające**. Nie wolno komplikować projektu mikroserwisami, Reactem, Keycloakiem, kolejkami zadań ani lokalnym silnikiem AI. Wersja na zaliczenie ma dobrze realizować główny proces zarządczy:

> zgłoszenie potrzeby → dopasowanie sali → wniosek o rezerwację → kontrola konfliktu → decyzja administratora → powiadomienie → widoczność wydarzenia.

## Status projektu

To jest **nieoficjalny prototyp studencki**. Nie należy sugerować, że aplikacja jest oficjalnym systemem AHE ani że uczelnia zatwierdziła wykorzystanie jej identyfikacji wizualnej.
