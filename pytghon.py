# Hospital Readmission Risk Prediction Project

# Step 1: Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

# Step 2: Load dataset
data_path = "diabetic_data.csv"  # Update with your dataset path
df = pd.read_csv(data_path)

# Step 3: Data cleaning (simplified example)
df = df.replace('?', np.nan)
df = df.dropna(axis=1, thresh=int(0.9 * len(df)))  # Drop columns with >10% missing
df = df.drop(['encounter_id', 'patient_nbr'], axis=1)

# Step 4: Feature engineering
df['readmitted'] = df['readmitted'].apply(lambda x: 1 if x == '<30' else 0)
df = pd.get_dummies(df, drop_first=True)

# Step 5: Split data
X = df.drop('readmitted', axis=1)
y = df['readmitted']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 6: Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Step 7: Evaluate
y_pred = model.predict(X_test)
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))
print("ROC AUC Score:", roc_auc_score(y_test, model.predict_proba(X_test)[:, 1]))

# Step 8: (Optional) Plot feature importance
feat_importances = pd.Series(model.feature_importances_, index=X.columns)
feat_importances.nlargest(10).plot(kind='barh')
plt.title('Top 10 Feature Importances')
plt.show()
