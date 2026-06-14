# StudentSpot — oficjalne koła naukowe AHE do zasilenia aplikacji

**Stan weryfikacji: 14 czerwca 2026 r.**

Ten plik jest źródłem danych dla modułu `clubs` w StudentSpot. Zawiera wyłącznie koła znalezione w oficjalnym serwisie AHE. Nie oznacza to jednak, że każde koło jest obecnie aktywne — część podstron ma treść archiwalną. Dlatego każdy rekord ma status weryfikacji.

## Zasady implementacji

1. Wyświetlaj domyślnie w rekomendacjach tylko rekordy ze statusem `active_verified`.
2. Rekordy `official_needs_verification` zachowaj w bazie, ale ukryj z publicznej listy do czasu potwierdzenia przez administratora.
3. Nazwiska opiekunów i publiczne e-maile są danymi informacyjnymi koła. **Nie twórz na ich podstawie kont użytkowników ani kont demo.**
4. Angielskie nazwy i opisy poniżej są tłumaczeniami roboczymi dla aplikacji, a nie oficjalnymi angielskimi nazwami AHE.
5. Każdy rekord musi przechowywać:
   - `source_url`,
   - `verification_status`,
   - `last_verified_at`,
   - `campus`,
   - `official_name_pl`,
   - `display_name_en`,
   - `major_slugs`,
   - `guardian_name`,
   - `contact_email`,
   - `is_public`.
6. Użytkownik nie może sam nadać sobie roli przewodniczącego. Każde członkostwo i rola wymagają zatwierdzenia przez opiekuna lub administratora.

## Statusy danych

- `active_verified` — oficjalna strona zawiera współczesne informacje, wydarzenie z lat 2025–2026 albo aktualny skład i kontakt.
- `official_needs_verification` — istnieje oficjalna podstrona AHE, ale treść jest stara, nie zawiera aktualnego składu albo nie potwierdza bieżącej aktywności.
- `archived` — rekord pozostaje wyłącznie historyczny i nie powinien być dostępny w publicznym katalogu.

## Skrócona lista

| Koło | Kierunek | Status |
|---|---|---|
| AIrON | Informatyka | `active_verified` |
| Kognitywistyczno-Eksperymentalne Koło Naukowe | Kognitywistyka | `active_verified` |
| Koło Naukowe Grafika | Grafika | `active_verified` |
| Warsztaty Emocji | Pedagogika | `active_verified` |
| Progressus | Zarządzanie, Ekonomia | `active_verified` |
| Wkręceni | Kulturoznawstwo | `active_verified` |
| Koło Naukowe Pedagogiki Dziecka | Pedagogika przedszkolna i wczesnoszkolna | `active_verified` |
| Moja Psychologia | Psychologia | `official_needs_verification` |
| Studenckie Koło Naukowe Pielęgniarstwa | Pielęgniarstwo | `official_needs_verification` |
| Koło Profilowania Kryminalistycznego | Filologia polska | `official_needs_verification` |
| Koło Naukowe Młodych Dziennikarzy | Dziennikarstwo, Filologia polska | `official_needs_verification` |
| Europa Nostra | Administracja | `official_needs_verification` |
| Koło Naukowe Młodego Samorządowca | Administracja | `official_needs_verification` |

# Rekordy szczegółowe

## 1. Koło Naukowe AIrON

- **Slug:** `airon`
- **Kierunek:** Informatyka
- **Status:** `active_verified`
- **Opiekun:** mgr inż. Zoltan Farkas
- **Opis PL:** Koło skupia studentów informatyki zainteresowanych sztuczną inteligencją, programowaniem, tworzeniem aplikacji, API, bazami danych, UX oraz projektami zespołowymi. Oficjalne materiały AHE opisują udział zespołu w 24-godzinnym FCP Hackathon: Łódź_Hack, podczas którego zbudowano stabilne MVP miejskiego portalu usług z modułem AI klasyfikującym opinie. W styczniu 2026 r. rada programowa kierunku ustaliła powołanie nowych sekcji AIrON.
- **Description EN:** A student research group for computer science students interested in artificial intelligence, software development, APIs, databases, user experience and team projects.
- **Tagi:** `AI`, `programowanie`, `aplikacje`, `API`, `bazy danych`, `UX`, `hackathony`
- **Preferowane sale:** K320, K200A oraz inne sale komputerowe
- **Oficjalne źródła:**
  - https://airon.ahe.lodz.pl/
  - https://www.ahe.lodz.pl/aktualnosci/studenci-kola-naukowego-airon-ahe-na-hackathonie-fcp
  - https://www.ahe.lodz.pl/aktualnosci/studenci-kola-airon-reprezentowali-ahe-na-poznan-game-arena
  - https://www.ahe.lodz.pl/informatyka/rada-programowa/200126
