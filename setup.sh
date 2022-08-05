mkdir -p ~/.streamlit/
echo "\
primaryColor = "#ffffff"
backgroundColor = "#92b39b"
secondaryBackgroundColor = "#55695a"
textColor = "#ffffff"
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml