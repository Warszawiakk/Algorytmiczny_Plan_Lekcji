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
    
    def set_working_directoy():
        global working_directory
        # default:
        working_directory = "hour_presets/szkoła_średnia/user_presets"
        
        print(f"""
    Lista zestawów użytkownika w: {working_directory}:
    {os.listdir(working_directory)}
              """)
        
        print("Wybierz:")
        
        working_directory_options = os.listdir(working_directory)
        
        while not keyboard.is_pressed("enter"):
            
            show_menu()
            key = keyboard.read_event().name

            working_directory_selected = 0
            
            if key == "up" and selected > 0:
                selected -= 1
                time.sleep(0.15)
            elif key == "down" and selected < len(working_directory_options) - 1:
                selected += 1
                time.sleep(0.15)
            
            elif key == "enter":
                if working_directory_options[working_directory_selected] == "liceum":
                    working_directory = working_directory + "liceum"
                    print(f"Wybrano: {"liceum"}")
                    
                elif working_directory_options[working_directory_selected] == "technikum":
                    working_directory = working_directory + "technikum"
                    print(f"Wybrano: {"technikum"}")
                    
                elif working_directory_options[working_directory_selected] == "zawodówka":
                    working_directory = working_directory + "zawodówka"
                    print(f"Wybrano: {"zawodówka"}")
        
        keyboard.wait("esc")

    options = [
        "Wybierz preset",
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
            elif options[selected] == "Wybierz preset":
                set_working_directoy()
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
                            # Work needs to be done here
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
                            # Work needs to be done here
                            keyboard.wait("esc")

                        elif class_options[class_selected] == "Dodaj klasę":
                            print("\n Aby wyjść, naciśnij esc")
                            print("Pamiętaj, że nazwa klasy to: [numer][litera]")
                            # Work needs to be done here
                            name = input("Podaj nazwę klasy >>> ")
                            
                            file_path_to_classes_preset = f"{working_directory}/classes.json"
                            if class_exists(str(name), file_path_to_classes_preset) == True:
                                print("Klasa o podanej nazwie istnieje. Jeżeli chcesz ją zmienic, użyj narzędzia do modyfikowania klas.")
                            else:
                                pass
                            
                            keyboard.wait("esc")

            

            elif options[selected] == "Edytuj dostępność nauczycieli":
                print("\n Aby wyjść, naciśnij esc")
                print("Edytowanie dostępności nauczycieli...")
                # Work needs to be done here
                keyboard.wait("esc")

            elif options[selected] == "Edytuj nauczycieli":
                print("\n Aby wyjść, naciśnij esc")
                print("Edytowanie nauczycieli...")
                # Work needs to be done here
                keyboard.wait("esc")

    os.system("cls" if os.name == "nt" else "clear")
    print("Zakończono edycję.")


# ----------------------
def calculate_plan():
    # Zapytać się, czy korzystać ze stockowego preseta, czy z własnego preseta.
    
    # -- Koncepcja dzialania -- #
    # * Zostaje wczytany json 'klasa[n]', dlatego program wie, jakie przedmioty powinien wypełnić
    # * Zostaje wczytany json 'teachers'
    # * Zostaje wczytany json 'teacher_availability'
    # *                     \/
    # * Program zaczyna wypełniać pierwszy przedmiot z listy przedmiotów dla klasy 1 (wypełnianie od klasy 1 do klasy ostatniej)
    # * Sprawdza, w jakich innych (i czy) klasach dany przedmiot występuje, na tej postawie ogranicza wypelnianie.
    # * Sprawdza, czy dany nauczyciel uczy innych przemiotów, jeżeli tak, to sprawdza jakich, na tej podstawie sprawdza również, czy inne
    # * klasy/grupy nie mają jednocześnie lekcji z danym nauczycielem, jeżeli tak, ogranicza odpowiednio pole wypełniania.
    # *                                \/ 
    # * Obszar wypełniania jest ograniczony poprzez podzielenie liczbę wszystkich godzin dla danej klasy na liczbę dni tygodnia.
    # *                                \/
    # * Program sprawdza listę nauczycieli uczących daną klasę -> dopasowywuje przedmiot do nauczyciela, który go uczy (dla danej klasy),
    #   ogranicza na podstawie nauczyciela, możliwy obszar wypełniania
    # *                                \/
    # * Program sprawdza, czy możliwe jest wypełnienie przedmiotu poniżej 3'ech lekcji tego samego dnia.
    # * Jeżeli tak, program rozkłada wypełnianie na inne wolne dni. Jeżeli nie, to stara się rozłożyć te lekcje jak najdalej od siebie,
    # * grupujac je w strukturze 2,1 lub 2,2.
    # *                                \/
    # * Wypełnianie:
    # * Program wypełnia wolne pola po kolei, od pierwszej możliwej lekcji (Realizuje to jednocześnie dawanie lekcji jak najwczesniej oraz
    #   kończenie jak najwcześniej lekcji).
    # * Kiedy zostaje zakończone wypelnianie dla pierwszej danej klasy, program przechodzi do klasy następnej (powtarza się cały poprzedni
    #   proces (poza wczytywaniem json'ów, gdyż są one już wczytane))
    
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
    


main()
# test()
