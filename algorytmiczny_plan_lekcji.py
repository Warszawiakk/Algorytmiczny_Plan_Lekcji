# Adam Henke 2025 all rights reserved

import json
import os
import keyboard
import time

working_school_type = 0

def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
    
def class_exists(class_name, file_path):
    data = load_json(file_path)
    return any(c["name"] == class_name for c in data["classes"])

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
        print(f"Obecna lokalizacja: {working_directory}")

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

            # ----------------
            # Podmenu: Edytuj klasy
            # ----------------
            elif options[selected] == "Edytuj klasy":
                class_options = [
                    "Edytuj wymiar godzinowy dla danego rocznika",
                    "Modyfikuj klasę",
                    "Usuń klasę",
                    "Dodaj klasę",
                    "Powrót",
                ]
                class_selected = 0

                def show_class_menu():
                    os.system("cls" if os.name == "nt" else "clear")
                    print(
                        """
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
            Edytor Klas
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
                        """
                    )
                    for i, option in enumerate(class_options):
                        prefix = "> " if i == class_selected else "  "
                        print(f"{prefix}{option}")

                return_ = False
                while return_ == False:
                    show_class_menu()
                    key = keyboard.read_event().name

                    if key == "up" and class_selected > 0:
                        class_selected -= 1
                        time.sleep(0.15)
                    elif key == "down" and class_selected < len(class_options) - 1:
                        class_selected += 1
                        time.sleep(0.15)
                    elif key == "enter":
                        if class_options[class_selected] == "Powrót":
                            return_ = True
                            break

                        elif class_options[class_selected] == "Edytuj wymiar godzinowy dla danego rocznika":
                            print("Czyli np. dla wszystkich klas pierwszych.")
                            
                            print("\n Aby wyjść, naciśnij esc")
                            
                            print("Wybierz klasę: ")
                            keyboard.wait("esc")
                            
                        elif class_options[class_selected] == "Modyfikuj klasę":
                            # Work needs to be done here
                            print("""
-------------------
Modyfikowanie klas
-------------------
                                  """)

                        elif class_options[class_selected] == "Usuń klasę":
                            print("\n Aby wyjść, naciśnij esc")
                            print("Wybierz klasę do usunięcia: ")
                            keyboard.wait("esc")

                        elif class_options[class_selected] == "Dodaj klasę":
                            print("\n Aby wyjść, naciśnij esc")
                            print("Pamiętaj, że nazwa klasy to: [numer][litera]")
                            name = input("Podaj nazwę klasy >>> ")
                            
                            if class_exists(str(name), file_path="data/classes.json") == True:
                                print("Klasa o podanej nazwie istnieje. Jeżeli chcesz ją zmienic, użyj narzędzia do modyfikowania klas.")
                            else:
                                pass
                            
                            keyboard.wait("esc")

            

            elif options[selected] == "Edytuj dostępność nauczycieli":
                print("\n Aby wyjść, naciśnij esc")
                print("Edytowanie dostępności nauczycieli...")
                keyboard.wait("esc")

            elif options[selected] == "Edytuj nauczycieli":
                print("\n Aby wyjść, naciśnij esc")
                print("Edytowanie nauczycieli...")
                keyboard.wait("esc")

    os.system("cls" if os.name == "nt" else "clear")
    print("Zakończono edycję.")


# ----------------------
def calculate_plan():
    # Zapytać się, czy korzystać ze stockowego preseta, czy z własnego preseta.
    
    # Work needs to be done here
    pass


# ----------------------


def main():
    print(
        """
--------------------------------------
ALGORYTMICZNY UKŁADACZ PLANU alpha 0.1
--------------------------------------
          
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
