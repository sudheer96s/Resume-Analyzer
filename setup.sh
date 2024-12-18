# mkdir -p ~/.streamlit/

# echo "\
# [server]\n\
# headless = true\n\
# port = $PORT\n\
# enableCORS = false\n\
# " > ~/.streamlit/config.toml




python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt 
python -m spacy download en_core_web_sm
