import streamlit as st
import time, requests, json

available_genres = [
    "World Geopolitics",
    "Indian Politics",
    "Entertainment",
    "Science",
    "Technology",
    "Business",
    "Lifestyle",
    "Sports",
    "Education",
    "Health",
]

st.title("NewGate")
st.header("The AI powered news digest.", divider="gray")

st.space(size="medium")

selected_genres = st.multiselect(
    label="Select the genres you want.", options=available_genres
)
st.session_state["selected_genres"] = selected_genres

st.space(size="medium")

with st.container(horizontal_alignment="center"):
    if st.button(
        label="Fetch!", icon=":material/sprint:", icon_position="right", type="primary"
    ):
        with st.spinner(text="Fetching news .... Please be patient", show_time=True):
            response = requests.post(
                "http://127.0.0.1:8000/run", json={"genres": selected_genres}
            )
            st.session_state["output"] = json.loads(response.text)
            time.sleep(len(selected_genres) * 5)
        st.success("Redirecting...")
        time.sleep(3)
        st.switch_page(r"pages/display.py")
