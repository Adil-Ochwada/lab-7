import requests
import json
from datetime import datetime

# Задание 1: Получение данных о погоде

def get_weather_data(city_name):
    api_key = "fc27212dd5eadaf13d9b6f2ca842de17"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении данных о погоде: {e}")
        return None

def display_weather_info(weather_data):
    if weather_data:
        city_name = weather_data["name"]
        weather = weather_data["weather"][0]["description"]
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        pressure = weather_data["main"]["pressure"]
        wind_speed = weather_data["wind"]["speed"]

        print(f"Погода в городе {city_name}:")
        print(f"- Описание: {weather}")
        print(f"- Температура: {temperature}°C")
        print(f"- Влажность: {humidity}%")
        print(f"- Давление: {pressure} гПа")
        print(f"- Скорость ветра: {wind_speed} м/с")
    else:
        print("Не удалось получить информацию о погоде.")

def main():
    city_name = "Saint Petersburg"
    weather_data = get_weather_data(city_name)
    display_weather_info(weather_data)

if __name__ == "__main__":
    main()

print()

# Задание 2: Получение вакансий с hh.ru

def get_vacancies(keyword, area_id):
    url = f"https://api.hh.ru/vacancies?text={keyword}&area={area_id}&currency_code=RUR&per_page=20&page=0"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print("Ошибка при получении данных о вакансиях")
        return []

    data = response.json()
    
    vacancies = []
    for item in data["items"]:
        salary = item.get('salary')
        if salary:
            salary_from = salary.get('from')
            salary_to = salary.get('to')
            salary_currency = salary.get('currency')
            if salary_from and salary_to:
                salary_str = f"{salary_from} - {salary_to} {salary_currency}"
            elif salary_from:
                salary_str = f"{salary_from} {salary_currency}"
            elif salary_to:
                salary_str = f"{salary_to} {salary_currency}"
            else:
                salary_str = "Н/Д"
        else:
            salary_str = "Н/Д"

        published_at = datetime.fromisoformat(item["published_at"]).strftime('%m.%d.%Y')
        vacancy = {
            "Название": item["name"],
            "Работодатель": item["employer"]["name"],
            "Зарплата": salary_str,
            "Регион": item["area"]["name"],
            "Дата публикации": published_at
        }
        vacancies.append(vacancy)
    
    return vacancies

keyword = "python"
area_id = 2  # Санкт-Петербург

vacancies = get_vacancies(keyword, area_id)

for vacancy in vacancies:
    for key, value in vacancy.items():
        print(f"{key}: {value}")
    print()
