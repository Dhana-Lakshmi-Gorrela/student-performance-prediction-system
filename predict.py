import pickle
import pandas as pd

# Load Trained Model
with open("model/student_model.pkl", "rb") as file:
    model = pickle.load(file)


# Prediction Function
def predict_performance(attendance, previous_marks,
                        study_hours, assignment_score):

    data = pd.DataFrame([{
        "attendance": attendance,
        "previous_marks": previous_marks,
        "study_hours": study_hours,
        "assignment_score": assignment_score
    }])

    prediction = model.predict(data)

    return prediction[0]

# Test Prediction
result = predict_performance(
    attendance=85,
    previous_marks=75,
    study_hours=15,
    assignment_score=80
)

print("Predicted Student Performance:", result)