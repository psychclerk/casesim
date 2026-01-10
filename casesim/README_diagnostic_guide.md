# Psychiatry Resident Diagnostic Guide

A comprehensive Streamlit application designed to help psychiatry residents develop systematic diagnostic reasoning skills through **80 psychiatric symptom presentations**. This is a diagnostic decision-tree tool that guides residents through differential diagnosis for each symptom one at a time.

## 🎯 Core Concept

Instead of presenting full clinical cases, this app focuses on **one symptom at a time** and guides residents through a structured differential diagnosis process using:

- **Clarifying Questions** – Interactive questions to narrow down the differential
- **Symptom Characteristics** – Duration, severity, context, and associated features  
- **Diagnostic Reasoning** – Why certain diagnoses fit and why others don't
- **Educational Content** – DSM-5 criteria, clinical pearls, and common pitfalls
- **Knowledge Checkpoints** – Test understanding after each symptom

## 🏗️ Architecture

### File Structure
```
casesim/
├── diagnostic_guide_app.py          # Main Streamlit application
├── diagnostic_engine.py             # Core diagnostic logic and reasoning
├── symptoms_database.json           # Complete 80 symptoms with differentials
├── questions_database.json          # Clarifying questions for each symptom
├── diagnostic_content.json          # Educational content (DSM-5, pearls, etc.)
├── README_diagnostic_guide.md       # This documentation
└── LICENSE
```

### Technical Components

#### **diagnostic_guide_app.py** (~400 lines)
- **Home Screen**: Welcome, progress tracking, symptom list with filtering
- **Symptom Analysis Interface**: Tab-based layout with 5 sections:
  - 📖 Definition & Context
  - ❓ Clarifying Questions (Interactive)
  - 🔍 Differentials & Reasoning
  - 📚 Educational Content
  - ✅ Knowledge Check
- **Navigation**: Previous/next symptom, random selection, progress tracking
- **Responsive Design**: Works on desktop and mobile

#### **diagnostic_engine.py** (~300 lines)
- **Core Logic**: Differential diagnosis generation, likelihood calculation
- **Data Management**: Load and validate JSON databases
- **Question Processing**: Weight answers to adjust diagnostic probabilities
- **Educational Content**: DSM-5 criteria, clinical pearls, red flags
- **Progress Tracking**: Session state management for completed symptoms

#### **symptoms_database.json** (~4800 lines)
Complete database of all 80 psychiatric symptom presentations:

**Mood & Affect Presentations (12)**
1. Persistent Sadness
2. Loss of Interest (Anhedonia)
3. Feeling Hopeless/Worthless
4. Crying Spells
5. Fatigue/Low Energy
6. Excessive Happiness/Elevated Mood
7. Irritability
8. Increased Activity/Goal-Directed Behavior
9. Decreased Need for Sleep
10. Grandiosity/Inflated Self-Esteem
11. Mood Fluctuations/Cycling
12. Rapid Mood Swings

**Anxiety & Fear Presentations (8)**
13. Excessive Worry
14. Panic Attacks
15. Palpitations/Breathlessness
16. Fear of Dying/Losing Control
17. Avoidance Behavior
18. Phobic Fear (Social/Specific)
19. Obsessions
20. Compulsions

**Thought Disturbances (7)**
21. Hearing Voices
22. Delusions (Persecution/Reference/Grandeur)
23. Disorganized Speech
24. Suspiciousness
25. Flight of Ideas
26. Tangentiality
27. Thought Blocking

**Behavioral Disturbances (6)**
28. Aggression/Violence
29. Disinhibition
30. Social Withdrawal
31. Self-Neglect
32. Wandering Behavior
33. Impulsivity

**Cognitive & Memory (5)**
34. Forgetfulness
35. Disorientation
36. Poor Attention/Concentration
37. Difficulty Planning
38. Sudden Confusion

**Sleep Presentations (6)**
39. Insomnia (Initial)
40. Insomnia (Middle)
41. Insomnia (Terminal)
42. Hypersomnia
43. Daytime Sleepiness
44. Nightmares

**Somatic Presentations (5)**
45. Chest Pain (Medically Unexplained)
46. Abdominal Pain (No Clear Cause)
47. Headache with Anxiety
48. Multiple Physical Complaints
49. Pseudoseizures

**Substance-Related (4)**
50. Craving
51. Intoxication Signs
52. Withdrawal Signs
53. Relapse Triggers

**Suicide & Self-Harm (2)**
54. Suicidal Ideation
55. Deliberate Self-Harm

