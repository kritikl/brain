import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="AI Hardware Second Brain", layout="wide")
st.title("AI Hardware Career Second Brain")

# Load local data
@st.cache_data
def load_local_todo():
    # Full data here (use the comprehensive list from previous messages)
    data = { ... }  # Paste the full data dict
    return pd.DataFrame(data)

if 'todo' not in st.session_state:
    st.session_state.todo = load_local_todo()

todo = st.session_state.todo

tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "To-Do List", "Auto Scan", "Manual Add"])

with tab1:
    st.subheader("Live Dashboard")
    completed = len(todo[todo['Status'] == 'Done'])
    total = len(todo)
    progress = int((completed / total) * 100) if total > 0 else 0
    st.metric("Progress", f"{progress}%", f"{completed}/{total} tasks")
    st.progress(progress)

with tab2:
    st.subheader("Master To-Do List")
    edited = st.data_editor(todo, use_container_width=True, num_rows="dynamic")
    if st.button("Save Changes"):
        st.session_state.todo = edited
        st.success("Saved")

with tab3:
    st.subheader("Auto Scan from GitHub")
    if st.button("Pull Latest Opportunities"):
        try:
            r = requests.get("https://raw.githubusercontent.com/kritikl/brain/main/opportunities.json")
            if r.status_code == 200:
                new_opps = r.json()
                st.success(f"Found {len(new_opps)} new opportunities!")
                for opp in new_opps:
                    st.write(f"• {opp.get('title')} (due {opp.get('deadline')})")
                    if st.button(f"Add {opp.get('title')}", key=opp.get('title')):
                        new_row = pd.DataFrame([{'Status': 'To Do', 'Deadline': opp.get('deadline'), 'Category': 'Application', 'Task Description': opp.get('title'), 'Notes': opp.get('match')}])
                        st.session_state.todo = pd.concat([st.session_state.todo, new_row], ignore_index=True)
                        st.success("Added!")
        except:
            st.error("Could not fetch updates. Make sure the repo exists.")

with tab4:
    st.subheader("Manual Add")
    with st.form("add"):
        deadline = st.date_input("Deadline", datetime(2026, 11, 15))
        category = st.selectbox("Category", ["Application", "Networking", "Internship", "Preparation"])
        task = st.text_input("Task Description")
        notes = st.text_input("Notes")
        if st.form_submit_button("Add"):
            new_row = pd.DataFrame([{'Status': 'To Do', 'Deadline': str(deadline), 'Category': category, 'Task Description': task, 'Notes': notes}])
            st.session_state.todo = pd.concat([st.session_state.todo, new_row], ignore_index=True)
            st.success("Added!")

st.caption("v1.5 - Connected to GitHub automation")
