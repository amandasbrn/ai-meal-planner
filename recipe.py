import streamlit as st
import base64
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

#### ---------- SET STREAMLIT PAGE ---------- ####

st.header("🍳 SEARCH RECIPE ♨️")
st.markdown("AI-based recipe search using LLM and Google Search grounding.")


#### ---------- SET GEMINI AI ---------- #### 

load_dotenv()  # Load environment variables from .env file

api_token = os.getenv('api_key')

def generate(system, recipe):
    client = genai.Client(
        api_key=os.environ.get("api_key"),
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"Please make me an easy and beginner-friendly {recipe}."),
            ],
        ),
    ]
    tools = [
        types.Tool(google_search=types.GoogleSearch())
    ]
    generate_content_config = types.GenerateContentConfig(
        tools=tools,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text=system),
        ],
    )
    output = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        output += chunk.text

    return st.write(output)

recipe = st.text_input("Type recipe", None)
clicked = st.button("Search recipe", type="primary")

system_instruction = f"The user wants a {recipe} recipe. You should search for {recipe} recipes on google search and provide one that is suitable for a university student, meaning it should be simple, quick and easy, beginner and budget-friendly. Please also put the link of recipe sources." 

if clicked:
    st.spinner("Searching the recipe...")
    generate(system_instruction, recipe)