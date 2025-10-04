from sklearn.model_selection import StratifiedGroupKFold
import pandas as pd
import xgboost as xgb
import numpy as np
import matplotlib as mpl


data = pd.read_csv("data.csv")
groups = data["kepid"]

data = data.replace("CANDIDATE", 1).replace("FALSE POSITIVE", 0).drop("kepid", axis=1)


X, Y = data.iloc[:,:-1], data.iloc[:,-1]
sgkf = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=123)
folds = list(sgkf.split(X=X, y=Y, groups=groups))



dmatrix = xgb.DMatrix(data=X, label=Y, enable_categorical=True)
params = {"objective":"reg:logistic", "max_depth":50, "learning_rate":0.50, "alpha":5}

results = xgb.cv(dtrain=dmatrix, params=params, nfold=5, num_boost_round=1000, early_stopping_rounds=500, 
                    metrics="auc", as_pandas=True, seed=123)

print(1-results["test-auc-mean"].iloc[-1])