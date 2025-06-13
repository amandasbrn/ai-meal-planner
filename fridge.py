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
from streamlit_tags import st_tags_sidebar

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

st.header("🍽️ PLAN FROM FRIDGE 🥢")
st.markdown("AI-based meal planner to help Dira, a university student, plan and cook her simple and nutritious meals based on what she already has in fridge.")
st.divider()
num_of_days = st.sidebar.select_slider(
    "Meal plan for how many days?",
    options=[
        1, 3, 5, 7
    ]
)

keyword = st_tags_sidebar(
    label="What's on your fridge?:",
    text='Press enter to add more',
    value=None,
    maxtags = 100,
    key='1')

ingredients = ', '.join(keyword)

generate = st.sidebar.button("generate meal plan", type="primary")

if generate:
    with st.spinner("Generating your meal plan from your fridge..."):
        messages = [
                (
                    "system",
                    {system_instruction},
                ),
                ("human", f"please make me a {num_of_days} days meal plan for breakfast, lunch, and dinner. I have these ingredients in my kitchen: {ingredients}, make me beginner-friendly and easy make sense meals out of it. Do not skip any of the meals. Note: just make me a meal plan."),
            ]

        ai_msg = llm.invoke(messages)
        st.write(ai_msg.content)