**Trauma & Stress (5)**
56. Flashbacks/Intrusive Memories
57. Hypervigilance
58. Avoidance of Trauma Reminders
59. Dissociative Symptoms
60. Conversion Symptoms

**Personality & Interpersonal (4)**
61. Emotional Instability
62. Impulsive Anger
63. Identity Disturbance
64. Fear of Abandonment

**Sexual & Gender (2)**
65. Sexual Dysfunction
66. Gender Dysphoria

**Child/Adolescent (4)**
67. Poor School Performance
68. Hyperactivity
69. Inattention
70. Oppositional Behavior

**Geriatric (3)**
71. Memory Loss (Aging)
72. Behavioral Changes
73. Late-Onset Psychosis

**Emergency (3)**
74. Acute Agitation
75. Acute Psychosis
76. Catatonia

**Liaison/Medical (2)**
77. Depression in Chronic Illness
78. Anxiety in Medical Illness

**Culture-Bound (India) (2)**
79. Possession-Like Experiences
80. Dhat Syndrome Concerns

#### **questions_database.json** (~1000 lines)
Interactive clarifying questions for each symptom with:
- Multiple choice and checkbox questions
- Diagnostic weighting for each answer
- Clinical reasoning behind each question
- Progressive questioning to narrow differentials

#### **diagnostic_content.json** (~2000 lines)
Educational material for each diagnosis including:
- **DSM-5 Criteria**: Complete diagnostic criteria
- **ICD-10 Codes**: International classification codes
- **Clinical Pearls**: What to look for, how to phrase questions
- **Common Pitfalls**: What doctors miss, diagnostic traps
- **Red Flags**: Warning signs requiring immediate action
- **Investigations**: What labs/imaging to order
- **Management Overview**: Treatment approaches (brief)

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Streamlit
- pandas

### Installation

1. **Clone or download the repository**
2. **Install dependencies**:
   ```bash
   pip install streamlit pandas
   ```

3. **Run the application**:
   ```bash
   streamlit run diagnostic_guide_app.py
   ```

4. **Open browser** to `http://localhost:8501`

### Usage

#### **For Residents:**
1. **Start with Home Screen**: Review all 80 symptoms
2. **Select a Symptom**: Choose from mood, anxiety, psychotic, etc.
3. **Answer Questions**: Fill out interactive clarifying questions
4. **Review Differentials**: See ranked diagnoses with reasoning
5. **Study Content**: Read DSM-5 criteria, pearls, pitfalls
6. **Test Knowledge**: Complete checkpoint quiz
7. **Track Progress**: Monitor completed symptoms

#### **Navigation Options:**
- **Sequential**: Go through symptoms 1-80 in order
- **Random**: Jump to random symptom for variety
- **Category**: Filter by symptom category
- **Progress**: Track completed symptoms

## 📚 Educational Features

### **Symptom Analysis Flow**

Each symptom follows a 5-step educational process:

#### **Step 1: Definition & Context**
- Clinical definition
- Why this symptom matters
- Common patient descriptions

#### **Step 2: Clarifying Questions**
Interactive questions like:
- "How long has the sadness been present?"
- "Is the sadness constant or episodic?"
- "What triggered the sadness?"
- "Can anything improve your mood temporarily?"

#### **Step 3: Differentials & Reasoning**
Ranked differential diagnoses with:
- **Likelihood percentages** (0-100%)
- **Key features** to look for
- **Clinical reasoning** why each diagnosis fits
- **Answer-based adjustments** from your responses
- **Next steps** for each diagnosis

#### **Step 4: Educational Content**
- **DSM-5/ICD-10 criteria** for top differentials
- **Clinical pearls** - What to look for in interview
- **Common pitfalls** - What doctors miss
- **Red flags** - Warning signs requiring action
- **Investigations** - What labs/imaging to order
- **Management overview** - Treatment approaches

#### **Step 5: Knowledge Check**
- Multiple choice question based on the symptom
- Immediate feedback with explanation
- Links to next symptom in sequence

### **Diagnostic Engine Features**

#### **Intelligent Differential Generation**
- **Base Likelihood**: Each diagnosis starts with clinical baseline
- **Answer Weights**: Your responses adjust probabilities
- **Clinical Reasoning**: Explains why each diagnosis fits
- **Safety Prioritization**: Red flags highlighted prominently

#### **Progressive Questioning**
- **6-10 questions** per symptom
- **Clinical relevance**: Each question narrows differentials
- **Weighted scoring**: Answers affect diagnostic likelihood
- **Real-time updates**: See probabilities change as you answer

## 🎯 Learning Objectives

