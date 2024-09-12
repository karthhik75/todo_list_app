import tkinter as tk
from tkinter import messagebox
import sqlite3

# Create database connection and table
def create_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY, task TEXT)''')
    conn.commit()
    conn.close()

# Add a task to the database
def add_task():
    task = entry_task.get()
    if task:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
        conn.commit()
        conn.close()
        entry_task.delete(0, tk.END)
        display_tasks()
    else:
        messagebox.showwarning("Warning", "You must enter a task.")

# Delete a task from the database
def delete_task():
    selected_task = listbox_tasks.get(tk.ACTIVE)
    if selected_task:
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute("DELETE FROM tasks WHERE task=?", (selected_task,))
        conn.commit()
        conn.close()
        display_tasks()
    else:
        messagebox.showwarning("Warning", "You must select a task.")

# Display all tasks
def display_tasks():
    listbox_tasks.delete(0, tk.END)
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute("SELECT task FROM tasks")
    tasks = c.fetchall()
    for task in tasks:
        listbox_tasks.insert(tk.END, task[0])
    conn.close()

# Initialize GUI
root = tk.Tk()
root.title("To-Do List App")

frame_tasks = tk.Frame(root)
frame_tasks.pack(pady=10)

entry_task = tk.Entry(frame_tasks, width=50)
entry_task.pack(side=tk.LEFT, padx=10)

button_add = tk.Button(frame_tasks, text="Add Task", command=add_task)
button_add.pack(side=tk.LEFT)

button_delete = tk.Button(frame_tasks, text="Delete Task", command=delete_task)
button_delete.pack(side=tk.LEFT)

listbox_tasks = tk.Listbox(root, width=60, height=15)
listbox_tasks.pack(pady=20)

# Initialize database and display tasks
create_db()
display_tasks()

root.mainloop()
