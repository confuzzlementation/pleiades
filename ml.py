from sklearn.model_selection import StratifiedGroupKFold
import pandas as pd
import xgboost as xgb
import numpy as np
import matplotlib as mpl
from sklearn.model_selection import RandomizedSearchCV
import scipy.stats as stats
from sklearn.model_selection import train_test_split


data = pd.read_csv("data.csv")
groups = data["kepid"]

data = data.replace("CANDIDATE", 1).replace("FALSE POSITIVE", 0).drop("kepid", axis=1)


X, Y = data.iloc[:,:-1], data.iloc[:,-1]
X_train, X_test, Y_train, Y_test= train_test_split(X, Y, test_size=0.2, random_state=123)

sgkf = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=123)
folds = list(sgkf.split(X=X, y=Y, groups=groups))



dmatrix = xgb.DMatrix(data=X, label=Y, enable_categorical=True)
params = {  
            
            "max_depth": stats.randint(3, 100),
            'learning_rate': stats.uniform(0.01, 1.00),
            "alpha": stats.uniform(0.01, 0.99),
            'subsample': stats.uniform(0.5, 0.5),
            'n_estimators':stats.randint(1, 200),
            "colsample_bytree": stats.uniform(0.1, 0.9),
            "min_child_weight": stats.randint(1, 10),
            "lambda": stats.uniform(0.01, 0.99)
        }


xgb_model = xgb.XGBClassifier(objective="binary:logistic", early_stopping_rounds= 250)
random_search = RandomizedSearchCV(xgb_model, param_distributions=params, n_iter= 1000, cv=5, scoring="roc_auc", error_score="raise", random_state=123)

random_search.fit(X_train, Y_train, eval_set=[(X_test, Y_test)])


print("Best Hyperparameters:", random_search.best_params_)
print("Best Cross-Validation Score:", random_search.best_score_)