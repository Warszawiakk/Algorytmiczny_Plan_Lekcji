
Rozwiązanie - brudnopis:

W szkole mamy:
- N klas
- M nauczycieli
- Każda klasa ma S przedmiotów
- Każdy nauczyciel może prowadzić R przedmiotów

- Nauczyciel nie może prowadzić 2'uch lekcji na raz
- Klasa musi mieć zrealizowane wszystkie lekcje zgodnie z planem.

Założenia:
    ==========================
    Funkcjonalne:

    - program powienien dążyć do minimalizacji liczby lekcji dziennie:
        - Suma wszystkich godzin dla danej klasy podzielona na 5 i zaokrąglona w sposob, by dążyć do niższej liczby lekcji w piątek oraz do najwyższej w poniedziałek.

    - program ma starać rozłożyć lekcje na każdy dzień tygodnia roboczego (pon-pt)

    - program powinien próbować rozłożyć lekcje w taki sposób, by nie mogło być 4'ech lekcji z tego samego przedmiotu dziennie.
    
    - w razie niemożności wciśnięcia odpowiedniej liczby lekcji dla danej klasy, proces dla danej klasy powinien zostać zatrzymany, a error
    zapisany do logów (Coudn't fit subject: [lesson] for class: [class] on [day of the week] lesson: [hour]. Need: [number of subject left] to satisfy.). Logi powinny być zapisywane w oddzielnej konsoli.

    - nauczyciel nie może prowadzić 2 lekcji jednocześnie.

    - program powinien najpierw uzupełniac przedmioty wspólne (całą klasą), następnie w ich ramach uzupełniać przedmioty grupowe.

    - 2 grupy nie mogą mieć tego samego przedmiotu grupowego na raz.

    - program powinien wypełniać wszystkie klasy na raz, przedmiotowo (Czyli idzie przedmiotami po kolei i wypełnia je dla wszystkich klas na raz).

    - każda szkoła ma możliwość dodawania własnych rozszerzeń poprzez narzędzie w programie lub poprzez wczytanie danych z excela.

    - Etyka/Religia musi dążyć do bycia na początku/końcu.

    - nauczyciele, z najmniejszymi ramami czasowymi powinni mieć stockowy priorytet.

    ==============================================
    Techniczne:

    - Powinien implementować funkcję, która zwraca czas do końca wyznaczania planu lekcji.

    - 1 dict = 1 klasa

    - STOCKOWO maksymalna długość listy dnia powinna wynosić 8 (lekcji)
    
    - program powinien odczytywać ilość godzin dla każdej lekcji ze względu na nazwę klasy (poziom klasy)

    - może być maksymalnie 5 poziomów lekcji dla technikum, 4 poziomy dla liceum
    
    - poprzez wbudowaną funkcjonalność, użytkownik powinien być w stanie zmienić priorytety przedmiotowe.

    - na podstawie czasu nauczyciela program powinien ograniczać pole wypełniania lekcji w celu optymalizacji.