import tkinter as tk
from tkinter import messagebox
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# CSV File Setup
CSV_FILE = "expenses.csv"
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Type", "Category", "Amount"])

# Function to add expense
def add_expense():
    date = date_entry.get()
    type_ = type_var.get()
    category = category_entry.get()
    amount = amount_entry.get()
    
    if not date or not category or not amount:
        messagebox.showerror("Error", "Please fill all fields")
        return
    
    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Invalid amount")
        return
    
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, type_, category, amount])
    
    messagebox.showinfo("Success", "Expense added successfully!")
    update_summary()
    date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

# Function to update summary
def update_summary():
    df = pd.read_csv(CSV_FILE)
    total_credit = df[df['Type'] == 'Credit']['Amount'].sum()
    total_debit = df[df['Type'] == 'Debit']['Amount'].sum()
    summary_label.config(text=f"Total Credit: ₹{total_credit:.2f}  |  Total Debit: ₹{total_debit:.2f}")

# Function to show graph
def show_graph():
    df = pd.read_csv(CSV_FILE)
    credit = df[df['Type'] == 'Credit']['Amount'].sum()
    debit = df[df['Type'] == 'Debit']['Amount'].sum()
    labels = ['Credit', 'Debit']
    values = [credit, debit]
    
    fig, ax = plt.subplots(2, 1, figsize=(6, 8))
    
    # Pie Chart
    ax[0].pie(values, labels=labels, autopct='%1.1f%%', colors=['green', 'red'])
    ax[0].set_title("Credit vs Debit")
    
    # Scatter Plot for Debit Transactions
    debit_data = df[df['Type'] == 'Debit']
    if not debit_data.empty:
        ax[1].scatter(debit_data['Date'], debit_data['Amount'], color='red', label='Debit')
        ax[1].set_title("Debit Transactions Over Time")
        ax[1].set_xlabel("Date")
        ax[1].set_ylabel("Amount")
        ax[1].legend()
        plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.show()

# Function to view CSV data
def view_csv():
    df = pd.read_csv(CSV_FILE)
    messagebox.showinfo("CSV Data", df.to_string(index=False))

# GUI Setup
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("400x400")

tk.Label(root, text="Date (YYYY-MM-DD):").pack()
date_entry = tk.Entry(root)
date_entry.pack()

type_var = tk.StringVar(value="Debit")

tk.Label(root, text="Category:").pack()
category_entry = tk.Entry(root)
category_entry.pack()

tk.Label(root, text="Amount:").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

tk.Label(root, text="Type:").pack()
tk.Radiobutton(root, text="Credit", variable=type_var, value="Credit").pack()
tk.Radiobutton(root, text="Debit", variable=type_var, value="Debit").pack()

tk.Button(root, text="Add Expense", command=add_expense).pack()
tk.Button(root, text="Show Graph", command=show_graph).pack()
tk.Button(root, text="View CSV", command=view_csv).pack()

summary_label = tk.Label(root, text="Total Credit: ₹0.00  |  Total Debit: ₹0.00")
summary_label.pack()

update_summary()
root.mainloop()
