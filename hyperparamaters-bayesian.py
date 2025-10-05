import optuna
from sklearn.model_selection import StratifiedGroupKFold, train_test_split
from sklearn.metrics import roc_auc_score
import pandas as pd
import xgboost as xgb
import warnings
from optuna.integration import XGBoostPruningCallback
from xgboost.callback import EarlyStopping
import numpy as np


warnings.filterwarnings("ignore")
xgb.set_config(verbosity=0)
optuna.logging.set_verbosity(optuna.logging.WARNING)

data = pd.read_csv("data.csv")
groups = data["kepid"]
data = data.replace("CANDIDATE", 1).replace("FALSE POSITIVE", 0).drop("kepid", axis=1)

X, y = data.iloc[:, :-1], data.iloc[:, -1]
X_train, X_test, y_train, y_test, groups_train, groups_test = train_test_split(
    X, y, groups, test_size=0.2, random_state=123, stratify=y
)

def objective(trial):
    sgkf = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=123)
    growMethod = trial.suggest_categorical("grow_method", ["depthwise", "lossguide"])
    
    

    params = {
        "objective": "binary:logistic",
        "eval_metric": "auc",
        "tree_method": "hist",       
        "learning_rate": trial.suggest_float("learning_rate", 0.005, 0.20, log=True),
        "subsample": trial.suggest_float("subsample", 0.70, 1.00),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.70, 1.00),
        "min_child_weight": trial.suggest_int("min_child_weight", 1, 128),
        "reg_alpha": trial.suggest_float("reg_alpha", 1e-8, 100.0, log=True),
        "reg_lambda": trial.suggest_float("reg_lambda", 1e-8, 100.0, log=True),
        "gamma": trial.suggest_float("gamma", 1e-8, 20.0, log=True),
        "n_estimators": 10000,
        "max_bin": trial.suggest_int("max_bin", 512, 2048),
        "grow_policy": growMethod,
        "max_delta_step": trial.suggest_int("max_delta_step", 0, 16),
    }

    if(growMethod == "lossguide"):
        params["max_leaves"] = trial.suggest_int("max_leaves", 32, 1024)
    else:
        params["max_depth"] = trial.suggest_int("max_depth", 3, 18)

    aucs = []
    for train_idx, val_idx in sgkf.split(X_train, y_train, groups_train):
        X_tr, X_val = X_train.iloc[train_idx], X_train.iloc[val_idx]
        y_tr, y_val = y_train.iloc[train_idx], y_train.iloc[val_idx]

        pos = float(np.sum(y_tr == 1))
        neg = float(np.sum(y_tr == 0))
        if(pos != 0):
            params["scale_pos_weight"] = neg / pos
        else:
            params["scale_pos_weight"] = 1.0

        callbacks=[
            EarlyStopping(rounds=250, save_best=True),
            XGBoostPruningCallback(trial, "validation_0-auc")
        ]
        model = xgb.XGBClassifier(**params, n_jobs=1, callbacks=callbacks, verbosity=0)

        
        model.fit(
            X_tr, y_tr,
            eval_set=[(X_val, y_val)],
            verbose=2,
        )

        

        preds = model.predict_proba(X_val)[:, 1]
        auc = roc_auc_score(y_val, preds)
        aucs.append(auc)

    return sum(aucs) / len(aucs)

study = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=123, multivariate=True, group=True), pruner=optuna.pruners.SuccessiveHalvingPruner(reduction_factor=2, min_resource=150))
study.optimize(objective, n_trials= 50, show_progress_bar=True)

print("Best parameters:", study.best_params)
print("Best CV AUC:", study.best_value)

# best_params = study.best_params
# final_model = xgb.XGBClassifier(**best_params, verbosity=0)
# final_model.fit(X_train, y_train, verbose=2)
# test_preds = final_model.predict_proba(X_test)[:, 1]
# test_auc = roc_auc_score(y_test, test_preds)
# print("Test AUC:", test_auc)

optuna.visualization.plot_optimization_history(study).show()
optuna.visualization.plot_param_importances(study).show()