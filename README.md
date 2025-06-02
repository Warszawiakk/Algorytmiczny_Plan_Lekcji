Plan lekcji

Twoim zadaniem jest napisanie programu, który pomoże w organizacji planu lekcji.
Logika programu Zakładamy, że w szkole mamy N klas i M nauczycieli. Każdy nauczyciel może
prowadzić R różnych przedmiotów. Każda klasa ma S przedmiotów, z których każdy ma zadaną,
tygodniową liczbę godzin. Załóżmy, że program wczytuje plik \*.json o następującej strukturze:

Program powinien zwrócić plan lekcji, który spełnia następujące warunki:

• Nauczyciel nie może prowadzić dwóch lekcji jednocześnie.
• Klasa musi mieć zrealizowane wszystkie lekcje zgodnie z planem.

Dodatkowo, jeśli możliwe jest ustalenie kilku planów lekcji spełniających powyższe warunki,
program powinien zwrócić najlepsze możliwe rozwiązanie, przy czym sam/a powinieneś określić, co
oznacza "najlepsze". Jeśli jednak nie jest możliwe ustalenie żadnego planu lekcji, program powinien
zwrócić odpowiedni komunikat.

Hint Jeśli będziemy mieli funkcję, która jako argument pobiera plan lekcji i zwraca wartość licz-
bową, która określa, jak dobry jest plan, to możemy zastosować algorytmy optymalizacji nieliniowej,
aby znaleźć najlepsze rozwiązanie. Nie każdy z nich jednak będzie przynosił sensowne rezultaty, bo
zadanie jest dość specyficzne.

Informacje dodatkowe Oczekujemy, że dobrze napisany program będzie na tyle modularny, że
będzie można go łatwo rozbudować o nowe funkcjonalności, np.: dwie lekcje z danego przedmiotu
muszą być obok siebie, nauczyciel nie może prowadzić więcej niż 5 lekcji w ciągu dnia, itp.


# =========================================================================
    
    # -- Koncepcja dzialania -- #
    # * \\ Zostaje wczytany json 'klasa[n]', dlatego program wie, jakie przedmioty powinien wypełnić
    # * \\ Zostaje wczytany json 'teachers'
    # * \\ Zostaje wczytany json 'teacher_availability'
    # *                     \/
    # * Program zaczyna wypełniać pierwszy przedmiot z listy przedmiotów dla pierwszego wczytanego rocznika (wypełnianie od rocznika #      najmniejszego do największego)
    # * Sprawdza, w jakich innych (i czy) rocznikach dany przedmiot występuje, na tej postawie ogranicza wypelnianie.
    # * Sprawdza, czy dany auczyciel uczy innych przemiotów, jeżeli tak, to sprawdza jakich, na tej podstawie sprawdza również, czy inne
    # * roczniki/grupy nie mają jednocześnie lekcji z danym nauczycielem, jeżeli tak, ogranicza odpowiednio pole wypełniania.
    # *                                \/ 
    # * Obszar wypełniania jest ograniczony poprzez podzielenie liczbę wszystkich godzin dla danego rocznika na liczbę dni tygodnia.
    # *                                \/
    # * Program sprawdza listę nauczycieli uczących dany rocznik -> dopasowywuje przedmiot do nauczyciela, który go uczy (dla danego #     rocznika),
    #   ogranicza na podstawie nauczyciela, możliwy obszar wypełniania
    # *                                \/
    # * Program sprawdza, czy możliwe jest wypełnienie przedmiotu poniżej 3'ech lekcji tego samego dnia.
    # * Jeżeli tak, program rozkłada wypełnianie na inne wolne godziny w inne dni. Jeżeli nie, to stara się rozłożyć te lekcje jak      #   najdalej od siebie,
    # * grupujac je w strukturze 2,1 lub 2,2.
    # *                                \/
    # * Wypełnianie:
    # * Program wypełnia wolne pola po kolei, od pierwszej możliwej lekcji (Realizuje to jednocześnie dawanie lekcji jak najwczesniej oraz
    #   kończenie jak najwcześniej lekcji) FIFO.
    # * Kiedy zostaje zakończone wypelnianie dla pierwszego danego rocznika, program przechodzi do rocznika następnego (powtarza się cały #   poprzedni proces (poza wczytywaniem json'ów, gdyż są one już wczytane))
    
# =========================================================================

classes.json:
    false = wolne pole
    true = pole zablokowane
    R-{false,true} = pole zajęte