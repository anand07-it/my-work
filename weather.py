import tkinter as tk
from tkinter import messagebox
import requests
from datetime import datetime, timezone, timedelta
import threading

API_KEY = "ceb4c502181682b2ca5102f95fb66fa0"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

BG_COLOR = "#010612"
CARD_COLOR = "#1CEB15"
PRIMARY_COLOR = "#E82B2B"
SECONDARY_COLOR = "#1384B9"
TEXT_COLOR = "#F8FAFC"
MUTED_COLOR = "#CBD5E1"
ERROR_COLOR = "#F51919"




WEATHER_ICONS = {
    "clear": "☀️",
    "clouds": "☁️",
    "rain": "🌧️",
    "drizzle": "🌦️",
    "thunderstorm": "⛈️",
    "snow": "❄️",
    "mist": "🌫️",
    "fog": "🌫️",
    "haze": "🌫️",
    "smoke": "🌫️",
    "dust": "🌫️",
    "sand": "🌫️",
    "ash": "🌋",
    "squall": "💨",
    "tornado": "🌪️",
}




def format_time(timestamp, timezone_offset):
    """
    Convert Unix timestamp to the city's local time.

    OpenWeather's timezone value is the offset from UTC in seconds.
    """
    try:
        city_timezone = timezone(timedelta(seconds=timezone_offset))

        return datetime.fromtimestamp(
            timestamp,
            tz=city_timezone
        ).strftime("%I:%M %p")

    except Exception:
        return "--"


def get_weather_icon(condition):
    """Return an emoji based on weather condition."""

    condition = condition.lower()

    for key, icon in WEATHER_ICONS.items():
        if key in condition:
            return icon

    return "🌤️"



def update_weather(data):

    try:
        city_name = data["name"]
        country = data["sys"]["country"]

        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]

        wind_speed = data["wind"]["speed"]

        visibility = data.get("visibility", 0) / 1000

        condition = data["weather"][0]["description"]
        main_condition = data["weather"][0]["main"]

        timezone_offset = data.get("timezone", 0)

        sunrise = format_time(
            data["sys"]["sunrise"],
            timezone_offset
        )

        sunset = format_time(
            data["sys"]["sunset"],
            timezone_offset
        )

        icon = get_weather_icon(main_condition)


        

        city_result.config(
            text=f"📍 {city_name}, {country}"
        )


       
        weather_icon.config(
            text=icon
        )


        
        temp_label.config(
            text=f"{temperature:.1f}°C"
        )


        
        condition_label.config(
            text=condition.title()
        )


        
        feels_label.config(
            text=f"🌡 Feels Like\n{feels_like:.1f}°C"
        )

        humidity_label.config(
            text=f"💧 Humidity\n{humidity}%"
        )

        wind_label.config(
            text=f"💨 Wind\n{wind_speed:.1f} m/s"
        )

        pressure_label.config(
            text=f"🔵 Pressure\n{pressure} hPa"
        )

        visibility_label.config(
            text=f"👁 Visibility\n{visibility:.1f} km"
        )

        sunrise_label.config(
            text=f"🌅 Sunrise\n{sunrise}"
        )

        sunset_label.config(
            text=f"🌇 Sunset\n{sunset}"
        )


       
        status_label.config(
            text=(
                f"Last updated: "
                f"{datetime.now().strftime('%d %b %Y, %I:%M:%S %p')}"
            ),
            fg=MUTED_COLOR
        )

    except KeyError as e:

        messagebox.showerror(
            "Data Error",
            f"Weather data is incomplete.\nMissing: {e}"
        )

    except Exception as e:

        messagebox.showerror(
            "Display Error",
            f"Could not display weather data.\n\n{e}"
        )




