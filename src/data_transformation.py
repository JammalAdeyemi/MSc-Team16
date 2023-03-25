import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class DataTransformation(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    def fit(self, X, y=None):
        return self
    def transform(self, X, y=None):
        X['Age'] = pd.cut(X['users_age'], [0,20,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100], 
                                  labels=['0-20', '20-30', '30-35', '35-40','40-45','45-50','50-55','55-60','60-65','65-70','70-75','75-80','80-85','85-90','90-95','95-100'])
        
        # Adding Body Mass Index
        X['bmi'] = X['users_weight']/((X['users_height']/100)**2)
        # Adding Body Mass Index Category
        rating = []
        for row in X['bmi']:
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
                rating.append('Not_Rated')
        # inserting Column
        X['BMI_Class'] = rating

        # creating a Column for MAP
        X['MAP'] = ((2* X['users_diastolic']) + X['users_systolic']) / 3

        #Creating Classes for MAP
        map_values = []
        for row in X['MAP']:
            if row < 69.9:    
                map_values.append(1) #Low
            elif row > 70 and row  < 79.9:   
                map_values.append(2)#Normal
            elif row > 79.9 and row < 89.9:  
                map_values.append(3)#Normal
            elif row > 89.9 and row < 99.9:  
                map_values.append(4)#Normal
            elif row > 99.9 and row < 109.9:  
                map_values.append(5)#High
            elif row > 109.9 and row < 119.9:  
                map_values.append(6)#Normal
            elif row > 119.9:  
                map_values.append(7)
                
            else:           
                map_values.append('Not_Rated')

        #inserting MAP_Class Column
        X['MAP_Class'] = map_values

        return X