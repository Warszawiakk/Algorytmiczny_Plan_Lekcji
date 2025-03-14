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


