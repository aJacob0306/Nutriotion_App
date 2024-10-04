import tkinter as tk
from tkinter import messagebox
import requests



def fetch_nutrition_data(food_item):
    api_key = ""
    url = f"https://api.nal.usda.gov/fdc/v1/foods/search?query={food_item}&api_key={api_key}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data and "foods" in data and len(data["foods"]) > 0:

                food = data["foods"][0]
                food_name = food["description"]
                calories = food["foodNutrients"][3]["value"]
                protein = food["foodNutrients"][0]["value"]

                return food_name, calories, protein
            else:
                return None
        else:
            return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None



def save_nutrition_data(food_name, calories, protein):
    conn = sqlite3.connect('nutrition_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO nutrition (food_name, calories, protein) VALUES (?, ?, ?)",
              (food_name, calories, protein))
    conn.commit()
    conn.close()

def get_nutrition_data():
    food_item = entry.get()
    if not food_item:
        messagebox.showwarning("Input error", "Please enter a food item.")
    else:
        result = fetch_nutrition_data(food_item)
        if result:
            food_name, calories, protein = result
            messagebox.showinfo("Nutrition Facts", f"Food: {food_name}\nCalories: {calories} kcal\nProtein: {protein} g")
            # Save the data to the database
            save_nutrition_data(food_name, calories, protein)
        else:
            messagebox.showerror("Error", "Search for something else.")



root = tk.Tk()
root.title("Nutrition Facts App")

entry_label = tk.Label(root, text="Enter Food Item:")
entry_label.pack(pady=5)
entry = tk.Entry(root, width=40)
entry.pack(pady=5)

search_button = tk.Button(root, text="Search", command=get_nutrition_data)
search_button.pack(pady=10)

root.mainloop()