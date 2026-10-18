import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime
from urllib.parse import quote
import threading
import time
import config  # Import the configuration file

# Names the OpenWeather query does not resolve when typed this way.
CITY_ALIASES = {
    "اللاذقية": "Latakia",
    "لاذقية": "Latakia",
    "latakia": "Latakia",
    "lattakia": "Latakia",
    "جبلة": "Jableh",
    "جبله": "Jableh",
    "jableh": "Jableh",
    "jabla": "Jableh",
    "jablah": "Jableh",
}


def normalize_city(city_name):
    cleaned = " ".join(str(city_name).strip().split())
    return CITY_ALIASES.get(cleaned, CITY_ALIASES.get(cleaned.casefold(), cleaned))


def describe_weather_code(code):
    descriptions = {
        0: "clear sky",
        1: "mainly clear",
        2: "partly cloudy",
        3: "overcast clouds",
        45: "fog",
        48: "fog",
        51: "drizzle",
        53: "drizzle",
        55: "drizzle",
        61: "rain",
        63: "rain",
        65: "rain",
        80: "rain showers",
        81: "rain showers",
        82: "rain showers",
        95: "thunderstorm",
    }
    return descriptions.get(int(code), "unknown")


def clock_from_value(value):
    text = str(value).split("T")[-1]
    if len(text) == 5:
        text += ":00"
    return text


def show_weather(city, country, temp, weather_desc, pressure, humidity, wind_speed, sunrise, sunset):
    city_entry.delete(0, tk.END)
    city_entry.insert(0, city)
    info_label.config(
        text=f"City: {city}, {country}\nTemperature: {temp}°C\n"
             f"Weather: {weather_desc.capitalize()}\n"
             f"Pressure: {pressure} hPa\nHumidity: {humidity}%\n"
             f"Wind Speed: {wind_speed} m/s\nSunrise: {sunrise}\nSunset: {sunset}",
        font=("Arial", 12), fg=config.INFO_TEXT_COLOR, bg="#FFFFFF"
    )
    info_label.lift()


def fetch_openweather(city_name):
    key = config.API_KEY
    if not key or key == "YOUR_OPENWEATHERMAP_API_KEY":
        return None
    complete_url = f"{config.BASE_URL}q={quote(city_name)}&appid={quote(key)}&units=metric"
    response = requests.get(complete_url, timeout=20)
    data = response.json()
    if str(data.get("cod")) != "200" or not data.get("weather") or not data.get("sys"):
        return None
    main = data.get("main", {})
    wind = data.get("wind", {})
    return {
        "city": data.get("name", city_name),
        "country": data["sys"].get("country", "N/A"),
        "temp": main.get("temp", "N/A"),
        "weather_desc": data["weather"][0].get("description", "N/A"),
        "pressure": main.get("pressure", "N/A"),
        "humidity": main.get("humidity", "N/A"),
        "wind_speed": wind.get("speed", "N/A"),
        "sunrise": datetime.fromtimestamp(data["sys"].get("sunrise", 0)).strftime("%H:%M:%S"),
        "sunset": datetime.fromtimestamp(data["sys"].get("sunset", 0)).strftime("%H:%M:%S"),
    }


def fetch_open_meteo(city_name):
    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city_name, "count": 1, "language": "en"},
        timeout=20,
    )
    results = geo.json().get("results") or []
    if not results:
        return None
    place = results[0]
    forecast = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": place["latitude"],
            "longitude": place["longitude"],
            "current": "temperature_2m,relative_humidity_2m,pressure_msl,wind_speed_10m,weather_code",
            "daily": "sunrise,sunset",
            "wind_speed_unit": "ms",
            "timezone": "auto",
            "forecast_days": 1,
        },
        timeout=20,
    )
    data = forecast.json()
    current = data.get("current") or {}
    daily = data.get("daily") or {}
    sunrises = daily.get("sunrise") or []
    sunsets = daily.get("sunset") or []
    if "temperature_2m" not in current or not sunrises or not sunsets:
        return None
    pressure = current.get("pressure_msl", "N/A")
    if isinstance(pressure, (int, float)):
        pressure = round(pressure)
    return {
        "city": place.get("name", city_name),
        "country": place.get("country_code", "N/A"),
        "temp": current.get("temperature_2m", "N/A"),
        "weather_desc": describe_weather_code(current.get("weather_code", -1)),
        "pressure": pressure,
        "humidity": current.get("relative_humidity_2m", "N/A"),
        "wind_speed": current.get("wind_speed_10m", "N/A"),
        "sunrise": clock_from_value(sunrises[0]),
        "sunset": clock_from_value(sunsets[0]),
    }


