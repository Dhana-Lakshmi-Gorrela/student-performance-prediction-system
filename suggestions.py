
def get_suggestions(attendance, previous_marks,
                    study_hours, assignment_score):

    suggestions = []

    if attendance < 75:
        suggestions.append(
            "Improve attendance and attend classes regularly."
        )

    if previous_marks < 60:
        suggestions.append(
            "Revise previous topics and practice more questions."
        )

    if study_hours < 10:
        suggestions.append(
            "Increase study time to at least 2 hours daily."
        )

    if assignment_score < 60:
        suggestions.append(
            "Complete assignments regularly and improve accuracy."
        )

    if not suggestions:
        suggestions.append(
            "Excellent work! Maintain your current study routine."
        )

    return suggestions
