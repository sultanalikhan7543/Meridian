# Meridian — Streamlit Edition (Free, powered by Google Gemini)

This version runs entirely on Google Gemini's free API tier — no credit card,
no billing required. Perfect for personal use and demos.

## Files
```
meridian-streamlit/
├── app.py                  <- the whole app
├── requirements.txt        <- streamlit + google-genai
├── secrets.toml.example    <- template for your API key
└── .gitignore
```

## Get a free Gemini API key
1. Go to https://aistudio.google.com/app/apikey
2. Sign in with any Google account
3. Click "Create API Key" — no credit card needed
4. Copy the key (starts with AIza...)

## Run locally (optional, to test before deploying)
1. Create a folder `.streamlit/` next to app.py
2. Inside it, create a file called `secrets.toml` with:
   ```
   GEMINI_API_KEY = "your-real-key-here"
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run:
   ```
   streamlit run app.py
   ```

## Deploy for free on Streamlit Community Cloud
1. Push this folder to a GitHub repository (do NOT include secrets.toml —
   it's already in .gitignore)
2. Go to https://share.streamlit.io
3. Sign in with GitHub
4. Click "New app" → select your repo → set main file path to `app.py`
5. Before deploying, click "Advanced settings" → "Secrets" and paste:
   ```
   GEMINI_API_KEY = "your-real-key-here"
   ```
6. Click "Deploy"

Your app will be live at a URL like:
`https://your-app-name.streamlit.app`

## Free tier limits to know
Gemini 2.5 Flash free tier: ~10 requests/minute, ~250 requests/day.
Plenty for personal use. If you hit limits, just wait a minute and retry.
