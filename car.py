from datetime import datetime, date
import os
import tkinter as tk
from tkinter import messagebox, font
import requests
from bs4 import BeautifulSoup
import re

money_list = []

live_diesel_price = 0
live_gas_price = 0
fuel_checks = int()
your_average_consumption = int()
total_money = 0
class Vehicle:
    def __init__(self):
        self.Type = ""
        self.Brand = ""
        self.Model = ""
        self.fuelType = ""
        self.Insurance = ""
        self.Inspection = ""

    def load_from_file(self, filename="vehicle_data.txt"):
        """Load vehicle data from file."""
        global fuel_checks
        global your_average_consumption
        global total_money
        if os.path.exists(filename):
            with open(filename, "r") as file:
                data = file.readlines()
                if len(data) >= 6:
                    self.Type = data[0].strip()
                    self.Brand = data[1].strip()
                    self.Model = data[2].strip()
                    self.fuelType = data[3].strip()
                    self.Insurance = data[4].strip()
                    self.Inspection = data[5].strip()
            with open("consumption.txt","r",newline='') as file:
                list = file.readlines()
                your_average_consumption = int(list[0])
                fuel_checks = int(list[1])
            with open("money.txt","r",newline='') as file:
                total_money = float(file.readline().strip())

    def save_to_file(self, filename="vehicle_data.txt"):
        """Save vehicle data to file."""
        with open(filename, "w") as file:
            file.write(f"{self.Type}\n")
            file.write(f"{self.Brand}\n")
            file.write(f"{self.Model}\n")
            file.write(f"{self.fuelType}\n")
            file.write(f"{self.Insurance}\n")
            file.write(f"{self.Inspection}\n")
        with open("consumption.txt","w") as file:
            file.write(f"{your_average_consumption}\n")
            file.write(f"{fuel_checks}\n")
        with open("money.txt","w") as file:
            file.write(f"{total_money}")
class VehicleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vehicle Management")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        self.root.geometry(f"{screen_width}x{screen_height}")
        self.root.configure(bg="#2b3638")
        self.font = font.Font(family='Segoe UI', size=14, weight='bold')
        self.vehicle = Vehicle()
        self.vehicle.load_from_file()
        self.popup_insurance()
        self.popup_inspection()
        if not self.vehicle.Type:
            self.show_vehicle_input()
        else:
            self.show_menu()

    def show_vehicle_input(self):
        self.clear_window()

        frame = tk.Frame(self.root, bg="#FFFFFF", padx=20, pady=20)
        frame.pack(pady=20)

        tk.Label(frame, text="Vehicle Type:", bg="#FFFFFF", fg="#2C3E50", font=self.font).pack(fill=tk.X, pady=5)

        self.type_entry = tk.StringVar(value="car")

        type_options = ["car", "van", "truck"]
        self.type_menu = tk.OptionMenu(frame, self.type_entry, *type_options)
        self.type_menu.config(font=self.font, bg="#3498DB", fg="#FFFFFF")
        self.type_menu.pack(fill=tk.X, pady=5)

        tk.Label(frame, text="Brand Name (ex. Audi):", bg="#FFFFFF", fg="#2C3E50", font=self.font).pack(fill=tk.X, pady=5)
        self.brand_entry = tk.Entry(frame, font=self.font, bg="#E7F0F8")
        self.brand_entry.pack(fill=tk.X, pady=5)

        tk.Label(frame, text="Model Name (ex. A8):", bg="#FFFFFF", fg="#2C3E50", font=self.font).pack(fill=tk.X, pady=5)
        self.model_entry = tk.Entry(frame, font=self.font, bg="#E7F0F8")
        self.model_entry.pack(fill=tk.X, pady=5)

        tk.Label(frame, text="Fuel Type:", bg="#FFFFFF", fg="#2C3E50", font=self.font).pack(fill=tk.X, pady=5)

        self.fuel_entry = tk.StringVar(value="gas")

        fuel_options = ["gas", "diesel"]
        self.fuel_menu = tk.OptionMenu(frame, self.fuel_entry, *fuel_options)
        self.fuel_menu.config(font=self.font, bg="#3498DB", fg="#FFFFFF")
        self.fuel_menu.pack(fill=tk.X, pady=5)

        tk.Button(frame, text="✓", command=self.save_vehicle_details, bg="#27AE60", fg="white", font=self.font, relief="flat").pack(pady=10)
        with open("transactions.txt","w") as f:
            f.write("")
        with open("consumption.txt","w") as f:
            f.write('0'+'\n')
            f.write('0')
        with open("vehicle_data.txt","w") as f:
            f.write("")
        with open("money.txt","w") as f:
            f.write("0")
        global total_money
        global money_list
        global live_diesel_price
        global live_gas_price
        global fuel_checks
        global your_average_consumption
        money_list = []

        live_diesel_price = 0
        live_gas_price = 0
        fuel_checks = int()
        your_average_consumption = int()
        total_money = 0
        self.vehicle.Insurance = ""
        self.vehicle.Inspection = ""
    def save_vehicle_details(self):
        """Save vehicle details entered by the user."""
        self.vehicle.Type = self.type_entry.get()
        self.vehicle.Brand = self.brand_entry.get()
        self.vehicle.Model = self.model_entry.get()
        self.vehicle.fuelType = self.fuel_entry.get()

        self.vehicle.save_to_file()
        self.show_menu()

    def show_menu(self):
        """Display the main menu."""
        self.vehicle.save_to_file()
        global total_money
        self.clear_window()

        frame = tk.Frame(self.root, bg="#39474a", padx=20, pady=20)
        frame.pack(pady=20)

        tk.Label(frame, text="=== Main Menu ===", bg="#39474a",fg="white", font=self.font).pack(pady=10)
        tk.Label(frame, text=f"Fuel expenses: {"{:.2f}".format(total_money)} RON", bg="#39474a",fg="white", font=self.font).pack(pady=10)
        tk.Button(frame, text="🕑 Drive History", command=self.road_history, bg="#007bff", fg="white", font=self.font,relief="flat").pack(pady=5)
        tk.Button(frame, text="⚙️ Car Settings", command=self.car_details, bg="#007bff", fg="white", font=self.font,relief="flat").pack(pady=5)

        tk.Button(frame, text="Insurance", command=self.show_insurance_menu, bg="#007bff", fg="white", font=self.font,relief="flat").pack(pady=5)
        tk.Button(frame, text="Inspection", command=self.show_inspection_menu, bg="#007bff", fg="white", font=self.font,relief="flat").pack(pady=5)
        tk.Button(frame, text="Exit", command=self.save_and_exit, bg="#dc3545", fg="white", font=self.font, relief="flat").pack(pady=10)

    def get_fuel_price(self):
        global live_gas_price
        global live_diesel_price
        url = "https://www.globalpetrolprices.com/Romania/"
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            value_elements = soup.find_all(class_="value")
        match = re.findall(r'\d+\.\d+|\d+', value_elements[4].get_text())
        match2 = re.findall(r'\d+\.\d+|\d+', value_elements[7].get_text())
        if match:
            gasprice = ''.join(match)

        if match2:
            dieselprice = ''.join(match2)

        live_gas_price = gasprice
        live_diesel_price = dieselprice
        self.clear_window()
        frame = tk.Frame(self.root, bg="#39474a", padx=20, pady=20)
        frame.pack(pady=20)


        tk.Label(frame, text=f'Gas: {gasprice} RON', bg="#39474a",fg="white", font=self.font).pack(pady=10)
        tk.Label(frame, text=f'Diesel: {dieselprice} RON', bg="#39474a",fg="white", font=self.font).pack(pady=10)
        tk.Button(frame, text="Calculator", command=self.calculate_fuel, bg="#007bff", fg="white", font=self.font,relief="flat").pack(pady=10)
        tk.Button(frame, text="Back to Menu", command=self.show_menu, bg="#dc3545", fg="white", font=self.font,relief="flat").pack(pady=10)
    def calculate_fuel(self):
        self.clear_window()
        frame = tk.Frame(self.root, bg="#39474a", padx=20, pady=20)
        frame.pack(pady=20)

        tk.Label(frame, text="Distance (Km):", bg="#39474a",fg="white", font=self.font).pack(pady=10)
        self.km_entry = tk.Entry(frame, font=self.font)
        self.km_entry.pack(fill=tk.X, pady=5)

        tk.Label(frame, text="Average Fuel Consumption (l/100km):", bg="#39474a",fg="white", font=self.font).pack(pady=10)
        self.avg_entry = tk.Entry(frame, font=self.font)
        self.avg_entry.pack(fill=tk.X, pady=5)
        tk.Button(frame, text="Calculate", command=self.money_spent, bg="#007bff", fg="white", font=self.font,relief="flat").pack(pady=10)

        tk.Button(frame, text="Back to Menu", command=self.show_menu, bg="#dc3545", fg="white", font=self.font,relief="flat").pack(pady=10)
    def money_spent(self):
        global live_gas_price
        global live_diesel_price
        global fuel_checks
        global your_average_consumption
        global total_money
        with open("vehicle_data.txt","r") as f:
            list = f.readlines()
        if list[3]=="diesel":
            local_price = live_diesel_price
        else:
            local_price = live_gas_price

        result = (float(self.km_entry.get())/100) * float(self.avg_entry.get()) * float(local_price)
        total_money += float(result)
        messagebox.showinfo("Calculator", f'{"{:.2f}".format(result)} RON spent on fuel')

        fuel_checks += 1
        your_average_consumption += int(self.avg_entry.get())
        today = date.today()
        transaction = f"{today} | {str("{:.2f}".format(result))} RON ({float(self.km_entry.get())} Km)"
        with open ("transactions.txt","a") as f:
            f.write(transaction+'\n')

    def road_history(self):
        self.clear_window()


        frame = tk.Frame(self.root, bg="#39474a")
        frame.pack(pady=20, fill=tk.BOTH, expand=True)


        canvas = tk.Canvas(frame, bg="#39474a")
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)


        inner_frame = tk.Frame(canvas, bg="#39474a")
        canvas.create_window((0, 0), window=inner_frame, anchor='nw')


        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=scrollbar.set)


        with open("transactions.txt", "r", newline='') as f:
            transactions = f.readlines()

        for transaction in transactions:
            tk.Label(inner_frame, text=transaction.strip(), bg="#39474a",fg="white", font=self.font).pack(pady=1)


        inner_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        tk.Button(frame, text="Back to Menu", command=self.show_menu, bg="#dc3545", fg="white", font=self.font,relief="flat").pack(pady=10)
    def car_details(self):
        self.clear_window()
        frame = tk.Frame(self.root, bg="#39474a", padx=20, pady=20)
        frame.pack(pady=20)
        tk.Label(frame, text="=== Car Details ===", bg="#39474a",fg="white", font=self.font).pack(pady=10)
        with open("vehicle_data.txt","r",newline='') as f:
            details = f.readlines()
        tk.Label(frame, text=f"Fuel Type: {details[3]}", bg="#39474a", fg="white", font=self.font).pack(pady=1)
        if int(fuel_checks)>0:
            tk.Label(frame, text=f"Your {self.vehicle.Brand} {self.vehicle.Model} has an average consumption of:{"{:.2f}".format(int(your_average_consumption)/int(fuel_checks))}l/100km", bg="#39474a",fg="white", font=self.font).pack(pady=10)
            if int(your_average_consumption) / int(fuel_checks) > 9:
                tk.Label(frame, text="High Consumption", bg="#dc3545",fg="white", font=self.font).pack(pady=3)
            else:
                tk.Label(frame, text="Normal Consumption", bg="#119911",fg="white", font=self.font).pack(pady=3)

        tk.Button(frame, text="⛽ Fuel Settings", command=self.get_fuel_price, bg="#007bff", fg="white", font=self.font,relief="flat").pack(pady=7)
        tk.Button(frame, text="🔄 Change and Reset", command=self.show_vehicle_input, bg="#007bff", fg="white", font=self.font,relief="flat").pack(pady=7)
        tk.Button(frame, text="Back to Menu", command=self.show_menu, bg="#dc3545", fg="white", font=self.font,relief="flat").pack(pady=10)

    def show_insurance_menu(self):
        """Display the insurance menu."""
        self.clear_window()

        frame = tk.Frame(self.root, bg="#39474a", padx=20, pady=20)
        frame.pack(pady=20)

        tk.Label(frame, text="=== Insurance Menu ===", bg="#39474a",fg="white", font=self.font).pack(pady=10)
        tk.Button(frame, text="Add Insurance", command=self.add_insurance, bg="#007bff", fg="white", font=self.font, relief="flat").pack(pady=5)
        tk.Button(frame, text="Check Insurance", command=self.check_insurance, bg="#007bff", fg="white", font=self.font, relief="flat").pack(pady=5)
        tk.Button(frame, text="Back to Menu", command=self.show_menu, bg="#dc3545", fg="white", font=self.font, relief="flat").pack(pady=10)

    def add_insurance(self):
        """Add insurance expiration date."""
        self.clear_window()
        frame = tk.Frame(self.root, bg="#39474a", padx=20, pady=20)
        frame.pack(pady=20)

        tk.Label(frame, text="Insurance expire date (format: DD-MM-YYYY):", bg="#39474a",fg="white", font=self.font).pack(fill=tk.X, pady=5)
        self.insurance_entry = tk.Entry(frame, font=self.font)
        self.insurance_entry.pack(fill=tk.X, pady=5)
        tk.Button(frame, text="✓", command=self.save_insurance, bg="#007bff", fg="white", font=self.font, relief="flat").pack(pady=10)
        tk.Button(frame, text="Back", command=self.show_insurance_menu, bg="#007bff", fg="white", font=self.font, relief="flat").pack(pady=5)

    def save_insurance(self):
        """Save insurance expiration date."""
        self.vehicle.Insurance = self.insurance_entry.get()
        self.vehicle.save_to_file()
        messagebox.showinfo("Info", "Insurance date saved successfully!")
        self.show_insurance_menu()

    def check_insurance(self):
        """Check insurance expiration date."""
        if self.vehicle.Insurance:
            insurance_date = datetime.strptime(self.vehicle.Insurance, "%d-%m-%Y").date()
            today = date.today()
            if insurance_date < today:
                messagebox.showwarning("Warning", "Insurance Expired!")
            else:
                messagebox.showinfo("Info", f"Insurance will expire on {self.vehicle.Insurance}")
        else:
            messagebox.showwarning("Warning", "No insurance data available.")
    def popup_insurance(self):
        """Check insurance expiration date."""
        if self.vehicle.Insurance:
            insurance_date = datetime.strptime(self.vehicle.Insurance, "%d-%m-%Y").date()
            today = date.today()
            if insurance_date < today:
                messagebox.showwarning("Warning", "Insurance Expired!")

    def show_inspection_menu(self):
        """Display the inspection menu."""
        self.clear_window()

        frame = tk.Frame(self.root, bg="#39474a", padx=20, pady=20)
        frame.pack(pady=20)

        tk.Label(frame, text="=== Inspection Menu ===", bg="#39474a",fg="white", font=self.font).pack(pady=10)
        tk.Button(frame, text="Add Inspection", command=self.add_inspection, bg="#007bff", fg="white", font=self.font, relief="flat").pack(pady=5)
        tk.Button(frame, text="Check Inspection", command=self.check_inspection, bg="#007bff", fg="white", font=self.font, relief="flat").pack(pady=5)
        tk.Button(frame, text="Back to Menu", command=self.show_menu, bg="#dc3545", fg="white", font=self.font, relief="flat").pack(pady=10)

    def add_inspection(self):
        """Add inspection expiration date."""
        self.clear_window()
        frame = tk.Frame(self.root, bg="#39474a", padx=20, pady=20)
        frame.pack(pady=20)

        tk.Label(frame, text="Inspection expire date (format: DD-MM-YYYY):", bg="#39474a", font=self.font).pack(fill=tk.X, pady=5)
        self.inspection_entry = tk.Entry(frame, font=self.font)
        self.inspection_entry.pack(fill=tk.X, pady=5)
        tk.Button(frame, text="✓", command=self.save_inspection, bg="#007bff", fg="white", font=self.font, relief="flat").pack(pady=10)
        tk.Button(frame, text="Back", command=self.show_inspection_menu, bg="#007bff", fg="white", font=self.font, relief="flat").pack(pady=5)

    def save_inspection(self):
        """Save inspection expiration date."""
        self.vehicle.Inspection = self.inspection_entry.get()
        self.vehicle.save_to_file()
        messagebox.showinfo("Info", "Inspection date saved successfully!")
        self.show_inspection_menu()

    def check_inspection(self):
        """Check inspection expiration date."""
        if self.vehicle.Inspection:
            inspection_date = datetime.strptime(self.vehicle.Inspection, "%d-%m-%Y").date()
            today = date.today()
            if inspection_date < today:
                messagebox.showwarning("Warning", "Inspection Expired!")
            else:
                messagebox.showinfo("Info", f"Inspection will expire on {self.vehicle.Inspection}")
        else:
            messagebox.showwarning("Warning", "No inspection data available.")
    def popup_inspection(self):
        if self.vehicle.Inspection:
            inspection_date = datetime.strptime(self.vehicle.Inspection, "%d-%m-%Y").date()
            today = date.today()
            if inspection_date < today:
                messagebox.showwarning("Warning", "Inspection Expired!")
    def save_and_exit(self):
        """Save data and exit the application."""
        self.vehicle.save_to_file()
        messagebox.showinfo("Info", "Car Management App - mihai288")
        self.root.quit()

    def clear_window(self):
        """Clear the window to make space for new widgets."""
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = VehicleApp(root)
    root.mainloop()
