# Projektowanie aplikacji MVP zgodnie z identyfikacją Akademii Humanistyczno‑Ekonomicznej w Łodzi

## Układ i struktura strony „Biuro Projektów Europejskich”

Widok strony *Biuro Projektów Europejskich* na portalu AHE pokazuje kilka charakterystycznych sekcji, które można odwzorować w aplikacji:

- **Nagłówek globalny** – górna belka z ciemnym tłem zawiera odnośniki do wirtualnych pokoi dla studentów/dydaktyków oraz platformy e‑learningowej. Pod belką znajduje się biały pasek z logo uczelni oraz rozwijanym menu (przycisk „Rekrutacja” w kolorze czerwono‑burgundowym).
- **Menu główne** – tuż pod logo i przyciskiem rekrutacji znajduje się poziome menu z kategoriami „O Akademii”, „Strefa kandydata”, „Strefa studenta”, „Działalność naukowa” i „Kontakt”. Kolor tła menu jest biały, a tekst – ciemnoszary lub granatowy.
- **Sekcja hero** – duże zdjęcie ilustrujące temat z białym lub granatowym paskiem z nagłówkiem. Na stronie BPE tytuł „Biuro Projektów Europejskich” znajduje się na niebieskim prostokącie umieszczonym na zdjęciu【57159700990028†screenshot】.
- **Nawigacja lokalna** – po lewej stronie tekstu głównego znajduje się pionowe menu (na szarym tle) z odnośnikami do podstron działu („Biblioteka”, „Wydawnictwo”, „Czasopisma” itd.)【126855689445385†L151-L164】. W wersji mobilnej menu powinno zwijać się do przycisku hamburgera.
- **Treść** – nagłówki artykułów są duże i wyraźne, pod nimi znajdują się akapity tekstu, listy punktowane oraz zdjęcia. Całość korzysta z dużo białej przestrzeni i mocnego kontrastu między tekstem a tłem.

Rekomendacja: aby zachować wygląd 1:1, zaprojektuj aplikację z głównym nagłówkiem/stopką w kolorze ciemnego granatu, wyróżnij ważne przyciski kolorem czerwonym (patrz sekcja kolorów) i użyj bocznego menu dla podrzędnych stron. Rozmiary marginesów i odstępów można wzorować na stronie BPE.

## Kolory marki

W *Księdze znaku* AHE znajdują się szczegółowe specyfikacje kolorów używanych w logo. Te kolory mogą służyć jako baza palety aplikacji:

| Element | Wartości CMYK | Wartości RGB | Kolor PANTONE | Opis |
|---|---|---|---|---|
| **Burgund (główna barwa logotypu)** | C 20  M 100  Y 64  K 20 | R 168  G 10  B 57 | **PANTONE 215C** | Stosowany w sygnetach oraz przyciskach (np. „Rekrutacja”)【802101499862182†screenshot】.  To nasycony kolor czerwono‑burgundowy – w zapisie heksadecymalnym około `#A80A39`. |
| **Szarość** | C 0  M 0  Y 0  K 80 | R 88  G 88  B 90 | **PANTONE Cool Gray 11c** | Używany jako uzupełniający kolor tła i ikon【802101499862182†screenshot】.  W systemie heksadecymalnym odpowiada `#58585A`. |
| **Czerń** | C 0  M 0  Y 0  K 100 | R 0  G 0  B 0 | **PANTONE Black C** | Kolor tekstu i elementów podkreślenia【802101499862182†screenshot】. |

Na stronie BPE pojawia się też **granatowy** prostokąt (nagłówek sekcji) oraz przyciski w odcieniach niebieskiego; prawdopodobnie odpowiada on barwie zbliżonej do `#263A71` (RGB około 38‑58‑113). Kolory te nie zostały bezpośrednio podane w księdze znaku – warto wybrać odcień ciemnego granatu, który zapewni odpowiedni kontrast z białym tekstem.

### Wskazówki implementacyjne

- Stosuj burgund (`#A80A39`) do elementów akcentowych: przycisków CTA („Rekrutacja”), ikon lub linków w stanach aktywnych.
- Używaj ciemnego granatu (`#263A71`) na paskach nagłówków, stopkach i tytułach sekcji. Zapewnia on profesjonalny wygląd i współgra z burgundem.
- Tekst podstawowy najlepiej pozostawić czarny (`#000000`) na białym tle, natomiast boczne menu można umieścić na jasnoszarym tle (`#F5F5F5`) – tak jak na stronie BPE.

## Fonty i typografia

