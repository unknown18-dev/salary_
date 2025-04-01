import datetime
import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog

def get_employees_next_weekday(weekday: int, start_date: datetime.date):
    days_ahead = weekday - start_date.weekday()
    if days_ahead < 0:
        days_ahead += 7
    return start_date + datetime.timedelta(days=days_ahead)

def calculate_monthly_salary(employee, month_year):
    start_date = datetime.date(month_year[0], month_year[1], 1)
    end_date = datetime.date(month_year[0], month_year[1] + 1, 1) - datetime.timedelta(days=1)
    
    total_payments = 0
    payment_dates = []
    
    for weekday in employee["payment_days"]:
        current_date = start_date
        while current_date <= end_date:
            next_payment_date = get_employees_next_weekday(weekday, current_date)
            if next_payment_date > end_date:
                break
            total_payments += 1
            payment_dates.append(next_payment_date)
            current_date = next_payment_date + datetime.timedelta(days=7)
    
    total_salary = total_payments * employee['salary']
    return total_salary, total_payments, payment_dates

def edit_employee():
    global employees
    name = simpledialog.askstring("Edit Employee", "Enter Employee Name:")
    for employee in employees:
        if employee["name"].upper() == name.upper():
            new_salary = simpledialog.askinteger("Edit Salary", f"Enter new salary for {name}:")
            if new_salary:
                employee["salary"] = new_salary
                messagebox.showinfo("Success", f"Updated {name}'s salary to R{new_salary}")
            return
    messagebox.showerror("Error", "Employee not found!")

def add_employee():
    global employees
    name = simpledialog.askstring("New Employee", "Enter Employee Name:")
    salary = simpledialog.askinteger("New Employee", "Enter Salary:")
    payment_days = simpledialog.askstring("New Employee", "Enter Payment Days (comma-separated, 0=Monday ... 6=Sunday):")
    
    if name and salary and payment_days:
        try:
            payment_days = list(map(int, payment_days.split(",")))
            employees.append({"name": name, "salary": salary, "payment_date": "", "payment_days": payment_days})
            messagebox.showinfo("Success", f"Added new employee: {name} with salary R{salary}")
        except ValueError:
            messagebox.showerror("Error", "Invalid payment days format! Use numbers 0-6 separated by commas.")

def display_salaries():
    month_input = entry_month.get()
    try:
        month_year = datetime.datetime.strptime(month_input, "%b-%y").date()
        month_year_tuple = (month_year.year, month_year.month)
    except ValueError:
        messagebox.showerror("Error", "Invalid Date Format! Use MMM-YY (e.g., Mar-25)")
        return
    
    report_text.delete(1.0, tk.END)
    report_text.insert(tk.END, f"=== Salary Report for {month_input} ===\n\n")
    
    for employee in employees:
        total_salary, total_payments, payment_dates = calculate_monthly_salary(employee, month_year_tuple)
        payment_dates.sort()
        formatted_dates = "\n  - " + "\n  - ".join([date.strftime('%A, %d %B %Y') for date in payment_dates])
        
        report_text.insert(tk.END, f"{employee['name']}\n")
        report_text.insert(tk.END, f"  Total Salary: R{total_salary:.2f}\n")
        report_text.insert(tk.END, f"  Number of Payments: {total_payments}\n")
        report_text.insert(tk.END, f"  Payment Dates:{formatted_dates}\n\n")

employees = [
    {"name": "PAT", "salary": 350, "payment_date": "2025-03-31", "payment_days": [0, 5]},
    {"name": "POL", "salary": 350, "payment_date": "2025-03-31", "payment_days": [5]},
    {"name": "WB", "salary": 350, "payment_date": "2025-03-31", "payment_days": [4]},
    {"name": "MAJ", "salary": 300, "payment_date": "2025-03-31", "payment_days": [2]},
    {"name": "NEW", "salary": 350, "payment_date": "2025-03-31", "payment_days": [0, 2, 4]},
    {"name": "GR", "salary": 300, "payment_date": "2025-02-28", "payment_days": [0, 1, 2, 3, 4]},
]

# UI Setup
root = tk.Tk()
root.title("BetterSalary - Salary Sorter")
root.geometry("600x500")
root.configure(bg="#f4f4f4")

title_label = tk.Label(root, text="BetterSalary V1.0", font=("Arial", 16, "bold"), bg="#f4f4f4")
title_label.pack(pady=10)

entry_label = tk.Label(root, text="Enter Month (MMM-YY):", font=("Arial", 12), bg="#f4f4f4")
entry_label.pack()

entry_month = tk.Entry(root, font=("Arial", 12))
entry_month.pack(pady=5)

process_button = tk.Button(root, text="Generate Report", font=("Arial", 12), bg="#007BFF", fg="white", command=display_salaries)
process_button.pack(pady=10)

edit_button = tk.Button(root, text="Edit Employee", font=("Arial", 12), bg="#28A745", fg="white", command=edit_employee)
edit_button.pack(pady=5)

add_button = tk.Button(root, text="Add Employee", font=("Arial", 12), bg="#17A2B8", fg="white", command=add_employee)
add_button.pack(pady=5)

report_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 10), height=15, width=70)
report_text.pack(pady=10)

root.mainloop()
