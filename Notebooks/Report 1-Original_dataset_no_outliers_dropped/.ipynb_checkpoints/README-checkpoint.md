# Notebook Performance Evaluation
In this project, I evaluated the performance of several machine learning models to predict a binary outcome. Since it was a `classification problem` I made use of `Accuracy`, `Precision`, `Recall`, and `F1-Score` as the performance metrics.

The evaluation was based on a `validation set` and a `test set`. The `validation set` was used during the training process to tune the models, while the `test set` was used to evaluate the final performance of the models.

As you may have notice from the title of the folder, I built the model without dropping any outliers in the dataset as I wanted to check the performance metrics to see the performance and that would decide what next to do.

The table shows that the `Adaboost classifier` and the `Gradientboost classifier` performed the best, with `accuracy scores` of `0.731` and `0.734` on the test set, respectively. These models also had high precision, recall, and F1-scores, indicating that they were effective at both correctly identifying positive cases and avoiding false positives.

The `Random-Forest classifier` had the lowest performance, with an `accuracy score` of `0.692` on both the `validation` and `test` sets.

We also used hyperparameter tuning techniques to optimize the `Adaboost` and `Gradientboost` classifiers. The best-performing `Adaboost` classifier had an accuracy score of `0.731` on the `test set`, while the best-performing `Gradientboost classifier` had an accuracy score of `0.736` on the test set.

Furthermore, we used a `voting classifier` to combine the predictions of several models. The `voting classifier` had an accuracy score of `0.733` on the test set, which was comparable to the performance of the individual Adaboost and Gradientboost classifiers.

In conclusion, the `Adaboost` and `Gradientboost` classifiers performed the best in predicting the binary outcome, with the best-performing models achieving an accuracy score of `0.731` and `0.736` on the test set, respectively. The benchmark performance metrics of the task is `0.73` which we've achieved, now we would go back to the datasets, drop any outliers, use our model and see the performance.




