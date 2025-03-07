import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import font
from PIL import Image, ImageTk

# Create the root window
root = tk.Tk()
root.title("Employment Salary Sorter")
root.geometry("600x650")
root.configure(bg="#f5f6fa")  # Light gray background for content

# Salary data list to store employee details
employees = []

# Professional color scheme
primary_color = "#2C3E50"  # Dark blue
secondary_color = "#3498db"  # Light blue
highlight_color = "#1abc9c"  # Teal for highlights

# Font style (modern)
header_font = font.Font(family="Helvetica", size=24, weight="bold")
button_font = font.Font(family="Helvetica", size=14)

# Function to display the employee list
def display_employees():
    for widget in employee_frame.winfo_children():
        widget.destroy()  # Clear the existing list before displaying updated one
    
    for employee in employees:
        employee_label = tk.Label(employee_frame, text=f"{employee['name']} - ${employee['salary']} - {employee['days_worked']} days",
                                  font=("Helvetica", 12), bg=secondary_color, fg="white", anchor="w", padx=10, pady=5)
        employee_label.pack(fill="x", pady=3)

# Function to add a new employee
def add_employee():
    name = simpledialog.askstring("Name", "Enter the employee's name:")
    if not name:
        return
    salary = simpledialog.askfloat("Salary", "Enter the employee's salary:")
    if salary is None:
        return
    days_worked = simpledialog.askinteger("Days Worked", "Enter the number of days worked:")
    if days_worked is None:
        return
    
    employees.append({"name": name, "salary": salary, "days_worked": days_worked})
    display_employees()

# Function to sort employees by salary
def sort_by_salary():
    if not employees:
        messagebox.showwarning("No Data", "No employee data available to sort.")
        return

    employees.sort(key=lambda x: x['salary'], reverse=True)
    display_employees()

# Function to sort employees by name
def sort_by_name():
    if not employees:
        messagebox.showwarning("No Data", "No employee data available to sort.")
        return

    employees.sort(key=lambda x: x['name'])
    display_employees()

# Function to load icons with error handling
def load_icon(icon_path):
    try:
        icon = Image.open(icon_path).resize((30, 30))  # Resize for better visibility
        return ImageTk.PhotoImage(icon)
    except FileNotFoundError:
        print(f"Icon file {icon_path} not found!")
        return None

# Frame to hold the employee list
employee_frame = tk.Frame(root, bg="#f5f6fa", padx=20, pady=20)
employee_frame.pack(pady=30, fill="both", expand=True)

# Create a frame for the header with the title
header_frame = tk.Frame(root, bg=primary_color, height=80)
header_frame.pack(fill="x", side="top")

logo_label = tk.Label(header_frame, text="Employment Salary Sorter", font=header_font, fg="white", bg=primary_color)
logo_label.pack(pady=20)

# Load the icons (Make sure to use the correct path to your image files)
salary_icon = load_icon("icons/salary_icon.png")  # Path to the salary sorting icon
name_icon = load_icon("icons/name_icon.png")  # Path to the name sorting icon
add_icon = load_icon("icons/add_icon.png")  # Path to the add icon

# Add buttons for different actions with enhanced styling
button_style = {"font": button_font, "bg": secondary_color, "fg": "white", "relief": "raised", "bd": 2, "activebackground": highlight_color}

# Add Employee Button
add_button = tk.Button(root, text="Add Employee", command=add_employee, image=add_icon, compound="left", **button_style)
add_button.pack(pady=10, fill="x")

# Sort by Salary Button with Icon
salary_button = tk.Button(root, text="Sort by Salary", command=sort_by_salary, image=salary_icon, compound="left", **button_style)
salary_button.pack(pady=10, fill="x")

# Sort by Name Button with Icon
name_button = tk.Button(root, text="Sort by Name", command=sort_by_name, image=name_icon, compound="left", **button_style)
name_button.pack(pady=10, fill="x")

# Display the employee list initially
display_employees()

root.mainloop()
