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

def add_teacher(name, surname, subjects):
    name = str(input("Proszę podać imię nauczyciela: >>> "))
    surname = str(input("Proszę podać nazwisko nauczyciela: >>> "))
    raw_subjects = input("Proszę podać przedmioty, jakich uczy nauczyciel (proszę podawać przedmioty po spacji): >>> ")
    subjects = []
    word = ""
    for letter in raw_subjects:
        
        if letter in set("aąbcćdeęfghijklłmnńoópqrsśtuvwxyzźżAĄBCĆDEĘFGHIJKLŁMNŃOÓPQRSŚTUVWXYZŹŻ"):
            word + letter
        else:
            subjects.append(word)
            word = ""
            
    id = int(max(data,key=lambda e: e['id'])) + 1
    new_teacher = {
        "id": id,
        "name": name,
        "surname": surname,
        "subjects": subjects
    }
    
    with open("teachers.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    data["teachers"].append(new_teacher)
    with open("teachers.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False) 


def load_teachers():
    pass


def modify_teacher():
    pass


def remove_teacher():
    pass

def load_teacher_availability():
    pass

def add_class():
    pass


def modify_class():
    pass


def remove_class():
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
        working_directory_selected = 0
        
        while not keyboard.is_pressed("enter"):
            
            show_menu(options=working_directory_options, selected=working_directory_selected)
            key = keyboard.read_event().name
            
            if key == "up" and working_directory_selected > 0:
                working_directory_selected -= 1
                time.sleep(0.15)
            elif key == "down" and working_directory_selected < len(working_directory_options) - 1:
                working_directory_selected += 1
                time.sleep(0.15)
            
            elif key == "enter":
                if working_directory_options[working_directory_selected] == "liceum":
                    working_directory = working_directory + "liceum"
                    print(f"Wybrano: liceum")
                    
                elif working_directory_options[working_directory_selected] == "technikum":
                    working_directory = working_directory + "technikum"
                    print(f"Wybrano: technikum")
                    
                elif working_directory_options[working_directory_selected] == "zawodówka":
                    working_directory = working_directory + "zawodówka"
                    print(f"Wybrano: zawodówka")
        
        keyboard.wait("esc")

def preset_editor():
    print(
            """
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    Narzędzie do edytowania zestawów danych
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
            """
        )
    working_directory = ""

    options = [
        "Wybierz preset",
        "Edytuj klasy",
        "Edytuj dostępność nauczycieli",
        "Edytuj nauczycieli",
        "Exit",
    ]
    selected = 0

    while True:
        show_menu(options=options, selected=selected)
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
                print(
                        """
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
            Edytor Klas
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
                        """
                    )
                class_options = [
                    "Edytuj wymiar godzinowy dla danego rocznika",
                    "Modyfikuj klasę",
                    "Usuń klasę",
                    "Dodaj klasę",
                    "Powrót",
                ]
                class_selected = 0

                return_ = False
                while return_ == False:
                    show_menu(options=class_options, selected=class_selected)
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
                        
    print("Proszę wybrać, z jakiego zestawu danych korzystać:")
    
    options = ["Podstawowe", "Własne"]
    
    end_choosing = False
    location = "hour_presets"
    
    
    while end_choosing == False:
        selected = 0
        
        show_menu(options=options, selected=selected)
        key = keyboard.read_event().name
        
        if key == "up" and selected > 0:
            selected -= 1
            time.sleep(0.15)
        elif key == "down" and selected < len(options) - 1:
            selected += 1
            time.sleep(0.15)
        
        elif key == "enter":
            if options[selected] == "Podstawowe":
                print("Wybrano podstawowe zestawy danych.")
                basic_options = os.listdir(location)
                print("Wybierz:")
                basic_selected = 0
                
                show_menu(options=basic_options, selected=basic_selected)
                if key == "up" and basic_selected > 0:
                    basic_selected -= 1
                    time.sleep(0.15)
                elif key == "down" and basic_selected < len(basic_options) - 1:
                    basic_selected += 1
                    time.sleep(0.15)
                    
                elif key== "enter":
                    if basic_options[basic_selected] == "szkoła_podstawowa":
                        print("Wybrano: szkoła_podstawowa")
                        
                        location = location + "/szkoła_podstawowa"
                        
                        elements = os.listdir(location)
                        print("Elementy w środku:")
                        for i in range(len(elements)):
                            print(elements[i])
                        
                        print("Czy kontynuować?")
                        continue_options = ["Tak", "Nie"]
                        continue_selected = 0
                        end_of_sequence = False

                        while not end_of_sequence:
                            show_menu(options=continue_options, selected=continue_selected)
                            if key == "up" and continue_selected > 0:
                                continue_selected -= 1
                                time.sleep(0.15)
                            elif key == "down" and continue_selected < len(continue_options) - 1:
                                continue_selected += 1
                                time.sleep(0.15)
                            elif key == "enter":
                                if continue_options[continue_selected] == "Tak":
                                    print("Kontynuowano wykonywanie programu.")
                                    end_of_sequence = True
                                    end_choosing = True
                                elif continue_options[continue_selected] == "Nie":
                                    print("Przerwanie obliczania planu.")
                                    return True
                        
                    
                    elif basic_options[basic_selected] == "szkoła_srednia":
                        print("Wybrano: szkoła_średnia")
                        location = location + "/szkoła_średnia/liceum"
                        zakres = ""
                        mid_school_options = os.listdir(location)
                        mid_school_selected = 0
                        end_basic_options = False
                        
                        while not end_basic_options:
                            show_menu(options=mid_school_options, selected=mid_school_selected)
                            if key == "up" and mid_school_selected > 0:
                                mid_school_selected -= 1
                                time.sleep(0.15)
                            elif key == "down" and mid_school_selected < len(mid_school_selected) - 1:
                                mid_school_selected += 1
                                time.sleep(0.15)
                            
                            elif key == "enter":
                                if mid_school_options[mid_school_selected] == "zakres_podstawowy":
                                    print(f"Wybrano {mid_school_options[mid_school_selected]}")
                                    location = location + str(mid_school_options[mid_school_selected])
                                    end_basic_options = True
                                    
                                elif mid_school_options[mid_school_selected] == "zakres_rozszerzony":
                                    print(f"Wybrano {mid_school_options[mid_school_selected]}")
                                    location = location + str(mid_school_options[mid_school_selected])
                                    end_basic_options = True
                            # Work needs to be done here
                
            elif options[selected] == "Własne":
                print("Wybrano własne zestwy danych.")
                choosen_preset = ""
                # Work needs to be done here
    
# Sprawdzanie integralności plików \/
    if location == "hour_presets/szkoła_podstawowa" or f"hour_presets/szkoła_średnia/liceum/zakres_{zakres}":
        teacher_path = "data/"
        
        open(teacher_path + "teachers.json", "w")
        open(teacher_path + "teacher_availability.json", 'w')
        open(teacher_path + "classes.json", 'w')
        
        with open(teacher_path + "teachers.json", 'r') as file_obj:
            first_char = file_obj.read(1)
            if not first_char:
                print("Nie wczytano nauczycieli! Proszę to uzupełnić, inaczej program się nie wykona")
                return True
            else:
                pass
        
        with open(teacher_path + "teacher_availability.json", 'r') as file_obj:
            first_char = file_obj.read(1)
            if not first_char:
                print("Nie wczytano dostępności nauczycieli! prosze to uzupełnić, inaczej program się nie wykona ")
                return True
            else:
                pass
        
        with open(teacher_path + "classes.json", 'r') as file_obj:
            first_char = file_obj.read(1)
            if not first_char:
                print("Nie wczytano klas! Nie można obliczyć planu. Proszę to uzupełnić.")
                return True
            else:
                pass
    
    elif location == f"hour_presets/szkoła_podstawowa/user_presets/liceum/{choosen_preset}":
        file_empty_error_list = []
        for klasa in range(4):
            open(location + f"klasa{klasa}", 'w')
            
            with open(location + f"klasa{klasa}", 'r') as file_obj:
                first_char = file_obj.read(1)
                if not first_char:
                    file_empty_error_list.append(f"Plik: klasa{klasa} jest pusty.")
                else:
                    pass
                            
        open(location + "classes.json", 'w')
        with open(location + "classes.json", 'r') as file_obj:
            first_char = file_obj.read(1)
            if not first_char:
                file_empty_error_list.append(f"Plik: klasy, jest pusty.")
            else:
                pass
                
        open(location + "teachers.json", 'w')
        with open(location + "teachers.json", 'r') as file_obj:
            first_char = file_obj.read(1)
            if not first_char:
                file_empty_error_list.append(f"Plik: nauczyciele, jest pusty.")
            else:
                pass
        
        open(location + "teacher_availability.json", 'w')
        with open(location + "teacher_availability.json", 'r') as file_obj:
            first_char = file_obj.read(1)
            if not first_char:
                file_empty_error_list.append(f"Plik: dostępność nauczycieli, jest pusty.")
            else:
                pass
            
        if len(file_empty_error_list) > 0:
            print("Obliczanie planu nie może być kontynuowane ze względu na następujące błędy: ")
            for element in file_empty_error_list:
                print(element)
            print("Obliczanie planu zostało przerwane.")
            return True
        else:
            print("Wszystkie pliki zgodne.")
        
    
    elif location == f"hour_presets/szkoła_podstawowa/user_presets/technikum/{choosen_preset}":
        file_empty_error_list = []
        for klasa in range(5):
            open(location + f"klasa{klasa}", 'w')
            with open(location + f"klasa{klasa}", 'r') as file_obj:
                first_char = file_obj.read(1)
                if not first_char:
                    file_empty_error_list.append(f"Plik: klasa{klasa} jest pusty.")
                else:
                    pass
        
        open(location + "classes.json", 'w')
        with open(location + "classes.json", 'r') as file_obj:
            first_char = file_obj.read(1)
            if not first_char:
                file_empty_error_list.append(f"Plik: klasy, jest pusty.")
            else:
                pass
                
        open(location + "teachers.json", 'w')
        with open(location + "teachers.json", 'r') as file_obj:
            first_char = file_obj.read(1)
            if not first_char:
                file_empty_error_list.append(f"Plik: nauczyciele, jest pusty.")
            else:
                pass
        
        open(location + "teacher_availability.json", 'w')
        with open(location + "teacher_availability.json", 'r') as file_obj:
            first_char = file_obj.read(1)
            if not first_char:
                file_empty_error_list.append(f"Plik: dostępność nauczycieli, jest pusty.")
            else:
                pass
            
        if len(file_empty_error_list) > 0:
            print("Obliczanie planu nie może być kontynuowane ze względu na następujące błędy: ")
            for element in file_empty_error_list:
                print(element)
            print("Obliczanie planu zostało przerwane.")
            return True
        else:
            print("Wszystkie pliki zgodne.")
            
# Sprawdzanie integralności plików /\
        
            
            
    
    
    # =========================================================================
    
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
    
    # =========================================================================
    
    # Work needs to be done here
    pass


# ----------------------

def show_menu(selected, options):
        os.system("cls" if os.name == "nt" else "clear")
        for i, option in enumerate(options):
                        prefix = "> " if i == selected else "  "
                        print(f"{prefix}{option}")

def main():
    options = ["Oblicz plan", "Edytuj dane", "Stwórz nowy preset", "Exit"]
    selected = 0

    while True:
        show_menu(options=options, selected=selected)
        key = keyboard.read_event().name

        if key == "up" and selected > 0:
            selected -= 1
            time.sleep(0.15)
        elif key == "down" and selected < len(options) - 1:
            selected += 1
            time.sleep(0.15)
        elif key == "enter":
            if options[selected] == "Oblicz plan":
                calculate_plan()
            elif options[selected] == "Edytuj dane":
                preset_editor()
            elif options[selected] == "Stwórz nowy preset":
                initialize_new_preset()
            elif options[selected] == "Exit":
                return 0
    


print(
        """
--------------------------------------
ALGORYTMICZNY UKŁADACZ PLANU alpha 0.1
--------------------------------------
          
          """
    )

if __name__ == "__main__":
    main()