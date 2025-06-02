# Adam Henke 2025 all rights reserved
# Algorytmiczny Układacz Planu alpha 1.0

import os
try:
    import tkinter as tk
except ImportError:
    print("Couldn't install tkinter. Trying to install, else, try downloading them manually.")
    os.system('python -m pip install tkinter')
import tkinter as tk

try:
    import json
except ImportError:
    print("Couldn't install json. Trying to install, else, try downloading them manually.")
    os.system('python -m pip install json')
import json
from tkinter import ttk


from tkinter import messagebox, simpledialog

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Algorytmiczny Układacz Planu")
        self.geometry("800x500")
        self.iconbitmap("icon.ico")
        self.working_directory = "data_sets/szkoła_średnia/user_data_sets/"
        self.live_preview_enabled = tk.BooleanVar(value=True)  # Zmienna kontrolna dla podglądu na żywo

        self.main_menu()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def create_scrollable_frame(self):
        self.clear_window()

        canvas = tk.Canvas(self)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return scrollable_frame

    def main_menu(self):
        self.clear_window()

        title = tk.Label(self, text="ALGORYTMICZNY UKŁADACZ PLANU alpha 1.0", font=("Arial", 16, "bold"))
        title.pack(pady=20)

        is_data_set_selected = self.working_directory != "data_sets/szkoła_średnia/user_data_sets/"

        btn1 = tk.Button(
            self,
            text="Oblicz plan",
            width=30,
            height=2,
            command=self.calculate_plan,
            state="normal" if is_data_set_selected else "disabled"
        )
        btn2 = tk.Button(self, text="Edytuj dane", width=30, height=2, command=self.data_set_editor)
        btn3 = tk.Button(self, text="Zarządzaj zestawami danych", width=30, height=2, command=self.data_set_manager)
        btn4 = tk.Button(self, text="Exit", width=30, height=2, command=self.quit)

        for btn in [btn1, btn2, btn3, btn4]:
            btn.pack(pady=5)

####################################
# DO ZROBIENIA:
# OBLICZANIE PLANU
# Importowanie danych z Excela do JSON.

