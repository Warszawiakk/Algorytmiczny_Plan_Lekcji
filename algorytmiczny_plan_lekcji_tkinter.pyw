import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import json

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Algorytmiczny Układacz Planu")
        self.geometry("800x300")
        self.iconbitmap("icon.ico")
        self.working_directory = "data_sets/szkoła_średnia/user_presets/"

        self.main_menu()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def main_menu(self):
        self.clear_window()

        title = tk.Label(self, text="ALGORYTMICZNY UKŁADACZ PLANU alpha 0.1", font=("Arial", 16, "bold"))
        title.pack(pady=20)

        btn1 = tk.Button(self, text="Oblicz plan", width=30, height=2, command=self.calculate_plan)
        btn2 = tk.Button(self, text="Edytuj dane", width=30, height=2, command=self.preset_editor)
        btn3 = tk.Button(self, text="Zarządzaj zestawami danych", width=30, height=2, command=self.preset_manager)
        btn4 = tk.Button(self, text="Exit", width=30, height=2, command=self.quit)

        for btn in [btn1, btn2, btn3, btn4]:
            btn.pack(pady=5)

    def calculate_plan(self):
        self.clear_window()
        label = tk.Label(self, text="Tutaj będzie GUI do obliczania planu")
        label.pack(pady=50)
        back = tk.Button(self, text="Wstecz", command=self.main_menu)
        back.pack()

    def preset_manager(self):
        self.clear_window()

        label = tk.Label(self, text="Zarządzanie zestawami danych", font=("Arial", 16))
        label.pack(pady=10)

        new_preset_button = tk.Button(self, text="Stwórz nowy preset", width=40, command=self.initialize_new_preset)
        new_preset_button.pack(pady=5)

        remove_preset_button = tk.Button(self, text="Usuń preset", width=40, command=self.remove_preset)
        remove_preset_button.pack(pady=5)
        
        rename_preset_button = tk.Button(self, text="Zmień nazwę zestawu danych", width=40, command=self.rename_preset)
        rename_preset_button.pack(pady=5)

        back_button = tk.Button(self, text="Powrót", width=40, command=self.main_menu)
        back_button.pack(pady=10)

    def remove_preset(self):
        self.clear_window()

        label = tk.Label(self, text="Usuń zestaw danych - wybierz typ szkoły", font=("Arial", 16))
        label.pack(pady=10)

        school_types = {
            "Podstawowa": "szkoła_podstawowa",
            "Liceum": "szkoła_średnia/user_presets/liceum",
            "Technikum": "szkoła_średnia/user_presets/technikum"
        }

        for school_name, school_folder in school_types.items():
            tk.Button(
                self,
                text=school_name,
                width=40,
                command=lambda folder=school_folder: self.select_preset_to_remove(folder)
            ).pack(pady=5)

        back_button = tk.Button(self, text="Powrót", width=40, command=self.preset_manager)
        back_button.pack(pady=10)

    def select_preset_to_remove(self, school_folder):
        self.clear_window()

        presets_path = os.path.join("data_sets", school_folder)
        if not os.path.exists(presets_path):
            messagebox.showwarning("Brak danych", f"Brak katalogu dla {school_folder}.")
            self.remove_preset()
            return

        presets = os.listdir(presets_path)
        if not presets:
            messagebox.showwarning("Brak danych", f"Brak zestawów danych w katalogu {school_folder}.")
            self.remove_preset()
            return

        label = tk.Label(self, text=f"Wybierz zestaw danych do usunięcia z {school_folder}", font=("Arial", 14))
        label.pack(pady=10)

        for preset in presets:
            tk.Button(
                self,
                text=preset,
                width=40,
                command=lambda p=preset: self.confirm_remove_preset(presets_path, p)
            ).pack(pady=5)

        back_button = tk.Button(self, text="Powrót", width=40, command=self.remove_preset)
        back_button.pack(pady=10)

    def confirm_remove_preset(self, presets_path, preset):
        confirm = messagebox.askyesno("Potwierdzenie", f"Czy na pewno chcesz usunąć zestaw danych '{preset}'?")
        if confirm:
            preset_path = os.path.join(presets_path, preset)
            try:
                import shutil
                shutil.rmtree(preset_path)
                messagebox.showinfo("Sukces", f"zestaw danych '{preset}' został usunięty.")
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się usunąć zestawu danych: {e}")
        self.remove_preset()
        
    def rename_preset(self):
        self.clear_window()

        label = tk.Label(self, text="Zmień nazwę zestawu danych - wybierz typ szkoły", font=("Arial", 16))
        label.pack(pady=10)

        school_types = {
            "Podstawowa": "szkoła_podstawowa",
            "Liceum": "szkoła_średnia/user_presets/liceum",
            "Technikum": "szkoła_średnia/user_presets/technikum"
        }

        for school_name, school_folder in school_types.items():
            tk.Button(
                self,
                text=school_name,
                width=40,
                command=lambda folder=school_folder: self.select_preset_to_rename(folder)
            ).pack(pady=5)

        back_button = tk.Button(self, text="Powrót", width=40, command=self.preset_manager)
        back_button.pack(pady=10)

    def select_preset_to_rename(self, school_folder):
        self.clear_window()

        presets_path = os.path.join("data_sets", school_folder)
        if not os.path.exists(presets_path):
            messagebox.showwarning("Brak danych", f"Brak katalogu dla {school_folder}.")
            self.rename_preset()
            return

        presets = os.listdir(presets_path)
        if not presets:
            messagebox.showwarning("Brak danych", f"Brak zestawów danych w katalogu {school_folder}.")
            self.rename_preset()
            return

        label = tk.Label(self, text=f"Wybierz zestaw danych do zmiany nazwy z {school_folder}", font=("Arial", 14))
        label.pack(pady=10)

        for preset in presets:
            tk.Button(
                self,
                text=preset,
                width=40,
                command=lambda p=preset: self.confirm_rename_preset(presets_path, p)
            ).pack(pady=5)

        back_button = tk.Button(self, text="Powrót", width=40, command=self.rename_preset)
        back_button.pack(pady=10)

    def confirm_rename_preset(self, presets_path, preset):
        new_name = simpledialog.askstring("Zmień nazwę zestawu danych", f"Podaj nową nazwę dla zestawu danych '{preset}':")
        if not new_name:
            return

        old_path = os.path.join(presets_path, preset)
        new_path = os.path.join(presets_path, new_name)

        if os.path.exists(new_path):
            messagebox.showerror("Błąd", "Preset o tej nazwie już istnieje.")
            return

        try:
            os.rename(old_path, new_path)
            messagebox.showinfo("Sukces", f"Preset '{preset}' został przemianowany na '{new_name}'.")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się zmienić nazwy zestawu danych: {e}")

        self.rename_preset()

    def initialize_new_preset(self):
        self.clear_window()

        label = tk.Label(self, text="Stwórz nowy zestaw danych - wybierz typ szkoły", font=("Arial", 16))
        label.pack(pady=10)

        school_types = {
            "Podstawowa": ("szkoła_podstawowa", 8),
            "Liceum": ("szkoła_średnia/user_presets/liceum", 4),
            "Technikum": ("szkoła_średnia/user_presets/technikum", 5)
        }

        for school_name, (directory, max_class) in school_types.items():
            tk.Button(
                self,
                text=school_name,
                width=40,
                command=lambda d=directory, m=max_class: self.create_preset(d, m)
            ).pack(pady=5)

        back_button = tk.Button(self, text="Powrót", width=40, command=self.preset_manager)
        back_button.pack(pady=10)

    def create_preset(self, directory, max_class):
        name = simpledialog.askstring("Nazwa zestawu danych", "Podaj nazwę nowego zestawu danych:")
        if not name:
            self.preset_manager()
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

        self.preset_manager()
        
    def edit_class_year(self):
        self.clear_window()
        label = tk.Label(self, text="Edytor roczników - wybierz akcję")
        label.pack(pady=10)
        options = [
            ("Wybierz rocznik", self.select_class_year),
            ("Edytuj wymiar godzinowy przedmiotów rocznika", self.edit_class_year_hours),
            ("Edytuj przedmioty dla rocznika", self.edit_class_year_subjects),
            ("Dodaj rocznik", self.add_class_year),
            ("Powrót", self.preset_editor)
        ]
        for (text, command) in options:
            tk.Button(self, text=text, width=40, command=command).pack(pady=4)
    
    def select_class_year(self):
        self.clear_window()
        label = tk.Label(self, text="Wybierz rocznik - funkcja jeszcze niezaimplementowana")
        label.pack(pady=50)
        back = tk.Button(self, text="Wstecz", command=self.edit_class_year)
        back.pack()
    
    def edit_class_year_hours(self):
        self.clear_window()
        label = tk.Label(self, text="Edytor wymiaru godzinowego przedmiotów rocznika")
        label.pack(pady=20)
        
        options = [
            ("Powrót", self.edit_class_year)
        ]
        
        for (text, command) in options:
            tk.Button(self, text=text, width=40, command=command).pack(pady=4)
        
    def edit_class_year_subjects(self):
        self.clear_window()
        label = tk.Label(self, text="Edytor przedmiotów dla rocznika")
        label.pack(pady=20)
        
        options = [
            ("Powrót", self.edit_class_year)
        ]
        
        for (text, command) in options:
            tk.Button(self, text=text, width=40, command=command).pack(pady=4)
    
    def add_class_year(self):
        self.clear_window()
        options = [
            ("Powrót", self.edit_class_year)
        ]
        
        for (text, command) in options:
            tk.Button(self, text=text, width=40, command=command).pack(pady=4)
        
    def preset_editor(self):
        self.clear_window()
        label = tk.Label(self, text="Edytor zestawów danych - wybierz akcję")
        label.pack(pady=10)
        
        select_preset_button = tk.Button(self, text="Wybierz zestaw danych", width=40, command=self.select_preset)
        select_preset_button.pack(pady=4)
            
        self.edit_classes_button = tk.Button(self, text="Edytuj klasy", width=40, command=self.edit_classes)
        self.edit_years_button = tk.Button(self, text="Edytuj roczniki", width=40, command=self.edit_class_year)
        self.edit_availability_button = tk.Button(self, text="Edytuj dostępność nauczycieli", width=40, command=self.edit_availability)
        self.edit_teachers_button = tk.Button(self, text="Edytuj nauczycieli", width=40, command=self.edit_teachers)

        self.edit_classes_button.pack(pady=4)
        self.edit_years_button.pack(pady=4)
        self.edit_availability_button.pack(pady=4)
        self.edit_teachers_button.pack(pady=4)
        
        if self.working_directory == "data_sets/szkoła_średnia/user_presets/":
            self.edit_classes_button.config(state="disabled")
            self.edit_years_button.config(state="disabled")
            self.edit_availability_button.config(state="disabled")
            self.edit_teachers_button.config(state="disabled")
        else:
            self.edit_classes_button.config(state="normal")
            self.edit_years_button.config(state="normal")
            self.edit_availability_button.config(state="normal")
            self.edit_teachers_button.config(state="normal")
        
        back_button = tk.Button(self, text="Powrót", width=40, command=self.main_menu)
        back_button.pack(pady=10)

    def select_preset(self):
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
                command=lambda folder=school_folder: self.display_presets(folder)
            ).pack(pady=5)
        
        

        back_button = tk.Button(self, text="Powrót", width=40, command=self.preset_editor)
        back_button.pack(pady=10)

    def display_presets(self, school_folder):
        self.clear_window()

        presets_path = os.path.join("data_sets/szkoła_średnia/user_presets", school_folder)
        if not os.path.exists(presets_path):
            messagebox.showwarning("Brak danych", f"Brak katalogu dla {school_folder}.")
            self.preset_editor()
            return

        presets = os.listdir(presets_path)
        if not presets:
            messagebox.showwarning("Brak danych", f"Brak zestawów danych w katalogu {school_folder}.")
            self.preset_editor()
            return

        label = tk.Label(self, text=f"Wybierz zestaw danych z {school_folder}", font=("Arial", 14))
        label.pack(pady=10)

        for preset in presets:
            tk.Button(
                self,
                text=preset,
                width=40,
                command=lambda p=preset: self.set_working_directory(presets_path, p)
            ).pack(pady=5)

        back_button = tk.Button(self, text="Powrót", width=40, command=self.preset_editor)
        back_button.pack(pady=10)

    def set_working_directory(self, presets_path, preset):
        self.working_directory = os.path.join(presets_path, preset)
        messagebox.showinfo("Wybrano", f"Aktywny katalog: {self.working_directory}")

        self.main_menu()
     
    def edit_availability(self):
        self.clear_window()
        label = tk.Label(self, text="Edytor dostępności nauczycieli - funkcja jeszcze niezaimplementowana")
        label.pack(pady=50)
        back = tk.Button(self, text="Wstecz", command=self.preset_editor)
        back.pack()
    
    def edit_teachers(self):
        self.clear_window()
        label = tk.Label(self, text="Edytor nauczycieli - wybierz akcję")
        label.pack(pady=10)

        options = [
            ("Dodaj nauczyciela", self.add_teacher),
            ("Modyfikuj nauczyciela", self.modify_teacher),
            ("Usuń nauczyciela", self.remove_teacher),
            ("Powrót", self.preset_editor)
        ]

        for (text, command) in options:
            tk.Button(self, text=text, width=40, command=command).pack(pady=3)

    def edit_classes(self):
        self.clear_window()
        label = tk.Label(self, text="Edytor klas - funkcja jeszcze niezaimplementowana")
        label.pack(pady=50)
        back = tk.Button(self, text="Wstecz", command=self.preset_editor)
        back.pack()

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

    def add_teacher(self):
        if not os.path.exists(self.working_directory) or "user_presets" not in self.working_directory:
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

    def remove_teacher(self):
        if not os.path.exists(self.working_directory) or "user_presets" not in self.working_directory:
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

        # Buttons for filtering options
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

        # Ask for the filter value
        filter_value = simpledialog.askstring("Filtruj", f"Podaj wartość dla {filter_type}:")
        if not filter_value:
            self.remove_teacher()
            return

        # Filter teachers based on the selected filter type
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
            self.remove_teacher()
            return

        # Display matching teachers
        for teacher in filtered_teachers:
            teacher_info = f"ID: {teacher['id']}, Imię: {teacher['name']}, Nazwisko: {teacher['surname']}, Przedmioty: {', '.join(teacher['subjects'])}"
            tk.Button(
                self,
                text=teacher_info,
                width=60,
                command=lambda t=teacher: self.confirm_remove_teacher(teachers, t)
            ).pack(pady=5)

        back_button = tk.Button(self, text="Powrót", width=40, command=self.remove_teacher)
        back_button.pack(pady=10)

    def confirm_remove_teacher(self, teachers, teacher):
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
        self.remove_teacher()

if __name__ == "__main__":
    app = App()
    app.mainloop()
