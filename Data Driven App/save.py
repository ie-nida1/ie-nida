import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests

def get_country_info():
    try:
        response = requests.get("https://restcountries.com/v3.1/all")
        response.raise_for_status()
        countries_data = response.json()

        # Display country information in a text widget
        result_text.delete(1.0, tk.END)
        for country_data in countries_data:
            common_name = country_data.get('name', {}).get('common', '')
            result_text.insert(tk.END, f"Country: {common_name}\n")

    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")

def show_flag_image():
    try:
        response = requests.get("https://restcountries.com/v3.1/all")
        response.raise_for_status()
        countries_data = response.json()

        # Display flag image of the first country in the text widget
        if countries_data:
            flag_url = countries_data[0].get('flags', {}).get('png', '')
            if flag_url:
                flag_image = load_flag_image(flag_url)
                flag_label.config(image=flag_image)
                flag_label.image = flag_image

    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")

def load_flag_image(flag_url):
    try:
        response = requests.get(flag_url)
        response.raise_for_status()
        flag_picture = Image.open(Image.io.BytesIO(response.content))
        flag_picture = flag_picture.resize((200, 120), resample=Image.LANCZOS)
        flag_picture = ImageTk.PhotoImage(flag_picture)
        return flag_picture
    except Exception as e:
        print(f"Error loading flag image: {e}")
        return None

def about_info():
    # Display information about the application in a message box
    about_message = (
        "Country Information Viewer\n\n"
        "This application retrieves information about countries from the REST Countries API.\n"
        "It allows users to view general country information, display flag images, and more.\n\n"
        "Version: 1.0"
    )
    messagebox.showinfo("About", about_message)

# Add this line before creating the root window
style = ttk.Style()
style.configure("TFrame", background='#d7b180')

# Create main window
root = tk.Tk()
root.title("Country Information Viewer")
root.geometry("600x400")

# Create a frame for the sidebar
sidebar_frame = tk.Frame(root, width=150, bg='#d7b180')
sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

# Create a frame for the main content
content_frame = ttk.Frame(root)
content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Sidebar buttons
about_button = tk.Button(sidebar_frame, text="About", command=about_info, bg='#a06418', fg='white', padx=10, pady=5)
info_button = tk.Button(sidebar_frame, text="Country Info", command=get_country_info, bg='#a06418', fg='white', padx=10, pady=5)
flag_button = tk.Button(sidebar_frame, text="Show Flag", command=show_flag_image, bg='#a06418', fg='white', padx=10, pady=5)


# Place sidebar buttons
about_button.pack(pady=10)
info_button.pack(pady=10)
flag_button.pack(pady=10)

# Create a text widget to display the country information
result_text = tk.Text(content_frame, wrap=tk.WORD, height=10, width=40)
result_text.pack(expand=True, fill=tk.BOTH, pady=10)

# Create a label to display the flag image
flag_label = ttk.Label(content_frame)
flag_label.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()