- **Uwaga:** dostępność strony `airon.ahe.lodz.pl` należy ponownie sprawdzić podczas wdrożenia; w razie niedostępności użyć jako źródła oficjalnych aktualności AHE.

## 2. Kognitywistyczno-Eksperymentalne Koło Naukowe

- **Slug:** `kognitywistyczno-eksperymentalne`
- **Kierunek:** Kognitywistyka
- **Status:** `active_verified`
- **Opiekun:** dr Rafał Tryścień
- **Opis PL:** Koło rozwija zainteresowania badaniami nad umysłem, poznaniem i sztuczną inteligencją. Popularyzuje kognitywistykę, neurokognitywistykę i filozofię umysłu, wspiera inicjatywy badawcze oraz organizację warsztatów, konferencji i spotkań naukowych. Oficjalne rozpoczęcie działalności opisano po spotkaniu inauguracyjnym z 12 kwietnia 2025 r.
- **Description EN:** An interdisciplinary research group focused on cognition, mind, experimental research, neurocognitive science and artificial intelligence.
- **Tagi:** `kognitywistyka`, `neuronauka`, `AI`, `psychologia poznawcza`, `badania eksperymentalne`
- **Preferowane sale:** K200A, sale szkoleniowe, Laboratorium Badań Kognitywnych
- **Źródło:** https://www.ahe.lodz.pl/kognitywistyka/kolo-naukowe

## 3. Koło Naukowe Grafika

- **Slug:** `grafika`
- **Kierunek:** Grafika
- **Status:** `active_verified`
- **Opiekun:** mgr Klaudia Gołojuch
- **Kontakt:** `kngrafika.ahe@gmail.com`
- **Opis PL:** Koło działa przy Wydziale Artystycznym od 2023 r. Rozwija kreatywność, dobry proces projektowy, umiejętności grafiki tradycyjnej i cyfrowej oraz networking między studentami, dydaktykami i otoczeniem społeczno-gospodarczym. Członkowie realizują projekty artystyczne i użytkowe, wystawy oraz działania portfolio.
- **Description EN:** A creative research group for students interested in graphic design, visual arts, photography, animation, digital tools and exhibitions.
- **Tagi:** `grafika`, `design`, `fotografia`, `animacja`, `wystawy`, `portfolio`
- **Preferowane sale:** K320, pracownie artystyczne, K200A
- **Źródło:** https://www.ahe.lodz.pl/grafika/kolo-naukowe-grafika

## 4. Koło Arteterapeutyczne „Warsztaty Emocji”

- **Slug:** `warsztaty-emocji`
- **Kierunki:** Pedagogika; dodatkowo otwarte dla zainteresowanych studentów innych kierunków
- **Status:** `active_verified`
- **Opiekun:** mgr Agnieszka Wójcik
- **Kontakt:** `awojcik@ahe.email`
- **Opis PL:** Koło działa od roku akademickiego 2023/2024. Organizuje warsztaty i projekty arteterapeutyczne, integruje środowisko studenckie, rozwija kreatywność oraz wspiera działalność publikacyjną. Oficjalna strona wskazuje cykliczne spotkania i wydarzenie zaplanowane na 27 marca 2026 r. w sali K005.
- **Description EN:** An art therapy group using creative activities to support student development, integration, reflection and project work.
- **Tagi:** `arteterapia`, `pedagogika`, `sztuka`, `emocje`, `warsztaty`, `integracja`
- **Preferowane sale:** K005, sale warsztatowe, sale dostępne bez barier
- **Źródło:** https://www.ahe.lodz.pl/pedagogika/kola-naukowe/kolo-arteterapeutyczne

