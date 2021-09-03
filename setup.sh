mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"colocue seu email aqui\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml