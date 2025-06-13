import streamlit as st

# # Function to load and apply CSS
# def load_css(file_name):
#     with open(file_name) as f:
#         st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# # Load and apply the CSS file at the start of your app
# load_css('style.css')

st.set_page_config(page_title="Personal AI Meal Planner", page_icon="🍥", layout="wide")

pages = {
    "What do you want to do?": 
    [st.Page("meal_grocery.py", title="🛒 Build a meal plan & grocery shop list"),
    st.Page("fridge.py", title="🍱 What's in your fridge? Plan it!"),
    st.Page("recipe.py", title="🔎 Search recipe on google"),
    st.Page("meal_log.py", title="🗂️ Meal plan & grocery log"),
    ]
}
pg = st.navigation(pages)
pg.run()