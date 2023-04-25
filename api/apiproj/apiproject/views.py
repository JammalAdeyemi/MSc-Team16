from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
import pickle
import os
import json
from types import SimpleNamespace
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from kmodes.kmodes import KModes
from lightgbm import LGBMClassifier

response_schema_dict = {
    "200": openapi.Response(
        description="Request Body",
        examples={
            "application/json": {              
                "age": 27,
                "weight": 70.2,
                "height": 20,
                "systolic": "Male",
                "diastolic": 0.34,
                "gender": 0.2,
                "cholesterol": 0,
                "glucose": 0,
                "physical_activity": 0,
                "smoking": 0,
                "alcohol": 0
            }
        }
    ),
    "400": openapi.Response(
        description="custom 205 description",
        examples={
            "application/json": {
                "205_key1": "205_value_1",
                "205_key2": "205_value_2",
            }
        }
    ),
}

@swagger_auto_schema(responses=response_schema_dict, method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'age': openapi.Schema(type=openapi.TYPE_INTEGER, description='What is your age?'),
        'weight': openapi.Schema(type=openapi.TYPE_NUMBER, description='What is your weight in kg?'),
        'height': openapi.Schema(type=openapi.TYPE_NUMBER, description='What is your height in cm?'),
        'systolic': openapi.Schema(type=openapi.TYPE_NUMBER, description='What is your systolic blood pressure (high BP in mmHg)?'),
        'diastolic': openapi.Schema(type=openapi.TYPE_NUMBER, description='What is your diastolic blood pressure (low BP in mmHg)?'),
        'gender': openapi.Schema(type=openapi.TYPE_INTEGER, description='0 for Male and 1 for Female'),
        'cholesterol': openapi.Schema(type=openapi.TYPE_NUMBER, description='What is your cholesterol level? Enter 1 for normal, 2 for above normal, or 3 for well above normal'),
        'glucose': openapi.Schema(type=openapi.TYPE_NUMBER, description='What is your glucose level? Enter 1 for normal, 2 for above normal, or 3 for well above normal'),
        'physical_activity': openapi.Schema(type=openapi.TYPE_INTEGER, description='Do you engage in physical activity? Enter 1 for yes or 0 for no'),
        'smoking': openapi.Schema(type=openapi.TYPE_INTEGER, description='Do you smoke? Enter 1 for yes or 0 for no:'),
        'alcohol': openapi.Schema(type=openapi.TYPE_INTEGER, description='Do you consume alcohol? Enter 1 for yes or 0 for no'),
    }
))



@api_view(['POST'])
def preditCvd(request, format=None):
    data = json.loads(request.body)
    
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'voting_classifier.pkl') 
    
    file = open(file_path, 'rb')
    p = pickle.load(file)   
    
    
    age = int(data['age'])
    weight = float(data['weight'])
    height = float(data['height'])
    systolic_bp = int(data['systolic'])
    diastolic_bp = int(data['diastolic'])
    gender = int(data['gender'])
    glucose = int(data['glucose'])
    physical_activity = int(data['physical_activity'])
    smoking = int(data['smoking'])
    alcohol = int(data['alcohol'])
    cholesterol = int(data['cholesterol'])

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
        'smoke': [smoking],
        'alcohol': [alcohol],
        'active': [physical_activity]
    })

    new_data = transform_user_data(df_user)  
    
    new_row_index = new_data.index[-1]

    # Make a prediction
    prediction_prob = p.predict_proba(new_data.loc[[new_row_index], :])
    
    prediction = prediction_prob[0][1] * 100        
        
    file.close()
    return Response({"result": prediction}, status = status.HTTP_201_CREATED)


def transform_user_data(df_user):
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, 'cardio_data1.csv') 
    old_data = pd.read_csv(file_path)
    
    data = pd.concat([old_data, df_user], ignore_index=True)
    
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