def request_weather(city):

    try:

        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }

        response = requests.get(
            BASE_URL,
            params=params,
            timeout=10
        )


        
        try:
            data = response.json()

        except ValueError:

            root.after(
                0,
                lambda: messagebox.showerror(
                    "Server Error",
                    "The weather server returned invalid data."
                )
            )

            return


        
        if response.status_code == 401:

            root.after(
                0,
                lambda: messagebox.showerror(
                    "Invalid API Key",
                    "Your OpenWeather API key is invalid.\n\n"
                    "Check that you copied the API key correctly."
                )
            )

            return

        if response.status_code == 404:

            root.after(
                0,
                lambda: messagebox.showerror(
                    "City Not Found",
                    f"Could not find weather for:\n{city}"
                )
            )

            return

        if response.status_code == 429:

            root.after(
                0,
                lambda: messagebox.showerror(
                    "API Limit",
                    "You have reached the OpenWeather API request limit."
                )
            )

            return

        if response.status_code != 200:

            error_message = data.get(
                "message",
                "Unknown API error."
            )

            root.after(
                0,
                lambda msg=error_message: messagebox.showerror(
                    "Weather Error",
                    msg.capitalize()
                )
            )

            return

        # ----------------------------------------------------
        # UPDATE GUI ON MAIN THREAD
        # ----------------------------------------------------

        root.after(
            0,
            lambda weather_data=data: update_weather(weather_data)
        )

    except requests.exceptions.ConnectionError:

        root.after(
            0,
            lambda: messagebox.showerror(
                "Connection Error",
                "Could not connect to the weather server.\n\n"
                "Please check your internet connection."
            )
        )

    except requests.exceptions.Timeout:

        root.after(
            0,
            lambda: messagebox.showerror(
                "Timeout",
                "The weather server took too long to respond."
            )
        )

    except requests.exceptions.RequestException as e:

        root.after(
            0,
            lambda error=e: messagebox.showerror(
                "Network Error",
                str(error)
            )
        )

    except Exception as e:

        root.after(
            0,
            lambda error=e: messagebox.showerror(
                "Unexpected Error",
                str(error)
            )
        )

    finally:

        root.after(
            0,
            lambda: set_loading(False)
        )

def get_weather(event=None):

    city = city_entry.get().strip()

    if not city:

        messagebox.showwarning(
            "Missing City",
            "Please enter a city name."
        )

        return

    if API_KEY == "YOUR_API_KEY_HERE" or not API_KEY:

        messagebox.showerror(
            "API Key Missing",
            "Please add your OpenWeather API key to API_KEY."
        )

        return

    set_loading(True)

    thread = threading.Thread(
        target=request_weather,
        args=(city,),
        daemon=True
    )

    thread.start()




def set_loading(loading):

    if loading:

        search_button.config(
            state="disabled",
            text="LOADING..."
        )

        status_label.config(
            text="Fetching weather data...",
            fg=PRIMARY_COLOR
        )

    else:

        search_button.config(
            state="normal",
            text="SEARCH 🔍"
        )




def clear_search():

    city_entry.delete(0, tk.END)
    city_entry.focus()

    city_result.config(
        text="📍 Search for a city"
    )

    weather_icon.config(
        text="🌤️"
    )

    temp_label.config(
        text="--°C"
    )

    condition_label.config(
        text="Weather Condition"
    )

    feels_label.config(
        text="🌡 Feels Like\n--"
    )

    humidity_label.config(
        text="💧 Humidity\n--"
    )

    wind_label.config(
        text="💨 Wind\n--"
    )

    pressure_label.config(
        text="🔵 Pressure\n--"
    )

    visibility_label.config(
        text="👁 Visibility\n--"
    )

    sunrise_label.config(
        text="🌅 Sunrise\n--"
    )

    sunset_label.config(
        text="🌇 Sunset\n--"
    )

    status_label.config(
        text="Ready",
        fg=MUTED_COLOR
    )



root = tk.Tk()

root.title("Advanced Weather App")
root.geometry("500x760")
root.resizable(False, False)
root.configure(bg=BG_COLOR)



