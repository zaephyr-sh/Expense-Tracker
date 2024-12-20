import os
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import matplotlib.pyplot as plt
import csv


# Function to add an expense
def add_expense():
    date = date_entry.get()
    category = category_entry.get()
    amount = amount_entry.get()

    # Validate date format
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        status_label.config(text="Invalid date format! Use YYYY-MM-DD.", fg="red")
        return

    # Validate amount
    try:
        amount = float(amount)
    except ValueError:
        status_label.config(text="Amount must be a number!", fg="red")
        return

    if date and category and amount:
        with open("expenses.txt", "a") as file:
            file.write(f"{date},{category},{amount}\n")
        status_label.config(text="Expense added successfully!", fg="green")
        date_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        view_expenses()
    else:
        status_label.config(text="Please fill all the fields!", fg="red")


# Function to delete an expense
def delete_expense():
    selected_item = expenses_tree.selection()
    if selected_item:
        item_text = expenses_tree.item(selected_item, "values")
        date, category, amount = item_text
        try:
            with open("expenses.txt", "r") as file:
                lines = file.readlines()
            with open("expenses.txt", "w") as file:
                for line in lines:
                    if line.strip() != f"{date},{category},{amount}":
                        file.write(line)
            status_label.config(text="Expense deleted successfully!", fg="green")
            view_expenses()
        except IOError:
            status_label.config(text="Error deleting the expense!", fg="red")
    else:
        status_label.config(text="Please select an expense to delete!", fg="red")


# Function to view expenses
def view_expenses():
    if os.path.exists("expenses.txt"):
        total_expense = 0
        expenses_tree.delete(*expenses_tree.get_children())
        try:
            with open("expenses.txt", "r") as file:
                for line in file:
                    date, category, amount = line.strip().split(",")
                    expenses_tree.insert("", tk.END, values=(date, category, amount))
                    total_expense += float(amount)
            total_label.config(text=f"Total Expense: {total_expense:.2f}")
        except IOError:
            status_label.config(text="Error reading the expenses file!", fg="red")
    else:
        total_label.config(text="No expenses recorded.")
        expenses_tree.delete(*expenses_tree.get_children())


# Function to plot expenses by category
def plot_expenses():
    categories = {}
    try:
        with open("expenses.txt", "r") as file:
            for line in file:
                _, category, amount = line.strip().split(",")
                categories[category] = categories.get(category, 0) + float(amount)

        plt.bar(categories.keys(), categories.values())
        plt.title("Expenses by Category")
        plt.xlabel("Category")
        plt.ylabel("Amount")
        plt.show()
    except IOError:
        status_label.config(text="Error plotting expenses!", fg="red")


# Function to export expenses to a CSV file
def export_to_csv():
    try:
        with open("expenses.txt", "r") as infile, open("expenses.csv", "w", newline="") as outfile:
            writer = csv.writer(outfile)
            writer.writerow(["Date", "Category", "Amount"])
            for line in infile:
                writer.writerow(line.strip().split(","))
        status_label.config(text="Expenses exported to expenses.csv!", fg="green")
    except IOError:
        status_label.config(text="Error exporting to CSV!", fg="red")


# Function to sort expenses
def sort_expenses(column):
    expenses = [(expenses_tree.set(k, column), k) for k in expenses_tree.get_children("")]
    expenses.sort(reverse=False)  # Change to True for descending order

    for index, (val, k) in enumerate(expenses):
        expenses_tree.move(k, "", index)


# Create the main application window
root = tk.Tk()
root.title("Expense Tracker")

# Create labels and entries for adding expenses
date_label = tk.Label(root, text="Date (YYYY-MM-DD):")
date_label.grid(row=0, column=0, padx=5, pady=5)
date_entry = tk.Entry(root)
date_entry.grid(row=0, column=1, padx=5, pady=5)

category_label = tk.Label(root, text="Category:")
category_label.grid(row=1, column=0, padx=5, pady=5)
category_entry = tk.Entry(root)
category_entry.grid(row=1, column=1, padx=5, pady=5)

amount_label = tk.Label(root, text="Amount:")
amount_label.grid(row=2, column=0, padx=5, pady=5)
amount_entry = tk.Entry(root)
amount_entry.grid(row=2, column=1, padx=5, pady=5)

add_button = tk.Button(root, text="Add Expense", command=add_expense)
add_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

# Create a treeview to display expenses
columns = ("Date", "Category", "Amount")
expenses_tree = ttk.Treeview(root, columns=columns, show="headings")
expenses_tree.heading("Date", text="Date", command=lambda: sort_expenses("Date"))
expenses_tree.heading("Category", text="Category", command=lambda: sort_expenses("Category"))
expenses_tree.heading("Amount", text="Amount", command=lambda: sort_expenses("Amount"))
expenses_tree.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

# Add a scrollbar for the Treeview
scrollbar = ttk.Scrollbar(root, orient="vertical", command=expenses_tree.yview)
expenses_tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=4, column=3, sticky="ns")

# Create a label to display the total expense
total_label = tk.Label(root, text="")
total_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

# Create a label to show the status of expense addition and deletion
status_label = tk.Label(root, text="", fg="green")
status_label.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

# Create buttons to view, delete, plot, and export expenses
view_button = tk.Button(root, text="View Expenses", command=view_expenses)
view_button.grid(row=7, column=0, padx=5, pady=10)

delete_button = tk.Button(root, text="Delete Expense", command=delete_expense)
delete_button.grid(row=7, column=1, padx=5, pady=10)

plot_button = tk.Button(root, text="Plot Expenses", command=plot_expenses)
plot_button.grid(row=7, column=2, padx=5, pady=10)

export_button = tk.Button(root, text="Export to CSV", command=export_to_csv)
export_button.grid(row=8, column=0, columnspan=3, padx=5, pady=10)

# Check if the 'expenses.txt' file exists; create it if it doesn't
if not os.path.exists("expenses.txt"):
    with open("expenses.txt", "w"):
        pass

# Display existing expenses on application start
view_expenses()

# Run the main application loop
root.mainloop()