### **For Residents**
1. **Develop systematic diagnostic reasoning**
2. **Learn symptom-based differential diagnosis**
3. **Master clarifying question techniques**
4. **Understand psychiatric diagnostic criteria**
5. **Recognize clinical pearls and pitfalls**
6. **Identify red flags and safety concerns**

### **For Educators**
1. **Track resident progress** through all 80 symptoms
2. **Assess diagnostic reasoning skills**
3. **Provide immediate feedback** via checkpoint questions
4. **Supplement clinical rotations** with systematic training
5. **Standardize diagnostic education** across programs

## 🔧 Technical Implementation

### **Data Structure**
Each symptom contains:
```json
{
  "id": 1,
  "name": "Persistent Sadness",
  "category": "Mood & Affect",
  "definition": "...",
  "clinical_significance": "...",
  "common_descriptions": ["..."],
  "differentials": [
    {
      "diagnosis": "Major Depressive Disorder",
      "likelihood": 85,
      "key_features": ["..."],
      "reasoning": "..."
    }
  ],
  "red_flags": ["..."],
  "investigations": ["..."]
}
```

### **Question Weighting System**
Each question answer affects diagnostic likelihood:
```json
{
  "question_id": "1_1",
  "question": "How long has sadness been present?",
  "options": [
    {"text": "Less than 2 weeks", "value": "lt_2w"},
    {"text": "2 weeks to 1 month", "value": "2w_1m"}
  ],
  "diagnostic_weights": {
    "Major Depressive Disorder": {
      "lt_2w": 20,
      "2w_1m": 70
    }
  }
}
```

### **Session State Management**
- **Progress Tracking**: Completed symptoms stored in session
- **Answer Persistence**: User responses saved between questions
- **Navigation State**: Current symptom and tab position
- **Random Access**: Jump to any symptom anytime

## 📖 Content Quality

### **Clinical Accuracy**
- All content based on **DSM-5** and **ICD-10** criteria
- **Evidence-based** diagnostic reasoning
- **Real-world** clinical scenarios
- **Safety-first** approach with prominent red flags

### **Educational Design**
- **Progressive difficulty**: Start simple, build complexity
- **Immediate feedback**: Right/wrong answers with explanations
- **Spaced repetition**: Random symptom selection
- **Multiple learning styles**: Visual, auditory, kinesthetic

### **Comprehensive Coverage**
- **All major psychiatric categories** represented
- **Cross-cultural considerations** (India-specific syndromes)
- **Age-specific presentations** (child, adult, geriatric)
- **Emergency situations** prioritized for safety

## 🚨 Safety Features

### **Red Flag Recognition**
Each symptom includes prominent red flags:
- **Suicide risk**: Immediate assessment required
- **Medical emergencies**: When to seek immediate help
- **Safety concerns**: Violence, self-harm, etc.

### **Clinical Decision Support**
- **Likelihood percentages**: Evidence-based probabilities
- **Next steps guidance**: What to do next clinically
- **Investigation recommendations**: What tests to order
- **Treatment approaches**: Initial management strategies

## 📊 Progress Tracking

### **Individual Metrics**
- **Completion status**: Which symptoms completed
- **Accuracy scores**: Knowledge check performance
- **Time tracking**: How long spent per symptom
- **Category progress**: Mood, anxiety, psychotic, etc.

### **Educational Analytics**
- **Weak areas identification**: Categories needing work
- **Strength building**: Build on successful areas
- **Random review**: Focus on missed or difficult symptoms

## 🔮 Future Enhancements

### **Planned Features**
1. **Performance Analytics**: Detailed progress reports
2. **Study Plans**: Customized learning paths
3. **Case Integration**: Link to full clinical cases
4. **Peer Comparison**: Anonymous benchmarking
5. **Mobile App**: Native iOS/Android versions
6. **Offline Mode**: Download for use without internet

### **Advanced Diagnostics**
1. **Machine Learning**: Improved differential generation
2. **Natural Language Processing**: Patient narrative analysis
3. **Image Recognition**: Visual symptom assessment
4. **Voice Analysis**: Speech pattern recognition

## 📄 License

This educational tool is provided under CC0 1.0 Universal License - see LICENSE file for details.

## 🤝 Contributing

This is an educational tool for psychiatry residents and educators. Contributions welcome for:
- Additional symptom content
- Question refinement
- Educational improvements
- Technical enhancements

## 📞 Support

For technical issues or educational content suggestions, please refer to the documentation or contact the development team.

---

**Built for psychiatry resident education with clinical accuracy and educational effectiveness as primary goals.**