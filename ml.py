import optuna
from sklearn.model_selection import StratifiedGroupKFold, train_test_split
from sklearn.metrics import roc_auc_score
import pandas as pd
import xgboost as xgb
import warnings

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

    params = {
        "objective": "binary:logistic",
        "eval_metric": "auc",
        "verbosity": 0,
        "tree_method": "hist",
        "max_depth": trial.suggest_int("max_depth", 6, 60),
        "learning_rate": trial.suggest_float("learning_rate", 0.001, 0.05, log=True),
        "alpha": trial.suggest_float("alpha", 0.0, 5.0),
        "lambda": trial.suggest_float("lambda", 0.0, 5.0),
        "subsample": trial.suggest_float("subsample", 0.6, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.4, 1.0),
        "min_child_weight": trial.suggest_int("min_child_weight", 1, 6),
        "n_estimators": trial.suggest_int("n_estimators", 1, 3000),
        
        "gamma": trial.suggest_float("gamma", 0.0, 10.0)
    }

    aucs = []
    for train_idx, val_idx in sgkf.split(X_train, y_train, groups_train):
        X_tr, X_val = X_train.iloc[train_idx], X_train.iloc[val_idx]
        y_tr, y_val = y_train.iloc[train_idx], y_train.iloc[val_idx]

        model = xgb.XGBClassifier(**params)
        model.fit(
            X_tr, y_tr,
            eval_set=[(X_val, y_val)],
            verbose=False
        )

        preds = model.predict_proba(X_val)[:, 1]
        auc = roc_auc_score(y_val, preds)
        aucs.append(auc)

    return sum(aucs) / len(aucs)

study = optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=123), pruner=optuna.pruners.MedianPruner())
study.optimize(objective, n_trials= 200, n_jobs=-1, show_progress_bar=True)

print("Best parameters:", study.best_params)
print("Best CV AUC:", study.best_value)

best_params = study.best_params
final_model = xgb.XGBClassifier(**best_params, verbosity=0)
final_model.fit(X_train, y_train, verbose=2)
test_preds = final_model.predict_proba(X_test)[:, 1]
test_auc = roc_auc_score(y_test, test_preds)
print("Test AUC:", test_auc)

optuna.visualization.plot_optimization_history(study).show()
optuna.visualization.plot_param_importances(study).show()