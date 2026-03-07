import streamlit as st
import requests
from agent import ask_space_agent
from dotenv import load_dotenv
import os

load_dotenv()

NASA_API_KEY = os.getenv("NASA_API_KEY")
NASA_APOD_URL = "https://api.nasa.gov/planetary/apod"

st.set_page_config(
    page_title="🌌 Space Explorer",
    page_icon="🚀",
    layout="centered"
)
st.markdown("🌠 *Explore the universe with AI*")

# ---- Custom CSS ----
st.markdown("""
<style>

/* Main background */
.stApp {
    background: radial-gradient(circle at top, #0b0f29, #020412);
    color: white;
}

/* Force text color everywhere */
html, body, [class*="css"]  {
    color: white !important;
}

/* Title styling */
.title {
    font-size: 48px;
    font-weight: bold;
    text-align: center;
}

/* Subtitle styling */
.subtitle {
    text-align: center;
    font-size: 18px;
    color: #b8c1ff;
}

/* Card container */
.card {
    background-color: rgba(255,255,255,0.05);
    padding: 25px;
    border-radius: 15px;
    margin-top: 20px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.08);
}

/* Input container (fixes white box in light mode) */
div[data-baseweb="input"] {
    background-color: rgba(255,255,255,0.08) !important;
    border-radius: 8px;
    border: 1px solid rgba(255,255,255,0.2);
}

/* Actual input field */
div[data-baseweb="input"] input {
    background-color: transparent !important;
    color: white !important;
}

/* Placeholder text */
div[data-baseweb="input"] input::placeholder {
    color: rgba(255,255,255,0.6);
}

/* Label above input */
label {
    color: rgba(255,255,255,0.85) !important;
    font-weight: 500;
}

/* Button styling */
.stButton button {
    background-color: #4c6fff;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 0.5rem 1.2rem;
    font-weight: 500;
}

.stButton button:hover {
    background-color: #6c85ff;
}

/* Spinner text */
.stSpinner {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# ---- Title ----
st.markdown('<div class="title">🌌 Space Explorer</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Discover NASA’s Astronomy Picture of the Day and ask space questions</div>',
    unsafe_allow_html=True
)

# ---- Fetch APOD ----
@st.cache_data(ttl=3600)
def fetch_apod():
    params = {"api_key": NASA_API_KEY}
    response = requests.get(NASA_APOD_URL, params=params)
    return response.json()

data = fetch_apod()

# ---- APOD Card ----
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)

    if data.get("media_type") == "image":
        st.image(data["url"], use_container_width=True)

    st.markdown(f"### {data.get('title')}")

    st.write(data.get("explanation"))

    st.markdown('</div>', unsafe_allow_html=True)

# ---- Question Section ----
st.divider()

st.subheader("🚀 Ask a Space Question")

question = st.text_input("What would you like to know about space?")

if question:
    with st.spinner("Consulting the cosmos... 🌠"):

        answer = ask_space_agent(
            data.get("title", ""),
            data.get("explanation", ""),
            question
        )

        st.markdown("### 🧠 Answer")
        st.write(answer)