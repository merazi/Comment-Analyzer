import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import mysql.connector
import os

def fetch_ids():
    # Fetch IDs from the database and populate the combobox
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Query to fetch IDs from another table
        cursor.execute("SELECT * FROM Temas")
        ids = cursor.fetchall()

        # Clear existing entries in the combobox
        id_combobox['values'] = [(id[0], id[1]) for id in ids]
        id_combobox.set('')  # Reset the combobox

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Can't connect to host")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def search_word():
    search_term = search_entry.get()
    selected_id = id_combobox.get()

    if not search_term:
        messagebox.showwarning("Warning", "Please enter a search term.")
        return

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Define the query with multiple conditions
        query = """
        SELECT * FROM Comentarios
        WHERE COMENTARIO LIKE %s AND ID_TEMAS = %s
        """
        cursor.execute(query, ('%' + search_term + '%', selected_id))

        # Fetch results 
        results = cursor.fetchall()
        results_text = len(results)
        results_area.delete('1.0', tk.END)
        results_area.insert(tk.END, results_text)

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Database connection details

password = input("Enter your password: ")
host = os.getenv("MYSQL_HOST_IP", "localhost")

db_config = {
    'user': 'grp1',
    'password': password,
    'host': host,
    'database': 'personas_cen'
}

# Create the main application window
#


root = tk.Tk()
root.title("Word Search in MariaDB")

# theme
theme_path = os.path.join(os.path.dirname(__file__), 'azure_theme', 'azure.tcl')
root.tk.call('source', theme_path)
root.tk.call('set_theme', 'dark')

# Create a label and entry for search term
search_label = tk.Label(root, text="Enter word to search:")
search_label.pack(pady=5)

search_entry = tk.Entry(root, width=50)
search_entry.pack(pady=5)

# Create a label and combobox for ID selection
id_label = tk.Label(root, text="Select ID:")
id_label.pack(pady=5)

id_combobox = ttk.Combobox(root, width=50)
id_combobox.pack(pady=5)

# Fetch IDs to populate the combobox
fetch_ids()

# Create a search button
search_button = tk.Button(root, text="Search", command=search_word)
search_button.pack(pady=10)

# Create a text area to display results
results_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=15)
results_area.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
