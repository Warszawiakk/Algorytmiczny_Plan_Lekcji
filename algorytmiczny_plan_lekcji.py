# Adam Henke 2025 all rights reserved

import json
import os
import keyboard
import time

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


def reset_school_type():
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
hour_preset = os.path


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

    directory = "hour_presets/"

    max_class = 0

    if school_type == 1:
        max_class = 8
        directory = directory + "szkoła_podstawowa"
    elif school_type == 2:
        max_class = 4
        directory = directory + "szkoła_średnia/user_presets/liceum"
    elif school_type == 3:
        max_class = 5
        directory = directory + "szkoła_średnia/user_presets/technikum"

    name = input("Podaj nazwę presetu: ")
    directory = directory + "/" + name

    while yes_no not in ["Y", "y", "N", "n"]:
        print("Czy chcesz kontynuować?")
        yes_no = input("(Y/n)? >>> ")
        if yes_no not in ["Y", "y", "N", "n"]:
            print(" Złe wejście! Program przyjmuje jedynie wartości: Y,y,N,n. ")
        elif yes_no in ["Y", "y"]:
            print("Inicjalizowanie presetu...")
            break
        elif yes_no in ["N", "n"]:
            print("Inicjalizacja przerwana")
            return 0

    try:
        os.makedirs(directory)
        for klasa in range(max_class):
            open(directory, "klasa" + klasa + ".json")
        open(directory, "teacher_availability.json")
        print(
            f"zainicjalizowano klasy od 1 do {max_class} oraz plik z dostępnościa nauczycieli"
        )
    except FileExistsError:
        print("Preset już istnieje. Spróbuj edytowac preset lub zmień nazwę presetu.")


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-
def preset_editor():
    working_directory = ""

    options = [
        "Edytuj klasy",
        "Edytuj dostępność nauczycieli",
        "Edytuj nauczycieli",
        "Exit",
    ]
    selected = 0

    def show_menu():
        os.system("cls" if os.name == "nt" else "clear")
        print(
            """
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    Narzędzie do edytowania zestawów danych
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
            """
        )
        # print(f"Obecna lokalizacja: {working_directory}\n")

        for i, option in enumerate(options):
            prefix = "> " if i == selected else "  "
            print(f"{prefix}{option}")

    while True:
        show_menu()
        key = keyboard.read_event().name

        if key == "up" and selected > 0:
            selected -= 1
            time.sleep(0.15)
        elif key == "down" and selected < len(options) - 1:
            selected += 1
            time.sleep(0.15)
        elif key == "enter":
            if options[selected] == "Exit":
                break

            # Class internal selection
            elif options[selected] == "Edytuj klasy":
                class_options = ["Edytuj wymiar godzinowy dla danej klasy","Usuń klasę","Dodaj klasę","Exit"]
                class_selected = 0

                for i, option in enumerate(class_options):
                    prefix = "> " if i == class_selected else "  "
                    print(f"{prefix}{option}")

                while keyboard.wait("esc"):
                    show_menu()
                    key = keyboard.read_event().name

                    if key == "up" and class_selected > 0:
                        class_selected -= 1
                        time.sleep(0.15)
                    elif key == "down" and class_selected < len(options) - 1:
                        class_selected += 1
                        time.sleep(0.15)
                    elif key == "enter":
                        if class_options[class_selected] == "Exit":
                            break
                        if class_options[class_selected] == "Edytuj wymiar godzinowy dla danej klasy":
                            print("Wybierz klasę: ")
                            # Work needs to be done here

            # Class internal selection

            print(f"\nWybrano: {options[selected]}")
            keyboard.wait("esc")


# ----------------------
def calculate_plan():
    # Zapytać się, czy korzystać ze stockowego preseta, czy z własnego preseta.
    pass


# ----------------------


def main():
    print(
        """
----------------------------          
ALGORYTMICZNY UKŁADACZ PLANU
----------------------------
          
          """
    )
    preset_editor()
    # while True:
    #     user_input = input(">> ")

    #     if user_input == "exit":
    #         break

    #     elif user_input == "help":
    #         pass


main()
# test()
