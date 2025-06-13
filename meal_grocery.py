import streamlit as st
from google import genai
from google.genai import types
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os
import datetime
import re
import sqlite3

#### ---------- SET CREDENTIALS & GENAI CLIENT ---------- ####

load_dotenv()  # Load environment variables from .env file

api_token = os.getenv('api_key')

if not api_token:
    raise ValueError("No API token found. Check your .env file.")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    api_key=api_token
    )

system_instruction = "You are an AI-based meal planner to help me, a university student, plan and cook my nutritious meals while also saving money." 

#### ---------- SET STREAMLIT PAGE ---------- ####

# # Function to load and apply CSS
# def load_css(file_name):
#     with open(file_name) as f:
#         st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# # Load and apply the CSS file at the start of your app
# load_css('style.css')

st.header("🥗 MEAL PLANNER 🥘")
st.markdown("AI-based meal planner to help Dira, a university student, plan and cook her simple and nutritious meals")

#### ---------- SET USER INPUT ON SIDEBAR ---------- ####

num_of_days = st.sidebar.select_slider(
    "Meal plan for how many days?",
    options=[
        1, 3, 5, 7
    ]
)

food_type = st.sidebar.multiselect(
    "What kind of food do you want to make?",
    ["Korean", "Western", "Japanese", "Indonesian", "Italian", "Mexican", "Chinese"]
)


generate = st.sidebar.button("generate meal plan", type="primary")

#### ---------- SET SQLITE DB TO SAVE MEAL PLANNER & GROCERY LIST ---------- ####
current_date = datetime.date.today().strftime("%d %B %Y")
con = sqlite3.connect("meal_planner.db")
cur = con.cursor()

#### ---------- SET OUTPUT ---------- ####

tab1, tab2 = st.tabs(["👨🏻‍🍳 Meal plan", "🛒 Grocery shopping list"])

if generate:
    with st.spinner("Generating your meal plan and shopping list..."):
        with tab1:
            messages = [
                (
                    "system",
                    {system_instruction},
                ),
                ("human", f"please make me a {num_of_days} days meal plan for breakfast, lunch, and dinner. I want to make beginner-friendly, quick and easy {food_type} kind of meals. Make the meals share the same base ingredients so I can cook in bulk. Note: just make me a meal plan."),
            ]

            ai_msg = llm.invoke(messages)
            st.write(ai_msg.content)

        
        with tab2:
            shopping_list = [
                (
                    "system",
                    {system_instruction},
                ),
                ("human", f"Extract a shopping list from the following meal plan: {ai_msg.content} Group ingredients into sections: Vegetables, Protein, Fruits, Carbs, Seasoning and spices, and snacks (for snacks, you don't have to follow the meal plan). For the quantity of each ingredients, please give recommendations for 1 person based on the meal plan. Make the ingredients list less than 8 items for each sections. ALWAYS include fruits although it's not in the meal plan. Avoid duplicates and quantities unless obvious. Keep things simple, dont make too much list. Please just list the goods right away."),
            ]
            ai_shopping_msg = llm.invoke(shopping_list)
            st.write(ai_shopping_msg.content)
        
            cur.execute(
                "INSERT INTO meal_planner (date, meal_plan, shopping_list) VALUES (?, ?, ?)",
                (current_date, ai_msg.content, ai_shopping_msg.content)
            )
            con.commit()
            st.toast("Saved successfully on database!")

            ## --- DOWNLOAD GROCERY LIST TO .TXT FILE ---##

            def handle_click():
                st.toast("🛒 Your shopping list is ready!")
            
            def clean_shopping_list(raw_text):
                # Remove everything before the first "**" (start of the sections)
                cleaned = re.sub(r"^.*?\*\*", "**", raw_text, flags=re.DOTALL)

                # Replace "* " bullets with "-"
                cleaned = re.sub(r"\*+", "", cleaned)

                # Optional: Strip double spaces or fix formatting
                cleaned = re.sub(r" +", " ", cleaned)

                return cleaned.strip()
            
            cleaned_text = clean_shopping_list(ai_shopping_msg.content)

            @st.fragment()
            def download_grocery():
                st.download_button(
                        label="📥  download grocery shop list",
                        data=cleaned_text,
                        file_name=f"{current_date}_grocery_shop_list.txt",
                        on_click=handle_click,
                        type="secondary"
                    )

            download_grocery()