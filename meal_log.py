import streamlit as st
import datetime
import re
import sqlite3

st.header("🛒 🧾 MEAL PLAN & GROCERY LOG")
st.markdown("This is where I save my generated meal plan & grocery shop list. I can download the shop list also.")

con = sqlite3.connect("meal_planner.db")
cur = con.cursor()

st.subheader("🏪 Saved Meal Plans")
rows = cur.execute("SELECT * FROM meal_planner ORDER BY id DESC").fetchall()
for row in rows:
    with st.expander(f"🗓 {row[1]}"):
        st.markdown("### 🍽 Meal Plan")
        st.write(row[2])
        st.markdown("### 🛒 Shopping List")
        st.write(row[3])

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button(f"🗑 Delete this meal plan", key=f"del-{row[0]}"):
                cur.execute("DELETE FROM meal_planner WHERE id = ?", (row[0],))
                con.commit()
                st.experimental_rerun()

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

            grocery_list = clean_shopping_list(row[3])
            st.download_button(
                    label="📥  download grocery shop list",
                    data=grocery_list,
                    file_name=f"{row[1]}_grocery_shop_list.txt",
                    on_click=handle_click,
                    type="secondary",
                    key=f"dow-{row[0]}"
                )