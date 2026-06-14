# AHE Łódź — `keyvisual_info`

## Cel dokumentu

Specyfikacja wizualna i layoutowa dla aplikacji MVP dopasowanej do serwisu Akademii Humanistyczno‑Ekonomicznej w Łodzi. Dokument powstał na podstawie:

- kodu HTML serwisu AHE,
- pełnego arkusza `/themes/custom/ahe/css/style.css`,
- oficjalnej księgi znaku AHE.

Najważniejsza korekta względem wcześniejszej analizy: dokładne fonty i kolory interfejsu są już znane z CSS — nie trzeba ich zgadywać.

---

## 1. Technologie i architektura frontendu AHE

Serwis korzysta z:

- Drupal 10,
- Bootstrap,
- Select2,
- Owl Carousel,
- własnego motywu `ahe`,
- CSS bez systemu zmiennych — wartości kolorów i odstępów są wpisane bezpośrednio w regułach.

Główny arkusz:

```text
/themes/custom/ahe/css/style.css
```

Dla MVP nie trzeba kopiować Drupala. Należy odwzorować design tokens, proporcje, komponenty i zachowania responsywne.

---

## 2. Typografia

### Font interfejsu i nagłówków

```css
font-family: "Mundial", sans-serif;
```

Font `Mundial` jest używany dla:

- całego interfejsu,
- nawigacji,
- nagłówków,
- przycisków,
- etykiet,
- kart,
- wyróżnionych liczb,
- tytułów sekcji.

### Font treści artykułów

```css
font-family: "Neue Haas Grotesk Text Pro", sans-serif;
font-weight: 300;
line-height: 1.8;
```

Stosowany do dłuższych tekstów i treści artykułów.

### Nagłówki w artykułach

```css
font-family: "Mundial", sans-serif;
font-weight: 600;
color: #343434;
line-height: 1.2;
```

### Font logo

W oficjalnym znaku uczelni użyto `RomanaEU Normal`. Nie należy używać go jako podstawowego fontu aplikacji. W aplikacji należy osadzać gotowy oficjalny plik logo.

### Ważne wdrożeniowo

W dostarczonym `style.css` nie ma deklaracji `@font-face`. Pliki fontów są prawdopodobnie ładowane w innym zasobie motywu. `Mundial` i `Neue Haas Grotesk Text Pro` są krojami licencjonowanymi. Dla wyglądu 1:1 należy uzyskać oficjalne webfonty od AHE.

Fallback podczas developmentu:

```css
--font-ui-fallback: Arial, Helvetica, sans-serif;
--font-body-fallback: "Helvetica Neue", Arial, sans-serif;
```

---

## 3. Oficjalna paleta interfejsu WWW

### Kolory podstawowe

| Token | HEX | Zastosowanie |
|---|---:|---|
| `--ahe-red` | `#A91539` | CTA, linki, aktywne elementy |
| `--ahe-navy` | `#222A56` | hero, nagłówki menu, aktywne filtry |
| `--ahe-heading` | `#343434` | nagłówki i główne etykiety |
| `--ahe-text` | `#515151` | tekst podstawowy |
| `--ahe-muted` | `#8B8B8B` | tekst pomocniczy |
| `--ahe-surface` | `#F1F1F1` | karty, formularze, footer |
| `--ahe-surface-dark` | `#E2E2E2` | separatory i submenu |
| `--ahe-surface-light` | `#F5F5F5` | mega-menu i dropdowny |
| `--ahe-border` | `#BBBBBB` | obramowania formularzy |
| `--ahe-white` | `#FFFFFF` | tekst na ciemnym tle |
| `--ahe-black` | `#000000` | gradienty i warianty logo |

### Kolor księgi znaku a kolor strony

Oficjalna księga znaku podaje burgund zbliżony do:

```text
Pantone 215 C
RGB 168 / 10 / 57
HEX około #A80A39
```

