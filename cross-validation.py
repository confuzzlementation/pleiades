from sklearn.model_selection import StratifiedGroupKFold
import pandas as pd
import xgboost as xgb
import numpy as np
import matplotlib as mpl

data = pd.read_csv("data.csv")
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
    "colsample_bytree": 0.10618800965831453,
    "gamma": 2.0757636574781273,
    "learning_rate": 0.2787769180988237,
    "max_delta_step": 48,
    "max_depth": 142,
    "min_child_weight": 1,
    "reg_alpha": 0.4812663415587328,
    "reg_lambda": 0.871666799399019,
    "subsample": 0.9978908750676403,
}

results = xgb.cv(
    dtrain=dmatrix,
    params=params,
    nfold=5,
    num_boost_round=629,
    early_stopping_rounds=150,
    metrics="auc",
    as_pandas=True,
    seed=123,
)

print(results["test-auc-mean"].iloc[-1])