####################################

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    def calculate_plan(self):
        self.clear_window()

        label = tk.Label(self, text="Obliczanie planu", font=("Arial", 16))
        label.pack(pady=10)

        label = tk.Label(self, text="Working data_set -> " + self.working_directory, font=("Arial", 10))
        label.pack(pady=5)

        # Dodanie przycisku "Wstecz"
        back_button = tk.Button(self, text="Wstecz", width=20, command=self.main_menu)
        back_button.pack(pady=10)

        # Dodanie przycisku do włączania/wyłączania podglądu na żywo
        toggle_preview_button = tk.Checkbutton(
            self,
            text="Podgląd na żywo",
            variable=self.live_preview_enabled,
            onvalue=True,
            offvalue=False
        )
        toggle_preview_button.pack(pady=5)

        # Pasek postępu
        progress_label = tk.Label(self, text="Postęp obliczania planu:")
        progress_label.pack(pady=5)

        progress_bar = ttk.Progressbar(self, orient="horizontal", length=400, mode="determinate")
        progress_bar.pack(pady=10)

        # Licznik operacji
        progress_counter_label = tk.Label(self, text="0/0 operacji wykonanych")
        progress_counter_label.pack(pady=5)

        # Ramka dla podglądu na żywo
        live_preview_frame = tk.Frame(self)
        live_preview_frame.pack(pady=10, fill="both", expand=True)

        # Load required files
        teacher_availability_path = os.path.join(self.working_directory, "teacher_availability.json")
        classes_path = os.path.join(self.working_directory, "classes.json")
        teachers_path = os.path.join(self.working_directory, "teachers.json")

        if not all(os.path.exists(path) for path in [teacher_availability_path, classes_path, teachers_path]):
            messagebox.showerror("Błąd", "Brak wymaganych plików do obliczenia planu.")
            return

        teacher_availability = json.load(open(teacher_availability_path, 'r', encoding='utf-8'))
        classes = json.load(open(classes_path, 'r', encoding='utf-8'))
        teachers = json.load(open(teachers_path, 'r', encoding='utf-8'))

        # Get all class year files
        class_year_files = [
            f for f in os.listdir(self.working_directory) if f.startswith("klasa") and f.endswith(".json")
        ]
        if not class_year_files:
            messagebox.showerror("Błąd", "Brak roczników do przetworzenia.")
            return

        # Ustawienia paska postępu
        total_tasks = len(classes["classes"]) * len(class_year_files) * 8 * 5  # 8 godzin dziennie, 5 dni w tygodniu
        progress_bar["maximum"] = total_tasks
        progress_value = 0

        # Helper function to restrict fields based on teacher availability
        def restrict_fields(plan, teacher, teacher_availability, day, hour):
            # Mapowanie dni tygodnia na indeksy
            day_to_index = {
                "pon": 0,
                "wt": 1,
                "sr": 2,
                "czw": 3,
                "pt": 4
            }

            # Pobierz indeks dnia
            day_index = day_to_index.get(day.lower())
            if day_index is None:
                print(f"Nieprawidłowy dzień: {day}")
                return False

            for availability in teacher_availability["data"][1:]:
                if availability[0] == teacher:
                    available_hours = availability[day_index + 2].split(", ")
                    for time_range in available_hours:
                        start, end = map(lambda t: int(t.replace(":", "")), time_range.split("-"))
                        if start <= hour < end:
                            plan[day][hour] = True  # Zablokuj pole
                            return True
            return False

        # Helper function to check if a teacher is teaching another class at the same time
        def is_teacher_busy(teacher, day, hour, classes):
            for clas in classes["classes"]:
                if teacher in clas["teachers"] and clas["plan"][day][hour] is True:
                    return True
            return False

        # Process each class year
        for class_year_file in class_year_files:
            class_year_path = os.path.join(self.working_directory, class_year_file)
            class_year_data = json.load(open(class_year_path, 'r', encoding='utf-8'))

            for clas_index, clas in enumerate(classes["classes"], start=1):
                # Dopasuj plik klasy na podstawie indeksu
                expected_class_file = f"klasa{clas_index}.json"
                if class_year_file != expected_class_file:
                    continue  # Pomijaj pliki, które nie pasują do bieżącej klasy

                plan = clas["plan"]
                class_name = clas["name"]
                subjects = class_year_data["subjects"]

                for subject in subjects:
                    subject_name = subject["name"]
                    subject_hours = int(subject["hours"])  # Konwersja na liczbę całkowitą

                    teacher = next(
                        (t for t in teachers["teachers"] if subject_name in t["subjects"] and t["name"] + " " + t["surname"] in clas["teachers"]),
                        None
                    )
                    if not teacher:
                        messagebox.showerror("Błąd", f"Brak nauczyciela dla przedmiotu {subject_name} w klasie {class_name}.")
                        return

                    # Wypełnij godziny przedmiotu
                    hours_filled = 0
                    attempts = 0
                    max_attempts = 1000  # Maksymalna liczba prób, aby zapobiec nieskończonej pętli

                    while hours_filled < subject_hours and attempts < max_attempts:
                        for day in plan.keys():
                            if hours_filled >= subject_hours:
                                break

                            # Specjalna logika dla "Etyki"
                            if subject_name.lower() == "etyka":
                                for hour in range(len(plan[day])):
                                    if hour > 0:  # Etyka musi być na początku dnia
                                        break

                                    if plan[day][hour] is False:  # Pole jest dostępne
                                        if restrict_fields(plan, teacher["name"] + " " + teacher["surname"], teacher_availability, day, hour):
                                            continue  # Pomijaj, jeśli pole jest zablokowane

                                        if is_teacher_busy(teacher["name"] + " " + teacher["surname"], day, hour, classes):
                                            continue  # Pomijaj, jeśli nauczyciel jest zajęty

                                        plan[day][hour] = subject_name  # Wypełnij pole
                                        hours_filled += 1
                                        attempts = 0  # Zresetuj licznik prób przy udanym przypisaniu

                                        # Debugowanie
                                        print(f"Wstawiono: {subject_name}, Klasa: {class_name}, Dzień: {day}, Godzina: {hour}")
                                        print(f"Wypełnione godziny: {hours_filled}/{subject_hours}")

                                        # Wywołanie podglądu na żywo, jeśli jest włączony
                                        if self.live_preview_enabled.get():
                                            self.display_plan(plan, class_name, live_preview_frame)

                                        # Aktualizacja paska postępu
                                        progress_value += 1
                                        progress_bar["value"] = progress_value
                                        progress_counter_label.config(text=f"{progress_value}/{total_tasks} operacji wykonanych")
                                        self.update_idletasks()

                                        break  # Przerwij pętlę godzin w danym dniu, aby przejść do kolejnego dnia

                            # Standardowa logika dla innych przedmiotów
                            else:
                                subject_count = sum(1 for h in plan[day] if h == subject_name)
                                if subject_count >= 3:
                                    continue  # Unikaj więcej niż 3 lekcji tego samego przedmiotu w jednym dniu

                                for hour in range(len(plan[day])):
                                    if hours_filled >= subject_hours:
                                        break

                                    if plan[day][hour] is False:  # Pole jest dostępne
                                        if restrict_fields(plan, teacher["name"] + " " + teacher["surname"], teacher_availability, day, hour):
                                            continue  # Pomijaj, jeśli pole jest zablokowane

                                        if is_teacher_busy(teacher["name"] + " " + teacher["surname"], day, hour, classes):
                                            continue  # Pomijaj, jeśli nauczyciel jest zajęty

                                        plan[day][hour] = subject_name  # Wypełnij pole
                                        hours_filled += 1
                                        attempts = 0  # Zresetuj licznik prób przy udanym przypisaniu

                                        # Debugowanie
                                        print(f"Wstawiono: {subject_name}, Klasa: {class_name}, Dzień: {day}, Godzina: {hour}")
                                        print(f"Wypełnione godziny: {hours_filled}/{subject_hours}")

                                        # Wywołanie podglądu na żywo, jeśli jest włączony
                                        if self.live_preview_enabled.get():
                                            self.display_plan(plan, class_name, live_preview_frame)

                                        # Aktualizacja paska postępu
                                        progress_value += 1
                                        progress_bar["value"] = progress_value
                                        progress_counter_label.config(text=f"{progress_value}/{total_tasks} operacji wykonanych")
                                        self.update_idletasks()

                        attempts += 1  # Zwiększ licznik prób

                    # Jeśli nie udało się przypisać wszystkich godzin, wyświetl ostrzeżenie
                    if hours_filled < subject_hours:
                        messagebox.showwarning(
                            "Ostrzeżenie",
                            f"Nie udało się przypisać wszystkich godzin dla przedmiotu {subject_name} w klasie {class_name}."
                        )

        messagebox.showinfo("Sukces", "Plan został obliczony.")
        
    def match_teacher_with_subject(class_name, subject_name, classes, teachers):
        # Znajdź klasę na podstawie nazwy
        class_data = next((clas for clas in classes["classes"] if clas["name"] == class_name), None)
        if not class_data:
            print(f"Klasa {class_name} nie została znaleziona.")
            return None

        # Pobierz nauczycieli przypisanych do klasy
        class_teachers = class_data["teachers"]

        # Iteruj przez nauczycieli i sprawdź, czy któryś uczy podanego przedmiotu
        for teacher_initials in class_teachers:
            teacher_data = next((teacher for teacher in teachers["teachers"] if teacher_initials == teacher["surname"][0] + teacher["name"][0]), None)
            if teacher_data and subject_name in teacher_data["subjects"]:
                return teacher_data

        print(f"Brak nauczyciela dla przedmiotu {subject_name} w klasie {class_name}.")
        return None
    
        
    def check_file_integrity(self):
        required_files = ["teacher_availability.json", "classes.json", "teachers.json"]
        for file in required_files:
            if not os.path.exists(os.path.join(self.working_directory, file)):
                messagebox.showerror("Błąd", f"Brak pliku: {file}")
                return False
        return True
            
    def set_priority(self):
        pass # Work in progress

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

    def data_set_manager(self):
        self.clear_window()

        label = tk.Label(self, text="Zarządzanie zestawami danych", font=("Arial", 16))
        label.pack(pady=10)

        new_data_set_button = tk.Button(self, text="Stwórz nowy zestaw danych", width=40, command=self.initialize_new_data_set)
        new_data_set_button.pack(pady=5)

        remove_data_set_button = tk.Button(self, text="Usuń zestaw danych", width=40, command=self.remove_data_set)
        remove_data_set_button.pack(pady=5)
        
        rename_data_set_button = tk.Button(self, text="Zmień nazwę zestawu danych", width=40, command=self.rename_data_set)
        rename_data_set_button.pack(pady=5)


        back_button = tk.Button(self, text="Powrót", width=40, command=self.main_menu)
        back_button.pack(pady=10)

    def remove_data_set(self):
        self.clear_window()

        label = tk.Label(self, text="Usuń zestaw danych - wybierz typ szkoły", font=("Arial", 16))
        label.pack(pady=10)

        school_types = {
            "Podstawowa": "szkoła_podstawowa",
            "Liceum": "szkoła_średnia/user_data_sets/liceum",
            "Technikum": "szkoła_średnia/user_data_sets/technikum"
        }

        for school_name, school_folder in school_types.items():
            tk.Button(
                self,
                text=school_name,
                width=40,
                command=lambda folder=school_folder: self.select_data_set_to_remove(folder)
            ).pack(pady=5)

        back_button = tk.Button(self, text="Powrót", width=40, command=self.remove_data_set)
        back_button.pack(pady=10)

    def select_data_set_to_remove(self, school_folder):
        self.clear_window()

        data_sets_path = os.path.join("data_sets", school_folder)
        if not os.path.exists(data_sets_path):
            messagebox.showwarning("Brak danych", f"Brak katalogu dla {school_folder}.")
            self.remove_data_set()
            return

        data_sets = os.listdir(data_sets_path)
        if not data_sets:
            messagebox.showwarning("Brak danych", f"Brak zestawów danych w katalogu {school_folder}.")
            self.remove_data_set()
            return

        label = tk.Label(self, text=f"Wybierz zestaw danych do usunięcia z {school_folder}", font=("Arial", 14))
        label.pack(pady=10)

        for data_set in data_sets:
            tk.Button(
                self,
                text=data_set,
                width=40,
                command=lambda p=data_set: self.confirm_remove_data_set(data_sets_path, p)
            ).pack(pady=5)

        back_button = tk.Button(self, text="Powrót", width=40, command=self.remove_data_set)
        back_button.pack(pady=10)

    def confirm_remove_data_set(self, data_sets_path, data_set):
        confirm = messagebox.askyesno("Potwierdzenie", f"Czy na pewno chcesz usunąć zestaw danych '{data_set}'?")
        if confirm:
            data_set_path = os.path.join(data_sets_path, data_set)
            try:
                import shutil
                shutil.rmtree(data_set_path)
                messagebox.showinfo("Sukces", f"zestaw danych '{data_set}' został usunięty.")
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się usunąć zestawu danych: {e}")
        self.remove_data_set()
        
    def rename_data_set(self):
        self.clear_window()

        label = tk.Label(self, text="Zmień nazwę zestawu danych - wybierz typ szkoły", font=("Arial", 16))
        label.pack(pady=10)

        school_types = {
            "Podstawowa": "szkoła_podstawowa",
            "Liceum": "szkoła_średnia/user_data_sets/liceum",
            "Technikum": "szkoła_średnia/user_data_sets/technikum"
        }

        for school_name, school_folder in school_types.items():
            tk.Button(
                self,
                text=school_name,
                width=40,
                command=lambda folder=school_folder: self.select_data_set_to_rename(folder)
            ).pack(pady=5)

        back_button = tk.Button(self, text="Powrót", width=40, command=self.data_set_manager)
        back_button.pack(pady=10)

    def select_data_set_to_rename(self, school_folder):
        self.clear_window()

        data_sets_path = os.path.join("data_sets", school_folder)
        if not os.path.exists(data_sets_path):
            messagebox.showwarning("Brak danych", f"Brak katalogu dla {school_folder}.")
            self.rename_data_set()
            return

        data_sets = os.listdir(data_sets_path)
        if not data_sets:
            messagebox.showwarning("Brak danych", f"Brak zestawów danych w katalogu {school_folder}.")
            self.rename_data_set()
            return

        label = tk.Label(self, text=f"Wybierz zestaw danych do zmiany nazwy z {school_folder}", font=("Arial", 14))
        label.pack(pady=10)

        for data_set in data_sets:
            tk.Button(
                self,
                text=data_set,
                width=40,
                command=lambda p=data_set: self.confirm_rename_data_set(data_sets_path, p)
            ).pack(pady=5)

        back_button = tk.Button(self, text="Powrót", width=40, command=self.rename_data_set)
        back_button.pack(pady=10)

    def confirm_rename_data_set(self, data_sets_path, data_set):
        new_name = simpledialog.askstring("Zmień nazwę zestawu danych", f"Podaj nową nazwę dla zestawu danych '{data_set}':")
        if not new_name:
            return

        old_path = os.path.join(data_sets_path, data_set)
        new_path = os.path.join(data_sets_path, new_name)

        if os.path.exists(new_path):
            messagebox.showerror("Błąd", "zestaw danych o tej nazwie już istnieje.")
            return

        try:
            os.rename(old_path, new_path)
            messagebox.showinfo("Sukces", f"zestaw danych '{data_set}' został przemianowany na '{new_name}'.")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się zmienić nazwy zestawu danych: {e}")

        self.rename_data_set()

    def initialize_new_data_set(self):
        self.clear_window()

        label = tk.Label(self, text="Stwórz nowy zestaw danych - wybierz typ szkoły", font=("Arial", 16))
        label.pack(pady=10)

        school_types = {
            "Podstawowa": ("szkoła_podstawowa", 8),
            "Liceum": ("szkoła_średnia/user_data_sets/liceum", 4),
            "Technikum": ("szkoła_średnia/user_data_sets/technikum", 5)
        }

        for school_name, (directory, max_class) in school_types.items():
            tk.Button(
                self,
                text=school_name,
                width=40,
                command=lambda d=directory, m=max_class: self.create_data_set(d, m)
            ).pack(pady=5)

        back_button = tk.Button(self, text="Powrót", width=40, command=self.data_set_manager)
        back_button.pack(pady=10)

    def create_data_set(self, directory, max_class):
        name = simpledialog.askstring("Nazwa zestawu danych", "Podaj nazwę nowego zestawu danych:")
        if not name:
            self.data_set_manager()
            return

        final_path = os.path.join("data_sets", directory, name)
        try:
            os.makedirs(final_path)
            for i in range(1, max_class + 1):
                open(os.path.join(final_path, f"klasa{i}.json"), 'w').close()
            open(os.path.join(final_path, "teacher_availability.json"), 'w').close()
            open(os.path.join(final_path, "classes.json"), 'w').close()
            open(os.path.join(final_path, "teachers.json"), 'w').close()
            messagebox.showinfo("Sukces", "Zestaw danych został utworzony.")
        except FileExistsError:
            messagebox.showerror("Błąd", "Zestaw danych już istnieje.")

        self.data_set_manager()
        
    def edit_class_year(self):
        self.clear_window()
        label = tk.Label(self, text="Edytor roczników - wybierz akcję", font=("Arial", 16))
        label.pack(pady=10)

        options = [
            ("Edytuj roczniki", self.select_class_year),
            ("Dodaj rocznik", self.add_class_year),
            ("Usuń rocznik", self.remove_class_year),
            ("Powrót", self.data_set_editor)
        ]
        for (text, command) in options:
            tk.Button(self, text=text, width=40, command=command).pack(pady=4)

    def remove_class_year(self):
        self.clear_window()

        class_year_files = [
            f for f in os.listdir(self.working_directory) if f.startswith("klasa") and f.endswith(".json")
        ]

        if not class_year_files:
            messagebox.showwarning("Brak danych", "Brak roczników do usunięcia.")
            self.edit_class_year()
            return

        label = tk.Label(self, text="Usuń rocznik - wybierz rocznik", font=("Arial", 16))
        label.pack(pady=10)

        for class_year in class_year_files:
            tk.Button(
                self,
                text=class_year.replace(".json", ""),
                width=40,
                command=lambda cy=class_year: self.confirm_remove_class_year(cy)
            ).pack(pady=5)

        back_button = tk.Button(self, text="Powrót", width=40, command=self.edit_class_year)
        back_button.pack(pady=10)

    def confirm_remove_class_year(self, class_year):
        confirm = messagebox.askyesno(
            "Potwierdzenie",
            f"Czy na pewno chcesz usunąć rocznik '{class_year.replace('.json', '')}'?"
        )
        if confirm:
            path = os.path.join(self.working_directory, class_year)
            try:
                os.remove(path)
                messagebox.showinfo("Sukces", f"Rocznik '{class_year.replace('.json', '')}' został usunięty.")
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się usunąć rocznika: {e}")
        self.remove_class_year()

    def select_class_year(self):
        self.clear_window()

        class_year_files = [
            f for f in os.listdir(self.working_directory) if f.startswith("klasa") and f.endswith(".json")
        ]

        if not class_year_files:
            messagebox.showwarning("Brak danych", "Brak roczników do wyboru.")
            self.edit_class_year()
            return

        label = tk.Label(self, text="Edytuj roczniki", font=("Arial", 16))
        label.pack(pady=10)

        for class_year in class_year_files:
            tk.Button(
                self,
                text=class_year.replace(".json", ""),
                width=40,
                command=lambda cy=class_year: self.edit_class_year_subjects(cy)
            ).pack(pady=5)

        back_button = tk.Button(self, text="Powrót", width=40, command=self.edit_class_year)
        back_button.pack(pady=10)

    def edit_class_year_subjects(self, class_year):
        self.clear_window()

        label = tk.Label(self, text=f"Edytor przedmiotów dla rocznika: {class_year.replace('.json', '')}", font=("Arial", 16))
        label.pack(pady=10)

        path = os.path.join(self.working_directory, class_year)
        if not os.path.exists(path):
            messagebox.showerror("Błąd", f"Plik {class_year} nie istnieje.")
            self.edit_class_year()
            return

        with open(path, 'r+', encoding='utf-8') as f:
            data = json.load(f)

        if "subjects" not in data:
            data["subjects"] = []

        subjects = data["subjects"]

        scrollable_frame = self.create_scrollable_frame()

        for subject in subjects:
            frame = tk.Frame(scrollable_frame)
            frame.pack(pady=5)

            name_var = tk.StringVar(value=subject["name"])
            tk.Entry(frame, textvariable=name_var, width=20).pack(side="left", padx=5)

            hours_var = tk.StringVar(value=str(subject["hours"]))
            tk.Entry(frame, textvariable=hours_var, width=5).pack(side="left", padx=5)

            def save_subject(sub=subject, name_var=name_var, hours_var=hours_var):
                try:
                    sub["name"] = name_var.get()
                    sub["hours"] = int(hours_var.get())
                    with open(path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                    messagebox.showinfo("Sukces", f"Przedmiot {sub['name']} został zaktualizowany.")
                except ValueError:
                    messagebox.showerror("Błąd", "Wprowadź poprawną liczbę godzin.")

            tk.Button(frame, text="Zapisz", command=save_subject).pack(side="left", padx=5)

            def remove_subject(sub=subject):
                subjects.remove(sub)
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                messagebox.showinfo("Sukces", f"Przedmiot {sub['name']} został usunięty.")
                self.edit_class_year_subjects(class_year)

            tk.Button(frame, text="Usuń", command=remove_subject).pack(side="left", padx=5)

        def add_subject():
            new_name = simpledialog.askstring("Dodaj przedmiot", "Podaj nazwę nowego przedmiotu:")
            if not new_name:
                return
            new_hours = simpledialog.askinteger("Dodaj przedmiot", "Podaj liczbę godzin dla nowego przedmiotu:")
            if new_hours is None:
                return
            subjects.append({"name": new_name, "hours": new_hours})
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Sukces", f"Przedmiot {new_name} został dodany.")
            self.edit_class_year_subjects(class_year)

        tk.Button(scrollable_frame, text="Dodaj przedmiot", width=40, command=add_subject).pack(pady=10)

        back_button = tk.Button(scrollable_frame, text="Powrót", width=40, command=self.edit_class_year)
        back_button.pack(pady=10)

    def add_class_year(self):
        self.clear_window()

        label = tk.Label(self, text="Dodaj nowy rocznik", font=("Arial", 16))
        label.pack(pady=10)

        new_class_year = simpledialog.askstring("Dodaj rocznik", "Podaj nazwę nowego rocznika (np. klasa1):")
        if not new_class_year:
            self.edit_class_year()
            return

        path = os.path.join(self.working_directory, f"{new_class_year}.json")
        if os.path.exists(path):
            messagebox.showerror("Błąd", "Rocznik o tej nazwie już istnieje.")
            self.edit_class_year()
            return

        with open(path, 'w', encoding='utf-8') as f:
            json.dump({"subjects": []}, f, ensure_ascii=False, indent=4)

        messagebox.showinfo("Sukces", f"Rocznik {new_class_year} został dodany.")
        self.edit_class_year()

    def data_set_editor(self):
        self.clear_window()
        label = tk.Label(self, text="Edytor zestawów danych - wybierz akcję")
        label.pack(pady=10)
        
        select_data_set_button = tk.Button(self, text="Wybierz zestaw danych", width=40, command=self.select_data_set)
        select_data_set_button.pack(pady=4)
            
        self.edit_classes_button = tk.Button(self, text="Edytuj klasy", width=40, command=self.edit_classes)
        self.edit_years_button = tk.Button(self, text="Edytuj roczniki", width=40, command=self.edit_class_year)
        self.edit_teacher_availability_button = tk.Button(self, text="Edytuj dostępność nauczycieli", width=40, command=self.edit_teacher_availability)
        self.edit_teachers_button = tk.Button(self, text="Edytuj nauczycieli", width=40, command=self.edit_teachers)

        self.edit_classes_button.pack(pady=4)
        self.edit_years_button.pack(pady=4)
        self.edit_teacher_availability_button.pack(pady=4)
        self.edit_teachers_button.pack(pady=4)
        
        if self.working_directory == "data_sets/szkoła_średnia/user_data_sets/":
            self.edit_classes_button.config(state="disabled")
            self.edit_years_button.config(state="disabled")
            self.edit_teacher_availability_button.config(state="disabled")
            self.edit_teachers_button.config(state="disabled")
        else:
            self.edit_classes_button.config(state="normal")
            self.edit_years_button.config(state="normal")
            self.edit_teacher_availability_button.config(state="normal")
            self.edit_teachers_button.config(state="normal")
        
        back_button = tk.Button(self, text="Powrót", width=40, command=self.main_menu)
        back_button.pack(pady=10)

    def select_data_set(self):
        self.clear_window()

        label = tk.Label(self, text="Wybierz typ szkoły", font=("Arial", 16))
        label.pack(pady=10)

        school_types = {
            "Liceum": "liceum",
            "Technikum": "technikum",
            "Szkoła Zawodowa": "szkoła_zawodowa"
        }

        for school_name, school_folder in school_types.items():
            tk.Button(
                self,
                text=school_name,
                width=40,
                command=lambda folder=school_folder: self.display_data_sets(folder)
            ).pack(pady=5)
        
        

        back_button = tk.Button(self, text="Powrót", width=40, command=self.data_set_editor)
        back_button.pack(pady=10)

    def display_data_sets(self, school_folder):
        self.clear_window()

        data_sets_path = os.path.join("data_sets/szkoła_średnia/user_data_sets", school_folder)
        if not os.path.exists(data_sets_path):
            messagebox.showwarning("Brak danych", f"Brak katalogu dla {school_folder}.")
            self.data_set_editor()
            return

        data_sets = os.listdir(data_sets_path)
        if not data_sets:
            messagebox.showwarning("Brak danych", f"Brak zestawów danych w katalogu {school_folder}.")
            self.data_set_editor()
            return

        label = tk.Label(self, text=f"Wybierz zestaw danych z {school_folder}", font=("Arial", 14))
        label.pack(pady=10)

        for data_set in data_sets:
            tk.Button(
                self,
                text=data_set,
                width=40,
                command=lambda p=data_set: self.set_working_directory(data_sets_path, p)
            ).pack(pady=5)

        back_button = tk.Button(self, text="Powrót", width=40, command=self.data_set_editor)
        back_button.pack(pady=10)

    def set_working_directory(self, data_sets_path, data_set):
        self.working_directory = os.path.join(data_sets_path, data_set)
        messagebox.showinfo("Wybrano", f"Aktywny katalog: {self.working_directory}")

        self.main_menu()
     
    def edit_teacher_availability(self):
        if not os.path.exists(self.working_directory) or "user_data_sets" not in self.working_directory:
            messagebox.showwarning("Brak zestawu danych", "Najpierw wybierz zestaw danych użytkownika.")
            return

        path = os.path.join(self.working_directory, "teacher_availability.json")
        if not os.path.exists(path):
            messagebox.showerror("Błąd", "Plik teacher_availability.json nie istnieje")
            return

        with open(path, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            teachers = data.get("data", [])
            if len(teachers) <= 1: 
                messagebox.showwarning("Brak danych", "Brak dostępności nauczycieli do edycji")
                return

        scrollable_frame = self.create_scrollable_frame()

        label = tk.Label(scrollable_frame, text="Edytor dostępności nauczycieli - wybierz nauczyciela", font=("Arial", 16))
        label.pack(pady=10)

        for teacher in teachers[1:]:
            teacher_info = f"{teacher[0]} - {teacher[1]}"
            tk.Button(
                scrollable_frame,
                text=teacher_info,
                width=60,
                command=lambda t=teacher: self.edit_availability_hours(data, t, path)
            ).pack(pady=5)

        back_button = tk.Button(scrollable_frame, text="Powrót", width=40, command=self.data_set_editor)
        back_button.pack(pady=10)

    def edit_availability_hours(self, data, teacher, path):
        self.clear_window()

        label = tk.Label(self, text=f"Edytuj dostępność nauczyciela: {teacher[0]} ({teacher[1]})", font=("Arial", 16))
        label.pack(pady=10)

        days = ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek"]
        day_vars = []

        for i, day in enumerate(days):
            day_label = tk.Label(self, text=day)
            day_label.pack(pady=5)

            day_var = tk.StringVar(value=teacher[i + 2])
            day_vars.append(day_var)

            day_entry = tk.Entry(self, textvariable=day_var, width=40)
            day_entry.pack(pady=5)

        save_button = tk.Button(
            self,
            text="Zapisz",
            width=20,
            command=lambda: self.save_availability(data, teacher, day_vars, path)
        )
        save_button.pack(pady=10)

        back_button = tk.Button(self, text="Powrót", width=20, command=self.edit_teacher_availability)
        back_button.pack(pady=10)

    def save_availability(self, data, teacher, day_vars, path):
        for i, day_var in enumerate(day_vars):
            teacher[i + 2] = day_var.get()

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        messagebox.showinfo("Sukces", f"Dostępność nauczyciela {teacher[0]} została zaktualizowana.")
        self.edit_teacher_availability()

    def edit_teachers(self):
        self.clear_window()
        label = tk.Label(self, text="Edytor nauczycieli - wybierz akcję")
        label.pack(pady=10)

        options = [
            ("Dodaj nauczyciela", self.add_class_teacher),
            ("Modyfikuj nauczyciela", self.modify_teacher),
            ("Usuń nauczyciela", self.remove_class_teacher),
            ("Powrót", self.data_set_editor)
        ]

        for (text, command) in options:
            tk.Button(self, text=text, width=40, command=command).pack(pady=3)

    def edit_classes(self):
        self.clear_window()
        label = tk.Label(self, text="Edytor klas - wybierz klasę", font=("Arial", 16))
        label.pack(pady=10)

        path = os.path.join(self.working_directory, "classes.json")
        if not os.path.exists(path):
            messagebox.showerror("Błąd", "Plik classes.json nie istnieje.")
            self.data_set_editor()
            return

        with open(path, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            classes = data.get("classes", [])

        if not classes:
            messagebox.showwarning("Brak danych", "Brak klas do edycji.")
            self.data_set_editor()
            return

        for class_data in classes:
            tk.Button(
                self,
                text=class_data["name"],
                width=40,
                command=lambda c=class_data: self.edit_class_menu(c, classes, path)
            ).pack(pady=5)

        back_button = tk.Button(self, text="Powrót", width=40, command=self.data_set_editor)
        back_button.pack(pady=10)

    def edit_class_menu(self, class_data, classes, path):
        self.clear_window()

        label = tk.Label(self, text=f"Edytor klasy: {class_data['name']}", font=("Arial", 16))
        label.pack(pady=10)

        options = [
            ("Edytuj nazwę klasy", lambda: self.edit_class_name(class_data, classes, path)),
            ("Edytuj nauczycieli klasy", lambda: self.edit_class_teachers(class_data, classes, path)),
            ("Powrót", self.edit_classes)
        ]

        for (text, command) in options:
            tk.Button(self, text=text, width=40, command=command).pack(pady=5)

    def edit_class_name(self, class_data, classes, path):
        new_name = simpledialog.askstring("Edytuj nazwę klasy", "Podaj nową nazwę klasy:", initialvalue=class_data["name"])
        if new_name:
            class_data["name"] = new_name
            with open(path, 'w', encoding='utf-8') as f:
                json.dump({"classes": classes}, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Sukces", f"Nazwa klasy została zmieniona na {new_name}.")
        self.edit_class_menu(class_data, classes, path)

    def edit_class_teachers(self, class_data, classes, path):
        self.clear_window()
        
        label = tk.Label(self, text=f"Edytuj nauczycieli klasy: {class_data['name']}", font=("Arial", 16))
        label.pack(pady=10)

        teachers = class_data.get("teachers", [])

        def remove_class_teacher(t):
            teachers.remove(t)
            with open(path, 'w', encoding='utf-8') as f:
                json.dump({"classes": classes}, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Sukces", f"Nauczyciel {t} został usunięty.")
            self.edit_class_teachers(class_data, classes, path)
        
        def add_class_teacher():
            new_teacher = simpledialog.askstring("Dodaj nauczyciela", "Podaj nazwę nauczyciela:")
            if new_teacher:
                teachers.append(new_teacher)
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump({"classes": classes}, f, ensure_ascii=False, indent=4)
                messagebox.showinfo("Sukces", f"Nauczyciel {new_teacher} został dodany.")
                self.edit_class_teachers(class_data, classes, path)

        for teacher in teachers:
            frame = tk.Frame(self)
            frame.pack(pady=5)

            tk.Label(frame, text=teacher, width=30, anchor="w").pack(side="left")
            tk.Button(frame, text="Usuń", command=lambda t=teacher: remove_class_teacher(t)).pack(side="left", padx=5)

        tk.Button(self, text="Dodaj nauczyciela", width=40, command=add_class_teacher).pack(pady=10)
        tk.Button(self, text="Powrót", width=40, command=lambda: self.edit_class_menu(class_data, classes, path)).pack(pady=10)



    def modify_teacher(self):
        path = os.path.join(self.working_directory, "teachers.json")
        if not os.path.exists(path):
            messagebox.showerror("Błąd", "Plik teachers.json nie istnieje")
            return

        with open(path, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            names = [f"{t['id']}: {t['name']} {t['surname']}" for t in data.get("teachers", [])]
            if not names:
                messagebox.showwarning("Brak danych", "Brak nauczycieli do edycji")
                return
            selected = simpledialog.askstring("Modyfikuj nauczyciela", "Wybierz ID nauczyciela:\n" + "\n".join(names))
            if not selected or not selected.isdigit():
                return
            selected_id = int(selected)
            teacher = next((t for t in data["teachers"] if t["id"] == selected_id), None)
            if not teacher:
                messagebox.showerror("Błąd", "Nie znaleziono nauczyciela")
                return

            new_name = simpledialog.askstring("Nowe imię", "Podaj nowe imię:", initialvalue=teacher["name"])
            new_surname = simpledialog.askstring("Nowe nazwisko", "Podaj nowe nazwisko:", initialvalue=teacher["surname"])
            new_subjects_input = simpledialog.askstring("Nowe przedmioty", "Podaj nowe przedmioty (spacją oddzielone):", initialvalue=" ".join(teacher["subjects"]))

            if new_name: teacher["name"] = new_name
            if new_surname: teacher["surname"] = new_surname
            if new_subjects_input:
                teacher["subjects"] = [s for s in new_subjects_input.strip().split(" ") if s]

            f.seek(0)
            json.dump(data, f, ensure_ascii=False, indent=4)
            f.truncate()

            messagebox.showinfo("Sukces", "Dane nauczyciela zostały zaktualizowane")

    def add_class_teacher(self):
        if not os.path.exists(self.working_directory) or "user_data_sets" not in self.working_directory:
            messagebox.showwarning("Brak zestawu danych", "Najpierw wybierz zestaw danych.")
            return

        name = simpledialog.askstring("Dodaj nauczyciela", "Imię:")
        surname = simpledialog.askstring("Dodaj nauczyciela", "Nazwisko:")
        subjects_input = simpledialog.askstring("Dodaj nauczyciela", "Przedmioty (oddzielone spacją):")
        if not all([name, surname, subjects_input]):
            messagebox.showwarning("Brak danych", "Wszystkie pola są wymagane")
            return

        subjects = [s for s in subjects_input.strip().split(" ") if s]
        path = os.path.join(self.working_directory, "teachers.json")

        if not os.path.exists(path):
            with open(path, 'w', encoding='utf-8') as f:
                json.dump({"teachers": []}, f)

        with open(path, 'r+', encoding='utf-8') as f:
            data = json.load(f)
            new_id = max([t["id"] for t in data["teachers"]], default=0) + 1
            new_teacher = {
                "id": new_id,
                "name": name,
                "surname": surname,
                "subjects": subjects
            }
            data["teachers"].append(new_teacher)
            f.seek(0)
            json.dump(data, f, ensure_ascii=False, indent=4)
            f.truncate()

        messagebox.showinfo("Sukces", f"Dodano nauczyciela {name} {surname}")    

    def remove_class_teacher(self):
        if not os.path.exists(self.working_directory) or "user_data_sets" not in self.working_directory:
            messagebox.showwarning("Brak zestawu danych", "Najpierw wybierz zestaw danych użytkownika.")
            return

        path = os.path.join(self.working_directory, "teachers.json")
        if not os.path.exists(path):
            messagebox.showerror("Błąd", "Plik teachers.json nie istnieje")
            return

        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            teachers = data.get("teachers", [])
            if not teachers:
                messagebox.showwarning("Brak danych", "Brak nauczycieli do usunięcia")
                return

        self.clear_window()
        label = tk.Label(self, text="Usuń nauczyciela - wybierz kryterium", font=("Arial", 16))
        label.pack(pady=10)

        tk.Button(self, text="Usuń po ID", width=40, command=lambda: self.filter_teachers(teachers, "id")).pack(pady=5)
        tk.Button(self, text="Usuń po imieniu", width=40, command=lambda: self.filter_teachers(teachers, "name")).pack(pady=5)
        tk.Button(self, text="Usuń po nazwisku", width=40, command=lambda: self.filter_teachers(teachers, "surname")).pack(pady=5)
        tk.Button(self, text="Usuń po przedmiocie", width=40, command=lambda: self.filter_teachers(teachers, "subject")).pack(pady=5)

        back_button = tk.Button(self, text="Powrót", width=40, command=self.edit_teachers)
        back_button.pack(pady=10)

    def filter_teachers(self, teachers, filter_type):
        self.clear_window()

        label = tk.Label(self, text=f"Usuń nauczyciela - filtruj po {filter_type}", font=("Arial", 16))
        label.pack(pady=10)

        filter_value = simpledialog.askstring("Filtruj", f"Podaj wartość dla {filter_type}:")
        if not filter_value:
            self.remove_class_teacher()
            return

        if filter_type == "id":
            filtered_teachers = [t for t in teachers if str(t["id"]) == filter_value]
        elif filter_type == "name":
            filtered_teachers = [t for t in teachers if t["name"].lower() == filter_value.lower()]
        elif filter_type == "surname":
            filtered_teachers = [t for t in teachers if t["surname"].lower() == filter_value.lower()]
        elif filter_type == "subject":
            filtered_teachers = [t for t in teachers if filter_value.lower() in [s.lower() for s in t["subjects"]]]
        else:
            filtered_teachers = []

        if not filtered_teachers:
            messagebox.showwarning("Brak wyników", "Nie znaleziono nauczycieli spełniających kryteria")
            self.remove_class_teacher()
            return

        for teacher in filtered_teachers:
            teacher_info = f"ID: {teacher['id']}, Imię: {teacher['name']}, Nazwisko: {teacher['surname']}, Przedmioty: {', '.join(teacher['subjects'])}"
            tk.Button(
                self,
                text=teacher_info,
                width=60,
                command=lambda t=teacher: self.confirm_remove_class_teacher(teachers, t)
            ).pack(pady=5)

        back_button = tk.Button(self, text="Powrót", width=40, command=self.remove_class_teacher)
        back_button.pack(pady=10)

    def confirm_remove_class_teacher(self, teachers, teacher):
        confirm = messagebox.askyesno(
            "Potwierdzenie",
            f"Czy na pewno chcesz usunąć nauczyciela?\n\nID: {teacher['id']}\nImię: {teacher['name']}\nNazwisko: {teacher['surname']}\nPrzedmioty: {', '.join(teacher['subjects'])}"
        )
        if confirm:
            teachers.remove(teacher)
            path = os.path.join(self.working_directory, "teachers.json")
            with open(path, 'w', encoding='utf-8') as f:
                json.dump({"teachers": teachers}, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Sukces", "Nauczyciel został usunięty")
        self.remove_class_teacher()

    def display_plan(self, plan, class_name, live_preview_frame):
        # Usuń poprzednią zawartość ramki
        for widget in live_preview_frame.winfo_children():
            widget.destroy()

        # Dodaj nagłówek
        label = tk.Label(live_preview_frame, text=f"Podgląd planu dla klasy: {class_name}", font=("Arial", 14))
        label.pack(pady=10)

        # Wyświetl plan
        for day, hours in plan.items():
            day_label = tk.Label(live_preview_frame, text=f"{day.capitalize()}: {', '.join(str(h) if h else '-' for h in hours)}")
            day_label.pack()

        # Odśwież interfejs użytkownika
        self.update_idletasks()

if __name__ == "__main__":
    app = App()
    app.mainloop()
