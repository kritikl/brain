import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="AI Hardware Second Brain", layout="wide")
st.title("AI Hardware Career Second Brain")

@st.cache_data
def load_full_todo():
    data = {
        'Status': ['To Do'] * 40,
        'Deadline': ['2026-10-31','Ongoing','Ongoing','Ongoing','Ongoing','Ongoing','Ongoing','Ongoing','2026-11-15','2026-12-01',
                     '2026-12-01','2026-12-01','2026-12-15','Self-Paced','2027-01-15','2027-03-31','Ongoing','Ongoing','Ongoing','Ongoing',
                     '2026-12-15','2026-12-15','2026-12-15','Self-Paced','2027-01-15','Ongoing','Ongoing','Ongoing','2027-04-10','Ongoing',
                     'Ongoing','Ongoing','Ongoing','Ongoing','Ongoing','Ongoing','Ongoing','Ongoing','Ongoing','Ongoing'],
        'Category': ['Application','Networking','Networking','Networking','Networking','Networking','Networking','Networking','Application','Internship',
                     'Internship','Internship','Application','Preparation','Application','Application','Networking','Networking','Networking','Networking',
                     'Application','Application','Application','Preparation','Application','Networking','Networking','Networking','Application','Preparation',
                     'Preparation','Preparation','Preparation','Preparation','Preparation','Preparation','Preparation','Preparation','Preparation','Preparation'],
        'Task Description': [
            'Apply to University of Tokyo IME Graduate Program',
            'Contact Masato Motomura - AI hardware accelerators',
            'Contact Tetsuya Asai - Neuromorphic',
            'Contact Koji Inoue - Computer architecture',
            'Contact Hidehiro Fujiwara - VLSI',
            'Contact Luca Benini - Energy-efficient computing',
            'Contact Giacomo Indiveri - Neuromorphic',
            'Contact Said Hamdioui - In-memory computing',
            'Apply to Institute of Science Tokyo IGP(A)',
            'Apply to RIKEN AIP Winter Internship',
            'Apply to AIST Internship',
            'Apply to IMEC Student Internship',
            'Apply to ETH Zurich',
            'Review Eyeriss paper series',
            'Apply to NUS PhD',
            'Apply to OIST PhD',
            'Contact Marian Verhelst (KU Leuven)',
            'Contact David Atienza (EPFL)',
            'Contact Ken Takeuchi (Tokyo)',
            'Contact Takahiro Hanyu (Tohoku)',
            'Apply to Stanford EE/CS PhD',
            'Apply to UC Berkeley EECS PhD',
            'Apply to MIT EECS PhD',
            'Review Loihi Neuromorphic paper',
            'Apply to KAIST EE PhD',
            'Contact Rapidus lab',
            'Contact Sony Semiconductor',
            'Contact Renesas Electronics',
            'Apply to Waseda IPS',
            'Prepare MEXT Scholarship Application',
            'Update CV with hardware projects',
            'Prepare research proposal on efficient inference',
            'Review ISSCC 2027 call',
            'Track application status weekly',
            'Schedule professor follow-ups',
            'Contact University of Tsukuba faculty',
            'Monitor MEXT 2027 updates',
            'Review new papers on quantized networks',
            'Prepare for USA applications',
            'Weekly progress review'
        ],
        'Notes': ['Tier 1 Core','High priority','High priority','High priority','High priority','High priority','High priority','High priority','Tier 1 Core','High priority',
                  'High priority','High priority','Tier 1 Core','Core reading','Backup','Core','High priority','High priority','High priority','High priority',
                  'Reach','Reach','Reach','Core','Backup','High priority','High priority','High priority','Tier 1 Core','High','High','High','Important','High','High','High','High','High','High','High']
    }
    return pd.DataFrame(data)

if 'todo' not in st.session_state:
    st.session_state.todo = load_full_todo()

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
            r = requests.get("https://raw.githubusercontent.com/kritikl/brain/main/opportunities.json")
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
                st.error("Could not fetch")
        except Exception as e:
            st.error(f"Error: {e}")

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

st.caption("v1.6 - Fixed and Full")
