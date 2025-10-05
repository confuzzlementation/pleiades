from sklearn.model_selection import StratifiedGroupKFold
import pandas as pd
import xgboost as xgb
import numpy as np
import matplotlib as mpl
import pickle as pkl

data = pd.read_csv("data.csv").drop("koi_time0", axis=1)
groups = data["kepid"]

data = data.replace("CANDIDATE", 1).replace("FALSE POSITIVE", 0).drop("kepid", axis=1)

X, Y = data.iloc[:, :-1], data.iloc[:, -1]
sgkf = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=123)
folds = list(sgkf.split(X=X, y=Y, groups=groups))

# print(data)
# print(X.columns)

dmatrix = xgb.DMatrix(data=X, label=Y)
params = {
    "objective": "binary:logistic",
    "max_depth": 16,
    "learning_rate": 0.0065871201940497885,
    "reg_alpha": 1.2833158015123136,
    "reg_lambda": 0.7421885850676595,
    "gamma": 0.48389372530923047,
    "subsample": 0.8360643402670199,
    "colsample_bytree": 0.4911275665288193,
    "min_child_weight": 2
}



results = xgb.cv(
    dtrain=dmatrix,
    params=params,
    folds=folds,
    num_boost_round=2576,
    early_stopping_rounds=150,
    metrics="error",
    as_pandas=True,
    seed=123,
)

print(results["test-error-mean"].iloc[-1])
