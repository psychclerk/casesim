"""
Psychiatry Case Simulator - Streamlit Application

A multi-presentation case-based learning tool for psychiatry education.
"""

import streamlit as st
from case_loader import (
    get_all_categories,
    load_category_metadata,
    load_case_by_category
)

# Page configuration
st.set_page_config(
    page_title="Psychiatry Case Simulator",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and branding
st.title("🧠 Psychiatry Case Simulator")
st.markdown("**Interactive case-based learning for psychiatry education**")
st.markdown("---")

# Initialize session state
if "current_case" not in st.session_state:
    st.session_state.current_case = None
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None
if "revealed_sections" not in st.session_state:
    st.session_state.revealed_sections = {
        "history": False,
        "mse": False,
        "investigations": False,
        "suicide": False,
        "explanation": False,
        "management": False
    }
if "diagnosis_submitted" not in st.session_state:
    st.session_state.diagnosis_submitted = False
if "diagnosis_correct" not in st.session_state:
    st.session_state.diagnosis_correct = False

# Sidebar - Category selector
st.sidebar.title("📚 Select Category")
categories = get_all_categories()

if not categories:
    st.error("❌ No case categories found. Please ensure case files exist in the cases/ directory.")
    st.stop()

# Display category selector
category_display_names = [cat.replace("_", " ").title() for cat in categories]
category_mapping = dict(zip(category_display_names, categories))

selected_display = st.sidebar.selectbox(
    "Choose a presentation category:",
    options=category_display_names,
    index=0 if not st.session_state.selected_category else 
          categories.index(st.session_state.selected_category) if st.session_state.selected_category in categories else 0
)

selected_category = category_mapping[selected_display]

# Load new case if category changed
if st.session_state.selected_category != selected_category:
    st.session_state.selected_category = selected_category
    st.session_state.current_case = load_case_by_category(selected_category)
    st.session_state.revealed_sections = {key: False for key in st.session_state.revealed_sections}
    st.session_state.diagnosis_submitted = False
    st.session_state.diagnosis_correct = False

# Load initial case if none exists
if st.session_state.current_case is None:
    st.session_state.current_case = load_case_by_category(selected_category)

# Get category metadata
try:
    metadata = load_category_metadata(selected_category)
    st.sidebar.info(f"**Category:** {metadata['category']}\n\n**Presentation:** {metadata['presentation']}")
except Exception as e:
    st.sidebar.warning(f"Could not load category metadata: {e}")

# Main case display
case = st.session_state.current_case

# Patient demographics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Age", f"{case['age']} years")
with col2:
    st.metric("Sex", case['sex'])
with col3:
    st.metric("Presentation", case['presenting_complaint'].split()[0] + "...")

st.markdown("---")

# Progressive disclosure sections
st.subheader("📋 Clinical Information")

# History section
if st.button("🔍 Reveal History", disabled=st.session_state.revealed_sections["history"]):
    st.session_state.revealed_sections["history"] = True

if st.session_state.revealed_sections["history"]:
    with st.expander("**Patient History**", expanded=True):
        st.markdown(f"**Presenting Complaint:** {case['presenting_complaint']}")
        st.markdown(f"**Duration:** {case['duration']}")
        st.markdown(f"**Associated Features:** {case['associated']}")
        st.markdown(f"**Risk Factors:** {case['risk_factors']}")

# MSE section
if st.button("🔍 Reveal Mental State Examination", disabled=st.session_state.revealed_sections["mse"]):
    st.session_state.revealed_sections["mse"] = True

if st.session_state.revealed_sections["mse"]:
    with st.expander("**Mental State Examination (MSE)**", expanded=True):
        st.markdown(case['mse'])

# Investigations section
if st.button("🔍 Reveal Investigations", disabled=st.session_state.revealed_sections["investigations"]):
    st.session_state.revealed_sections["investigations"] = True

if st.session_state.revealed_sections["investigations"]:
    with st.expander("**Investigations**", expanded=True):
        st.markdown(case['investigations'])

# Suicide risk section
if st.button("🔍 Reveal Suicide Risk Assessment", disabled=st.session_state.revealed_sections["suicide"]):
    st.session_state.revealed_sections["suicide"] = True

if st.session_state.revealed_sections["suicide"]:
    with st.expander("**Suicide Risk Assessment**", expanded=True):
        st.markdown(case['suicide_risk'])

st.markdown("---")

# Diagnosis section
st.subheader("🎯 Make Your Diagnosis")

# Get all unique diagnoses from current category
all_cases = load_case_by_category(selected_category, return_all=True)
unique_diagnoses = sorted(list(set([c['diagnosis'] for c in all_cases])))

# Diagnosis selectbox
selected_diagnosis = st.selectbox(
    "Select your diagnosis:",
    options=["-- Select a diagnosis --"] + unique_diagnoses,
    disabled=st.session_state.diagnosis_submitted
)

# Submit diagnosis button
if st.button("✅ Submit Diagnosis", disabled=st.session_state.diagnosis_submitted or selected_diagnosis == "-- Select a diagnosis --"):
    st.session_state.diagnosis_submitted = True
    st.session_state.diagnosis_correct = (selected_diagnosis == case['diagnosis'])

# Display feedback
if st.session_state.diagnosis_submitted:
    if st.session_state.diagnosis_correct:
        st.success(f"✅ **Correct!** The diagnosis is: **{case['diagnosis']}**")
    else:
        st.error(f"❌ **Incorrect.** The correct diagnosis is: **{case['diagnosis']}**")
    
    # Reveal explanation
    st.session_state.revealed_sections["explanation"] = True
    st.session_state.revealed_sections["management"] = True

# Explanation section
if st.session_state.revealed_sections["explanation"]:
    with st.expander("**📖 Explanation**", expanded=True):
        st.markdown(case['explanation'])

# Management section
if st.session_state.revealed_sections["management"]:
    with st.expander("**💊 Management**", expanded=True):
        st.markdown(case['management'])

st.markdown("---")

# New case button
if st.button("🔄 Load New Case"):
    st.session_state.current_case = load_case_by_category(selected_category)
    st.session_state.revealed_sections = {key: False for key in st.session_state.revealed_sections}
    st.session_state.diagnosis_submitted = False
    st.session_state.diagnosis_correct = False
    st.rerun()

# Footer
st.markdown("---")
st.caption("💡 Tip: Use the sidebar to switch between different presentation categories.")
st.markdown(
    """
    <div class="footer">
        🧠 Psychiatry Case Simulator · Case-based psychiatry education · © 2026 · Only to be used for educational purpose
    </div>
    """,
    unsafe_allow_html=True
)
