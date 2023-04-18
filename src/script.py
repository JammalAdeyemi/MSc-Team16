import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder
from kmodes.kmodes import KModes

# Load the existing data
old_data = pd.read_csv('cardio_data1')

# Ask user for input
age = int(input("What is your age? "))
weight = float(input("What is your weight in kg? "))
height = float(input("What is your height in cm? "))
systolic_bp = int(input("What is your systolic blood pressure (high BP in mmHg)? "))
diastolic_bp = int(input("What is your diastolic blood pressure (low BP in mmHg)? "))
gender = input("What is your gender (female/male)? ")
while gender.lower() not in ['female', 'male']:
    gender = input("Invalid input. Please enter either 'female' or 'male': ")
gender = 2 if gender.lower() == 'female' else 1
cholesterol = int(
    input("What is your cholesterol level? Enter 1 for normal, 2 for above normal, or 3 for well above normal: "))
glucose = int(input("What is your glucose level? Enter 1 for normal, 2 for above normal, or 3 for well above normal: "))
physical_activity = int(input("Do you engage in physical activity? Enter 1 for yes or 0 for no: "))
smoking = int(input("Do you smoke? Enter 1 for yes or 0 for no: "))
alcohol = int(input("Do you consume alcohol? Enter 1 for yes or 0 for no: "))

# Transforming the user input
df_user = pd.DataFrame({
    'age': [age],
    'gender': [gender],
    'height': [height],
    'weight': [weight],
    'systolic': [systolic_bp],
    'diastolic': [diastolic_bp],
    'cholesterol': [cholesterol],
    'glucose': [glucose],
    'smoke': [smoking],
    'alcohol': [alcohol],
    'active': [physical_activity]
})

# Concatenate the old data and the new user data
new_data = pd.concat([old_data, df_user], ignore_index=True)

# Write the new data to the CSV file
new_data.to_csv('cardio_data1', index=False)

def transform_data(data):
    # Transforming the column AGE(measured in days) for Age_Bin
    data['age_bin'] = pd.cut(data['age'], [0, 20, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100],
                                 labels=['0-20', '20-30', '30-35', '35-40', '40-45', '45-50', '50-55', '55-60', '60-65',
                                         '65-70', '70-75', '75-80', '80-85', '85-90', '90-95', '95-100'])

    # Transforming the column bmi in Body Mass Index Classes (1 to 6)
    data['bmi'] = data['weight'] / ((data['height'] / 100) ** 2)
    rating = []
    for row in data['bmi']:
        if row < 18.5:
            rating.append(1)  # UnderWeight
        elif row >= 18.5 and row < 24.9:
            rating.append(2)  # NormalWeight
        elif row >= 24.9 and row < 29.9:
            rating.append(3)  # OverWeight
        elif row >= 29.9 and row < 34.9:
            rating.append(4)  # ClassObesity_1
        elif row >= 34.9 and row < 39.9:
            rating.append(5)  # ClassObesity_2
        elif row >= 39.9 and row < 49.9:
            rating.append(6)  # ClassObesity_3
        elif row >= 49.9:
            rating.append('Error')  # Error
        else:
            rating.append('Not_Rated')  # Not_Rated
    data['BMI_Class'] = rating

    # Transforming the column systolic in Systolic Blood Pressure Classes (1 to 6)
    data['MAP'] = (data['systolic'] + 2 * data['diastolic']) / 3
    map_values = []
    for row in data['MAP']:
        if row < 69.9:
            map_values.append(1)  # Low
        elif row >= 69.9 and row < 79.9:
            map_values.append(2)  # Normal
        elif row >= 79.9 and row < 89.9:
            map_values.append(3)  # Pre_Hypertension
        elif row >= 89.9 and row < 99.9:
            map_values.append(4)  # Stage_1_Hypertension
        elif row >= 99.9 and row < 109.9:
            map_values.append(5)  # Stage_2_Hypertension
        elif row >= 109.9 and row < 119.9:
            map_values.append(6)  # Hypertensive_Crisis
        elif row >= 119.9:
            map_values.append(7)  # Hypertensive_Emergency
        else:
            map_values.append('Not_Rated')
    data['MAP_Class'] = map_values

    new_data = data[["gender", "age_bin", "BMI_Class", "MAP_Class", "cholesterol", "glucose", "smoke", "alcohol", "active"]]
    le = LabelEncoder()
    new_data = new_data.apply(le.fit_transform)
    km_huang = KModes(n_clusters=2, init="Huang", n_init=5, verbose=0)
    clusters = km_huang.fit_predict(new_data)
    # Inserting clusters in DataFrame
    new_data.insert(0, "Cluster", clusters, True)

    return new_data

# Load the trained model
model = pickle.load(open('../Models/voting_classifier.pkl', 'rb'))

# Load the new data data
df = pd.read_csv('cardio_data1.csv')

new_data = transform_data(df)

# Get the index of the new row
new_row_index = new_data.index[-1]

# Make a prediction
prediction_prob = model.predict_proba(new_data.loc[[new_row_index], :])

print("Your probability of having a cardiovascular disease is: {:.2f}%".format(prediction_prob[0][1] * 100))