## 5. Koło Naukowe Progressus

- **Slug:** `progressus`
- **Kierunki:** Zarządzanie, Ekonomia
- **Status:** `active_verified`
- **Opiekun:** mgr Anna Bojanowska-Sosnowska
- **Kontakty:** `progressus@ahe.lodz.pl`, `bbogusz@ahe.lodz.pl`
- **Opis PL:** Koło działa przy Wydziale Ekonomii i Zarządzania i powstało na początku 2024 r. Wspiera projekty badawcze, konferencje, warsztaty edukacyjne, wyjazdy technologiczne i kontakty z otoczeniem biznesowym. Stawia na realizację pomysłów studentów, rozwój organizacyjny i naukowy.
- **Description EN:** A management and economics student group focused on practical projects, research, conferences, business relations and technology visits.
- **Tagi:** `zarządzanie`, `ekonomia`, `biznes`, `projekty`, `konferencje`, `organizacja`
- **Preferowane sale:** sale konferencyjne, K200A, A01
- **Źródło:** https://www.ahe.lodz.pl/zarzadzanie/kolo-naukowe-progressus

## 6. Studenckie Koło Naukowe Miłośników Kultury „Wkręceni”

- **Slug:** `wkreceni`
- **Kierunek:** Kulturoznawstwo
- **Status:** `active_verified`
- **Opiekunki:** dr Katarzyna Filutowska, mgr Monika Kamieńska
- **Kontakty:** `katarzyna.filutowska@ahe.email`, `mkamienska@ahe.lodz.pl`
- **Opis PL:** Koło zrzesza studentów zainteresowanych kulturą i zarządzaniem kulturą. Organizuje prelekcje dotyczące teatru, sztuki, gier, sztucznej inteligencji i neuroestetyki, wspiera udział w konferencjach, projekty naukowe, publikacje oraz wydarzenia badawcze i kulturalne. Koło reaktywowano w maju 2023 r., a oficjalna strona wymienia wydarzenia z 2025 r.
- **Description EN:** A cultural studies group supporting lectures, cultural events, research projects, academic publications and conference participation.
- **Tagi:** `kultura`, `sztuka`, `teatr`, `gry`, `AI`, `wydarzenia kulturalne`
- **Preferowane sale:** A01, A03, sale konferencyjne i audialne
- **Źródło:** https://www.ahe.lodz.pl/kulturoznawstwo/kola-naukowe/kolo-wkreceni

## 7. Koło Naukowe Pedagogiki Dziecka

- **Slug:** `pedagogika-dziecka`
- **Kierunek:** Pedagogika przedszkolna i wczesnoszkolna
- **Status:** `active_verified`
- **Opiekun:** dr Daria Modrzejewska
- **Kontakt:** `dmodrzejewska@ahe.lodz.pl`
- **Opis PL:** Koło rozwija życie naukowe oraz wiedzę i umiejętności z zakresu pedagogiki przedszkolnej i wczesnoszkolnej, teorii wychowania, dydaktyki i psychologii rozwoju dziecka. Organizuje spotkania naukowe, warsztaty, konferencje, badania i spotkania otwarte dla społeczności akademickiej.
- **Description EN:** A child education research group focused on preschool and early school pedagogy, teaching methods, developmental psychology and educational research.
- **Tagi:** `pedagogika dziecka`, `edukacja`, `dydaktyka`, `psychologia rozwoju`, `warsztaty`
- **Preferowane sale:** sale szkoleniowe i warsztatowe, K200A
- **Źródło:** https://www.ahe.lodz.pl/pedagogika-przedszkolna-i-wczesnoszkolna/kola-naukowe/kolo-naukowo-metodyczne

## 8. Koło Naukowe „Moja Psychologia”

