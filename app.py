import streamlit as st
import requests
from datetime import datetime, timezone, timedelta

st.set_page_config(
    page_title="Advanced Weather App",
    page_icon="🌤️",
    layout="centered"
)

BG_COLOR = "#010612"
CARD_COLOR = "#1CEB15"
PRIMARY_COLOR = "#E82B2B"
SECONDARY_COLOR = "#1384B9"
TEXT_COLOR = "#F8FAFC"
MUTED_COLOR = "#CBD5E1"

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

st.markdown(f"""
<style>
.stApp {{
    background: {BG_COLOR};
    color: {TEXT_COLOR};
}}
.main-title {{
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    margin-top: 10px;
}}
.subtitle {{
    text-align: center;
    color: {MUTED_COLOR};
    margin-bottom: 25px;
}}
.weather-card {{
    background: {CARD_COLOR};
    border-radius: 18px;
    padding: 25px;
    color: {TEXT_COLOR};
    text-align: center;
}}
.temp {{
    font-size: 64px;
    font-weight: 800;
    color: {PRIMARY_COLOR};
}}
.condition {{
    font-size: 22px;
    margin-bottom: 18px;
}}
.detail {{
    background: #334155;
    border-radius: 10px;
    padding: 14px 8px;
    min-height: 70px;
    margin-bottom: 10px;
}}
.detail-title {{
    font-weight: 700;
}}
.small {{
    color: {MUTED_COLOR};
    font-size: 14px;
}}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🌤 WEATHER</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Real-time weather information</div>', unsafe_allow_html=True)

city = st.text_input("City", value="Mumbai", placeholder="Enter city name")

def format_time(timestamp, timezone_offset):
    try:
        city_timezone = timezone(timedelta(seconds=timezone_offset))
        return datetime.fromtimestamp(
            timestamp, tz=city_timezone
        ).strftime("%I:%M %p")
    except Exception:
        return "--"

def get_weather_icon(condition):
    condition = condition.lower()
    for key, icon in WEATHER_ICONS.items():
        if key in condition:
            return icon
    return "🌤️"

try:
    API_KEY = st.secrets["OPENWEATHER_API_KEY"]
except Exception:
    API_KEY = ""

if st.button("SEARCH 🔍", type="primary", use_container_width=True):
    city = city.strip()

    if not city:
        st.warning("Please enter a city name.")
    elif not API_KEY:
        st.error("API key is not configured. Add OPENWEATHER_API_KEY in Streamlit Secrets.")
    else:
        with st.spinner("Fetching weather data..."):
            try:
                response = requests.get(
                    "https://api.openweathermap.org/data/2.5/weather",
                    params={
                        "q": city,
                        "appid": API_KEY,
                        "units": "metric"
                    },
                    timeout=10
                )

                try:
                    data = response.json()
                except ValueError:
                    st.error("The weather server returned invalid data.")
                    st.stop()

                if response.status_code == 401:
                    st.error("Invalid API key. Check your OpenWeather API key.")
                    st.stop()

                if response.status_code == 404:
                    st.error(f"Could not find weather for: {city}")
                    st.stop()

                if response.status_code == 429:
                    st.error("You have reached the OpenWeather API request limit.")
                    st.stop()

                if response.status_code != 200:
                    st.error(data.get("message", "Unknown API error.").capitalize())
                    st.stop()

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
                sunrise = format_time(data["sys"]["sunrise"], timezone_offset)
                sunset = format_time(data["sys"]["sunset"], timezone_offset)
                icon = get_weather_icon(main_condition)

                st.markdown(
                    f'<div class="weather-card">'
                    f'<h2>📍 {city_name}, {country}</h2>'
                    f'<div style="font-size:70px;">{icon}</div>'
                    f'<div class="temp">{temperature:.1f}°C</div>'
                    f'<div class="condition">{condition.title()}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

                st.write("")
                cols = st.columns(3)

                details = [
                    ("🌡️", "Feels Like", f"{feels_like:.1f}°C"),
                    ("💧", "Humidity", f"{humidity}%"),
                    ("💨", "Wind", f"{wind_speed:.1f} m/s"),
                    ("🔵", "Pressure", f"{pressure} hPa"),
                    ("👁️", "Visibility", f"{visibility:.1f} km"),
                    ("🌅", "Sunrise", sunrise),
                    ("🌇", "Sunset", sunset),
                ]

                for i, (emoji, title, value) in enumerate(details):
                    with cols[i % 3]:
                        st.markdown(
                            f'<div class="detail">'
                            f'<div class="detail-title">{emoji} {title}</div>'
                            f'<div>{value}</div>'
                            f'</div>',
                            unsafe_allow_html=True
                        )

                st.caption(
                    "Last updated: "
                    + datetime.now().strftime("%d %b %Y, %I:%M:%S %p")
                )

            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the weather server. Check your internet connection.")
            except requests.exceptions.Timeout:
                st.error("The weather server took too long to respond.")
            except requests.exceptions.RequestException as e:
                st.error(f"Network error: {e}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")
