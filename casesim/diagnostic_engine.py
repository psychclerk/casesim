"""
Diagnostic Engine for Psychiatry Resident Training App
Handles core diagnostic logic, symptom data, and differential generation
"""

import json
import os
from typing import Dict, List, Tuple, Any, Optional
import random

class DiagnosticEngine:
    def __init__(self, symptoms_file: str = "symptoms_database.json",
                 questions_file: str = "questions_database.json",
                 content_file: str = "diagnostic_content.json"):
        """Initialize the diagnostic engine with data files"""
        self.symptoms_file = symptoms_file
        self.questions_file = questions_file
        self.content_file = content_file
        
        # Load all data
        self.symptoms_data = self._load_json(symptoms_file)
        self.questions_data = self._load_json(questions_file)
        self.content_data = self._load_json(content_file)
        
        # Initialize checkpoint questions
        self.checkpoint_questions = self._load_checkpoint_questions()
    
    def _load_json(self, file_path: str) -> Dict:
        """Load JSON data from file"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: File {file_path} not found. Using empty data.")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error loading {file_path}: {e}")
            return {}
    
    def get_all_symptoms(self) -> List[Dict]:
        """Get list of all symptoms with basic information"""
        if not self.symptoms_data.get("symptoms"):
            return []
        
        symptoms = []
        for symptom_id, symptom_data in self.symptoms_data["symptoms"].items():
            symptoms.append({
                "id": symptom_data.get("id"),
                "name": symptom_data.get("name"),
                "category": symptom_data.get("category"),
                "definition": symptom_data.get("definition", "")[:100] + "..." if len(symptom_data.get("definition", "")) > 100 else symptom_data.get("definition", "")
            })
        
        # Sort by ID
        symptoms.sort(key=lambda x: x["id"])
        return symptoms
    
    def get_symptom_details(self, symptom_id: int) -> Optional[Dict]:
        """Get full details for a specific symptom"""
        symptom_str = str(symptom_id)
        if not self.symptoms_data.get("symptoms") or symptom_str not in self.symptoms_data["symptoms"]:
            return None
        
        return self.symptoms_data["symptoms"][symptom_str]
    
    def get_questions_for_symptom(self, symptom_id: int) -> Optional[Dict]:
        """Get clarifying questions for a specific symptom"""
        symptom_str = str(symptom_id)
        if not self.questions_data.get("questions") or symptom_str not in self.questions_data["questions"]:
            return None
        
        return self.questions_data["questions"][symptom_str]
    
    def generate_differentials(self, symptom_id: int, answers: Dict[str, Any]) -> List[Dict]:
        """Generate ranked differentials based on answers"""
        symptom_data = self.get_symptom_details(symptom_id)
        if not symptom_data or "differentials" not in symptom_data:
            return []
        
        # Start with base differentials from symptom data
        differentials = []
        for diff in symptom_data["differentials"]:
            differential = {
                "diagnosis": diff["diagnosis"],
                "base_likelihood": diff["likelihood"],
                "key_features": diff.get("key_features", []),
                "reasoning": diff.get("reasoning", ""),
                "final_likelihood": diff["likelihood"],
                "adjustments": []
            }
            differentials.append(differential)
        
        # Apply answer-based adjustments
        questions_data = self.get_questions_for_symptom(symptom_id)
        if questions_data and "questions" in questions_data:
            for question in questions_data["questions"]:
                question_id = question["id"]
                if question_id in answers and question_id in question.get("diagnostic_weights", {}):
                    answer_value = answers[question_id]
                    weights = question["diagnostic_weights"]
                    
                    for differential in differentials:
                        diagnosis = differential["diagnosis"]
                        if diagnosis in weights and answer_value in weights[diagnosis]:
                            weight = weights[diagnosis][answer_value]
                            
                            # Adjust likelihood based on answer weight
                            adjustment = weight - 50  # Neutral is 50
                            differential["final_likelihood"] += adjustment * 0.3  # Scale factor
                            differential["adjustments"].append({
                                "question": question["question"],
                                "answer": self._get_answer_text(question, answer_value),
                                "adjustment": adjustment * 0.3
                            })
        
        # Ensure likelihood stays within bounds and sort
        for differential in differentials:
            differential["final_likelihood"] = max(0, min(100, differential["final_likelihood"]))
        
        # Sort by final likelihood
        differentials.sort(key=lambda x: x["final_likelihood"], reverse=True)
        
        # Add next steps and red flags
        for differential in differentials:
            differential["next_steps"] = self._get_next_steps(differential["diagnosis"])
            differential["clinical_pearls"] = self._get_clinical_pearls(differential["diagnosis"])
        
        return differentials
    
    def _get_answer_text(self, question: Dict, answer_value: str) -> str:
        """Get text for specific answer value"""
        for option in question.get("options", []):
            if option["value"] == answer_value:
                return option["text"]
        return answer_value
    
    def _get_next_steps(self, diagnosis: str) -> List[str]:
        """Get next diagnostic steps for a diagnosis"""
        content = self.content_data.get("diagnostic_content", {}).get(diagnosis, {})
        management = content.get("management", {})
        
        if "mania" in management:
            return ["Assess for current mania/hypomania", "Consider mood stabilizer", "Monitor for mixed features"]
        elif "first_line" in management:
            return [f"Treatment: {management['first_line']}", "Monitor response", "Consider combination therapy"]
        else:
            return ["Clinical assessment", "Monitor symptoms", "Consider referral"]
    
    def _get_clinical_pearls(self, diagnosis: str) -> List[str]:
        """Get clinical pearls for a diagnosis"""
        content = self.content_data.get("diagnostic_content", {}).get(diagnosis, {})
        pearls = content.get("clinical_pearls", [])
        return pearls[:3] if pearls else ["General clinical assessment", "Monitor treatment response", "Consider comorbidities"]
    
    def calculate_likelihood(self, symptom_id: int, answers: Dict[str, Any]) -> Dict[str, float]:
        """Calculate diagnostic likelihood percentages for all relevant diagnoses"""
        differentials = self.generate_differentials(symptom_id, answers)
        
        likelihoods = {}
        for diff in differentials:
            likelihoods[diff["diagnosis"]] = round(diff["final_likelihood"], 1)
        
        return likelihoods
    
    def get_checkpoint_question(self, symptom_id: int) -> Optional[Dict]:
        """Get checkpoint question for a symptom"""
        symptom_data = self.get_symptom_details(symptom_id)
        if not symptom_data:
            return None
        
        # Create a checkpoint question based on symptom differentials
        question_data = {
            "symptom_name": symptom_data.get("name"),
            "question": f"Based on the presentation of {symptom_data.get('name').lower()}, which diagnosis would be MOST likely in a typical case?",
            "options": [],
            "correct_answer": "",
            "explanation": ""
        }
        
        # Get top 3 differentials
        differentials = symptom_data.get("differentials", [])
        top_differentials = sorted(differentials, key=lambda x: x["likelihood"], reverse=True)[:3]
        
        # Set correct answer as most likely
        question_data["correct_answer"] = top_differentials[0]["diagnosis"] if top_differentials else ""
        
        # Create options
        for i, diff in enumerate(top_differentials):
            option_letter = chr(65 + i)  # A, B, C
            question_data["options"].append({
                "text": diff["diagnosis"],
                "correct": i == 0
            })
        
        # Add distractors if needed
        all_diagnoses = ["Major Depressive Disorder", "Persistent Depressive Disorder", "Adjustment Disorder", 
                        "Bipolar Disorder", "Panic Disorder", "Generalized Anxiety Disorder", 
                        "Borderline Personality Disorder", "PTSD", "Schizophrenia"]
        
        while len(question_data["options"]) < 4:
            diagnosis = random.choice([d for d in all_diagnoses if d not in [opt["text"] for opt in question_data["options"]]])
            question_data["options"].append({
                "text": diagnosis,
                "correct": False
            })
        
        # Shuffle options
        random.shuffle(question_data["options"])
        
        # Find correct answer after shuffle
        for option in question_data["options"]:
            if option["text"] == question_data["correct_answer"]:
                option["correct"] = True
                break
        
        question_data["explanation"] = f"The correct answer is {question_data['correct_answer']} because it is the most likely diagnosis based on the typical presentation of {symptom_data.get('name').lower()}."
        
        return question_data
    
    def load_diagnostic_content(self, diagnosis: str) -> Optional[Dict]:
        """Get diagnostic content for a specific diagnosis"""
        return self.content_data.get("diagnostic_content", {}).get(diagnosis)
    
    def get_educational_content(self, symptom_id: int) -> Dict:
        """Get comprehensive educational content for a symptom"""
        symptom_data = self.get_symptom_details(symptom_id)
        if not symptom_data:
            return {}
        
        educational_content = {
            "symptom_name": symptom_data.get("name"),
            "definition": symptom_data.get("definition", ""),
            "clinical_significance": symptom_data.get("clinical_significance", ""),
            "common_descriptions": symptom_data.get("common_descriptions", []),
            "red_flags": symptom_data.get("red_flags", []),
            "investigations": symptom_data.get("investigations", []),
            "differentials": []
        }
        
        # Get detailed content for each differential
        for diff in symptom_data.get("differentials", [])[:3]:  # Top 3
            diagnosis_content = self.load_diagnostic_content(diff["diagnosis"])
            if diagnosis_content:
                educational_content["differentials"].append({
                    "diagnosis": diff["diagnosis"],
                    "dsm5_criteria": diagnosis_content.get("dsm5_criteria", {}),
                    "clinical_pearls": diagnosis_content.get("clinical_pearls", []),
                    "common_pitfalls": diagnosis_content.get("common_pitfalls", []),
                    "red_flags": diagnosis_content.get("red_flags", []),
                    "investigations": diagnosis_content.get("investigations", []),
                    "management": diagnosis_content.get("management", {})
                })
        
        return educational_content
    
    def _load_checkpoint_questions(self) -> Dict:
        """Load checkpoint questions for all symptoms"""
        checkpoint_data = {}
        
        # Generate checkpoint questions for symptoms with data
        if self.symptoms_data.get("symptoms"):
            for symptom_id in self.symptoms_data["symptoms"].keys():
                question = self.get_checkpoint_question(int(symptom_id))
                if question:
                    checkpoint_data[symptom_id] = question
        
        return checkpoint_data
    
    def get_completed_symptoms(self) -> List[int]:
        """Get list of symptom IDs that have complete data"""
        completed = []
        if self.symptoms_data.get("symptoms"):
            for symptom_id in self.symptoms_data["symptoms"].keys():
                # Check if symptom has required data
                symptom_data = self.symptoms_data["symptoms"][symptom_id]
                if (symptom_data.get("name") and 
                    symptom_data.get("definition") and 
                    symptom_data.get("differentials")):
                    completed.append(int(symptom_id))
        
        return sorted(completed)
    
    def validate_data_integrity(self) -> Dict[str, List[str]]:
        """Validate that all data files are properly structured"""
        errors = {
            "symptoms": [],
            "questions": [],
            "content": []
        }
        
        # Validate symptoms data
        if not self.symptoms_data.get("symptoms"):
            errors["symptoms"].append("No symptoms data found")
        else:
            for symptom_id, symptom_data in self.symptoms_data["symptoms"].items():
                if not symptom_data.get("name"):
                    errors["symptoms"].append(f"Symptom {symptom_id}: Missing name")
                if not symptom_data.get("definition"):
                    errors["symptoms"].append(f"Symptom {symptom_id}: Missing definition")
                if not symptom_data.get("differentials"):
                    errors["symptoms"].append(f"Symptom {symptom_id}: Missing differentials")
        
        # Validate questions data
        if not self.questions_data.get("questions"):
            errors["questions"].append("No questions data found")
        else:
            for question_id, question_data in self.questions_data["questions"].items():
                if not question_data.get("questions"):
                    errors["questions"].append(f"Question set {question_id}: Missing questions")
        
        # Validate content data
        if not self.content_data.get("diagnostic_content"):
            errors["content"].append("No diagnostic content found")
        
        return errors