Aktualna strona WWW używa w interfejsie:

```text
#A91539
```

Dla dopasowania aplikacji do **aktualnego serwisu 1:1** należy używać `#A91539`.  
Dla materiałów stricte drukowanych lub zgodnych z księgą znaku należy konsultować `Pantone 215 C`.

### Gradient marki

Najczęstszy gradient:

```css
background: linear-gradient(90deg, #A91539 0%, #222A56 100%);
```

Występują także odwrócone kierunki:

```css
linear-gradient(270deg, #A91539 0%, #222A56 100%);
linear-gradient(135deg, #A91539 0%, #222A56 100%);
```

Zastosowanie:

- CTA „Rekrutacja”,
- linia nad footerem,
- górna linia kart,
- bloki informacyjne,
- elementy promocyjne.

---

## 4. Gotowe design tokens

```css
:root {
  --ahe-red: #A91539;
  --ahe-navy: #222A56;

  --ahe-heading: #343434;
  --ahe-text: #515151;
  --ahe-muted: #8B8B8B;

  --ahe-surface: #F1F1F1;
  --ahe-surface-dark: #E2E2E2;
  --ahe-surface-light: #F5F5F5;
  --ahe-border: #BBBBBB;

  --ahe-white: #FFFFFF;
  --ahe-black: #000000;

  --font-ui: "Mundial", Arial, Helvetica, sans-serif;
  --font-body: "Neue Haas Grotesk Text Pro", "Helvetica Neue", Arial, sans-serif;

  --radius: 0;
  --transition: 0.3s ease;

  --gradient-ahe: linear-gradient(90deg, var(--ahe-red), var(--ahe-navy));
  --gradient-ahe-reverse: linear-gradient(270deg, var(--ahe-red), var(--ahe-navy));
}
```

### Charakterystyczna zasada

AHE praktycznie nie używa zaokrągleń:

```css
border-radius: 0;
```

Wyjątki:

- okrągłe ikony,
- liczniki,
- elementy dostępności,
- drobne ikony statusów.

---

## 5. Struktura strony desktop

```text
Top bar
Header: logo + menu główne
Hero ze zdjęciem i tytułem
Breadcrumbs
Sidebar 4/12 + treść 8/12
Footer 3 kolumny
```

### Grid

Z kodu HTML:

```text
sidebar: col-xl-4
content: col-xl-8
logo: col-xl-3
menu: col-xl-9
```

Czyli:

- sidebar około 33%,
- treść około 67%,
- logo około 25% headera,
- nawigacja około 75%.

---

## 6. Top bar

```css
position: absolute;
top: 0;
padding: 15px 0 10px;
z-index: 3;
```

Typografia:

```css
font-size: 12px;
font-weight: 300;
text-transform: uppercase;
color: #FFFFFF;
```

Zawiera:

- wybór miasta,
- Wirtualny Pokój Studenta,
- Wirtualny Pokój Dydaktyka,
- Platformę Akademii.

W aplikacji można ten element uprościć do cienkiej belki narzędziowej lub pominąć na ekranach po zalogowaniu.

---

## 7. Header i nawigacja

### Header desktop

```css
.header_container {
  position: absolute;
  top: 50px;
  width: 100%;
}

header.main_header {
  background: #FFFFFF;
  padding: 0 30px;
  z-index: 3;
}
```

Logo:

```css
max-width: 200px;
```

Elementy menu:

```css
padding: 30px 10px;
color: #343434;
```

### CTA „Rekrutacja”

```css
background: linear-gradient(135deg, #A91539 0%, #222A56 100%);
color: #FFFFFF;
padding: 30px 40px 30px 20px;
```

CTA ma ikonę strzałki:

```text
/themes/custom/ahe/img/go.svg
```

### Mega-menu desktop

Od `1199 px`:

```css
grid-template-columns: 1fr 1fr 1fr;
padding: 40px 40px 30px 50px;
background: #F5F5F5;
```