- **Slug:** `moja-psychologia`
- **Kierunek:** Psychologia
- **Status:** `official_needs_verification`
- **Opiekun / kontakt z oficjalnej strony:** dr Joanna Paul-Kańska, `jpaul@ahe.lodz.pl`
- **Opis PL:** Oficjalna strona opisuje spotkania, rozmowy i dyskusje, webinary z wykładowcami i specjalistami oraz możliwość realizowania projektów badawczych, konferencji, szkoleń, warsztatów i seminariów.
- **Description EN:** A psychology student group offering discussions, webinars, research projects, workshops, seminars and conference activities.
- **Tagi:** `psychologia`, `badania`, `webinary`, `rozwój`, `warsztaty`
- **Powód weryfikacji:** treść oficjalnej strony odnosi się do okresu pandemii i nie potwierdza jednoznacznie bieżącej aktywności w 2026 r.
- **Źródło:** https://www.ahe.lodz.pl/psychologia/kolo-naukowe-moja-psychologia

## 9. Studenckie Koło Naukowe Pielęgniarstwa

- **Slug:** `pielegniarstwo`
- **Kierunek:** Pielęgniarstwo
- **Status:** `official_needs_verification`
- **Opiekun z oficjalnej strony:** mgr Aleksandra Zdrojewska
- **Opis PL:** Koło powstało w 2004 r. i służy poszerzaniu wiedzy z zakresu współczesnego pielęgniarstwa, poznawaniu jego interdyscyplinarnego charakteru oraz rozwijaniu zainteresowań naukowych. Studenci są zachęcani do pisania prac i wystąpień konferencyjnych.
- **Description EN:** A nursing research group focused on contemporary nursing, interdisciplinary practice, scientific writing and conference participation.
- **Tagi:** `pielęgniarstwo`, `medycyna`, `badania`, `konferencje`, `zdrowie`
- **Preferowane sale:** Centrum Symulacji Medycznej, sale szkoleniowe
- **Powód weryfikacji:** oficjalna strona nie podaje aktualnego składu ani wydarzenia z lat 2025–2026.
- **Źródło:** https://www.ahe.lodz.pl/pielegniarstwo/kola-naukowe

## 10. Studenckie Koło Naukowe Profilowania Kryminalistycznego

- **Slug:** `profilowanie-kryminalistyczne`
- **Kierunek:** Filologia polska
- **Status:** `official_needs_verification`
- **Prowadzące z oficjalnej strony:** mgr Justyna Wolter, dr Natalia Piórczyńska-Krawczyńska
- **Opis PL:** Koło łączy filologię polską, psychologię postaci i profilowanie kryminalistyczne. Analizuje motywy działania przestępców, zachowania, wpływ środowiska i wykorzystanie wiedzy analitycznej do budowania wiarygodnych postaci oraz fabuł.
- **Description EN:** A Polish studies research group combining criminal profiling, character psychology and narrative construction.
- **Tagi:** `profilowanie`, `kryminologia`, `psychologia postaci`, `literatura`, `fabuła`
- **Powód weryfikacji:** oficjalna strona nie wskazuje aktualnej daty ani bieżących wydarzeń.
- **Źródło:** https://www.ahe.lodz.pl/filologia-polska/kola-naukowe

## 11. Koło Naukowe Młodych Dziennikarzy

- **Slug:** `mlodzi-dziennikarze`
- **Kierunki:** Dziennikarstwo i komunikacja społeczna, Filologia polska
- **Status:** `official_needs_verification`
- **Opis PL:** Oficjalna strona opisuje interdyscyplinarne koło studentów dziennikarstwa i filologii polskiej, które współtworzyło gazetę studencką „Głos Akademii”, przygotowywało artykuły oraz dzieliło role redakcyjne.
- **Description EN:** A journalism and Polish studies student group focused on editorial work, writing, reporting and student media.
- **Tagi:** `dziennikarstwo`, `media`, `redakcja`, `artykuły`, `komunikacja`
- **Powód weryfikacji:** główny opis dotyczy działalności rozpoczętej w 2013 r. i nie zawiera współczesnego składu.
- **Źródło:** https://www.ahe.lodz.pl/dziennikarstwo/kola-naukowe

