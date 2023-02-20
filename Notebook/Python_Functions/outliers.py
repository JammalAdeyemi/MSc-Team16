import seaborn as sns
import matplotlib.pyplot as plt

def check_outliers(df):
  num_col = df.select_dtypes(['int32', 'int64']).columns
  nCols = len(num_col)//3+1

  fig,ax = plt.subplots(nCols, 3, figsize = (30, 8*nCols))
  for i, col in enumerate(num_col):
        sns.boxplot(data=df, x=col, ax=ax[i//3][i%3])

  for i in range(len(num_col), 3*nCols):
        fig.delaxes(ax[i//3][i%3])

  plt.show()
   

