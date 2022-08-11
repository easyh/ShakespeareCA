mkdir -p ~/.streamlit/

echo " [theme]
primaryColor = '#ffffff'
backgroundColor = '#92b39b'
secondaryBackgroundColor = '#55695a'
textColor = '#ffffff'

[server]
headless = true
port = $PORT
enableCORS = false

" > ~/.streamlit/config.toml