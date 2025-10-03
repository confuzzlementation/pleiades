import pandas as pd
import xgboost as xgb
import numpy as np
import matplotlib as mpl


data = pd.read_csv("data.csv")
data = data.replace("CANDIDATE", 1).replace("FALSE POSITIVE", 0)


X, Y = data.iloc[:,:-1], data.iloc[:,-1]

# print(data)

#print(X.columns)


dmatrix = xgb.DMatrix(data=X, label=Y, enable_categorical=True)
params = {"objective":"reg:logistic", "max_depth":50, "learning_rate":0.50, "alpha":5}

results = xgb.cv(dtrain=dmatrix, params=params, nfold=5, num_boost_round=1000, early_stopping_rounds=500, 
                    metrics="auc", as_pandas=True, seed=123)

print(results["test-auc-mean"].iloc[-1])


