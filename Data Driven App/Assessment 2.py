import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
import io
from urllib.parse import urlparse
import tkinter.messagebox

# Function to display frames
def switch_to_frame(frame):
    frame.tkraise()

# Function to display the page2 
def page2():
    switch_to_frame(frame2) 
    
# Function to display the page3
def page3():
    switch_to_frame(frame3)  

def page4():
    switch_to_frame(frame4)
    
def page5():
    switch_to_frame(frame5)

# Function to get information on countries
def app_country_info():
    country_code = country.get().upper()
    country_info = api_country_info(country_code)

    comic_sans_font = ("Comic Sans MS", 10, 'bold')  # Comic sans font

    # All the countries info (country name, capital, population, area, region, and subregion)
    if country_info:
        result_content = f"Country: {country_info['name']['common']}\n"
        result_content += f"Capital: {country_info['capital'][0]}\n"
        result_content += f"Population: {country_info['population']}\n"
        result_content += f"Area: {country_info['area']} square kilometers\n"
        result_content += f"Region: {country_info['region'][0]}\n"
        result_content += f"Subregion: {country_info['subregion'][0]}\n"

        if 'currencies' in country_info:  # All countries currencies displayed
            currencies = country_info['currencies']
            result_content += "Currencies:\n"
            for currency_code, currency_info in currencies.items():
                result_content += f"  {currency_code}: {currency_info['name']} ({currency_info['symbol']})\n"  # The display of currency symbol for each country

        if 'flags' in country_info:  # The flag images provided for each country
            flags = country_info['flags']
            result_content += "Flags:\n"
            for flag_type, flag_value in flags.items():
                result_content += f"  {flag_type}: {flag_value}\n"

                if image_url(flag_value):  # The flag image URL from the API link
                    flag_image = load_flag_image(flag_value)
                    if flag_image:
                        flag.config(image=flag_image)
                        flag.image = flag_image
                        flag.place(x=110, y=40)  # The placement of the flag image

                        # Check if frame5 is currently displayed
                        if frame5.winfo_ismapped():
                            tkinter.messagebox.showinfo("Flag Information", "Flag is displayed in the Show Flag area.\nGo back to see it.")
    else:
        result_content = f"Country with code '{country_code}' not found."

    result_content_text.delete(1.0, tk.END)
    result_content_text.insert(tk.END, result_content)

    result_content_text.tag_configure("comic_sans", font=comic_sans_font)  # The result of the comic sans font style
    result_content_text.tag_add("comic_sans", 1.0, "end")

# The function to display the code and data in entry field according to the name of the country
def api_country_info(country_code):
    api_link = "https://restcountries.com/v3.1/all"

    try:
        response = requests.get(api_link)
        response.raise_for_status()
        countries_data = response.json()

        for country_data in countries_data:
            if country_code in country_data['cca2'] or country_code in country_data['cca3']:
                return country_data

    except requests.exceptions.HTTPError as errh: # The errors if the country or the code or the link is not valid
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")

    return None

# The use of "from urllib.parse import urlparse" for the flag images to display in any format
def image_url(url):
    parsed_url = urlparse(url)
    return parsed_url.scheme in ('http', 'https') and any(parsed_url.path.lower().endswith(ext) for ext in ('.png', '.jpg', '.jpeg', '.gif'))

#The function to load a flag image depending on which ever country is selected
def load_flag_image(flag_url):
    try:
        response = requests.get(flag_url)
        response.raise_for_status()
        flag_pictures = Image.open(io.BytesIO(response.content))
        flag_pictures = flag_pictures.resize((300, 200), resample=Image.LANCZOS) # The resizing of the pictures
        flag_pictures = ImageTk.PhotoImage(flag_pictures)
        return flag_pictures
    except Exception as e:
        print(f"Error loading flag image: {e}")
    return None

def select(event):
    select_country = country.get()
   
    for data in countries_data:
        if select_country == data['name']['common']:
            country.set(data['cca2'])   

# Main root tkinter window 
root = tk.Tk()
root.title("Global Cultures Unveiled")
root.geometry("530x300")

# Frame 1
frame1 = tk.Frame(root)

img = ImageTk.PhotoImage(Image.open("vintage.jpg")) # Image of the frame1 background
imgLabel = tk.Label(frame1, image=img)
imgLabel.place(x=0, y=0, width=530, height=300)

# Frame 1 button
B1 = tk.Button(frame1, text="START", font=('Comic Sans MS', 12, "bold italic"), bg='#e5cc9e', fg='white', command=page2)
B1.place(x=25, y=254, width=150)

# End of frame1
frame1.place(x=0 , y=0, width=530, height=300)

# Frame 2
frame2 = tk.Frame(root)

img_map = ImageTk.PhotoImage(Image.open("map.jpg"))# Image for frame 2 background
imgLabel_map = tk.Label(frame2, image=img_map)
imgLabel_map.place(x=0, y=0, width=530, height=300)

# Sidebar frame
sidebar_frame = tk.Frame(frame2, width=150, bg='#cc947a')
sidebar_frame.place(x=0, y=0, width=200, height=450)

# Sidebar buttons
main_button = tk.Button(sidebar_frame, text="Main", command=lambda: switch_to_frame(frame1), bg='#eadcca', fg='#b48e54', padx=29, pady=5)
about_button = tk.Button(sidebar_frame, text="About", command=lambda: switch_to_frame(frame3), bg='#eadcca', fg='#b48e54', padx=27, pady=5)
info_button = tk.Button(sidebar_frame, text="Country Info", command=lambda: switch_to_frame(frame4), bg='#eadcca', fg='#b48e54', padx=10, pady=5)
flag_button = tk.Button(sidebar_frame, text="Show Flag", command=lambda:switch_to_frame(frame5), bg='#eadcca', fg='#b48e54', padx=17, pady=5)