Nagłówek grupy:

```css
font-size: 20px;
font-weight: 500;
border-bottom: 1px solid #BBBBBB;
```

---

## 8. Hero

### Wymiary

```css
height: 60vh;
min-height: 600px;
background-size: cover;
background-position: center;
```

Strona główna:

```css
height: 90vh;
```

### Górny gradient poprawiający czytelność

```css
height: 30%;
background: linear-gradient(
  180deg,
  #000000A1 0%,
  #80808000 100%
);
```

### Położenie tytułu

```css
bottom: 50px;
```

### Tytuł hero

```css
background: #222A56;
color: #FFFFFF;
padding: 10px 20px 16px;
font-weight: 600;
line-height: 1.5;
```

Efekt tekstu w kilku liniach uzyskano przez:

```css
box-decoration-break: clone;
-webkit-box-decoration-break: clone;
```

To jeden z najbardziej charakterystycznych elementów key visual AHE.

---

## 9. Breadcrumbs

```css
margin-bottom: 20px;
font-size: 15px;
```

Separator jest rysowany CSS-em jako chevron:

```css
width: 8px;
height: 8px;
border-right: 2px solid #CCC;
border-bottom: 2px solid #CCC;
transform: rotate(-45deg);
```

Pierwszy link może być wyróżniony burgundem.

---

## 10. Sidebar

### Nagłówek

```css
background: #222A56;
color: #FFFFFF;
padding: 18px 20px;
font-size: 16px;
```

### Element podstawowy

```css
background: #F1F1F1;
color: #343434;
padding: 12px 25px;
border-bottom: 7px solid #E2E2E2;
```

### Element aktywny

```css
border-bottom-color: #A91539;
```

### Element drugiego poziomu

```css
background: #E2E2E2;
padding: 10px 25px 10px 45px;
```

Aktywny tekst submenu:

```css
color: #A91539;
```

Sidebar nie jest kartą z cienką ramką. Jest zbudowany z mocnych, prostokątnych bloków i grubych separatorów.

---

## 11. Treść

### Kontener

```css
.main_content {
  margin-top: 50px;
}
```

### Tekst artykułu

```css
font-family: "Neue Haas Grotesk Text Pro", sans-serif;
font-weight: 300;
line-height: 1.8;
color: #515151;
```

### Nagłówki

```css
font-family: "Mundial", sans-serif;
font-weight: 600;
line-height: 1.2;
color: #343434;
```

### Listy

Standardowy punkt listy:

```css
width: 4px;
height: 4px;
background: #A91539;
```

AHE zamiast domyślnych kropek stosuje małe burgundowe kwadraty.

---

## 12. Przyciski

### Czerwony CTA

```css
background: #A91539;
color: #FFFFFF;
padding: 15px 25px;
font-size: 17px;
font-weight: 300;
font-family: "Mundial", sans-serif;
border: none;
border-radius: 0;
```

Alternatywny wariant:

```css
padding: 17px 22px;
```

### Granatowy CTA

```css
background: #222A56;
color: #FFFFFF;
padding: 17px 22px;
```

### Hover

```css
opacity: 0.9;
```

Nie stosować:

- mocnych cieni,
- dużych promieni zaokrąglenia,
- efektów glassmorphism,
- neonowych hoverów.

---

## 13. Formularze

Bazowe pola:

```css
background: #F1F1F1;
border: none;
padding: 8px 10px;
border-radius: 0;
```

Pola formularzy webowych:

```css
background: transparent;
border: 1px solid #BBBBBB;
padding: 10px;
color: #6C757D;
max-width: 600px;
```

Checkbox:

- obrys `#8B8B8B`,
- zaznaczenie `#A91539`,
- własny kwadrat, bez natywnego wyglądu przeglądarki.

Focus:

```css
box-shadow: none;
```

Dla aplikacji należy jednak dodać wyraźny focus WCAG, np.:

```css
outline: 3px solid rgba(169, 21, 57, 0.35);
outline-offset: 2px;
```

---

## 14. Karty i powierzchnie

Najczęstsza powierzchnia:

```css
background: #F1F1F1;
```

Charakterystyka:

- brak zaokrągleń,
- mało cieni,
- dużo paddingu,
- nagłówki `#343434`,
- burgundowe akcje,
- granatowe aktywne stany.

Typowe wartości paddingu:

```text
20 px
30 px
40 px
50 px
60 px
```

Jedyny wyraźny cień w głównych komponentach:

```css
box-shadow: 0 0 30px #51515124;
```

Jest stosowany m.in. w wyszukiwarce nachodzącej na hero.

---

## 15. Bloki gradientowe

```css
background: linear-gradient(270deg, #A91539 0%, #222A56 100%);
color: #FFFFFF;
padding: 50px;
```

Używane dla:

- ważnych komunikatów,
- sekcji promocyjnych,
- wyróżnionych treści,
- disclaimerów,
- CTA.

Nagłówki i tekst w takich blokach:

```css
color: #FFFFFF;
```

---

## 16. Gridy i listy kart

### Eksperci

Desktop:

```css
grid-template-columns: repeat(3, 1fr);
gap: 10px;
```

Do `992 px`:

```css
grid-template-columns: repeat(2, 1fr);
```

Do `550 px`:

```css
grid-template-columns: 1fr;
```

Karta eksperta ma:

- zdjęcie,
- gradient od transparentnego do ciemnego,
- biały tekst na dole,
- nazwę około `20 px`,
- opis około `12 px`.

### Aktualności

Desktop:

```css
grid-template-columns: repeat(3, 1fr);
gap: 30px;
```

Podstrona:

```css
grid-template-columns: repeat(2, 1fr);
```

Tło karty:

```css
background: #F1F1F1;
```

---

## 17. Footer

```css
background: #F1F1F1;
color: #515151;
font-weight: 300;
padding: 50px 0;
margin-top: 100px;
position: relative;
```

Górna linia:

```css
height: 8px;
background: linear-gradient(90deg, #A91539 0%, #222A56 100%);
```

Nagłówki:

```css
font-size: 26px;
margin-bottom: 20px;
```

Social media:

```css
width: 25px;
margin-right: 20px;
```

Na desktopie footer ma trzy kolumny. Poniżej `768 px` kolumny układają się pionowo i otrzymują `30 px` marginesu.

---

## 18. Breakpointy i responsywność

### `min-width: 1199px`

- desktopowe mega-menu,
- trzy kolumny submenu,
- hover otwiera menu.

### `max-width: 1500px`

- tytuł slidera zmniejszony do `40 px`.

### `max-width: 1400px`

- tekst slidera około `22 px`,
- ograniczenie szerokości wskaźników,
- korekta pozycji submenu.

### `max-width: 1199px`

Najważniejszy breakpoint aplikacyjny:

- top bar znika,
- header zaczyna się od góry,
- białe menu desktopowe znika,
- pojawia się hamburger,
- menu działa jako pełnoekranowy panel,
- tło panelu jest białe,
- body jest blokowane podczas otwartego menu,
- logo dostaje większą szerokość mobilną,
- menu jest pionowe,
- podmenu przesuwają się jak kolejne widoki,
- header otrzymuje czarny, półprzezroczysty gradient nad hero.

Hamburger:

```css
width: 30px;
height: 4px;
background: #FFFFFF;
```

### `max-width: 992px`

- grid ekspertów: 2 kolumny,
- część układów dwu- i trzykolumnowych przechodzi do jednej kolumny,
- bloki dziekana i filtrów układają się pionowo.

### `max-width: 768px`

