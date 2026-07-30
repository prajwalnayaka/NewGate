import streamlit as st

if not st.session_state["output"]['news']:
    with st.container(horizontal_alignment="center"):
        st.error("There was an error while fetching news for you. I am sorry for the inconvenience.")
        st.write("Please retry again in a few minutes.")
        if st.button("Back to home",icon=":material/arrow_back:"):
            st.switch_page("../front_app.py")
        st.stop()


news = st.session_state['output']['news']

for genre, data in news.items():
    with st.expander(genre):
        st.divider()
        if data["status"]:
            st.warning(data["status"])

        for article in data["articles"]:
            st.subheader(article["title"])
            st.caption(f"{article['source']} — {article['publish_date']}")
            st.write(article["content"])
        st.divider()