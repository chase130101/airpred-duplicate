import pandas as pd
import numpy as np
import xgboost as xgb
import sklearn.metrics
import pickle
#from matplotlib import pyplot
from data_split_tune_utils import X_y_site_split

train = pd.read_csv('../data/train_ridgeImp.csv')
test = pd.read_csv('../data/test_ridgeImp.csv')
#train = pd.read_csv('../data/train_rfImp.csv')
#test = pd.read_csv('../data/test_rfImp.csv')
train = train.dropna(axis=0)
test = test.dropna(axis=0)
train_x, train_y, train_sites = X_y_site_split(train, y_var_name='MonitorData', site_var_name='site')
test_x, test_y, test_sites = X_y_site_split(test, y_var_name='MonitorData', site_var_name='site')

best_hyperparams = pickle.load(open('best_xgboost_hyperparams.pkl', 'rb'))
xgboost = xgb.XGBRegressor(random_state=1, n_jobs=-1)
for key in list(hyperparam_dict.keys()):
    setattr(xgboost, key, best_hyperparams[key])
    
xgboost.fit(train_x, train_y)
test_pred_xgboost = xgboost.predict(test_x)
test_r2_xgboost = sklearn.metrics.r2_score(test_y, test_pred_xgboost)
print('Test R^2: ' + str(test_r2_xgboost))

#Variable importance plot
#xgb.plot_importance(model, max_num_features=20)
#pyplot.show()