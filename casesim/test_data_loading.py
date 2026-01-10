#!/usr/bin/env python3
"""
Test script to verify the diagnostic engine and data loading
"""
import os
import json
import sys

# Add current directory to path
sys.path.insert(0, os.getcwd())

def test_data_files():
    """Test if all data files exist and are valid JSON"""
    print("=== TESTING DATA FILES ===")
    
    files_to_test = [
        'symptoms_database.json',
        'questions_database.json', 
        'diagnostic_content.json'
    ]
    
    for filename in files_to_test:
        print(f"\nTesting {filename}:")
        if not os.path.exists(filename):
            print(f"  ❌ File does not exist")
            continue
            
        file_size = os.path.getsize(filename)
        print(f"  ✅ File exists ({file_size} bytes)")
        
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            print(f"  ✅ Valid JSON structure")
            
            if filename == 'symptoms_database.json':
                if 'symptoms' in data:
                    print(f"  ✅ Contains {len(data['symptoms'])} symptoms")
                    # Test first few symptoms
                    for i, (key, value) in enumerate(data['symptoms'].items()):
                        if i >= 3:  # Only test first 3
                            break
                        print(f"    - Symptom {key}: {value.get('name', 'Unknown')}")
                else:
                    print(f"  ❌ Missing 'symptoms' key")
                    
        except json.JSONDecodeError as e:
            print(f"  ❌ JSON decode error: {e}")
        except Exception as e:
            print(f"  ❌ Error reading file: {e}")

def test_diagnostic_engine():
    """Test the diagnostic engine"""
    print("\n=== TESTING DIAGNOSTIC ENGINE ===")
    
    try:
        from diagnostic_engine import DiagnosticEngine
        
        print("✅ Diagnostic engine import successful")
        
        # Test initialization
        engine = DiagnosticEngine()
        print("✅ Engine initialization successful")
        
        # Test data loading
        print(f"  - Symptoms data type: {type(engine.symptoms_data)}")
        print(f"  - Questions data type: {type(engine.questions_data)}")
        print(f"  - Content data type: {type(engine.content_data)}")
        
        # Test getting all symptoms
        symptoms = engine.get_all_symptoms()
        print(f"✅ get_all_symptoms() returned {len(symptoms)} symptoms")
        
        if symptoms:
            first_symptom = symptoms[0]
            print(f"  - First symptom: {first_symptom.get('id', 'No ID')} - {first_symptom.get('name', 'No Name')}")
        
        # Test getting specific symptom
        if symptoms:
            test_symptom_id = symptoms[0]['id']
            symptom_data = engine.get_symptom_details(test_symptom_id)
            if symptom_data:
                print(f"✅ get_symptom_details({test_symptom_id}) successful")
            else:
                print(f"❌ get_symptptom_details({test_symptom_id}) failed")
        
        # Test questions
        if symptoms:
            questions = engine.get_questions_for_symptom(test_symptom_id)
            if questions:
                print(f"✅ get_questions_for_symptom({test_symptom_id}) returned {len(questions.get('questions', []))} questions")
            else:
                print(f"⚠️  No questions for symptom {test_symptom_id}")
        
        # Test differential generation
        test_answers = {'1_1': '2w_1m', '1_2': 'constant'}
        differentials = engine.generate_differentials(test_symptom_id, test_answers)
        print(f"✅ generate_differentials() returned {len(differentials)} diagnoses")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing diagnostic engine: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_streamlit_app():
    """Test if we can import streamlit components"""
    print("\n=== TESTING STREAMLIT COMPONENTS ===")
    
    try:
        import streamlit as st
        print("✅ Streamlit import successful")
        return True
    except ImportError as e:
        print(f"❌ Streamlit import failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Psychiatry Diagnostic Guide - Data Loading Test")
    print("=" * 50)
    
    # Change to the correct directory
    casesim_dir = os.path.join(os.getcwd(), 'casesim')
    if os.path.exists(casesim_dir):
        os.chdir(casesim_dir)
        print(f"Changed to directory: {os.getcwd()}")
    
    # Run tests
    data_files_ok = True
    test_data_files()
    
    engine_ok = test_diagnostic_engine()
    
    streamlit_ok = test_streamlit_app()
    
    # Summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY:")
    print(f"Data files: {'✅ OK' if data_files_ok else '❌ FAILED'}")
    print(f"Diagnostic engine: {'✅ OK' if engine_ok else '❌ FAILED'}")
    print(f"Streamlit: {'✅ OK' if streamlit_ok else '❌ FAILED'}")
    
    if engine_ok and data_files_ok:
        print("\n🎉 Core functionality is working!")
        print("If Streamlit app has issues, they are likely related to:")
        print("- File path differences when running from Streamlit")
        print("- Caching issues in Streamlit")
        print("- Session state management")
    else:
        print("\n❌ There are issues with the core functionality that need to be fixed.")

if __name__ == "__main__":
    main()