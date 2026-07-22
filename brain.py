import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="AI Hardware Second Brain", layout="wide")
st.title("AI Hardware Career Second Brain")

data = {
    'Status': ['To Do', 'To Do', 'To Do', 'To Do', 'To Do'],
    'Deadline': ['2026-10-31', 'Ongoing', '2026-11-15', 'Self-Paced', '2026-12-01'],
    'Category': ['Application', 'Networking', 'Application', 'Preparation', 'Internship'],
    'Task Description': [
        'Apply to University of Tokyo IME Graduate Program',
        'Contact Masato Motomura - AI hardware accelerators',
        'Apply to Institute of Science Tokyo IGP(A)',
        'Review Eyeriss paper series',
        'Apply to RIKEN AIP Winter Internship'
    ],
    'Notes': ['Tier 1 Core', 'High priority', 'Tier 1 Core', 'Core reading', 'High priority']
}

todo = pd.DataFrame(data)

tab1, tab2, tab3 = st.tabs(["Dashboard", "To-Do List", "Add Task"])

with tab1:
    st.subheader("Dashboard")
    completed = len(todo[todo['Status'] == 'Done'])
    total = len(todo)
    progress = int((completed / total) * 100) if total > 0 else 0
    st.metric("Progress", f"{progress}%", f"{completed}/{total} tasks")
    st.progress(progress)

with tab2:
    st.subheader("Master To-Do List")
    edited = st.data_editor(todo, width='stretch', num_rows="dynamic")
    if st.button("Save Changes"):
        st.success("Saved (session only)")

with tab3:
    st.subheader("Add New Task")
    with st.form("new_task"):
        deadline = st.date_input("Deadline", datetime(2026, 11, 15))
        category = st.selectbox("Category", ["Application", "Networking", "Internship", "Preparation"])
        task = st.text_input("Task Description")
        notes = st.text_input("Notes")
        if st.form_submit_button("Add"):
            st.success("Task added (session only)")

st.caption("Ultra Minimal Stable Version")
