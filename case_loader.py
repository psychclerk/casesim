"""
Case Loader Utility Module

This module provides functions for loading and validating psychiatry case data
from JSON files organized by presentation category.
"""

import json
import logging
import random
from pathlib import Path
from typing import Dict, List, Optional, Union

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CASES_DIR = Path(__file__).parent / "cases"
REQUIRED_CASE_FIELDS = [
    "diagnosis", "age", "sex", "presenting_complaint", "duration",
    "associated", "risk_factors", "mse", "investigations",
    "suicide_risk", "explanation", "management"
]


def get_all_categories() -> List[str]:
    """
    Return list of all available presentation categories.
    
    Returns:
        List of category names (without .json extension)
    """
    if not CASES_DIR.exists():
        logger.error(f"Cases directory not found: {CASES_DIR}")
        return []
    
    try:
        category_files = sorted(CASES_DIR.glob("*.json"))
        categories = [f.stem for f in category_files]
        logger.info(f"Found {len(categories)} categories")
        return categories
    except Exception as e:
        logger.error(f"Error reading categories: {e}")
        return []


def load_category_metadata(category_name: str) -> Dict[str, str]:
    """
    Get category name and presentation type from category file.
    
    Args:
        category_name: Name of the category (with or without .json)
        
    Returns:
        Dictionary with 'category' and 'presentation' keys
        
    Raises:
        FileNotFoundError: If category file doesn't exist
        ValueError: If JSON is malformed or missing required fields
    """
    file_path = _find_category_file(category_name)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'category' not in data or 'presentation' not in data:
            raise ValueError(f"Category file missing 'category' or 'presentation' field")
        
        return {
            'category': data['category'],
            'presentation': data['presentation']
        }
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {file_path}: {e}")
        raise ValueError(f"Invalid JSON in category file: {e}")
    except Exception as e:
        logger.error(f"Error loading category metadata: {e}")
        raise


def load_case_by_category(category_name: str, return_all: bool = False) -> Union[Dict, List[Dict]]:
    """
    Load random case or all cases from a category.
    
    Args:
        category_name: Name of the category (with or without .json)
        return_all: If True, return all cases; if False, return random case
        
    Returns:
        Single case dict (if return_all=False) or list of case dicts (if return_all=True)
        
    Raises:
        FileNotFoundError: If category file doesn't exist
        ValueError: If JSON is malformed or no cases found
    """
    file_path = _find_category_file(category_name)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'cases' not in data or not data['cases']:
            raise ValueError(f"No cases found in category: {category_name}")
        
        cases = data['cases']
        
        # Validate all cases
        for idx, case in enumerate(cases):
            try:
                validate_case_schema(case)
            except ValueError as e:
                logger.warning(f"Case {idx} in {category_name} failed validation: {e}")
        
        if return_all:
            return cases
        else:
            return random.choice(cases)
            
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {file_path}: {e}")
        raise ValueError(f"Invalid JSON in category file: {e}")
    except Exception as e:
        logger.error(f"Error loading cases: {e}")
        raise


def validate_case_schema(case: Dict) -> bool:
    """
    Validate that a case follows the required schema.
    
    Args:
        case: Case dictionary to validate
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If case is missing required fields or has invalid values
    """
    if not isinstance(case, dict):
        raise ValueError("Case must be a dictionary")
    
    # Check for missing fields
    missing_fields = [field for field in REQUIRED_CASE_FIELDS if field not in case]
    if missing_fields:
        raise ValueError(f"Case missing required fields: {missing_fields}")
    
    # Check for empty required fields
    empty_fields = [field for field in REQUIRED_CASE_FIELDS 
                   if not case[field] or str(case[field]).strip() == ""]
    if empty_fields:
        raise ValueError(f"Case has empty required fields: {empty_fields}")
    
    # Validate age is a number
    try:
        age = int(case['age'])
        if age < 0 or age > 120:
            raise ValueError(f"Age must be between 0 and 120, got {age}")
    except (ValueError, TypeError):
        raise ValueError(f"Age must be a valid integer, got {case['age']}")
    
    # Validate sex field
    valid_sex_values = ['Male', 'Female', 'Other']
    if case['sex'] not in valid_sex_values:
        raise ValueError(f"Sex must be one of {valid_sex_values}, got {case['sex']}")
    
    return True


def _find_category_file(category_name: str) -> Path:
    """
    Internal helper to locate category JSON file.
    
    Args:
        category_name: Name of the category (with or without .json)
        
    Returns:
        Path to the category file
        
    Raises:
        FileNotFoundError: If category file doesn't exist
    """
    if not CASES_DIR.exists():
        raise FileNotFoundError(f"Cases directory not found: {CASES_DIR}")
    
    # Handle both with and without .json extension
    if category_name.endswith('.json'):
        file_path = CASES_DIR / category_name
    else:
        file_path = CASES_DIR / f"{category_name}.json"
    
    if not file_path.exists():
        raise FileNotFoundError(f"Category file not found: {file_path}")
    
    return file_path
