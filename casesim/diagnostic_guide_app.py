"""
Psychiatry Resident Diagnostic Guide
Streamlit App for Differential Diagnosis Training
"""

import streamlit as st
import json
import os
from typing import Dict, List, Any, Optional
import pandas as pd
from diagnostic_engine import DiagnosticEngine

# Page configuration
st.set_page_config(
    page_title="Psychiatry Diagnostic Guide",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .symptom-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
    }
    
    .differential-high {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-radius: 0.25rem;
    }
    
    .differential-medium {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-radius: 0.25rem;
    }
    
    .differential-low {
        background-color: #e8f5e8;
        border-left: 4px solid #4caf50;
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-radius: 0.25rem;
    }
    
    .red-flag {
        background-color: #ffebee;
        color: #c62828;
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin: 0.25rem 0;
        font-weight: bold;
    }
    
    .clinical-pearl {
        background-color: #e3f2fd;
        color: #1565c0;
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin: 0.25rem 0;
        border-left: 3px solid #1976d2;
    }
    
    .question-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border: 1px solid #dee2e6;
    }
    
    .progress-container {
        background-color: #e9ecef;
        height: 20px;
        border-radius: 10px;
        margin: 1rem 0;
        overflow: hidden;
    }
    
    .progress-bar {
        background-color: #007bff;
        height: 100%;
        transition: width 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

def initialize_diagnostic_engine():
    """Initialize the diagnostic engine (no caching for debugging)"""
    try:
        engine = DiagnosticEngine()
        # Verify data is loaded
        symptoms = engine.get_all_symptoms()
        if not symptoms:
            st.error("Failed to load symptoms data. Please check the data files.")
            return None
        st.success(f"Diagnostic engine initialized with {len(symptoms)} symptoms")
        return engine
    except Exception as e:
        st.error(f"Error initializing diagnostic engine: {str(e)}")
        return None

def main():
    """Main application function"""
    # Initialize diagnostic engine
    engine = initialize_diagnostic_engine()
    
    # Check if engine was initialized successfully
    if engine is None:
        st.error("Failed to initialize diagnostic engine. Please check the data files.")
        return
    
    # Initialize session state for progress tracking
    if 'completed_symptoms' not in st.session_state:
        st.session_state.completed_symptoms = set()
    if 'current_symptom' not in st.session_state:
        st.session_state.current_symptom = 1
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    
    # Main title
    st.markdown('<h1 class="main-header">🧠 Psychiatry Resident Diagnostic Guide</h1>', unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    ### Welcome to the Psychiatry Differential Diagnosis Training Tool
    
    This interactive guide helps psychiatry residents develop systematic diagnostic reasoning skills 
    by working through **80 psychiatric symptom presentations** one at a time. 
    
    **How it works:**
    - **Symptom Focus**: Each case presents ONE psychiatric symptom (not full clinical cases)
    - **Guided Questions**: Interactive questions to gather differential diagnostic information  
    - **Ranked Differentials**: See diagnoses ranked by likelihood with reasoning
    - **Educational Content**: DSM-5 criteria, clinical pearls, and common pitfalls
    - **Knowledge Checks**: Test your understanding after each symptom
    - **Progress Tracking**: Monitor your learning journey
    """)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    
    # Get all symptoms for navigation with error handling
    all_symptoms = []
    total_symptoms = 0
    
    try:
        all_symptoms = engine.get_all_symptoms()
        total_symptoms = len(all_symptoms)
        
        if not all_symptoms:
            st.sidebar.warning("No symptoms found in database.")
        
    except Exception as e:
        st.sidebar.error(f"Error loading symptoms: {str(e)}")
        # Continue with empty list instead of returning
    
    # Progress tracking
    completed_count = len(st.session_state.completed_symptoms)
    progress_percentage = (completed_count / max(total_symptoms, 1) * 100) if total_symptoms > 0 else 0
    
    st.sidebar.markdown("### Progress Tracking")
    st.sidebar.markdown(f"**Completed: {completed_count}/{total_symptoms} symptoms**")
    
    # Progress bar
    st.sidebar.markdown(f"""
    <div class="progress-container">
        <div class="progress-bar" style="width: {progress_percentage}%"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation options
    st.sidebar.markdown("### Quick Navigation")
    
    # Home screen option
    if st.sidebar.button("🏠 Home", use_container_width=True):
        st.session_state.current_symptom = 0  # 0 indicates home screen
        st.rerun()
    
    # Comprehensive symptom list in sidebar
    if all_symptoms:
        st.sidebar.markdown("### All Symptoms")
        # Group symptoms by category for better organization
        categories = {}
        for symptom in all_symptoms:
            category = symptom.get('category', 'Other')
            if category not in categories:
                categories[category] = []
            categories[category].append(symptom)
        
        # Display symptoms by category
        for category, symptoms in sorted(categories.items()):
            with st.sidebar.expander(f"{category} ({len(symptoms)})"):
                for symptom in symptoms:
                    # Use emoji indicators for completion status
                    indicator = "✅" if symptom['id'] in st.session_state.completed_symptoms else "🔵"
                    if st.button(f"{indicator} {symptom['id']:02d}: {symptom['name']}", 
                               key=f"nav_{symptom['id']}"):
                        st.session_state.current_symptom = symptom['id']
                        st.rerun()
    
    # Random symptom option
    if all_symptoms and st.sidebar.button("🎲 Random Symptom", use_container_width=True):
        import random
        random_symptom = random.choice(all_symptoms)['id']
        st.session_state.current_symptom = random_symptom
        st.rerun()
    
    # Reset progress
    if st.sidebar.button("🔄 Reset Progress", use_container_width=True):
        st.session_state.completed_symptoms = set()
        st.session_state.current_symptom = 1
        st.session_state.user_answers = {}
        st.rerun()
    
    # Additional navigation info
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Navigation Tips")
    st.sidebar.markdown("• Click any symptom below to start")
    st.sidebar.markdown("• ✅ = Completed, 🔵 = Not started")
    st.sidebar.markdown("• Use Home button to return to main page")
    st.sidebar.markdown("• Random button for surprise selection")
    
    # Main content area
    if st.session_state.current_symptom == 0:
        if all_symptoms:
            show_home_screen(all_symptoms, completed_count, total_symptoms)
        else:
            st.error("No symptoms available. Please check the database files.")
    else:
        # Validate current symptom is valid
        valid_symptom_ids = [s['id'] for s in all_symptoms] if all_symptoms else []
        if st.session_state.current_symptom not in valid_symptom_ids:
            # Reset to first valid symptom
            st.session_state.current_symptom = 1
        
        show_symptom_analysis(engine, st.session_state.current_symptom)

def show_home_screen(symptoms: List[Dict], completed: int, total: int):
    """Display the home screen with all symptoms"""
    st.markdown("## 📋 All Symptom Presentations")
    
    # Progress summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Symptoms", total)
    with col2:
        st.metric("Completed", completed)
    with col3:
        st.metric("Remaining", total - completed)
    
    # Filter options
    st.markdown("### Filter by Category")
    categories = ["All"] + list(set([s.get('category', 'Unknown') for s in symptoms]))
    selected_category = st.selectbox("Category:", categories, key="category_filter")
    
    # Filter symptoms
    if selected_category == "All":
        filtered_symptoms = symptoms
    else:
        filtered_symptoms = [s for s in symptoms if s.get('category') == selected_category]
    
    # Display symptoms in a grid
    st.markdown("### Symptom List")
    
    # Create columns for better layout
    cols_per_row = 3
    for i in range(0, len(filtered_symptoms), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            if i + j < len(filtered_symptoms):
                symptom = filtered_symptoms[i + j]
                symptom_id = symptom['id']
                
                # Check if completed
                is_completed = symptom_id in st.session_state.completed_symptoms
                status_icon = "✅" if is_completed else "🔵"
                
                with col:
                    st.markdown(f"""
                    <div class="symptom-card">
                        <h4>{status_icon} {symptom['id']:02d}: {symptom['name']}</h4>
                        <p><strong>Category:</strong> {symptom.get('category', 'Unknown')}</p>
                        <p>{symptom.get('definition', 'No description available')[:100]}...</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Analyze {symptom['name']}", key=f"analyze_{symptom_id}"):
                        st.session_state.current_symptom = symptom_id
                        st.rerun()
    
    # Quick stats
    st.markdown("---")
    st.markdown("### Quick Statistics")
    
    # Category breakdown
    category_counts = {}
    for symptom in symptoms:
        category = symptom.get('category', 'Unknown')
        category_counts[category] = category_counts.get(category, 0) + 1
    
    st.markdown("**Symptoms by Category:**")
    for category, count in sorted(category_counts.items()):
        st.markdown(f"• {category}: {count} symptoms")
    
    # Completion progress
    st.markdown(f"**Overall Progress:** {completed}/{total} symptoms completed ({completed/total*100:.1f}%)")
    
    # Progress bar visualization
    if completed > 0:
        progress = completed / total * 100
        st.progress(progress / 100)

def show_symptom_analysis(engine: DiagnosticEngine, symptom_id: int):
    """Display the detailed symptom analysis interface"""
    
    # Validate symptom_id
    if not isinstance(symptom_id, int) or symptom_id <= 0:
        st.error(f"Invalid symptom ID: {symptom_id}")
        return
    
    # Get symptom details with error handling
    try:
        symptom_data = engine.get_symptom_details(symptom_id)
        if not symptom_data:
            # Debug information
            all_symptoms = engine.get_all_symptoms()
            available_ids = [s['id'] for s in all_symptoms] if all_symptoms else []
            
            st.error(f"Symptom {symptom_id} not found. Please select a different symptom.")
            if available_ids:
                st.info(f"Available symptom IDs: {sorted(available_ids)}")
                
                # Show suggestion for closest symptom
                closest_symptom = min(all_symptoms, key=lambda x: abs(x['id'] - symptom_id))
                st.info(f"Closest available symptom: {closest_symptom['id']}: {closest_symptom['name']}")
                
                if st.button(f"Go to {closest_symptom['id']}: {closest_symptom['name']}"):
                    st.session_state.current_symptom = closest_symptom['id']
                    st.rerun()
            else:
                st.warning("No symptoms available in database.")
            return
        
        # Success - show the symptom
        st.markdown(f"## {symptom_data.get('name', 'Unknown Symptom')}")
        st.markdown(f"**Category:** {symptom_data.get('category', 'Unknown')}")
        
        # Create tabs for different sections
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📖 Definition & Context", 
            "❓ Clarifying Questions", 
            "🔍 Differentials & Reasoning", 
            "📚 Educational Content", 
            "✅ Knowledge Check"
        ])
        
        with tab1:
            show_definition_tab(symptom_data)
        
        with tab2:
            show_questions_tab(engine, symptom_id, symptom_data)
        
        with tab3:
            show_differentials_tab(engine, symptom_id)
        
        with tab4:
            show_educational_tab(engine, symptom_id)
        
        with tab5:
            show_checkpoint_tab(engine, symptom_id)
        
        # Navigation buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("⬅️ Previous Symptom"):
                if symptom_id > 1:
                    st.session_state.current_symptom = symptom_id - 1
                    st.rerun()
        
        with col2:
            if st.button("🏠 Back to Home"):
                st.session_state.current_symptom = 0
                st.rerun()
        
        with col3:
            if st.button("Next Symptom ➡️"):
                all_symptoms = engine.get_all_symptoms()
                if all_symptoms:
                    max_id = max([s['id'] for s in all_symptoms])
                    if symptom_id < max_id:
                        st.session_state.current_symptom = symptom_id + 1
                        st.rerun()
    
    except Exception as e:
        st.error(f"Error loading symptom {symptom_id}: {str(e)}")
        st.info("Please try refreshing the page or selecting a different symptom.")
        
        # Fallback: show available symptoms
        try:
            all_symptoms = engine.get_all_symptoms()
            if all_symptoms:
                st.markdown("### Available Symptoms:")
                for symptom in all_symptoms[:10]:  # Show first 10
                    if st.button(f"{symptom['id']}: {symptom['name']}", key=f"fallback_{symptom['id']}"):
                        st.session_state.current_symptom = symptom['id']
                        st.rerun()
        except:
            st.warning("Unable to load symptom list. Please check database files.")

def show_definition_tab(symptom_data: Dict):
    """Display symptom definition and clinical context"""
    st.markdown("### Definition")
    st.write(symptom_data.get('definition', 'No definition available.'))
    
    st.markdown("### Clinical Significance")
    st.write(symptom_data.get('clinical_significance', 'No clinical significance information available.'))
    
    st.markdown("### Common Patient Descriptions")
    descriptions = symptom_data.get('common_descriptions', [])
    if descriptions:
        for desc in descriptions:
            st.markdown(f"• \"{desc}\"")
    else:
        st.write("No common descriptions available.")
    
    st.markdown("### Red Flags")
    red_flags = symptom_data.get('red_flags', [])
    if red_flags:
        for flag in red_flags:
            st.markdown(f'<div class="red-flag">⚠️ {flag}</div>', unsafe_allow_html=True)
    else:
        st.write("No specific red flags identified.")

def show_questions_tab(engine: DiagnosticEngine, symptom_id: int, symptom_data: Dict):
    """Display interactive clarifying questions"""
    st.markdown("### Clarifying Questions")
    st.write("Answer these questions to help generate differential diagnoses based on clinical evidence:")
    
    # Get questions for this symptom
    questions_data = engine.get_questions_for_symptom(symptom_id)
    
    if not questions_data or 'questions' not in questions_data:
        st.info("No specific questions available for this symptom yet. The diagnostic reasoning will be based on general clinical knowledge.")
        # Still show differentials based on typical presentation
        if st.button("Generate Differential Diagnosis"):
            # Use empty answers to get base differentials
            answers = {}
            differentials = engine.generate_differentials(symptom_id, answers)
            show_differentials_content(differentials)
        return
    
    # Initialize answers if not present
    if symptom_id not in st.session_state.user_answers:
        st.session_state.user_answers[symptom_id] = {}
    
    current_answers = st.session_state.user_answers[symptom_id]
    
    # Display questions
    for question in questions_data['questions']:
        question_id = question['id']
        question_text = question['question']
        question_type = question.get('type', 'multiple_choice')
        
        st.markdown(f'<div class="question-box">', unsafe_allow_html=True)
        st.markdown(f"**{question_text}**")
        
        if question_type == 'multiple_choice':
            options = [opt['text'] for opt in question['options']]
            selected_option = st.radio("Select an answer:", options, key=question_id)
            
            # Store the selected value
            for opt in question['options']:
                if opt['text'] == selected_option:
                    current_answers[question_id] = opt['value']
                    break
        
        elif question_type == 'checkbox':
            selected_options = []
            for option in question['options']:
                checkbox_key = f"{question_id}_{option['value']}"
                if st.checkbox(option['text'], key=checkbox_key):
                    selected_options.append(option['value'])
            current_answers[question_id] = selected_options
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Save answers to session state
    st.session_state.user_answers[symptom_id] = current_answers
    
    # Generate differentials button
    if st.button("🔍 Generate Differential Diagnosis", use_container_width=True):
        if current_answers:
            differentials = engine.generate_differentials(symptom_id, current_answers)
            show_differentials_content(differentials)
            
            # Mark as completed
            st.session_state.completed_symptoms.add(symptom_id)
        else:
            st.warning("Please answer at least one question before generating differentials.")

def show_differentials_tab(engine: DiagnosticEngine, symptom_id: int):
    """Display differential diagnoses and reasoning"""
    st.markdown("### Differential Diagnosis")
    
    # Check if answers exist
    if symptom_id in st.session_state.user_answers:
        answers = st.session_state.user_answers[symptom_id]
        if answers:
            differentials = engine.generate_differentials(symptom_id, answers)
            show_differentials_content(differentials)
        else:
            st.info("Please answer the clarifying questions to generate personalized differentials.")
    else:
        st.info("Complete the clarifying questions to generate differential diagnoses.")
        # Show base differentials
        differentials = engine.generate_differentials(symptom_id, {})
        show_differentials_content(differentials)

def show_differentials_content(differentials: List[Dict]):
    """Display differential diagnoses with color coding"""
    if not differentials:
        st.warning("No differential diagnoses available.")
        return
    
    st.markdown("### Ranked Differential Diagnoses")
    
    for i, diff in enumerate(differentials):
        likelihood = diff['final_likelihood']
        
        # Color code based on likelihood
        if likelihood >= 70:
            css_class = "differential-high"
            severity = "High Probability"
        elif likelihood >= 40:
            css_class = "differential-medium"
            severity = "Medium Probability"
        else:
            css_class = "differential-low"
            severity = "Lower Probability"
        
        with st.expander(f"{i+1}. {diff['diagnosis']} ({likelihood:.1f}% - {severity})"):
            st.markdown(f'<div class="{css_class}">', unsafe_allow_html=True)
            
            st.markdown(f"**Reasoning:** {diff['reasoning']}")
            
            if diff.get('key_features'):
                st.markdown("**Key Features to Look For:**")
                for feature in diff['key_features']:
                    st.markdown(f"• {feature}")
            
            if diff.get('adjustments'):
                st.markdown("**Answer-Based Adjustments:**")
                for adj in diff['adjustments']:
                    adj_direction = "↑" if adj['adjustment'] > 0 else "↓"
                    st.markdown(f"• {adj['question']}: {adj['answer']} {adj_direction}")
            
            if diff.get('next_steps'):
                st.markdown("**Next Steps:**")
                for step in diff['next_steps']:
                    st.markdown(f"→ {step}")
            
            st.markdown('</div>', unsafe_allow_html=True)

def show_educational_tab(engine: DiagnosticEngine, symptom_id: int):
    """Display educational content"""
    st.markdown("### Educational Content")
    
    educational_content = engine.get_educational_content(symptom_id)
    if not educational_content:
        st.info("Educational content not available for this symptom.")
        return
    
    # Symptom overview
    st.markdown("#### Symptom Overview")
    st.write(educational_content.get('definition', ''))
    
    # Red flags
    red_flags = educational_content.get('red_flags', [])
    if red_flags:
        st.markdown("#### 🚩 Red Flags")
        for flag in red_flags:
            st.markdown(f'<div class="red-flag">⚠️ {flag}</div>', unsafe_allow_html=True)
    
    # Investigations
    investigations = educational_content.get('investigations', [])
    if investigations:
        st.markdown("#### 🔬 Recommended Investigations")
        for inv in investigations:
            st.markdown(f"• {inv}")
    
    # Differential diagnosis details
    differentials = educational_content.get('differentials', [])
    if differentials:
        st.markdown("#### 📋 Differential Diagnosis Details")
        
        for diff in differentials:
            with st.expander(f"**{diff['diagnosis']}**"):
                # DSM-5 criteria
                dsm5 = diff.get('dsm5_criteria', {})
                if dsm5:
                    st.markdown("**DSM-5 Criteria:**")
                    if 'criteria_a' in dsm5:
                        st.markdown(f"• {dsm5['criteria_a']}")
                    if 'symptoms' in dsm5:
                        st.markdown("**Symptoms:**")
                        for symptom in dsm5['symptoms']:
                            st.markdown(f"  - {symptom}")
                
                # Clinical pearls
                pearls = diff.get('clinical_pearls', [])
                if pearls:
                    st.markdown("**Clinical Pearls:**")
                    for pearl in pearls:
                        st.markdown(f'<div class="clinical-pearl">💡 {pearl}</div>', unsafe_allow_html=True)
                
                # Common pitfalls
                pitfalls = diff.get('common_pitfalls', [])
                if pitfalls:
                    st.markdown("**Common Pitfalls:**")
                    for pitfall in pitfalls:
                        st.markdown(f"⚠️ {pitfall}")
                
                # Management
                management = diff.get('management', {})
                if management:
                    st.markdown("**Management Overview:**")
                    for key, value in management.items():
                        st.markdown(f"• *{key.replace('_', ' ').title()}:* {value}")

def show_checkpoint_tab(engine: DiagnosticEngine, symptom_id: int):
    """Display knowledge checkpoint quiz"""
    st.markdown("### Knowledge Check")
    
    checkpoint = engine.get_checkpoint_question(symptom_id)
    if not checkpoint:
        st.info("Checkpoint question not available for this symptom.")
        return
    
    st.markdown(f"**Question:** {checkpoint['question']}")
    
    # Display options
    user_answer = st.radio(
        "Select your answer:",
        [opt['text'] for opt in checkpoint['options']],
        key=f"checkpoint_{symptom_id}"
    )
    
    if st.button("Submit Answer"):
        # Check if answer is correct
        correct_answer = checkpoint['correct_answer']
        is_correct = user_answer == correct_answer
        
        if is_correct:
            st.success(f"✅ Correct! The answer is **{correct_answer}**.")
        else:
            st.error(f"❌ Incorrect. The correct answer is **{correct_answer}**.")
        
        # Show explanation
        st.markdown("**Explanation:**")
        st.write(checkpoint['explanation'])
        
        # Mark as completed if not already
        st.session_state.completed_symptoms.add(symptom_id)

if __name__ == "__main__":
    main()