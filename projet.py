import os
import subprocess
import streamlit as st
from streamlit_lottie import st_lottie
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def load_lottieurl(url):
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    try:
        r = session.get(url, timeout=10)
        r.raise_for_status()
        return r.json()
    except (requests.RequestException, ValueError) as e:
        print(f"Error fetching Lottie animation: {e}")
        return None

# Set the SWI-Prolog environment
os.environ["SWI_HOME_DIR"] = "C:\\Program Files\\swipl"

def prolog_query(query):
    prolog_file = os.path.abspath("miniprojet.pl")
    prolog_command = f"{query}"
    command = ['swipl', '-s', prolog_file, '-g', prolog_command, '-t', 'halt']

    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = p.communicate()

    try:
        output_decoded = output.decode('utf-8').strip()
    except UnicodeDecodeError:
        output_decoded = output.decode('latin-1').strip()

    try:
        error_decoded = error.decode('utf-8').strip()
    except UnicodeDecodeError:
        error_decoded = error.decode('latin-1').strip()

    if error_decoded:
        st.error(f"Prolog error: {error_decoded}")
    return output_decoded

def get_symptoms():
    query = "symptomes(Symptoms), maplist(writeln, Symptoms)"
    results = prolog_query(query)
    return results.split("\n") if results else []

def diagnose(symptoms):
    symptoms_list = ','.join([f"'{s.strip()}'" for s in symptoms])
    query = f"diagnose([{symptoms_list}])"
    results = prolog_query(query)
    return results.split("\n") if results else []

def verify_login(user, password):
    user_atom = f"'{user}'"
    password_atom = f"'{password}'"
    query = f"verify_credentials({user_atom}, {password_atom})"
    result = prolog_query(query)
    return "true" in result

def main():
    st.title("Disease Diagnosis System")

    lottie_url = "https://lottie.host/5ba847e7-fe20-4201-aa21-9bbdaa016681/1PFKQZwa5A.json"
    lottie_animation = load_lottieurl(lottie_url)
    if lottie_animation:
        st_lottie(lottie_animation, height=500, width=500)
        
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.sidebar.header("Login")
        user = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")

        if st.sidebar.button("Login"):
            if verify_login(user, password):
                st.session_state.logged_in = True
                st.session_state.user = user
                st.success("Login successful")
                st.experimental_rerun()
            else:
                st.sidebar.error("Invalid username or password")
    else:
        st.header("Select your symptoms")

        symptoms = get_symptoms()
        selected_symptoms = st.multiselect("Symptoms", symptoms)

        if st.button("Diagnose"):
            with st.spinner('Diagnosing...'):
                import time
                time.sleep(2)
                diagnoses = diagnose(selected_symptoms)
                if diagnoses:
                    st.write("You might have:")
                    for diagnosis in diagnoses:
                        st.write(diagnosis)
                else:
                    st.write("No matching diseases found.")

if __name__ == "__main__":
    main()