- `.container` ma maksymalnie `90%` szerokości,
- footer przechodzi do jednej kolumny,
- hero title dostaje mobilne łamanie z granatowym tłem,
- listy i gradientowe bloki przechodzą do jednej kolumny,
- sidebar dostaje boczne paddingi `15 px`,
- tabele mogą przewijać się poziomo.

### `max-width: 600px`

- ambasadorzy: jedna kolumna,
- sekcje full-width otrzymują padding `30 px`.

### `max-width: 550px`

- eksperci: jedna kolumna,
- carousel przenosi podpis bliżej dołu,
- zdjęcie eksperta na stronie szczegółowej zajmuje pełną szerokość.

### `max-width: 500px`

- logo headera: maksymalnie `160 px`,
- logotypy partnerów: jedna kolumna,
- slider informacyjny: jedna kolumna,
- tytuł carousel około `34 px`.

---

## 19. Oficjalne assety

### Logo

```text
https://www.ahe.lodz.pl/sites/default/files/ahe_black.webp
https://www.ahe.lodz.pl/sites/default/files/ahe_white.webp
```

Zastosowanie:

- `ahe_black.webp` — jasne tło,
- `ahe_white.webp` — ciemne tło lub hero.

### Księga znaku

```text
https://www.ahe.lodz.pl/sites/default/files/pages/logo/ahe_ksiega_znakow.pdf
```

### Hero analizowanej strony

```text
https://www.ahe.lodz.pl/sites/default/files/2023-11/dla_osob_z_niepelnosprawnoscia.jpg
```

### Ikony i elementy UI

```text
/themes/custom/ahe/img/go.svg
/themes/custom/ahe/img/menu_arrow.png
/themes/custom/ahe/img/circle_plus.svg
/themes/custom/ahe/img/circle_minus.svg
/themes/custom/ahe/img/check-circle.svg
/themes/custom/ahe/img/icon_menu.svg
/themes/custom/ahe/img/back.svg
/themes/custom/ahe/img/place.svg
```

W aplikacji należy skopiować wyłącznie assety, do których projekt ma prawo użycia. Najbezpieczniej zachować oficjalne logo AHE i odtworzyć zwykłe ikony przy pomocy jednej biblioteki, np. Lucide.

---

## 20. Zasady dostępności

Serwis HTML przewiduje:

- powiększanie i zmniejszanie tekstu,
- wysoki kontrast,
- odwrócony kontrast,
- podkreślanie linków,
- reset ustawień,
- `aria-current`,
- `aria-labelledby`,
- ukryte wizualnie nagłówki dla czytników ekranowych.

Dla MVP należy zachować:

- kontrast co najmniej WCAG AA,
- focus visible,
- obsługę klawiatury,
- minimalny obszar dotykowy `44 × 44 px`,
- skalowanie tekstu,
- poprawne etykiety formularzy,
- brak informacji przekazywanych wyłącznie kolorem.

---

## 21. Minimalny styl aplikacji MVP

Aplikacja nie powinna kopiować całego portalu uczelni jako strony WWW. Powinna przejąć jego język wizualny:

### App shell

```text
Header biały
Logo AHE po lewej
Nawigacja lub profil po prawej
Granatowe nagłówki sekcji
Burgundowe CTA
Jasnoszare powierzchnie
Brak zaokrąglonych kart
```

### Dashboard

- tło główne: `#FFFFFF`,
- karty: `#F1F1F1`,
- nagłówki: `#343434`,
- tekst: `#515151`,
- CTA: `#A91539`,
- aktywna nawigacja: `#222A56`,
- pasek aktywny lub status: gradient AHE,
- ikony: proste, liniowe, bez wielokolorowych ilustracji.

### Stan aktywny

Najbardziej zgodne rozwiązanie:

```css
border-bottom: 7px solid #A91539;
```

Dla kompaktowej aplikacji można zmniejszyć grubość do `3–4 px`, zachowując ten sam język wizualny.

---

## 22. Gotowy fundament CSS dla MVP

