import requests
import json
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO
from datetime import datetime

# === Weather Fetching ===
def get_weather_data(city_name):
    api_key = "fc27212dd5eadaf13d9b6f2ca842de17"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def display_weather_info(city_name):
    weather_data = get_weather_data(city_name)
    if weather_data:
        print(f"\nWeather in {weather_data['name']}:\n" + "-" * 30)
        print(f"Description: {weather_data['weather'][0]['description'].capitalize()}")
        print(f"Temperature: {weather_data['main']['temp']}°C")
        print(f"Humidity: {weather_data['main']['humidity']}%")
        print(f"Pressure: {weather_data['main']['pressure']} hPa")
        print(f"Wind Speed: {weather_data['wind']['speed']} m/s\n")
    else:
        print("Failed to retrieve weather information.")

# === Job Fetching ===
def get_vacancies(keyword, area_id):
    url = f"https://api.hh.ru/vacancies?text={keyword}&area={area_id}&currency_code=RUR&per_page=10&page=0"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        vacancies = []

        for item in data.get("items", []):
            salary_info = item.get('salary', {})
            salary_from = salary_info.get('from', 'N/A')
            salary_to = salary_info.get('to', 'N/A')
            salary_currency = salary_info.get('currency', '')
            salary_str = f"{salary_from} - {salary_to} {salary_currency}" if salary_currency else "Salary not specified"
            
            vacancies.append({
                "Title": item["name"],
                "Company": item["employer"]["name"],
                "Salary": salary_str,
                "Location": item["area"]["name"],
                "Published Date": datetime.fromisoformat(item["published_at"]).strftime('%d-%m-%Y')
            })
        
        return vacancies
    except requests.exceptions.RequestException as e:
        print(f"Error fetching job vacancies: {e}")
        return []

def display_vacancies(keyword, area_id):
    vacancies = get_vacancies(keyword, area_id)
    if vacancies:
        print("\nTop Job Vacancies:\n" + "-" * 40)
        for vac in vacancies:
            print(f"Title: {vac['Title']}")
            print(f"Company: {vac['Company']}")
            print(f"Salary: {vac['Salary']}")
            print(f"Location: {vac['Location']}")
            print(f"Published Date: {vac['Published Date']}\n")
    else:
        print("No job vacancies found.")

# === Fox Image Generator ===
class FoxImageGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Fox Image Generator")
        
        self.image_label = tk.Label(root)
        self.image_label.pack()

        self.next_button = tk.Button(root, text="Next Fox Image 🦊", command=self.load_new_image, bg="orange", fg="white", font=("Verdana", 14, "bold"))
        self.next_button.pack(pady=10)
        
        self.load_new_image()

    def load_new_image(self):
        try:
            response = requests.get("https://randomfox.ca/floof/")
            response.raise_for_status()
            image_url = response.json().get('image', '')
            
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            image_data = Image.open(BytesIO(image_response.content))
            image_data = image_data.resize((400, 400), Image.Resampling.LANCZOS)  # Resize image
            
            self.photo = ImageTk.PhotoImage(image_data)
            self.image_label.config(image=self.photo)
            self.image_label.image = self.photo
        except requests.exceptions.RequestException as e:
            print(f"Error loading fox image: {e}")

# === Run Scripts ===
if __name__ == "__main__":
    display_weather_info("Saint Petersburg")
    display_vacancies("python", 2)  # Moscow region (area_id=2)
    
    root = tk.Tk()
    app = FoxImageGenerator(root)
    root.mainloop()
