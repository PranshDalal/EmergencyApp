import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import json
import requests
from datetime import datetime
from time import strftime

with open("password.json", "r") as f:
    password = json.loads(f.read())["password"]

URL = "https://cs-api.pltw.org/EmergencyPal"


class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.title("Emergency Application")
        self.geometry(f"{400}x{400}")

        self.user_select_frame = ctk.CTkFrame(self)
        self.user_select_frame.pack(pady=50)
        self.user_type_label = ctk.CTkLabel(self.user_select_frame, text="Select User Type", font=ctk.CTkFont(size=25, weight="bold"))
        self.user_type_label.grid(row=0, column=0, columnspan=2)
        self.admin_button = ctk.CTkButton(self.user_select_frame, text="Admin", command=self.sign_in_as_admin)
        self.admin_button.grid(row=1, column=0, padx=10, pady=50)
        self.user_button = ctk.CTkButton(self.user_select_frame, text="User", command=self.show_latest_emergency)
        self.user_button.grid(row=1, column=1, padx=10, pady=50)

        self.clock_label = ctk.CTkLabel(self.user_select_frame, font=('calibri', 20, 'bold'))
        self.clock_label.grid(row=2, column=0, columnspan=2, pady=10)

        self.update_clock()
        self.after(1000, self.update_clock)

        self.admin_frame = ctk.CTkFrame(self)
        self.tabview = ctk.CTkTabview(self.admin_frame)
        self.tabview.pack()
        self.tabview.add("Create Report")
        self.tabview.add("See Previous Reports")

        self.report_radio_var = tk.IntVar()
        self.fire_var = tk.BooleanVar()
        self.shooter_var = tk.BooleanVar()
        self.earthquake_var = tk.BooleanVar()

        self.report_radiobuton_fire = ctk.CTkRadioButton(self.tabview.tab("Create Report"), variable=self.report_radio_var, text="Fire", value=0, command=lambda: self.check_checkbox_state(self.report_radiobuton_fire))
        self.report_radiobuton_fire.pack(pady=10)
        self.report_radiobuton_intruder = ctk.CTkRadioButton(self.tabview.tab("Create Report"), variable=self.report_radio_var, text="Intruder",value=1, command=lambda: self.check_checkbox_state(self.report_radiobuton_intruder))
        self.report_radiobuton_intruder.pack(pady=10)
        self.report_radiobuton_earthquake = ctk.CTkRadioButton(self.tabview.tab("Create Report"), variable=self.report_radio_var, text="Earthquake", value=2, command=lambda: self.check_checkbox_state(self.report_radiobuton_earthquake))
        self.report_radiobuton_earthquake.pack(pady=10)
        self.report_button = ctk.CTkButton(self.tabview.tab("Create Report"), text="Submit Report", command=self.send_emergency_alert)
        self.report_button.pack(pady=10)

        self.back_button_create_report = ctk.CTkButton(self.tabview.tab("Create Report"), text="Back", command=self.show_home_screen)
        self.back_button_create_report.pack(pady=10)
        self.previous_reports_text = ctk.CTkTextbox(self.tabview.tab("See Previous Reports"), height=150, width=500)
        self.previous_reports_text.pack(pady=10)
        self.show_previous_reports_button = ctk.CTkButton(self.tabview.tab("See Previous Reports"), text="Show Previous Reports", command=self.show_previous_reports)
        self.show_previous_reports_button.pack()
        self.delete_reports_button = ctk.CTkButton(self.tabview.tab("See Previous Reports"), text="Delete Reports", command=self.delete_reports)
        self.delete_reports_button.pack(pady=10)

        self.back_button_previous_reports = ctk.CTkButton(self.tabview.tab("See Previous Reports"), text="Back", command=self.show_home_screen)
        self.back_button_previous_reports.pack()

    def delete_reports(self):
        pass

    def sign_in_as_admin(self):
        password_input = ctk.CTkInputDialog(
            text="Enter admin password", title="Admin password").get_input()

        if password_input == password:
            self.user_select_frame.pack_forget()
            self.admin_frame.pack(pady=(50, 0))

        else:
            messagebox.showerror("Admin", "Incorrect password. Please try again")

    def send_emergency_alert(self):
        selected_emergencies = []
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if self.fire_var.get():
            selected_emergencies.append((
                "Fire", 
                "Evacuate the building immediately."))
            response = requests.post(
                URL + "?text=" +
                f"Fire, Evacuate the building immediately and go to Brighton Parking Lot, Date: {current_date}"
            )
        if self.shooter_var.get():
            selected_emergencies.append((
                "School Shooter",
                "Take shelter and stay in a safe location."))
            response = requests.post(
                URL + "?text=" +
                f"School Shooter, Take shelter and stay in a safe location.  Avoid Deny Defend, Date: {current_date}"
            )
        if self.earthquake_var.get():
            selected_emergencies.append((
                "Earthquake",
                "Drop, Cover, and Hold On. Stay indoors until shaking stops."))
            response = requests.post(
                URL + "?text=" +
                f"Earthquake, Drop, Cover, and Hold On. Stay indoors until shaking stops and then evacuate to Brighton Parking Lot, Date: {current_date}"
            )
        if not selected_emergencies:
            messagebox.showwarning(
                "No Emergency Selected",
                "Please select at least one emergency type.")
        else:
            for emergency_type, date in selected_emergencies:
                self.display_emergency_info(emergency_type, date)

    def check_checkbox_state(self, checkbox):
        checkbox_var = None
        if checkbox == self.report_radiobuton_fire:
            checkbox_var = self.fire_var
        elif checkbox == self.report_radiobuton_intruder:
            checkbox_var = self.shooter_var
        elif checkbox == self.report_radiobuton_earthquake:
            checkbox_var = self.earthquake_var

        if checkbox_var is not None:
            checkbox_var.set(not checkbox_var.get())

    def display_emergency_info(self, emergency_type=None, instructions=None):
        if emergency_type and instructions:
            message = f"Emergency Alert - {emergency_type}\n\nInstructions:\n{instructions}"
            messagebox.showinfo("Emergency Alert", message)

    def update_clock(self):
        current_time = strftime('%H:%M:%S %p')
        self.clock_label.configure(text=current_time)
        self.after(1000, self.update_clock)

    def show_home_screen(self):
        self.admin_frame.pack_forget()
        self.user_select_frame.pack(pady=50)

    def show_latest_emergency(self):
        latest_emergency = self.get_latest_emergency()
        if latest_emergency:
            emergency_type, date, instructions = latest_emergency
            message = f"Latest Emergency Alert - {emergency_type}\n\nInstructions: {instructions}\nDate: {date}"

            messagebox.showinfo("Latest Emergency Alert", message)
        else:
            messagebox.showinfo("No Emergency Alert", "No recent emergency alerts.")

    def show_previous_reports(self):
        previous_reports = self.get_previous_reports()
        if previous_reports:
            report_text = "\n\n".join(previous_reports)
            self.previous_reports_text.insert(tk.END, report_text)

        else:
            self.previous_reports_text.insert(tk.END, "No previous reports.")

    def get_latest_emergency(self):
        try:
            response = requests.get(URL)
            response_data = response.json()
            strings = response_data.get("strings", [])

            if strings:
                latest_emergency = strings[-1].split(', Date: ')
                if len(latest_emergency) == 2:
                    emergency_type, instructions = latest_emergency[0].rsplit(', ', 1)
                    date_str = latest_emergency[1].strip()
                    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                    return emergency_type, date, instructions
                else:
                    return "No Emergency", "No Instructions", None

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to fetch emergency information: {e}")

        return "No Emergency", "No Instructions", None
    
    def delete_reports(self):
        response = requests.post(URL + "/reset?password=58")
        self.previous_reports_text.delete("1.0", tk.END)
        messagebox.showinfo("Reports Deleted", "Previous reports have been deleted.")

    def get_previous_reports(self):
        try:
            response = requests.get(URL)
            response_data = response.json()
            strings = response_data.get("strings", [])

            previous_reports = []
            for emergency in strings:
                emergency_parts = emergency.split(', Date: ')
                emergency_type = emergency_parts[0].strip()

                if len(emergency_parts) == 2:
                    date, instructions = emergency_parts[1].strip(), "No Instructions"
                elif len(emergency_parts) == 1:
                    date, instructions = "No Date", "No Instructions"
                else:
                    date, instructions = emergency_parts[2].strip(), emergency_parts[1].strip()

                report_entry = (
                    f"Emergency: {emergency_type}\nDate: {date}"
                )
                previous_reports.append(report_entry)

            return previous_reports

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to fetch previous reports: {e}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