# Function to fetch and display weather information based on the city
def get_weather(city_name=config.DEFAULT_CITY):
    # Show a loading message while fetching data
    info_label.config(text="Loading", font=("Arial", 14, "bold"), fg="#000000")
    app.update()  # Refresh the window to show the "Loading" text

    time.sleep(3)  # Simulate a delay of 3 seconds to represent fetching data

    try:
        city_name = normalize_city(city_name)
        weather = fetch_openweather(city_name) or fetch_open_meteo(city_name)
        if weather:
            show_weather(
                weather["city"], weather["country"], weather["temp"], weather["weather_desc"],
                weather["pressure"], weather["humidity"], weather["wind_speed"],
                weather["sunrise"], weather["sunset"]
            )
        else:
            info_label.config(text="Not Found. Please provide a valid city name.", fg="#000000", font=("Arial", 12, "bold"))
    except Exception:
        info_label.config(text="Provide a valid city name to get info", fg="#000000", font=("Arial", 12, "bold"))
    search_button.config(state="normal", text="Search", image=search_icon, compound="left")

# Function to handle the search action when the user clicks the "Search" button
def search_city():
    city_name = city_entry.get()  # Get the city name entered by the user
    if city_name:
        search_button.config(state="disabled", text="Searching", image=None, fg="#FFFFFF")  # Disable button and show "Searching"
        threading.Thread(target=get_weather, args=(city_name,)).start()  # Start a new thread to fetch weather data
    else:
        # Show a message to prompt the user to enter a city name
        info_label.config(text="Enter city name to get weather info", fg="#000000", font=("Arial", 12, "bold"))

# Function to bind the Enter key to the search function
def on_enter_press(event):
    search_city()  # Call search_city function when Enter key is pressed

# Function to handle resizing of the background image when the window is resized
def resize_bg(event):
    new_bg = bg_image.resize((event.width, event.height), Image.LANCZOS)  # Resize the background image
    bg_photo = ImageTk.PhotoImage(new_bg)  # Convert the resized image into a format suitable for Tkinter
    bg_label.config(image=bg_photo)  # Update the background label with the new image
    bg_label.image = bg_photo  # Keep a reference to the image

# Function to set the background image (path is passed as argument)
def set_background(image_path):
    try:
        global bg_image  # Declare bg_image as global so it can be accessed in resize_bg
        bg_image = Image.open(image_path)  # Open the background image
        bg_photo = ImageTk.PhotoImage(bg_image.resize((500, 400), Image.LANCZOS))  # Resize it to fit the window
        bg_label.config(image=bg_photo)  # Set the background image in the label
        bg_label.image = bg_photo  # Store the reference to the background image
    except FileNotFoundError:
        messagebox.showerror("Error", "Background image not found!")  # Show an error message if the file is not found

# Function to show the default weather info for the default city
def show_default_info():
    get_weather(config.DEFAULT_CITY)  # Fetch and display weather info for the default city

# GUI setup
app = tk.Tk()  # Create the main window
app.title("Weather Info")  # Set the window title
app.geometry("500x400")  # Set the window size
app.iconbitmap("assets/weather.ico") # Set the window icon

# Set up the background label (initialize it here)
bg_label = tk.Label(app)
bg_label.place(relwidth=1, relheight=1)  # Fill the entire window with background image

# Set a customizable background image (default to background.png)
set_background(config.DEFAULT_BACKGROUND_IMAGE)

# Heading label with drop shadow (No background)
title_label = tk.Label(app, text="☂ Weather Info ☂", font=("Arial", config.HEADER_TOP_TEXT_SIZE, "bold"),
                       fg=config.HEADER_TOP_TEXT_COLOR, relief="solid", bd=config.HEADER_TEXT_TOP_BORDER_THICKNESS, padx=10, pady=5)
title_label.place(relx=0.5, rely=0.06, anchor="n")  # Centered at the top of the window

# City input field with custom border color
city_entry = tk.Entry(app, font=("Arial", 14), width=30, bd=2, relief="solid", 
                      highlightbackground=config.SEARCH_BAR_BORDER_COLOR,
                      highlightcolor=config.SEARCH_BAR_BORDER_COLOR,
                      justify="center")  # Center align the text in the search box
city_entry.place(relx=0.5, rely=0.2, anchor="n")  # Centered below the title label
city_entry.insert(0, "Enter city name here")  # Set the placeholder text
city_entry.bind("<Return>", on_enter_press)  # Bind Enter key to the search function

# Search button with a custom icon
search_icon = ImageTk.PhotoImage(Image.open(config.SEARCH_ICON_IMAGE).resize((20, 20)))  # Load the search icon
search_button = tk.Button(app, text="Search", command=search_city, font=("Arial", 12, "bold"), image=search_icon,
                          compound="left", bg=config.SEARCH_BUTTON_COLOR, fg=config.SEARCH_BUTTON_TEXT_COLOR, padx=10)
search_button.place(relx=0.5, rely=0.3, anchor="n")  # Centered below the city entry box

# Info box for displaying weather details with black text and border
info_label = tk.Label(app, text="Weather info will appear here", font=("Arial", 12), fg=config.INFO_TEXT_COLOR, bg="#FFFFFF", relief="solid", bd=config.INFO_BORDER_THICKNESS)
info_label.place(relx=0.5, rely=0.43, anchor="n", width=370)  # Centered below the search button

# Show default info when the app starts
show_default_info()  # Display weather info for the default city when the app loads

app.mainloop()  # Run the main event loop to keep the window open
