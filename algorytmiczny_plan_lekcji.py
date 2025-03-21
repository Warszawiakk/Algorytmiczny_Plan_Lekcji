import json
import os

working_school_type = 0


def chose_school_type():
    print(
        """
Wybierz typ szkoły:
1: Szkoła Podstawowa
2: Liceum
3: Technikum
        """
    )
    command = input(">>> ")
    working_school_type = int(command)


def reset_school_model():
    working_school_type = 0
    print("Typ szkoły został zresetowany.")


def add_teacher():
    pass


def load_teachers():
    pass


def modify_teacher():
    pass


def remove_teacher():
    pass


def add_class():
    pass


def modify_class():
    pass


def remove_class():
    pass


#
hour_preset = [str, str, str]


def load_hour_preset():
    print("Zestaw został wczytany.")


def unload_hour_preset():
    pass


# ----
def initialize_new_preset():
    print(
        """
Wybierz typ szkoły:
1: Szkoła Podstawowa
2: Liceum
3: Technikum
        """
    )
    school_type = 0
    while school_type not in range(1, 3):
        command = input(">>>")
        school_type = int(command)
        if school_type not in range(1, 3):
            print("Nie można wybrać opcji poza 1-3")
        else:
            print(f"Wybrano: {school_type}")
            break

    max_class = 0
    if school_type == 1:
        max_class = 8
    elif school_type == 2:
        max_class = 4
    elif school_type == 3:
        max_class = 5

    klasa = 0
    while klasa not in range(max_class):
        print("Dla jakiej klasy chcesz stworzyć preset?  (np. klasa 1)")
        command = input(">>> ")
        klasa = int(command)
        if klasa not in range(max_class):
            print(f"Należy wybrać klasę w zakresie {"1-"+ max_class}")
        else:
            print(f"Wybrano klasę: {klasa}")
            break

    while yes_no not in ["Y", "y", "N", "n"]:
        print("Czy chcesz kontynuować?")
        yes_no = input("(Y/n)? >>> ")
        if yes_no not in ["Y", "y", "N", "n"]:
            print(" Złe wejście! Program przyjmuje jedynie wartości: Y,y,N,n. ")
        elif yes_no in ["Y", "y"]:
            print("Inicjalizowanie presetu kontynuowane.")
            break
        elif yes_no in ["N", "n"]:
            print("Inicjalizacja przerwana")
            return 0


# ----------------------
def calculate_plan():
    # Zapytać się, czy korzystać ze stockowego preseta, czy z własnego preseta.
    pass


# ----------------------


def main():
    while True:
        user_input = input(">> ")

        if user_input == "exit":
            break


main()
