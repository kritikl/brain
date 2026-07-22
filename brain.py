import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="AI Hardware Second Brain", layout="wide")
st.title("AI Hardware Career Second Brain")

# Minimal stable data
data = {
    'Status': ['To Do'] * 15,
    'Deadline': ['2026-10-31','Ongoing','Ongoing','Ongoing','2026-11-15','2026-12-01','2026-12-15','Self-Paced','2027-01-15','2027-03-31','Ongoing','Ongoing','Ongoing','Ongoing','Ongoing'],
    'Category': ['Application','Networking','Networking','Networking','Application','Internship','Application','Preparation','Application','Application','Networking','Networking','Networking','Application','Preparation'],
    'Task Description': [
        'Apply to University of Tokyo IME Graduate Program',
        'Contact Masato Motomura - AI hardware accelerators',
        'Contact Tetsuya Asai - Neuromorphic',
        'Contact Koji Inoue - Computer architecture',
        'Apply to Institute of Science Tokyo IGP(A)',
        'Apply to RIKEN AIP Winter Internship',
        'Apply to ETH Zurich',
        'Review Eyeriss paper series',
        'Apply to NUS PhD',
        'Apply to OIST PhD',
        'Contact Marian Verhelst (KU Leuven)',
        'Contact David Atienza (EPFL)',
        'Contact Ken Takeuchi (Tokyo)',
        'Apply to Stanford EE/CS PhD',
        'Prepare MEXT Scholarship Application'
    ],
    'Notes': ['Tier 1 Core','High priority','High priority','High priority','Tier 1 Core','High priority','Tier 1 Core','Core reading','Backup','Core','High priority','High priority','High priority','Reach','High']
}

if 'todo' not in st.session_state:
    st.session_state.todo = pd.DataFrame(data)

todo = st.session_state.todo

tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "To-Do List", "Auto Pull", "Manual Add"])

with tab1:
    st.subheader("Live Dashboard")
    completed = len(todo[todo['Status'] == 'Done'])
    total = len(todo)
    progress = int((completed / total) * 100) if total > 0 else 0
    st.metric("Overall Progress", f"{progress}%", f"{completed}/{total} tasks")
    st.progress(progress)

with tab2:
    st.subheader("Master To-Do List")
    edited = st.data_editor(todo, use_container_width=True, num_rows="dynamic", key="todo_editor")
    if st.button("Save Changes"):
        st.session_state.todo = edited
        st.success("Saved")

with tab3:
    st.subheader("Auto Pull from GitHub")
    if st.button("Pull Latest Opportunities"):
        try:
            r = requests.get("https://raw.githubusercontent.com/kritikl/brain/main/opportunities.json", timeout=10)
            if r.status_code == 200:
                new_opps = r.json()
                st.success(f"Found {len(new_opps)} new opportunities!")
                for opp in new_opps:
                    new_row = pd.DataFrame([{
                        'Status': 'To Do',
                        'Deadline': opp.get('deadline', 'Ongoing'),
                        'Category': 'Application',
                        'Task Description': opp.get('title', 'New Opportunity'),
                        'Notes': opp.get('match', 'New')
                    }])
                    st.session_state.todo = pd.concat([st.session_state.todo, new_row], ignore_index=True)
                st.success("New entries added!")
            else:
                st.error(f"Failed. Status: {r.status_code}. Make sure repo is public and opportunities.json exists.")
        except Exception as e:
            st.error(f"Could not fetch. Error: {str(e)}")

with tab4:
    st.subheader("Manual Add")
    with st.form("new_task"):
        deadline = st.date_input("Deadline", datetime(2026, 11, 15))
        category = st.selectbox("Category", ["Application", "Networking", "Internship", "Preparation"])
        task = st.text_input("Task Description")
        notes = st.text_input("Notes")
        if st.form_submit_button("Add"):
            new_row = pd.DataFrame([{'Status': 'To Do', 'Deadline': str(deadline), 'Category': category, 'Task Description': task, 'Notes': notes}])
            st.session_state.todo = pd.concat([st.session_state.todo, new_row], ignore_index=True)
            st.success("Added!")

st.caption("v1.6 Stable - Fixed")
