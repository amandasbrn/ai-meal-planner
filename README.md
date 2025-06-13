## 💡 Project Summary
A simple, intelligent meal planning system that utilizes Generative AI from Gemini AI to recommend personalized meals based on user preferences. At the moment, this app is personalized with my own needs, so the options are only the number of days and the kind of food I want to make (example: Korean, Western, Japanese, Indonesian, etc). The options are endless. I can add dietary restrictions, halal food cautions, etc.

The idea to build this app is because I will be a university student again this year, and I will be living alone. As I am constantly confused about what food to make, along with the short amount of time to meal prep due to busy uni life, this app will surely support my lifestyle.

## 🛠️ Tech Stacks
Python
Streamlit for UI and deployment (with template customization) 
Google Gemini
Langchain for prompting, generating, and implementing the agentic feature
Google Search grounding
Sqlite3

## 👾 Application Features
### Build a meal plan & grocery shop list
When the user generates a meal plan, the LLM will generate x days' worth of meal plan, along with the grocery shop list to make those meals. The user can also download the grocery shop, then airdrop it to the phone (in my case, I am using an iOS environment, so it's convenient.) This brings me to the next feature.
After the plan & grocery shop list are generated, it will be automatically stored in the database I built with sqlite3. Then, the plan and grocery list will be presented in the "Meal plan & grocery log" menu.

### Plan what's on your fridge
I took the consideration when I still have some leftover ingredients from my past grocery shop. The user can input what ingredients are still in the fridge, and the LLM will suggest what meals can be cooked with those ingredients. The user can also choose how many days of meal plan using those ingredients, but I usually just pick 1 day, depending on how much of the ingredients are still available.

### Search recipe on Google
Gemini AI has a new feature to apply Google search grounding within the generated items, along with the URL, so the LLM could utilize the Google search to support its answers. I implemented this so the user could search recipes directly from the app.
Although using Google search directly is also okay, this is a form of practicing how to implement agentic behavior in the LLM. The drawback of this feature is, the URLs of the sources given are not always legit, sometimes the LLM gives us broken links.
