
import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load Dataset
data = pd.read_csv("dataset/student_data.csv")

# Input Features
X = data[
    [
        "attendance",
        "previous_marks",
        "study_hours",
        "assignment_score"
    ]
]

# Target Output
y = data["performance"]

# Split Dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create Random Forest Model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# Train Model
model.fit(X_train, y_train)

# Test Model
predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("Model Training Completed!")
print("Model Accuracy:", accuracy * 100, "%")

# Save Trained Model
with open("model/student_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Model Saved Successfully!")
