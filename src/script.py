import pandas as pd
from sklearn.preprocessing import LabelEncoder
from kmodes.kmodes import KModes

def generate_user_data():
    # Ask user for input
    age = int(input("What is your age? "))
    weight = float(input("What is your weight in kg? "))
    height = float(input("What is your height in cm? "))
    systolic_bp = int(input("What is your systolic blood pressure (high BP in mmHg)? "))
    diastolic_bp = int(input("What is your diastolic blood pressure (low BP in mmHg)? "))
    gender = input("What is your gender (female/male)? ")
    while gender.lower() not in ['female', 'male']:
        gender = input("Invalid input. Please enter either 'female' or 'male': ")
    gender = 1 if gender.lower() == 'female' else 0
    cholesterol = int(input("What is your cholesterol level? Enter 1 for normal, 2 for above normal, or 3 for well above normal: "))
    glucose = int(input("What is your glucose level? Enter 1 for normal, 2 for above normal, or 3 for well above normal: "))
    physical_activity = int(input("Do you engage in physical activity? Enter 1 for yes or 0 for no: "))
    smoking = int(input("Do you smoke? Enter 1 for yes or 0 for no: "))
    alcohol = int(input("Do you consume alcohol? Enter 1 for yes or 0 for no: "))
    
    # Transforming the user input
    df_user = pd.DataFrame({
        'age': [age],
        'weight': [weight],
        'height': [height],
        'systolic': [systolic_bp],
        'diastolic': [diastolic_bp],
        'gender': [gender],
        'cholesterol': [cholesterol],
        'glucose': [glucose],
        'physical_activity': [physical_activity],
        'smoking': [smoking],
        'alcohol': [alcohol]
    })
    
    # Transforming the column AGE(measured in days) for Age_Bin
    # age_bin in quinquenium 5 years spam
    df_user['age_bin'] = pd.cut(df_user['age'], [0,20,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100], 
                              labels=['0-20', '20-30', '30-35', '35-40','40-45','45-50','50-55','55-60','60-65','65-70','70-75'])

    # Transforming the column bmi in Body Mass Index Classes (1 to 6)
    # Adding Body Mass Index
    df_user['bmi'] = df_user['weight']/((df_user['height']/100)**2)
    rating = []
    for row in df_user['bmi']:
        if row < 18.5 :    
            rating.append(1) #UnderWeight
        elif row > 18.5 and row  < 24.9:   
            rating.append(2) #NormalWeight
        elif row > 24.9 and row < 29.9:  
            rating.append(3) #OverWeight
        elif row > 29.9 and row < 34.9:  
            rating.append(4) #ClassObesity_1
        elif row > 34.9 and row < 39.9:  
            rating.append(5) #ClassObesity_2
        elif row > 39.9 and row < 49.9:  
            rating.append(6) #ClassObesity_3
        elif row > 49.9:  
            rating.append('Error') #Error
        else:
            rating.append('Not_Rated') #Not_Rated

    df_user['bmi_class'] = rating

    # Transforming the column systolic in Systolic Blood Pressure Classes (1 to 6)
    df_user['MAP'] = (df_user['systolic'] + 2*df_user['diastolic'])/3
    map_values = []
    for row in df_user['MAP']:
        if row < 69.9:
            map_values.append(1) #Low
        elif row > 69.9 and row < 79.9:
            map_values.append(2) #Normal
        elif row > 79.9 and row < 89.9:
            map_values.append(3) #Pre_Hypertension
        elif row > 89.9 and row < 99.9:
            map_values.append(4) #Stage_1_Hypertension
        elif row > 99.9 and row < 109.9:
            map_values.append(5) #Stage_2_Hypertension
        elif row > 109.9 and row < 119.9:
            map_values.append(6) #Hypertensive_Crisis
        elif row > 119.9:
            map_values.append(7) #Hypertensive_Emergency
        else:
            map_values.append('Not_Rated')

    df_user['MAP_class'] = map_values
    
    return df_user

generate_user_data()