# Place sidebar buttons
main_button.pack(pady=10)
about_button.pack(pady=10)
info_button.pack(pady=10)
flag_button.pack(pady=10)

# The end of frame 2
frame2.place(x=0 , y=0, width=530, height=300)

# Frame 3
frame3 = tk.Frame(root)

img_bg = ImageTk.PhotoImage(Image.open("bg.png"))# Image for frame 2 background
imgLabel_bg = tk.Label(frame3, image=img_bg)
imgLabel_bg.place(x=0, y=0, width=530, height=300)

# The buttons that have the ability to switch to frame 1 and 2 
B2 = tk.Button(frame3, text="🢦",font=('Arial',25),fg="white", bg="#d7b180", command=lambda: switch_to_frame(frame2)) 
B3 = tk.Button(frame3, text="➪", font=('Arial',19),fg="white", bg="#d7b180", command=page3)   

B2.place(x=0, y=0, width=30, height=30)
B3.place(x=370, y=420, width=30, height=30)

style = ttk.Style() # The container_frame2 background style 
style.configure("color.TFrame", background="#cc947a")

# A container frame for frame 2
container_frame2 = ttk.Frame(frame3, style="color.TFrame", padding=(20, 20, 20, 20))
container_frame2.place(x=50, y=100, width=300, height=300)

# Label and the font
L1 = tk.Label(frame3, text="API Information", font=("Comic Sans MS", 11, "bold italic"),fg='#a06418')
L1.place(x=200, y=20)

# Paragraph for the information about the api
paragraph = (
    "The API link applied is 'https://restcountries.com/v3.1/all', and it sends data in JSON format. "
    "The application addresses a request to the API, operates the response, and withdraw the information "
    "such as the country's common name, capital, population, area, region, subregion, currencies, "
    "and flags. Users can input a country code, click the 'Country Info' button, and receive real-time "
    "information about the selected country, enhancing their knowledge of global cultures."
)

# Text for the cotainer_frame2
Text = ttk.Label(container_frame2, text=paragraph, font=("Comic Sans MS", 9, "bold"),foreground="#af8756", wraplength=260, justify=tk.LEFT)
Text.pack(side="left", fill="both", expand=True)

# The end of frame 3
frame3.place(x=0 , y=0, width=530, height=300)

# Frame 4
frame4 = tk.Frame(root)

img_bckg = ImageTk.PhotoImage(Image.open("bg.png"))  # The background image for frame 4
imgLabel_bckg = tk.Label(frame4, image=img_bckg)
imgLabel_bckg.place(x=0, y=0, width=530, height=300)

B4 = tk.Button(frame4, text="🢦", font=('Comic Sans MS', 25), fg="white", bg="#d7b180", command=lambda: switch_to_frame(frame2))
B4.place(x=0, y=0, width=30, height=30)

L2 = ttk.Label(frame4, text="Input Country Code:", font=("Comic Sans MS", 14, 'bold'), background="#e5d3ac", foreground="#a06418")
L2.pack(pady=10)

# API LINK
api_link = "https://restcountries.com/v3.1/all"
response = requests.get(api_link)
response.raise_for_status()
countries_data = response.json()
country_names = [country_data['name']['common'] for country_data in countries_data]

# Sort the country names alphabetically
country_names.sort()

# Combobox for country selection
country = ttk.Combobox(frame4, values=country_names)
country.place(x=190, y=50)  # Adjusted the position
country.bind("<<ComboboxSelected>>", select)

B5 = tk.Button(frame4, text="Country Info", font=('Comic Sans MS', 10, 'bold italic'), fg="white", bg="#d7b180", command=app_country_info)
B5.place(x=215, y=80)  # Adjusted the position

# Container_frame4
container_frame4 = ttk.Frame(frame4)
container_frame4.place(x=120, y=130, width=300, height=150)  # Adjusted the width and height

# Scrollbar 
scrollbar = ttk.Scrollbar(container_frame4)
scrollbar.pack(side="right", fill="y")

# Result content text box
result_content_text = tk.Text(container_frame4, wrap=tk.WORD, height=10, width=40, yscrollcommand=scrollbar.set)
result_content_text.pack(side="left", fill="both", expand=True)
scrollbar.config(command=result_content_text.yview)

# The end of frame 4
frame4.place(x=0, y=0, width=530, height=300)

# Frame 5
frame5 = tk.Frame(root)

L3 = ttk.Label(frame5, text="Flags", font=("Comic Sans MS", 14, 'bold'), background="#e5d3ac", foreground="#a06418")
L3.pack(pady=10)


img_bck = ImageTk.PhotoImage(Image.open("bg.png"))  # The background image for frame 4
imgLabel_bck = tk.Label(frame5, image=img_bck)
imgLabel_bck.place(x=0, y=0, width=530, height=300)

B5 = tk.Button(frame5, text="🢦",font=('Arial',25),fg="white", bg="#d7b180", command=lambda: switch_to_frame(frame2)) 
B5.place(x=0, y=0, width=30, height=30)
flag = ttk.Label(frame5)

# The end of frame 5
frame5.place(x=0 , y=0, width=530, height=300)

switch_to_frame(frame1)

root.mainloop()


