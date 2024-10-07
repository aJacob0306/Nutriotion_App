import tkinter as tk
from tkinter import messagebox
import requests
import sqlite3

# Function to set up the SQLite database and create the table
def setup_database():
    conn = sqlite3.connect('nutrition_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS nutrition (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_name TEXT,
            calories REAL,
            protein REAL  
        )
    ''')
    conn.commit()
    conn.close()


# Function to save nutritional data into the database
def save_nutrition_data(food_name, calories, protein):
    conn = sqlite3.connect('nutrition_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO nutrition (food_name, calories, protein) VALUES (?, ?, ?)",
              (food_name, calories, protein))
    conn.commit()
    conn.close()


# Function to get nutrition data from an API
def get_nutrition_from_api(food_item):
    url = f"https://api.edamam.com/api/food-database/v2/parser?ingr={food_item}&app_id=YOUR_APP_ID&app_key=YOUR_APP_KEY"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()


        calories = data['hints'][0]['food']['nutrients'].get('ENERC_KCAL', 0)
        protein = data['hints'][0]['food']['nutrients'].get('PROCNT', 0)

        return calories, protein
    else:
        return None, None


# Function to handle the submission from the GUI
def on_submit():
    food_item = entry_food.get()

    if not food_item:
        messagebox.showwarning("Input Error", "Please enter a food item.")
        return

    # Get nutritional data from the API
    calories, protein = get_nutrition_from_api(food_item)

    if calories is None and protein is None:
        messagebox.showerror("Error", "Could not retrieve nutritional information.")
    else:
        # Save data to the database
        save_nutrition_data(food_item, calories, protein)
        messagebox.showinfo("Success", f"Saved: {food_item} | Calories: {calories}, Protein: {protein}g")


# Function to retrieve data from the database and display it in the GUI
def show_saved_data():
    conn = sqlite3.connect('nutrition_data.db')
    c = conn.cursor()
    c.execute("SELECT food_name, calories, protein FROM nutrition")
    rows = c.fetchall()
    conn.close()

    # Display data in a simple list format
    data_window = tk.Toplevel()
    data_window.title("Stored Nutrition Data")

    text_box = tk.Text(data_window, width=40, height=10)
    text_box.pack(padx=10, pady=10)

    for row in rows:
        text_box.insert(tk.END, f"Food: {row[0]}, Calories: {row[1]}, Protein: {row[2]}g\n")



root = tk.Tk()
root.title("Nutrition Facts App")
label_food = tk.Label(root, text="Enter Food Item:")
label_food.pack(padx=10, pady=5)

entry_food = tk.Entry(root, width=30)
entry_food.pack(padx=10, pady=5)

# Submit button
submit_button = tk.Button(root, text="Get Nutrition", command=on_submit)
submit_button.pack(padx=10, pady=5)


show_button = tk.Button(root, text="Show Saved Data", command=show_saved_data)
show_button.pack(padx=10, pady=5)


setup_database()


root.mainloop()


def setup_database():
    conn = sqlite3.connect('nutrition_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS nutrition (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            food_name TEXT,
            calories REAL,
            protein REAL  
        )
    ''')
    conn.commit()
    conn.close()



def save_nutrition_data(food_name, calories, protein):
    conn = sqlite3.connect('nutrition_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO nutrition (food_name, calories, protein) VALUES (?, ?, ?)",
              (food_name, calories, protein))
    conn.commit()
    conn.close()



def get_nutrition_from_api(food_item):
    api_key = "cJutW20jlk79MifUMgXGO4Uiu77uxAPxT9TBUSXB"
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?api_key={cJutW20jlk79MifUMgXGO4Uiu77uxAPxT9TBUSXB}&query={food_item}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data['foods']:

            food = data['foods'][0]
            calories = next((item['value'] for item in food['foodNutrients'] if item['nutrientName'] == 'Energy'), 0)
            protein = next((item['value'] for item in food['foodNutrients'] if item['nutrientName'] == 'Protein'), 0)

            return calories, protein
        else:
            return None, None
    else:
        return None, None


# Function for sumitting the GUI
def on_submit():
    food_item = entry_food.get()

    if not food_item:
        messagebox.showwarning("Input Error", "Please enter a food item.")
        return

    # Get nutritional data from the API
    calories, protein = get_nutrition_from_api(food_item)

    if calories is None and protein is None:
        messagebox.showerror("Error", "Could not retrieve nutritional information.")
    else:
        # Save data to the database
        save_nutrition_data(food_item, calories, protein)
        messagebox.showinfo("Success", f"Saved: {food_item} | Calories: {calories}, Protein: {protein}g")


# Function to retrieve data from the database and display it in the GUI
def show_saved_data():
    conn = sqlite3.connect('nutrition_data.db')
    c = conn.cursor()
    c.execute("SELECT food_name, calories, protein FROM nutrition")
    rows = c.fetchall()
    conn.close()

    # Display data in a simple list format
    data_window = tk.Toplevel()
    data_window.title("Stored Nutrition Data")

    text_box = tk.Text(data_window, width=40, height=10)
    text_box.pack(padx=10, pady=10)

    for row in rows:
        text_box.insert(tk.END, f"Food: {row[0]}, Calories: {row[1]}, Protein: {row[2]}g\n")


# GUI Setup with Tkinter
root = tk.Tk()
root.title("Nutrition Facts App")

# Input
label_food = tk.Label(root, text="Enter Food Item:")
label_food.pack(padx=10, pady=5)

entry_food = tk.Entry(root, width=30)
entry_food.pack(padx=10, pady=5)

# Submit button
submit_button = tk.Button(root, text="Get Nutrition", command=on_submit)
submit_button.pack(padx=10, pady=5)

#  saved data button
show_button = tk.Button(root, text="Show Saved Data", command=show_saved_data)
show_button.pack(padx=10, pady=5)


setup_database()

# Run the Tkinter event loop
root.mainloop()
