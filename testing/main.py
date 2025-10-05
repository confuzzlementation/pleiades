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

# print(data)
#print(X.columns)

dmatrix = xgb.DMatrix(data=X, label=Y, enable_categorical=True)
params = {
    "objective": "binary:logistic",
    "max_depth": 16,
    "learning_rate": 0.0065871201940497885,
    "alpha": 1.2833158015123136,
    "lambda": 0.7421885850676595,
    "gamma": 0.48389372530923047,
    "subsample": 0.8360643402670199,
    "colsample_bytree": 0.4911275665288193,
    "min_child_weight": 2
    # "n_estimators": 2576
}

results = xgb.cv(
    dtrain=dmatrix,
    params=params, nfold=5,
    num_boost_round=1000,
    early_stopping_rounds=500,
    metrics="auc",
    as_pandas=True,
    seed=123
)

print(results["test-auc-mean"].iloc[-1])