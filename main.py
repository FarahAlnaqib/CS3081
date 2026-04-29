import pandas as pd

students = pd.read_excel("student_dataset_30.xlsx")
majors = pd.read_excel("majors_dataset.xlsx", sheet_name="Majors")


def calculate_score(student, major):
    logic = (
        student["Math_Skill"] * major["Math_Required"] +
        student["Programming_Skill"] * major["Programming_Required"] +
        student["ProblemSolving"] * major["ProblemSolving_Required"] +
        student["AnalyticalThinking"] * major["Analytical_Required"]
    ) / 4

    emotion = (
        student["Interest_Tech"] * major["Interest_Tech"] +
        student["Interest_Business"] * major["Interest_Business"] +
        student["Interest_Design"] * major["Interest_Design"] +
        student["Interest_Communication"] * major["Interest_Communication"] +
        student["Interest_Psychology"] * major["Interest_Psychology"]
    ) / 5

    psych = 3 if student["MBTI_Type"] in str(major["Suitable_MBTI"]) else 1
    market = major["Market_Demand"]

    final_score = (0.4 * logic) + (0.3 * emotion) + (0.2 * psych) + (0.1 * market)

    return final_score


def generate_explanation(student, major):
    reasons = []

    if student["Programming_Skill"] >= 3:
        reasons.append("strong programming skills")
    if student["Math_Skill"] >= 3:
        reasons.append("strong mathematical ability")
    if student["AnalyticalThinking"] >= 3:
        reasons.append("strong analytical thinking")
    if student["Interest_Tech"] >= 3:
        reasons.append("high interest in technology")
    if student["Interest_Business"] >= 3:
        reasons.append("interest in business")
    if student["Interest_Design"] >= 3:
        reasons.append("creative and design-oriented interests")
    if student["Interest_Communication"] >= 3:
        reasons.append("strong communication interest")
    if student["Interest_Psychology"] >= 3:
        reasons.append("interest in psychology and people-oriented fields")
    if student["MBTI_Type"] in str(major["Suitable_MBTI"]):
        reasons.append("a personality type that matches this field")

    if len(reasons) == 0:
        return "This major fits your overall academic, emotional, and psychological profile."

    return "We recommend this major because you have " + ", ".join(reasons) + "."


results = []

for i, student in students.iterrows():
    student_scores = []

    for j, major in majors.iterrows():
        score = calculate_score(student, major)

        student_scores.append({
            "Major_ID": major["Major_ID"],
            "Major": major["Major_Name"],
            "College": major["College"],
            "Score": score,
            "Major_Row": major
        })

    sorted_scores = sorted(student_scores, key=lambda x: x["Score"], reverse=True)
    top3 = sorted_scores[:3]

    explanation = generate_explanation(student, top3[0]["Major_Row"])

    print("\n====================================")
    print(f"Student: {student['Student_ID']}")
    print("Top 3 Recommended Majors:")
    print(f"1. {top3[0]['Major']} - Score: {round(top3[0]['Score'], 2)}")
    print(f"2. {top3[1]['Major']} - Score: {round(top3[1]['Score'], 2)}")
    print(f"3. {top3[2]['Major']} - Score: {round(top3[2]['Score'], 2)}")
    print("Explanation:")
    print(explanation)

    # User feedback with validation
    while True:
        choice = input("Choose final major (1, 2, 3, or type another major): ").strip()

        if choice in ["1", "2", "3"]:
            break
        elif len(choice) > 3:
            break
        else:
            print("❌ Invalid input! Please enter 1, 2, 3 or a valid major name.")

    if choice == "1":
        final_choice = top3[0]["Major"]
    elif choice == "2":
        final_choice = top3[1]["Major"]
    elif choice == "3":
        final_choice = top3[2]["Major"]
    else:
        final_choice = choice

    results.append({
        "Student_ID": student["Student_ID"],
        "Recommended_1": top3[0]["Major"],
        "Score_1": round(top3[0]["Score"], 2),
        "Recommended_2": top3[1]["Major"],
        "Score_2": round(top3[1]["Score"], 2),
        "Recommended_3": top3[2]["Major"],
        "Score_3": round(top3[2]["Score"], 2),
        "Explanation": explanation,
        "Final_User_Choice": final_choice
    })


results_df = pd.DataFrame(results)
results_df.to_excel("final_recommendations_with_feedback.xlsx", index=False)

print("\n✅ Done!")
print("File saved as: final_recommendations_with_feedback.xlsx")