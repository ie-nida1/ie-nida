import requests
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import io

class CountryInfoGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Country Information")
        self.master.geometry("400x400")

        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self.master, text="Enter Country Code:")
        self.label.pack(pady=10)

        self.entry = ttk.Entry(self.master)
        self.entry.pack(pady=10)

        self.button = ttk.Button(self.master, text="Get Country Info", command=self.get_country_info)
        self.button.pack(pady=10)

        self.result_text = tk.Text(self.master, wrap=tk.WORD, height=10, width=40)
        self.result_text.pack(pady=10)

        self.flag_label = ttk.Label(self.master)
        self.flag_label.pack(pady=10)

    def get_country_info(self):
        country_code = self.entry.get().upper()
        country_info = self.fetch_country_info(country_code)

        if country_info:
            result_text = f"Country: {country_info['name']['common']}\n"
            result_text += f"Capital: {country_info['capital'][0]}\n"
            result_text += f"Population: {country_info['population']}\n"
            result_text += f"Area: {country_info['area']} square kilometers\n"
            result_text += f"Region: {country_info['region'][0]}\n"
            result_text += f"Subregion: {country_info['subregion'][0]}\n"

            if 'flags' in country_info:
                flags = country_info['flags']
                result_text += "Flags:\n"
                for flag_type, flag_url in flags.items():
                    result_text += f"  {flag_type}: {flag_url}\n"

                    # Display the flag image
                    flag_image = self.load_flag_image(flag_url)
                    if flag_image:
                        self.flag_label.config(image=flag_image)
                        self.flag_label.image = flag_image  # Keep a reference to avoid garbage collection

        else:
            result_text = f"Country with code '{country_code}' not found."

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, result_text)

    def fetch_country_info(self, country_code):
        api_url = "https://restcountries.com/v3.1/all"

        try:
            response = requests.get(api_url)
            response.raise_for_status()
            countries_data = response.json()

            for country_data in countries_data:
                if country_code in country_data['cca2'] or country_code in country_data['cca3']:
                    return country_data

        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            print(f"Request Error: {err}")

        return None

    def load_flag_image(self, flag_url):
        try:
            response = requests.get(flag_url)
            response.raise_for_status()
            flag_image = Image.open(io.BytesIO(response.content))
            flag_image = flag_image.resize((100, 60), Image.ANTIALIAS)
            flag_image = ImageTk.PhotoImage(flag_image)
            return flag_image
        except Exception as e:
            print(f"Error loading flag image: {e}")
            return None


if __name__ == "__main__":
    root = tk.Tk()
    app = CountryInfoGUI(root)
    root.mainloop()