- **Font logotypu**: Zgodnie z *Księgą znaku* w logo AHE użyto kroju **RomanaEU** w odmianie Normal【404330630084564†screenshot】. Jeżeli w aplikacji pojawi się tekstowy logotyp uczelni, należy zastosować tę czcionkę lub jej odpowiednik (serifowy krój z charakterystycznymi polskimi znakami).  Minimalny rozmiar znaku w sieci według księgi znaku to 128 px szerokości (logotyp) i 23 px wysokości (sygnet) – szczegóły znajdują się w rozdziałach o wielkościach minimalnych.
- **Fonty strony internetowej**: Na stronie BPE do nagłówków i nawigacji użyto nowoczesnej czcionki bezszeryfowej (w stylu **Lato**, **Montserrat** lub podobnej). Tekst główny wydaje się korzystać z klasycznej rodziny sans‑serif. Do zbudowania aplikacji można więc przyjąć dwa style:
  - **Nagłówki / elementy interfejsu** – lekka, geometryczna czcionka bezszeryfowa o wzmocnionej szerokości (np. Montserrat SemiBold) zapewniająca dobrą czytelność i nowoczesny wygląd.
  - **Treść główna** – neutralny sans‑serif (np. Open Sans, Lato) w wariancie Regular, z rozmiarem 16 – 18 px na urządzeniach mobilnych.

Pamiętaj, aby uwzględnić odpowiednie odstępy między wierszami (line‑height 1.5 – 1.6) oraz zwiększyć rozmiar nagłówków w stosunku do tekstu podstawowego.

## Logo i jego stosowanie

- Pełny znak AHE składa się z **sygnetu** (tarczy z orłem trzymającym stylizowaną księgę i monogram „ahe”) oraz **logotypu** „Akademia Humanistyczno‑Ekonomiczna w Łodzi”. Wariant podstawowy pokazano w księdze znaku【404330630084564†screenshot】.
- Logo powinno być umieszczone na białym tle lub w wersji monochromatycznej na ciemnym tle zgodnie z wariantami opisanymi w księdze znaku (kolory w skali szarości i czerni przedstawiono na stronach 4–10 PDF‑u). Logo w kolorze burgundowym na białym tle jest rekomendowanym wariantem. Na ciemnym tle należy użyć wersji jasnej (białej) lub z odwróconym sygnetem.
- **Link do księgi znaku**: pełny dokument z wersjami logo oraz specyfikacją kolorów dostępny jest na stronie uczelni w sekcji do pobrania: `https://www.ahe.lodz.pl/sites/default/files/pages/logo/ahe_ksiega_znakow.pdf`. W tym PDF‑ie można znaleźć wszystkie dopuszczalne układy znaku i wymogi dotyczące marginesów oraz minimalnych rozmiarów.

## Inne elementy wizualne

- **Ikonografia i akcenty**: Strona AHE wykorzystuje proste ikony line art, np. ikonę „osoby” w przycisku dostępności (widoczną w prawym dolnym rogu) oraz strzałki nawigacyjne. Kolor ikon zwykle odpowiada kolorowi tekstu lub barwie akcentowej.
- **Obrazy**: Sekcja hero zawiera duże zdjęcie o wysokim kontraście, które przedstawia studentów lub sceny z życia akademickiego【57159700990028†screenshot】.  Zdjęcia są rozciągnięte na pełną szerokość sekcji i przykryte półprzezroczystą warstwą w kolorze niebieskim, aby napis na nim był czytelny.
- **Kontrast**: Strona posiada funkcję zwiększenia kontrastu oraz możliwość powiększenia tekstu – w aplikacji warto rozważyć tryb wysokiego kontrastu oraz skalowanie czcionki dla użytkowników z trudnościami wzrokowymi.

## Podsumowanie i zalecenia dla aplikacji MVP

Aby aplikacja MVP nawiązywała 1:1 do stylistyki AHE, należy:

1. **Użyć dedykowanej palety barw** opartej na kolorze burgundowym (PANTONE 215C / `#A80A39`), ciemnym granacie (`#263A71`), chłodnej szarości (`#58585A`) oraz bieli.  Kolory te odpowiadają specyfikacji w księdze znaku【802101499862182†screenshot】.
2. **Zastosować font RomanaEU** wyłącznie w logotypie, natomiast dla nawigacji i treści wybrać nowoczesny sans‑serif (np. Montserrat i Open Sans), który wizualnie przypomina użyte na stronie czcionki【404330630084564†screenshot】.
3. **Odwzorować układ strony**: górny pasek z linkami, logo i przycisk rekrutacji; poziome menu główne; duża sekcja hero ze zdjęciem i tytułem; lewostronne menu sekcji; czytelne akapity z nagłówkami i listami punktowanymi【57159700990028†screenshot】.
4. **Zachować spójność ikon i przycisków** – ikonografia powinna być minimalistyczna, a przyciski i linki wyróżniać się kolorem burgundu. Używaj jasnej lub ciemnej wersji logo w zależności od tła.

Realizacja tych zaleceń pozwoli stworzyć aplikację MVP, która wizualnie i funkcjonalnie będzie zgodna z identyfikacją wizualną Akademii Humanistyczno‑Ekonomicznej w Łodzi.
