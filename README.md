# 🧠 Psychiatry Case Simulator

An interactive, multi-presentation case-based learning tool for psychiatry education, built with Streamlit. This application provides medical students, residents, and practicing clinicians with realistic psychiatric case scenarios across 20 different presentation categories.

## Features

- **20 Presentation Categories**: Comprehensive coverage of psychiatric presentations
- **200 Clinically Accurate Cases**: 10 cases per category, each with realistic clinical details
- **Progressive Disclosure**: Reveal clinical information step-by-step (History → MSE → Investigations → Risk Assessment → Diagnosis → Explanation → Management)
- **Interactive Learning**: Test your diagnostic skills with instant feedback
- **Dynamic Case Loading**: Cases loaded randomly from JSON files for varied learning
- **Clean, Responsive UI**: Modern interface optimized for learning

## Installation

### Requirements

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd casesim
```

2. Install dependencies:
```bash
pip install streamlit
```

That's it! The application has minimal dependencies.

## Running the Application

Launch the Streamlit app with:

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

## Project Structure

```
casesim/
├── app.py                          # Main Streamlit application
├── case_loader.py                  # Utility functions for loading cases
├── README.md                       # This file
├── LICENSE                         # CC0 1.0 Universal License
└── cases/                          # Case data directory (20 JSON files)
    ├── 01_mood_sad.json
    ├── 02_mood_elevated.json
    ├── 03_mood_fluctuations.json
    ├── 04_anxiety.json
    ├── 05_psychotic.json
    ├── 06_thought_form.json
    ├── 07_behavioral.json
    ├── 08_cognitive.json
    ├── 09_sleep.json
    ├── 10_somatic.json
    ├── 11_substance.json
    ├── 12_suicide.json
    ├── 13_trauma.json
    ├── 14_personality.json
    ├── 15_sexual.json
    ├── 16_child_adolescent.json
    ├── 17_geriatric.json
    ├── 18_emergency.json
    ├── 19_liaison.json
    └── 20_india_culture.json
```

## How to Use the Simulator

1. **Select a Category**: Use the sidebar to choose a presentation category (e.g., "Mood Sad", "Anxiety", "Psychotic")
2. **Review Demographics**: See patient age, sex, and presenting complaint
3. **Reveal Clinical Information**: Click buttons to progressively reveal:
   - Patient History (presenting complaint, duration, associated features, risk factors)
   - Mental State Examination (MSE)
   - Investigations (lab results, imaging, rating scales)
   - Suicide Risk Assessment
4. **Make Your Diagnosis**: Select from the dropdown list of diagnoses specific to the category
5. **Submit and Learn**: Get instant feedback on your diagnosis
6. **Read Explanation**: Understand the clinical reasoning and differential diagnosis
7. **Review Management**: Learn evidence-based treatment approaches
8. **Try Another Case**: Click "Load New Case" to practice with a different scenario from the same category

## Supported Categories

The simulator covers 20 major psychiatric presentation categories:

### Mood Disorders
1. **Sad/Low Mood** - Depression spectrum disorders
2. **Elevated/Expansive Mood** - Manic and hypomanic presentations
3. **Mood Fluctuations** - Rapid cycling, cyclothymia, and mood instability

### Anxiety Disorders
4. **Anxiety & Fear-Based Presentations** - GAD, panic disorder, phobias, social anxiety

### Psychotic Disorders
5. **Psychotic Presentations** - Schizophrenia, psychosis, delusional disorders
6. **Thought Form Disorders** - Formal thought disorder presentations

### Behavioral & Cognitive Disorders
7. **Behavioral Disturbances** - Aggression, conduct problems, impulsivity
8. **Cognitive & Memory Complaints** - Dementia, delirium, MCI

### Sleep & Somatic Disorders
9. **Sleep-Related Presentations** - Insomnia, hypersomnia, parasomnias
10. **Somatic & Medically Unexplained Symptoms** - Somatization, conversion, illness anxiety

### Substance Use Disorders
11. **Substance-Related Presentations** - Intoxication, withdrawal, substance use disorders

### Crisis & High-Risk Presentations
12. **Suicide & Self-Harm Presentations** - Suicidality assessment and management
13. **Stress-Related & Trauma Presentations** - PTSD, acute stress, adjustment disorders

### Personality & Sexual Disorders
14. **Personality & Interpersonal Problems** - Personality disorders
15. **Sexual & Gender-Related Presentations** - Gender dysphoria, sexual dysfunctions

### Specialized Populations
16. **Child & Adolescent Presentations** - ADHD, autism, conduct disorders
17. **Geriatric Psychiatry Presentations** - Late-life psychiatric disorders

### Emergency & Liaison Psychiatry
18. **Emergency Psychiatry Presentations** - Acute agitation, NMS, serotonin syndrome
19. **Liaison Psychiatry / Medical Interface** - Depression in medical illness, delirium

### Culture-Specific Syndromes
20. **India-Focused Culture-Bound Syndromes** - Dhat, possession states, Koro

## Adding New Cases

To add new cases to existing categories:

1. Open the relevant JSON file in the `cases/` directory
2. Add a new case object to the `cases` array with all required fields:

```json
{
  "diagnosis": "Name of Diagnosis",
  "age": 35,
  "sex": "Male",
  "presenting_complaint": "Chief complaint and symptoms",
  "duration": "Timeline of symptoms",
  "associated": "Associated features and symptoms",
  "risk_factors": "Risk factors present",
  "mse": "Mental State Examination findings",
  "investigations": "Investigation results",
  "suicide_risk": "Risk assessment",
  "explanation": "Clinical explanation and reasoning",
  "management": "Treatment plan"
}
```

3. Save the file - changes will be reflected immediately (no restart needed)

## Adding New Categories

To create a new category:

1. Create a new JSON file in the `cases/` directory following the naming convention: `##_category_name.json`

