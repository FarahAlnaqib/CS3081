import os
from datetime import datetime

import pandas as pd
import streamlit as st


# ============================================================
# Page Setup
# ============================================================

st.set_page_config(
    page_title="A Multi-Factor Intelligent Major Recommendation System",
    layout="wide"
)

# ============================================================
# Custom CSS
# ============================================================

st.markdown("""
<style>
.main-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 0px;
}
.subtitle {
    font-size: 18px;
    color: #b8b8b8;
    margin-bottom: 25px;
}
.card {
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #333;
    background-color: #161a23;
    min-height: 230px;
}
.card h3 {
    margin-top: 0;
}
.rank {
    font-size: 28px;
    font-weight: bold;
    color: #9d7cff;
}
.score {
    font-size: 24px;
    font-weight: bold;
}
.section-title {
    font-size: 28px;
    font-weight: 700;
    margin-top: 30px;
}
.small-note {
    color: #a0a0a0;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# Header
# ============================================================

st.markdown(
    '<div class="main-title">A Multi-Factor Intelligent Major Recommendation System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Personalized major recommendations using logical, emotional, psychological, and job market factors.</div>',
    unsafe_allow_html=True
)


# ============================================================
# Helper Maps
# ============================================================

level_map = {
    "Low": 1,
    "Medium": 2,
    "High": 3
}

reverse_level_map = {
    1: "Low",
    2: "Medium",
    3: "High"
}

mbti_types = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]


# ============================================================
# Load Dataset
# ============================================================

@st.cache_data
def load_majors():
    return pd.read_excel("majors_dataset.xlsx", sheet_name="Majors")


majors = load_majors()


# ============================================================
# Utility Functions
# ============================================================

def get_gpa_level(gpa):
    if gpa >= 4.5:
        return 3
    elif gpa >= 3.5:
        return 2
    else:
        return 1


def calculate_score(student, major):
    logic = (
        student["Math_Skill"] * major["Math_Required"] +
        student["Programming_Skill"] * major["Programming_Required"] +
        student["ProblemSolving"] * major["ProblemSolving_Required"] +
        student["AnalyticalThinking"] * major["Analytical_Required"] +
        student["GPA_Level"] * major["GPA_Requirement"]
    ) / 5

    emotion = (
        student["Interest_Tech"] * major["Interest_Tech"] +
        student["Interest_Business"] * major["Interest_Business"] +
        student["Interest_Design"] * major["Interest_Design"] +
        student["Interest_Communication"] * major["Interest_Communication"] +
        student["Interest_Psychology"] * major["Interest_Psychology"]
    ) / 5

    psychology = 3 if student["MBTI_Type"] in str(major["Suitable_MBTI"]) else 1

    market = major["Market_Demand"]

    final_score = (
        0.40 * logic +
        0.30 * emotion +
        0.20 * psychology +
        0.10 * market
    )

    return round(final_score, 2), round(logic, 2), round(emotion, 2), psychology, market


def generate_explanation(student, major):
    reasons = []

    if student["GPA_Level"] >= major["GPA_Requirement"]:
        reasons.append("your academic level matches the major requirement")

    if student["Programming_Skill"] >= major["Programming_Required"] and major["Programming_Required"] >= 2:
        reasons.append("your programming skill fits this field")

    if student["Math_Skill"] >= major["Math_Required"] and major["Math_Required"] >= 2:
        reasons.append("your math skill supports this major")

    if student["AnalyticalThinking"] >= major["Analytical_Required"] and major["Analytical_Required"] >= 2:
        reasons.append("you have strong analytical thinking")

    if student["Interest_Tech"] >= 3 and major["Interest_Tech"] >= 2:
        reasons.append("you show high interest in technology")

    if student["Interest_Business"] >= 3 and major["Interest_Business"] >= 2:
        reasons.append("you show strong business interest")

    if student["Interest_Design"] >= 3 and major["Interest_Design"] >= 2:
        reasons.append("you show creative and design-oriented interests")

    if student["Interest_Communication"] >= 3 and major["Interest_Communication"] >= 2:
        reasons.append("you have strong communication interest")

    if student["Interest_Psychology"] >= 3 and major["Interest_Psychology"] >= 2:
        reasons.append("you are interested in psychology and people-oriented fields")

    if student["MBTI_Type"] in str(major["Suitable_MBTI"]):
        reasons.append("your MBTI type is compatible with this major")

    if major["Market_Demand"] >= 3:
        reasons.append("this major has high job market demand")

    major_name = major["Major_Name"]

    if not reasons:
        return f"We recommended **{major_name}** because it is the closest match among the available majors."

    top_reasons = reasons[:4]
    return f"We recommended **{major_name}** because " + ", ".join(top_reasons) + "."


def validate_student(student):
    warnings = []

    skills = [
        student["Math_Skill"],
        student["Programming_Skill"],
        student["ProblemSolving"],
        student["AnalyticalThinking"],
        student["Engagement"]
    ]

    interests = [
        student["Interest_Tech"],
        student["Interest_Business"],
        student["Interest_Design"],
        student["Interest_Communication"],
        student["Interest_Psychology"]
    ]

    if not str(student["Student_ID"]).strip():
        warnings.append("Student ID / Name is empty.")

    if student["GPA_Min"] < 3.0 and sum(1 for s in skills if s == 3) >= 4:
        warnings.append("Possible inconsistency: GPA is low but most skills are marked High.")

    if all(s == 3 for s in skills) and all(i == 3 for i in interests):
        warnings.append("Extreme input detected: all skills and interests are High. Please provide more realistic input.")

    if all(s == 1 for s in skills) and all(i == 1 for i in interests):
        warnings.append("Very low input detected: all skills and interests are Low. The system does not have enough strong signals.")

    if student["Interest_Tech"] == 3 and student["Programming_Skill"] == 1:
        warnings.append("Technology interest is High but programming skill is Low. Please review the input.")

    if student["Interest_Psychology"] == 3 and student["Interest_Communication"] == 1:
        warnings.append("Psychology interest is High but communication interest is Low. Please review the input.")

    return warnings


def save_excel_row(file_name, row_dict):
    new_row = pd.DataFrame([row_dict])

    try:
        if os.path.exists(file_name):
            old_data = pd.read_excel(file_name)
            final_data = pd.concat([old_data, new_row], ignore_index=True)
        else:
            final_data = new_row

        final_data.to_excel(file_name, index=False)
        return True, None

    except PermissionError:
        return False, f"Please close {file_name} if it is open, then try again."


def reset_recommendations():
    for key in ["top3", "explanation", "score_details"]:
        if key in st.session_state:
            del st.session_state[key]


# ============================================================
# Sidebar Input
# ============================================================

st.sidebar.header("👤 New Student Profile")
st.sidebar.caption("Enter the student information to generate personalized recommendations.")

student_id = st.sidebar.text_input("Student ID / Name", value="NEW_USER")

gpa = st.sidebar.slider(
    "GPA",
    min_value=2.0,
    max_value=5.0,
    value=4.0,
    step=0.1
)

st.sidebar.info("Scale used internally: Low = 1, Medium = 2, High = 3")

st.sidebar.subheader("Skills")

math_label = st.sidebar.selectbox("Math Skill", ["Low", "Medium", "High"], index=1)
programming_label = st.sidebar.selectbox("Programming Skill", ["Low", "Medium", "High"], index=1)
problem_label = st.sidebar.selectbox("Problem Solving", ["Low", "Medium", "High"], index=1)
analytical_label = st.sidebar.selectbox("Analytical Thinking", ["Low", "Medium", "High"], index=1)
engagement_label = st.sidebar.selectbox("Engagement", ["Low", "Medium", "High"], index=1)

st.sidebar.subheader("Interests")

interest_tech_label = st.sidebar.selectbox("Interest in Technology", ["Low", "Medium", "High"], index=1)
interest_business_label = st.sidebar.selectbox("Interest in Business", ["Low", "Medium", "High"], index=1)
interest_design_label = st.sidebar.selectbox("Interest in Design", ["Low", "Medium", "High"], index=1)
interest_comm_label = st.sidebar.selectbox("Interest in Communication", ["Low", "Medium", "High"], index=1)
interest_psy_label = st.sidebar.selectbox("Interest in Psychology", ["Low", "Medium", "High"], index=1)

st.sidebar.subheader("Personality")

mbti = st.sidebar.selectbox("MBTI Type", mbti_types)

student = {
    "Student_ID": student_id,
    "GPA_Min": gpa,
    "GPA_Max": gpa,
    "GPA_Level": get_gpa_level(gpa),
    "Math_Skill": level_map[math_label],
    "Programming_Skill": level_map[programming_label],
    "ProblemSolving": level_map[problem_label],
    "AnalyticalThinking": level_map[analytical_label],
    "Engagement": level_map[engagement_label],
    "Interest_Tech": level_map[interest_tech_label],
    "Interest_Business": level_map[interest_business_label],
    "Interest_Design": level_map[interest_design_label],
    "Interest_Communication": level_map[interest_comm_label],
    "Interest_Psychology": level_map[interest_psy_label],
    "MBTI_Type": mbti
}

profile_display = {
    "Student_ID": student_id,
    "GPA": gpa,
    "GPA_Level": reverse_level_map[student["GPA_Level"]],
    "Math_Skill": math_label,
    "Programming_Skill": programming_label,
    "ProblemSolving": problem_label,
    "AnalyticalThinking": analytical_label,
    "Engagement": engagement_label,
    "Interest_Tech": interest_tech_label,
    "Interest_Business": interest_business_label,
    "Interest_Design": interest_design_label,
    "Interest_Communication": interest_comm_label,
    "Interest_Psychology": interest_psy_label,
    "MBTI_Type": mbti
}


# ============================================================
# Student Profile Section
# ============================================================

st.markdown('<div class="section-title">👩‍🎓 Student Profile</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Student", student_id)
    st.metric("GPA", gpa)

with col2:
    st.metric("GPA Level", reverse_level_map[student["GPA_Level"]])
    st.metric("MBTI", mbti)

with col3:
    st.metric("Math", math_label)
    st.metric("Programming", programming_label)

with col4:
    top_interest_values = {
        "Technology": student["Interest_Tech"],
        "Business": student["Interest_Business"],
        "Design": student["Interest_Design"],
        "Communication": student["Interest_Communication"],
        "Psychology": student["Interest_Psychology"]
    }
    st.metric("Top Interest", max(top_interest_values, key=top_interest_values.get))
    st.metric("Engagement", engagement_label)

with st.expander("View full student profile"):
    st.dataframe(pd.DataFrame([profile_display]), use_container_width=True)


# ============================================================
# Validation / Adversarial Handling
# ============================================================

st.markdown('<div class="section-title">🛡️ Input Validation & Robustness</div>', unsafe_allow_html=True)

warnings = validate_student(student)

if warnings:
    reset_recommendations()
    st.error("Recommendation is blocked until the input issues are fixed.")
    st.warning("The system detected possible input issues:")
    for warning in warnings:
        st.write(f"- {warning}")
else:
    st.success("No input inconsistencies detected. The profile is ready for recommendation.")

with st.expander("Why validation matters"):
    st.write(
        "This module helps the system handle noisy, inconsistent, or extreme inputs. "
        "If validation issues are detected, the system blocks recommendation generation and feedback saving "
        "until the user corrects the input."
    )


# ============================================================
# Save Student Profile
# ============================================================

profile_row = {
    **profile_display,
    "Saved_At": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

col_save_profile, col_reset = st.columns([1, 1])

with col_save_profile:
    if st.button("💾 Save Student Profile"):
        if warnings:
            st.error("Student profile cannot be saved because validation issues were detected. Please correct the inputs first.")
        else:
            success, error = save_excel_row("new_students_profiles.xlsx", profile_row)
            if success:
                st.success("Student profile saved successfully in new_students_profiles.xlsx")
            else:
                st.error(error)

with col_reset:
    if st.button("🔄 Reset Recommendation Results"):
        reset_recommendations()
        st.info("Recommendation results have been reset.")


# ============================================================
# Recommendation Section
# ============================================================

st.markdown('<div class="section-title">🤖 Major Recommendation</div>', unsafe_allow_html=True)

st.write(
    "The system compares the student profile with Effat University majors, "
    "then ranks the best matches using a weighted scoring model."
)

st.caption("Final Score = 40% Logical + 30% Emotional + 20% Psychological + 10% Market Demand")

if st.button("🚀 Get Top 3 Recommendations"):

    if warnings:
        reset_recommendations()
        st.error("Recommendation blocked. Please correct the validation issues before continuing.")
        st.info("No recommendations will be generated until the profile becomes valid.")

    else:
        scores = []
        details = []

        for _, major in majors.iterrows():
            final_score, logic, emotion, psychology, market = calculate_score(student, major)

            scores.append({
                "Major_ID": major["Major_ID"],
                "College": major["College"],
                "Major_Name": major["Major_Name"],
                "Score": final_score,
                "Major_Row": major
            })

            details.append({
                "Major": major["Major_Name"],
                "Logic": logic,
                "Emotion": emotion,
                "Psychology": psychology,
                "Market": market,
                "Final Score": final_score
            })

        scores = sorted(scores, key=lambda x: x["Score"], reverse=True)
        top3 = scores[:3]

        st.session_state["top3"] = top3
        st.session_state["score_details"] = pd.DataFrame(details).sort_values(
            by="Final Score",
            ascending=False
        )
        st.session_state["explanation"] = generate_explanation(student, top3[0]["Major_Row"])


# ============================================================
# Results Display
# ============================================================

if "top3" in st.session_state and not warnings:
    top3 = st.session_state["top3"]

    st.success("Top 3 recommended majors generated successfully!")

    st.markdown('<div class="section-title">🏆 Top 3 Recommended Majors</div>', unsafe_allow_html=True)

    cols = st.columns(3)

    for index, rec in enumerate(top3):
        with cols[index]:
            match_label = "High Match" if rec["Score"] >= 5 else "Medium Match" if rec["Score"] >= 4 else "Possible Match"

            st.markdown(f"""
            <div class="card">
                <div class="rank">#{index + 1}</div>
                <h3>{rec["Major_Name"]}</h3>
                <p><b>College:</b><br>{rec["College"]}</p>
                <p class="score">Score: {rec["Score"]}</p>
                <p>{match_label}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">🧠 Explanation</div>', unsafe_allow_html=True)
    st.info(st.session_state["explanation"])

    with st.expander("View detailed scoring for all majors"):
        st.dataframe(st.session_state["score_details"], use_container_width=True)

    st.markdown('<div class="section-title">📝 Final Student Choice</div>', unsafe_allow_html=True)

    choice = st.selectbox(
        "Choose the final major",
        [
            top3[0]["Major_Name"],
            top3[1]["Major_Name"],
            top3[2]["Major_Name"],
            "Other"
        ]
    )

    if choice == "Other":
        final_choice = st.text_input("Type another major")
    else:
        final_choice = choice

    if st.button("✅ Save Feedback"):
        if warnings:
            st.error("Feedback cannot be saved because validation issues were detected. Please correct the inputs first.")
        elif not final_choice:
            st.error("Please enter a valid major.")
        else:
            feedback = {
                "Student_ID": student["Student_ID"],
                "GPA": student["GPA_Min"],
                "GPA_Level": reverse_level_map[student["GPA_Level"]],
                "Math_Skill": math_label,
                "Programming_Skill": programming_label,
                "ProblemSolving": problem_label,
                "AnalyticalThinking": analytical_label,
                "Engagement": engagement_label,
                "Interest_Tech": interest_tech_label,
                "Interest_Business": interest_business_label,
                "Interest_Design": interest_design_label,
                "Interest_Communication": interest_comm_label,
                "Interest_Psychology": interest_psy_label,
                "MBTI_Type": student["MBTI_Type"],
                "Recommended_1": top3[0]["Major_Name"],
                "Score_1": top3[0]["Score"],
                "Recommended_2": top3[1]["Major_Name"],
                "Score_2": top3[1]["Score"],
                "Recommended_3": top3[2]["Major_Name"],
                "Score_3": top3[2]["Score"],
                "Explanation": st.session_state["explanation"],
                "Final_User_Choice": final_choice,
                "Validation_Warnings": "None",
                "Saved_At": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            success, error = save_excel_row("recommendation_feedback.xlsx", feedback)

            if success:
                st.success("Feedback saved successfully in recommendation_feedback.xlsx")
            else:
                st.error(error)

elif warnings:
    st.info("Fix the validation issues above to enable recommendations and feedback saving.")


# ============================================================
# Footer
# ============================================================

st.divider()
st.caption(
    "CS3081 Artificial Intelligence Project | Knowledge-Based Recommendation Agent | "
    "Logic + Emotion + Psychology + Market Demand"
)