## 12. Koło Naukowe Studentów Administracji „Europa Nostra”

- **Slug:** `europa-nostra`
- **Kierunek:** Administracja
- **Status:** `official_needs_verification`
- **Opiekun wskazany na stronie:** mgr Mariusz Olężałek
- **Opis PL:** Koło rozwija zainteresowania prawem i administracją, organizuje konferencje, wspiera inicjatywy studenckie, integrację, wyjazdy naukowe i szkoleniowe oraz podnoszenie kwalifikacji zawodowych.
- **Description EN:** A public administration student group focused on administrative law, conferences, student initiatives and professional development.
- **Tagi:** `administracja`, `prawo`, `samorząd`, `konferencje`, `rozwój zawodowy`
- **Powód weryfikacji:** opis dotyczy koła utworzonego w 2010 r. i nie potwierdza aktualnej działalności w Łodzi.
- **Źródło:** https://www.ahe.lodz.pl/administracja/kola_naukowe

## 13. Studenckie Koło Naukowe Młodego Samorządowca

- **Slug:** `mlody-samorzadowiec`
- **Kierunek:** Administracja
- **Status:** `official_needs_verification`
- **Opis PL:** Koło rozwija praktyczną wiedzę z administracji samorządowej, świadomość prawną oraz zainteresowania samorządnością, polityką lokalną i społeczeństwem. Ma wspierać badania, działalność organizatorską i pracę grupową.
- **Description EN:** A local government and public administration group focused on legal awareness, local policy, research and teamwork.
- **Tagi:** `samorząd`, `administracja`, `prawo`, `polityka lokalna`, `społeczeństwo`
- **Powód weryfikacji:** podstrona opisuje powstanie koła w 2011 r. i nie zawiera aktualnego składu.
- **Źródło:** https://www.ahe.lodz.pl/administracja/kola_naukowe

# Dane seed w formacie YAML

Codex ma przenieść poniższe dane do kodu seedującego. `guardian_name` i `contact_email` są wyłącznie metadanymi katalogowymi — nie tworzą kont.