```css
:root {
  --ahe-red: #A91539;
  --ahe-navy: #222A56;
  --ahe-heading: #343434;
  --ahe-text: #515151;
  --ahe-muted: #8B8B8B;
  --ahe-surface: #F1F1F1;
  --ahe-surface-dark: #E2E2E2;
  --ahe-surface-light: #F5F5F5;
  --ahe-border: #BBBBBB;
  --ahe-white: #FFFFFF;

  --font-ui: "Mundial", Arial, Helvetica, sans-serif;
  --font-body: "Neue Haas Grotesk Text Pro", "Helvetica Neue", Arial, sans-serif;

  --gradient-ahe: linear-gradient(90deg, #A91539, #222A56);
}

body {
  margin: 0;
  color: var(--ahe-text);
  background: var(--ahe-white);
  font-family: var(--font-ui);
  overflow-x: hidden;
}

.app-content {
  font-family: var(--font-body);
  font-weight: 300;
  line-height: 1.8;
}

h1,
h2,
h3,
h4 {
  color: var(--ahe-heading);
  font-family: var(--font-ui);
  font-weight: 600;
  line-height: 1.2;
}

button,
input,
select,
textarea,
.card {
  border-radius: 0;
}

.btn-primary {
  border: 0;
  background: var(--ahe-red);
  color: var(--ahe-white);
  padding: 15px 25px;
  font-family: var(--font-ui);
}

.btn-secondary {
  border: 0;
  background: var(--ahe-navy);
  color: var(--ahe-white);
  padding: 15px 25px;
}

.card {
  background: var(--ahe-surface);
  padding: 30px;
}

.section-title {
  display: inline;
  background: var(--ahe-navy);
  color: var(--ahe-white);
  padding: 10px 20px 16px;
  box-decoration-break: clone;
  -webkit-box-decoration-break: clone;
}

.brand-line {
  height: 8px;
  background: var(--gradient-ahe);
}
```

---

## 23. Elementy obowiązkowe dla zgodności wizualnej

1. Font `Mundial` w interfejsie i nagłówkach.
2. Font `Neue Haas Grotesk Text Pro` w dłuższej treści.
3. Granat `#222A56`.
4. Burgund `#A91539`.
5. Nagłówki `#343434`.
6. Tekst `#515151`.
7. Jasnoszare powierzchnie `#F1F1F1`.
8. Prostokątne komponenty bez zaokrągleń.
9. Gradient burgund → granat.
10. Hero title na granatowym, wielowierszowym tle.
11. Oficjalne logo czarne lub białe zależnie od tła.
12. Responsywne menu przełączane przy około `1199 px`.
13. Czytelny panel dostępności i widoczny focus.

---

## 24. Czego nie stosować

- zaokrągleń `16–24 px`,
- pastelowego UI,
- glassmorphism,
- wielu cieni,
- fontów Montserrat, Poppins lub Open Sans jako rzekomo oficjalnych,
- przybliżonego granatu `#263A71` — właściwy kolor WWW to `#222A56`,
- przybliżonego burgundu `#A80A39` jako koloru całego UI — strona używa `#A91539`,
- gradientów niezwiązanych z burgundem i granatem,
- kolorowych ikon z różnych zestawów,
- tekstowego odtwarzania logotypu zamiast oficjalnego assetu.

---

## 25. Finalna rekomendacja

Dla aplikacji MVP należy stworzyć nowoczesny interfejs aplikacyjny, ale utrzymać dokładny system wizualny serwisu AHE:

```text
Mundial + Neue Haas Grotesk Text Pro
#A91539 + #222A56
#343434 + #515151
#F1F1F1 + #E2E2E2
brak zaokrągleń
gradient burgund–granat
duża typografia i dużo białej przestrzeni
```

To jest najkrótszy zestaw zasad, który sprawi, że aplikacja będzie natychmiast rozpoznawalna jako produkt powiązany z AHE.
