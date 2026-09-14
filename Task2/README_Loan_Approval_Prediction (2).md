# Loan Approval Prediction using Logistic Regression

## Project Overview

**Loan Approval Prediction** is a machine learning classification project that predicts whether a loan application will be **Approved** or **Rejected**.

The project uses **Logistic Regression** and applicant details such as income, education, credit history, marital status, and property area.

The complete workflow is implemented in the Jupyter Notebook:

```text
Loan approval.ipynb
```

## Objectives

- Understand the loan approval dataset.
- Perform data preprocessing.
- Handle missing values.
- Convert categorical data into numerical form.
- Train a Logistic Regression model.
- Evaluate the model using different performance metrics.
- Predict loan approval for new applicant details.
- Save the trained model using Pickle.

## Technologies and Libraries

- Python
- NumPy
- Pandas
- Matplotlib
- Seaborn
- Scikit-learn
- Jupyter Notebook
- Pickle

## Dataset

The notebook loads the dataset using:

```python
df = pd.read_csv("train_csv.csv")
```

Therefore, the dataset file must be named:

```text
train_csv.csv
```

and placed in the same folder as the Jupyter Notebook.

### Dataset Features

The project uses the following applicant details:

| Feature | Description |
|---|---|
| Gender | Applicant gender |
| Married | Marital status |
| Dependents | Number of dependents |
| Education | Graduate or Not Graduate |
| Self_Employed | Self-employment status |
| ApplicantIncome | Applicant income |
| CoapplicantIncome | Co-applicant income |
| LoanAmount | Requested loan amount |
| Loan_Amount_Term | Loan repayment term |
| Credit_History | Credit history value |
| Property_Area | Urban, Semiurban, or Rural |

### Target Variable

```text
Loan_Status
```

Target values:

- `Y` – Loan Approved
- `N` – Loan Rejected

## Project Workflow

### 1. Import Libraries

The project imports NumPy, Pandas, Matplotlib, Seaborn, and required Scikit-learn modules.

### 2. Load the Dataset

```python
df = pd.read_csv("train_csv.csv")
```

### 3. Understand the Data

The following functions are used:

```python
df.head()
df.tail()
df.info()
df.describe()
df.shape
```

These functions help understand the dataset structure, data types, statistical information, and number of rows and columns.

### 4. Data Preprocessing

The `Loan_ID` column is removed because it is an identification column and is not useful for prediction.

```python
df.drop("Loan_ID", axis=1, inplace=True)
```

Missing values are filled using the mode of each column:

```python
for column in df.columns:
    df[column] = df[column].fillna(df[column].mode()[0])
```

### 5. Encoding

Categorical columns are converted into numerical values using `LabelEncoder`.

```python
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()

for column in df.select_dtypes(include="object").columns:
    df[column] = le.fit_transform(df[column])
```

### 6. Separate Input and Output

The input features are stored in `X`, and the target column is stored in `y`.

```python
X = df.drop("Loan_Status", axis=1)
y = df["Loan_Status"]
```

### 7. Split the Dataset

The dataset is divided into training and testing data.

```python
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)
```

- Training data: 80%
- Testing data: 20%
- Random state: 42
- Stratification: Used to preserve class distribution

## Machine Learning Algorithm

### Logistic Regression

Logistic Regression is a supervised machine learning algorithm used for classification.

In this project, it performs binary classification:

```text
Approved / Rejected
```

The model is created using:

```python
model = LogisticRegression(max_iter=1000)
```

The model is trained using:

```python
model.fit(X_train, y_train)
```

## Model Evaluation

The project evaluates the model using:

### 1. Accuracy

Accuracy measures the percentage of correctly predicted samples.

```python
accuracy_score(y_test, test_pred)
```

### 2. Confusion Matrix

The confusion matrix shows correct and incorrect predictions for both classes.

- True Negative: Correctly predicted rejected loan
- False Positive: Rejected loan predicted as approved
- False Negative: Approved loan predicted as rejected
- True Positive: Correctly predicted approved loan

### 3. Classification Report

The classification report displays:

- Precision
- Recall
- F1-score
- Support
- Accuracy

### 4. ROC Curve and ROC-AUC

The ROC curve is plotted using the predicted probability of the approved class.

The ROC-AUC score measures how well the model separates approved and rejected loan applications.

## Model Performance

The current notebook reports the following accuracy values:

| Metric | Result |
|---|---:|
| Training Accuracy | 79.84% |
| Testing Accuracy | 86.18% |

The testing accuracy is higher than the training accuracy for the current train-test split. The confusion matrix, classification report, and ROC-AUC score should also be considered for a complete evaluation.

## Prediction on New Applicant Data

The notebook accepts new applicant details using Python `input()` statements.

The user enters:

- Gender
- Married status
- Dependents
- Education
- Self-employed status
- Applicant income
- Co-applicant income
- Loan amount
- Loan amount term
- Credit history
- Property area

The entered values are converted into numerical form and passed to the trained model.

Example prediction logic:

```python
prediction = model.predict(input_data)[0]

if prediction == 1:
    print("Loan Approved")
else:
    print("Loan Rejected")
```

## Saving the Model

The trained Logistic Regression model is saved using Pickle:

```python
import pickle

with open("loan_approval_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Model saved successfully!")
```

The saved model file is:

```text
loan_approval_model.pkl
```

## Installation

Install the required libraries using:

```bash
pip install numpy pandas matplotlib seaborn scikit-learn jupyter
```

## How to Run

### Step 1: Download or clone the project

Keep the following files in one folder:

```text
Loan-Approval-Prediction/
│
├── Loan approval.ipynb
├── train_csv.csv
├── loan_approval_model.pkl
└── README.md
```

### Step 2: Start Jupyter Notebook

```bash
jupyter notebook
```

### Step 3: Open the Notebook

Open:

```text
Loan approval.ipynb
```

### Step 4: Run the Cells

Run the cells from top to bottom in the same order.

### Step 5: Enter Applicant Details

When the prediction cell runs, enter the applicant information in the input prompts.

## Expected Output

The model displays one of the following:

```text
Loan Approved
```

or

```text
Loan Rejected
```

## Important Notes

- The dataset file must be named `train_csv.csv`, or the file path in the notebook must be updated.
- The input column order must be the same as the training column order.
- The encoding used for new input data must match the encoding used during training.
- The model is a prediction aid and should not be used as the only basis for real financial decisions.
- For a production-ready project, a preprocessing pipeline and saved encoders should be used.

## Future Improvements

- Use a `Pipeline` and `ColumnTransformer` for safer preprocessing.
- Save the label encoders or preprocessing pipeline.
- Apply cross-validation.
- Tune Logistic Regression hyperparameters.
- Compare Logistic Regression with Decision Tree, Random Forest, and other classifiers.
- Handle class imbalance.
- Create a Streamlit web application with input boxes.
- Deploy the application online.
- Add more financial features for better prediction.

## Conclusion

This project demonstrates how Logistic Regression can be used to predict loan approval status. The workflow includes data understanding, preprocessing, encoding, model training, evaluation, new applicant prediction, and model saving.

The current model achieved **79.84% training accuracy** and **86.18% testing accuracy** on the reported train-test split. Further improvements can be made through better preprocessing, model tuning, and deployment.