```yaml
clubs:
  - slug: airon
    official_name_pl: "Koło Naukowe AIrON"
    display_name_en: "AIrON Student Research Group"
    campus: "lodz"
    major_slugs: ["informatyka"]
    verification_status: "active_verified"
    last_verified_at: "2026-06-14"
    guardian_name: "mgr inż. Zoltan Farkas"
    contact_email: null
    source_url: "https://www.ahe.lodz.pl/aktualnosci/studenci-kola-naukowego-airon-ahe-na-hackathonie-fcp"
    website_url: "https://airon.ahe.lodz.pl/"
    tags: ["AI", "programowanie", "API", "bazy danych", "UX", "hackathony"]
    is_public: true
    is_featured: true

  - slug: kognitywistyczno-eksperymentalne
    official_name_pl: "Kognitywistyczno-Eksperymentalne Koło Naukowe"
    display_name_en: "Cognitive and Experimental Research Group"
    campus: "lodz"
    major_slugs: ["kognitywistyka"]
    verification_status: "active_verified"
    last_verified_at: "2026-06-14"
    guardian_name: "dr Rafał Tryścień"
    contact_email: null
    source_url: "https://www.ahe.lodz.pl/kognitywistyka/kolo-naukowe"
    tags: ["kognitywistyka", "neuronauka", "AI", "badania eksperymentalne"]
    is_public: true
    is_featured: true

  - slug: grafika
    official_name_pl: "Koło Naukowe Grafika"
    display_name_en: "Graphic Design Student Research Group"
    campus: "lodz"
    major_slugs: ["grafika"]
    verification_status: "active_verified"
    last_verified_at: "2026-06-14"
    guardian_name: "mgr Klaudia Gołojuch"
    contact_email: "kngrafika.ahe@gmail.com"
    source_url: "https://www.ahe.lodz.pl/grafika/kolo-naukowe-grafika"
    tags: ["grafika", "design", "fotografia", "animacja", "wystawy"]
    is_public: true
    is_featured: true

  - slug: warsztaty-emocji
    official_name_pl: "Koło Arteterapeutyczne Warsztaty Emocji"
    display_name_en: "Emotions Workshop Art Therapy Group"
    campus: "lodz"
    major_slugs: ["pedagogika"]
    verification_status: "active_verified"
    last_verified_at: "2026-06-14"
    guardian_name: "mgr Agnieszka Wójcik"
    contact_email: "awojcik@ahe.email"
    source_url: "https://www.ahe.lodz.pl/pedagogika/kola-naukowe/kolo-arteterapeutyczne"
    tags: ["arteterapia", "pedagogika", "sztuka", "emocje", "warsztaty"]
    is_public: true
    is_featured: true

  - slug: progressus
    official_name_pl: "Koło Naukowe Progressus"
    display_name_en: "Progressus Student Research Group"
    campus: "lodz"
    major_slugs: ["zarzadzanie", "ekonomia"]
    verification_status: "active_verified"
    last_verified_at: "2026-06-14"
    guardian_name: "mgr Anna Bojanowska-Sosnowska"
    contact_email: "progressus@ahe.lodz.pl"
    source_url: "https://www.ahe.lodz.pl/zarzadzanie/kolo-naukowe-progressus"
    tags: ["zarządzanie", "ekonomia", "biznes", "projekty", "konferencje"]
    is_public: true
    is_featured: true

  - slug: wkreceni
    official_name_pl: "Studenckie Koło Naukowe Miłośników Kultury Wkręceni"
    display_name_en: "Wkręceni Cultural Studies Group"
    campus: "lodz"
    major_slugs: ["kulturoznawstwo"]
    verification_status: "active_verified"
    last_verified_at: "2026-06-14"
    guardian_name: "dr Katarzyna Filutowska; mgr Monika Kamieńska"
    contact_email: "katarzyna.filutowska@ahe.email"
    source_url: "https://www.ahe.lodz.pl/kulturoznawstwo/kola-naukowe/kolo-wkreceni"
    tags: ["kultura", "sztuka", "teatr", "gry", "AI", "wydarzenia"]
    is_public: true
    is_featured: true

  - slug: pedagogika-dziecka
    official_name_pl: "Koło Naukowe Pedagogiki Dziecka"
    display_name_en: "Child Education Research Group"
    campus: "lodz"
    major_slugs: ["pedagogika-przedszkolna-i-wczesnoszkolna"]
    verification_status: "active_verified"
    last_verified_at: "2026-06-14"
    guardian_name: "dr Daria Modrzejewska"
    contact_email: "dmodrzejewska@ahe.lodz.pl"
    source_url: "https://www.ahe.lodz.pl/pedagogika-przedszkolna-i-wczesnoszkolna/kola-naukowe/kolo-naukowo-metodyczne"
    tags: ["pedagogika dziecka", "edukacja", "dydaktyka", "psychologia rozwoju"]
    is_public: true
    is_featured: true

  - slug: moja-psychologia
    official_name_pl: "Koło Naukowe Moja Psychologia"
    display_name_en: "My Psychology Student Research Group"
    campus: "lodz"
    major_slugs: ["psychologia"]
    verification_status: "official_needs_verification"
    last_verified_at: "2026-06-14"
    guardian_name: "dr Joanna Paul-Kańska"
    contact_email: "jpaul@ahe.lodz.pl"
    source_url: "https://www.ahe.lodz.pl/psychologia/kolo-naukowe-moja-psychologia"
    tags: ["psychologia", "badania", "webinary", "warsztaty"]
    is_public: false
    is_featured: false

  - slug: pielegniarstwo
    official_name_pl: "Studenckie Koło Naukowe Pielęgniarstwa"
    display_name_en: "Nursing Student Research Group"
    campus: "lodz"
    major_slugs: ["pielegniarstwo"]
    verification_status: "official_needs_verification"
    last_verified_at: "2026-06-14"
    guardian_name: "mgr Aleksandra Zdrojewska"
    contact_email: null
    source_url: "https://www.ahe.lodz.pl/pielegniarstwo/kola-naukowe"
    tags: ["pielęgniarstwo", "medycyna", "badania", "konferencje"]
    is_public: false
    is_featured: false

  - slug: profilowanie-kryminalistyczne
    official_name_pl: "Studenckie Koło Naukowe Profilowania Kryminalistycznego"
    display_name_en: "Criminal Profiling Student Research Group"
    campus: "lodz"
    major_slugs: ["filologia-polska"]
    verification_status: "official_needs_verification"
    last_verified_at: "2026-06-14"
    guardian_name: "mgr Justyna Wolter; dr Natalia Piórczyńska-Krawczyńska"
    contact_email: null
    source_url: "https://www.ahe.lodz.pl/filologia-polska/kola-naukowe"
    tags: ["profilowanie", "kryminologia", "psychologia postaci", "literatura"]
    is_public: false
    is_featured: false

  - slug: mlodzi-dziennikarze
    official_name_pl: "Koło Naukowe Młodych Dziennikarzy"
    display_name_en: "Young Journalists Student Research Group"
    campus: "lodz"
    major_slugs: ["dziennikarstwo-i-komunikacja-spoleczna", "filologia-polska"]
    verification_status: "official_needs_verification"
    last_verified_at: "2026-06-14"
    guardian_name: null
    contact_email: null
    source_url: "https://www.ahe.lodz.pl/dziennikarstwo/kola-naukowe"
    tags: ["dziennikarstwo", "media", "redakcja", "artykuły"]
    is_public: false
    is_featured: false

  - slug: europa-nostra
    official_name_pl: "Koło Naukowe Studentów Administracji Europa Nostra"
    display_name_en: "Europa Nostra Public Administration Group"
    campus: "lodz"
    major_slugs: ["administracja"]
    verification_status: "official_needs_verification"
    last_verified_at: "2026-06-14"
    guardian_name: "mgr Mariusz Olężałek"
    contact_email: null
    source_url: "https://www.ahe.lodz.pl/administracja/kola_naukowe"
    tags: ["administracja", "prawo", "samorząd", "konferencje"]
    is_public: false
    is_featured: false

  - slug: mlody-samorzadowiec
    official_name_pl: "Studenckie Koło Naukowe Młodego Samorządowca"
    display_name_en: "Young Local Government Student Research Group"
    campus: "lodz"
    major_slugs: ["administracja"]
    verification_status: "official_needs_verification"
    last_verified_at: "2026-06-14"
    guardian_name: null
    contact_email: null
    source_url: "https://www.ahe.lodz.pl/administracja/kola_naukowe"
    tags: ["samorząd", "administracja", "prawo", "polityka lokalna"]
    is_public: false
    is_featured: false
```