2. Structure your file as follows:

```json
{
  "category": "Full Category Name",
  "presentation": "Presentation Type Description",
  "cases": [
    {
      "diagnosis": "...",
      "age": 30,
      "sex": "Female",
      ...
    }
  ]
}
```

3. The category will automatically appear in the sidebar selector

## Case Data Schema

Each case must include all 12 required fields:

| Field | Type | Description |
|-------|------|-------------|
| `diagnosis` | string | The primary psychiatric diagnosis |
| `age` | integer | Patient age (18-80 typically) |
| `sex` | string | "Male", "Female", or "Other" |
| `presenting_complaint` | string | Chief complaint and presenting symptoms |
| `duration` | string | Timeline of current presentation |
| `associated` | string | Associated features, comorbid symptoms |
| `risk_factors` | string | Risk factors present in history |
| `mse` | string | Mental State Examination findings |
| `investigations` | string | Laboratory, imaging, and rating scale results |
| `suicide_risk` | string | Suicide risk assessment and stratification |
| `explanation` | string | Clinical reasoning, differential diagnosis, key features |
| `management` | string | Evidence-based treatment plan |

## Educational Features

### Progressive Disclosure
Cases use progressive disclosure to mimic real clinical practice:
- Start with limited information (demographics, presenting complaint)
- Reveal history and examination findings systematically
- Make diagnostic decisions before seeing explanations
- Learn management after understanding the diagnosis

### Instant Feedback
- Submit your diagnosis and receive immediate feedback
- Understand correct diagnosis with detailed explanations
- Learn evidence-based management strategies

### Diverse Case Mix
Each category includes 10 diverse cases featuring:
- Various ages (young adults through elderly)
- Different sexes
- Range of severities (mild, moderate, severe)
- Comorbidities and complications
- Different presentations of the same disorder

## Clinical Accuracy

All cases are:
- Clinically accurate and educationally appropriate
- Based on DSM-5-TR and ICD-11 diagnostic criteria
- Aligned with current evidence-based practice guidelines
- Suitable for MBBS/MD education and OSCE preparation
- Reviewed for realistic presentation and management

## Validation

The application includes built-in validation:
- All JSON files are validated on load
- Required fields are checked
- Age ranges are validated (0-120)
- Sex field validation
- Empty field detection

To manually validate all cases:
```python
from case_loader import load_case_by_category, validate_case_schema

# Test loading and validation
category = "01_mood_sad"
cases = load_case_by_category(category, return_all=True)
for case in cases:
    validate_case_schema(case)
```

## Technology Stack

- **Streamlit**: Web application framework
- **Python 3.8+**: Core programming language
- **JSON**: Case data storage format

## Contributing

To contribute cases or improvements:

1. Ensure cases are clinically accurate
2. Follow the required schema exactly
3. Include all 12 required fields
4. Use clear, educational language
5. Cite evidence-based management guidelines
6. Test cases in the application before submitting

## License

This project is released under the CC0 1.0 Universal License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

This simulator was created to support psychiatric education and training. All cases are fictional but based on realistic clinical scenarios.

## Support & Feedback

For issues, suggestions, or contributions, please open an issue in the repository.

---

**Disclaimer**: This tool is for educational purposes only and should not be used for actual clinical decision-making. Always consult appropriate clinical guidelines and seek supervision when managing real patients.

## Quick Start Guide

1. Install: `pip install streamlit`
2. Run: `streamlit run app.py`
3. Select a category from the sidebar
4. Work through a case step-by-step
5. Test your diagnostic skills
6. Learn from detailed explanations
7. Review evidence-based management

## Tips for Effective Learning

- **Try to formulate your diagnosis** before revealing the explanation
- **Consider the differential** for each presentation
- **Pay attention to risk factors** and how they influence diagnosis
- **Review the management plans** even for familiar diagnoses
- **Use the "New Case" button** to practice multiple cases in each category
- **Switch categories** to maintain a broad knowledge base

## Future Enhancements

Potential future features:
- Difficulty levels (beginner, intermediate, advanced)
- Progress tracking and performance analytics
- Timed case challenges
- Multiplayer collaborative diagnosis
- Customizable case parameters
- Export functionality for study notes
- Mobile-optimized interface

---

**Version**: 1.0.0  
**Last Updated**: January 2025  
**Cases**: 200 (20 categories × 10 cases each)