title = tk.Label(
    root,
    text="🌤 WEATHER",
    font=("Arial", 30, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)

title.pack(pady=(25, 5))


subtitle = tk.Label(
    root,
    text="Real-time weather information",
    font=("Arial", 11),
    bg=BG_COLOR,
    fg=MUTED_COLOR
)

subtitle.pack(pady=(0, 20))





search_frame = tk.Frame(
    root,
    bg=CARD_COLOR,
    padx=12,
    pady=12
)

search_frame.pack(
    padx=25,
    fill="x"
)


city_entry = tk.Entry(
    search_frame,
    font=("Arial", 15),
    bg="#334155",
    fg=TEXT_COLOR,
    insertbackground=TEXT_COLOR,
    relief="flat",
    width=23,
    justify="center"
)

city_entry.grid(
    row=0,
    column=0,
    padx=(0, 10),
    ipady=8
)

city_entry.insert(
    0,
    "Mumbai"
)


search_button = tk.Button(
    search_frame,
    text="SEARCH 🔍",
    font=("Arial", 10, "bold"),
    bg=PRIMARY_COLOR,
    fg="#0F172A",
    activebackground=SECONDARY_COLOR,
    relief="flat",
    cursor="hand2",
    command=get_weather
)

search_button.grid(
    row=0,
    column=1,
    ipadx=8,
    ipady=7
)


clear_button = tk.Button(
    root,
    text="Clear",
    font=("Arial", 9),
    bg=BG_COLOR,
    fg=MUTED_COLOR,
    activebackground=BG_COLOR,
    activeforeground=TEXT_COLOR,
    relief="flat",
    cursor="hand2",
    command=clear_search
)

clear_button.pack(
    pady=5
)
weather_card = tk.Frame(
    root,
    bg=CARD_COLOR,
    padx=20,
    pady=15
)

weather_card.pack(
    padx=25,
    pady=10,
    fill="x"
)
city_result = tk.Label(
    weather_card,
    text="📍 Mumbai",
    font=("Arial", 19, "bold"),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
)

city_result.pack(
    pady=(0, 5)
)
weather_icon = tk.Label(
    weather_card,
    text="🌤️",
    font=("Segoe UI Emoji", 50),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
)

weather_icon.pack()
temp_label = tk.Label(
    weather_card,
    text="--°C",
    font=("Arial", 48, "bold"),
    bg=CARD_COLOR,
    fg=PRIMARY_COLOR
)

temp_label.pack()

condition_label = tk.Label(
    weather_card,
    text="Weather Condition",
    font=("Arial", 16),
    bg=CARD_COLOR,
    fg=TEXT_COLOR
)

condition_label.pack(
    pady=(0, 10)
)
details_frame = tk.Frame(
    weather_card,
    bg=CARD_COLOR
)

details_frame.pack(
    fill="x",
    pady=5
)
def create_detail_label(parent, text, row, column):

    label = tk.Label(
        parent,
        text=text,
        font=("Arial", 10, "bold"),
        bg="#334155",
        fg=TEXT_COLOR,
        width=14,
        height=3,
        relief="flat"
    )

    label.grid(
        row=row,
        column=column,
        padx=4,
        pady=4
    )

    return label


feels_label = create_detail_label(
    details_frame,
    "🌡 Feels Like\n--",
    0,
    0
)

humidity_label = create_detail_label(
    details_frame,
    "💧 Humidity\n--",
    0,
    1
)

wind_label = create_detail_label(
    details_frame,
    "💨 Wind\n--",
    0,
    2
)

pressure_label = create_detail_label(
    details_frame,
    "🔵 Pressure\n--",
    1,
    0
)

visibility_label = create_detail_label(
    details_frame,
    "👁 Visibility\n--",
    1,
    1
)

sunrise_label = create_detail_label(
    details_frame,
    "🌅 Sunrise\n--",
    1,
    2
)

sunset_label = create_detail_label(
    details_frame,
    "🌇 Sunset\n--",
    2,
    1
)
status_label = tk.Label(
    root,
    text="Ready",
    font=("Arial", 9),
    bg=BG_COLOR,
    fg=MUTED_COLOR
)

status_label.pack(
    pady=8
)
root.bind(
    "<Return>",
    get_weather
)
city_entry.focus()
root.mainloop()