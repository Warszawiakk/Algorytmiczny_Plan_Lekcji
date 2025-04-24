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
        self.working_directory = "data_sets/szkoła_średnia/user_presets/technikum/technischools"

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
        btn3 = tk.Button(self, text="Stwórz nowy preset", width=30, height=2, command=self.initialize_new_preset)
        btn4 = tk.Button(self, text="Exit", width=30, height=2, command=self.quit)

        for btn in [btn1, btn2, btn3, btn4]:
            btn.pack(pady=5)

    def calculate_plan(self):
        self.clear_window()
        label = tk.Label(self, text="Tutaj będzie GUI do obliczania planu")
        label.pack(pady=50)
        back = tk.Button(self, text="Wstecz", command=self.main_menu)
        back.pack()

    def initialize_new_preset(self):
        self.clear_window()
        name = simpledialog.askstring("Nazwa presetu", "Podaj nazwę nowego presetu:")
        if not name:
            self.main_menu()
            return

        school_type = simpledialog.askinteger("Typ szkoły", "Wybierz typ szkoły:\n1: Podstawowa\n2: Liceum\n3: Technikum", minvalue=1, maxvalue=3)
        if not school_type:
            self.main_menu()
            return

        directory = "data_sets/"
        if school_type == 1:
            directory += "szkoła_podstawowa"
            max_class = 8
        elif school_type == 2:
            directory += "szkoła_średnia/user_presets/liceum"
            max_class = 4
        elif school_type == 3:
            directory += "szkoła_średnia/user_presets/technikum"
            max_class = 5

        final_path = os.path.join(directory, name)
        try:
            os.makedirs(final_path)
            for i in range(max_class):
                open(os.path.join(final_path, f"klasa{i}.json"), 'w').close()
            open(os.path.join(final_path, "teacher_availability.json"), 'w').close()
            open(os.path.join(final_path, "classes.json"), 'w').close()
            open(os.path.join(final_path, "teachers.json"), 'w').close()
            messagebox.showinfo("Sukces", "Preset został utworzony.")
        except FileExistsError:
            messagebox.showerror("Błąd", "Preset już istnieje.")

        self.main_menu()

    def preset_editor(self):
        self.clear_window()
        label = tk.Label(self, text="Edytor presetów - wybierz akcję")
        label.pack(pady=10)

        options = [
            ("Wybierz preset", self.select_preset),
            ("Edytuj klasy", self.edit_classes),
            ("Edytuj dostępność nauczycieli", self.edit_availability),
            ("Edytuj nauczycieli", self.edit_teachers),
            ("Powrót", self.main_menu)
        ]

        for (text, command) in options:
            tk.Button(self, text=text, width=40, command=command).pack(pady=4)

    def select_preset(self):
        # Ask the user to choose the school type
        school_type = simpledialog.askstring(
            "Wybierz typ szkoły",
            "Wybierz typ szkoły:\n1: Liceum\n2: Technikum\n3: Szkoła Zawodowa"
        )

        if school_type == "1":
            school_folder = "liceum"
        elif school_type == "2":
            school_folder = "technikum"
        elif school_type == "3":
            school_folder = "szkoła_zawodowa"
        else:
            messagebox.showerror("Błąd", "Nieprawidłowy wybór typu szkoły.")
            return

        # Update the presets directory based on the chosen school type
        presets_path = os.path.join("data_sets/szkoła_średnia/user_presets", school_folder)
        if not os.path.exists(presets_path):
            messagebox.showwarning("Brak danych", f"Brak katalogu dla {school_folder}.")
            return

        # List presets in the selected school type directory
        presets = os.listdir(presets_path)
        if not presets:
            messagebox.showwarning("Brak danych", f"Brak presetów w katalogu {school_folder}.")
            return

        # Ask the user to select a preset
        selected = simpledialog.askstring(
            "Wybierz preset",
            f"Dostępne w {school_folder}: {', '.join(presets)}\nWpisz nazwę:"
        )

        if selected and selected in presets:
            self.working_directory = os.path.join(presets_path, selected)
            messagebox.showinfo("Wybrano", f"Aktywny katalog: {self.working_directory}")
        else:
            messagebox.showerror("Błąd", "Nieprawidłowa nazwa presetu.")
     
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
            ("Usuń nauczyciela", lambda: messagebox.showinfo("TODO", "Usuwanie nauczyciela jeszcze niezaimplementowane")),
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
            messagebox.showwarning("Brak presetu", "Najpierw wybierz preset użytkownika.")
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

if __name__ == "__main__":
    app = App()
    app.mainloop()