# Zadanie dla Codex

Po przeczytaniu tego pliku Codex ma:

1. rozszerzyć model `Club` o pola katalogowe i weryfikacyjne,
2. utworzyć migrację,
3. dodać powyższe rekordy do idempotentnego seeda,
4. powiązać koła z kierunkami przez relację wiele-do-wielu,
5. pokazywać aktywne koła na stronie `/clubs`,
6. proponować koła po kierunku użytkownika,
7. dodać wyszukiwanie po nazwie i tagach,
8. dodać filtry kierunku i rodzaju aktywności,
9. dodać kartę koła zawierającą nazwę, krótki opis, kierunki, tagi, opiekuna, kontakt i link „Oficjalne źródło”,
10. nie wyświetlać publicznie rekordów `official_needs_verification`, dopóki administrator nie ustawi `is_public=true`,
11. dodać w panelu administratora akcję „Potwierdź aktualność danych”, która ustawia:
    - `verification_status=active_verified`,
    - `last_verified_at=current_date`,
    - `is_public=true`,
12. dodać testy seeda, rekomendacji, filtrów, widoczności i uprawnień administratora.

## Kryterium akceptacji

Po uruchomieniu `python seed.py` aktywne, potwierdzone koła mają być widoczne w katalogu i rekomendowane zgodnie z kierunkiem studenta. Koła wymagające potwierdzenia mają istnieć w bazie i panelu administracyjnym, ale nie mogą być publiczne.
