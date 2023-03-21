# ABOUT PROJECT

## Problem Statements
`Cardiovascular disease (CVD)` is a leading cause of mortality globally, and early identification and management of risk factors can significantly reduce the burden of CVD. The UCI heart dataset has been widely used in recent studies to develop predictive models for CVD. However, the limited size of this dataset and the lack of diversity in its sources raise concerns about the generalizability of the models developed using it. Additionally, joining different datasets from various repositories led to the removal of a substantial amount of data due to duplicates. To address these issues, we propose the use of a new dataset that includes objective medical information, results of medical examinations, and subjective information given by patients. Our objective is to develop a predictive model that can accurately predict the risk of CVD, expressed as a percentage, using this new dataset.

## Evaluation
The error metric used is the `F1-score`, which ranges from 0 (total failure) to 1 (perfect score). Hence, the closer one scores is to 1, the better the model.

1. `F1 Score`: A performance score that combines both precision and recall. It is a harmonic mean of these two variables. Formula is given as: 2*Precision*Recall/(Precision + Recall)
2. `Precision`: This is an indicator of the number of items correctly identified as positive out of total items identified as positive. Formula is given as: TP/(TP+FP)
3. `Recall / Sensitivity / True Positive Rate (TPR)`: This is an indicator of the number of items correctly identified as positive out of total actual positives. Formula is given as: TP/(TP+FN)

Where:

* TP = True Positive
* FP = False Positive
* TN = True Negative
* FN = False Negative

## Folders
We have 3 folders in the projects
1. `Data`: Contains all the datasets used in the project.
2. `Models`: Contains the final models that will be used in the web interface to make predictions on unseen data.
3. `Notebooks`: Contains three sub-folders, each with a self-explanatory name.

## Tools and Technologies
The project was implemented using Python and the following libraries:

1. `Python`, `Pandas`, and `Numpy` for data manipulation and analysis.
2. `Matplotlib` and `Seaborn` for data visualization.
3. `Pycaret` to automate the ML-Flow and get the general overview of what model to use on the dataset.
4. `Scikit-learn` libraries for training, and evaluating the machine learning model
5. `XGBOOST` and `LightGBM` for training our dataset

We hope that our project can contribute to the field of `CVD` risk prediction and encourage further research in this area.
