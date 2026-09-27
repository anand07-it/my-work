# Advanced Weather App 🌤️

A real-time weather web app built with Python, Streamlit, and OpenWeather.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Cloud

1. Upload `app.py` and `requirements.txt` to your GitHub repository.
2. Deploy the repository on Streamlit Community Cloud.
3. In the app settings, add this secret:

```toml
OPENWEATHER_API_KEY = "YOUR_NEW_API_KEY"
```

Do not upload your API key directly into Python code or GitHub.
