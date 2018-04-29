import pandas as pd
import numpy as np
import pickle
from data_split_tune_utils import train_test_split, X_y_site_split, train_val_test_split
from predictiveImputer_mod import PredictiveImputer

np.random.seed(1)

data = pd.read_csv('../data/data_to_impute.csv')

train, val, test = train_val_test_split(data, train_prop = 0.7, test_prop = 0.15, site_var_name = 'site')
train1, train2 = train_test_split(train, train_prop = 0.34, site_var_name = 'site')

train1_x, train1_y, train1_sites = X_y_site_split(train1, y_var_name='MonitorData', site_var_name='site')
train2_x, train2_y, train2_sites = X_y_site_split(train2, y_var_name='MonitorData', site_var_name='site')
val_x, val_y, val_sites = X_y_site_split(val, y_var_name='MonitorData', site_var_name='site')
test_x, test_y, test_sites = X_y_site_split(test, y_var_name='MonitorData', site_var_name='site')

rf_imputer = PredictiveImputer(max_iter=10, initial_strategy='mean', f_model='RandomForest')
rf_imputer.fit(train1_x, max_features=15, n_estimators=50, n_jobs=-1, verbose=0, random_state=1)

train1_x_imp, train1_r2_scores_df = rf_imputer.transform(train1_x, evaluate = True, backup_impute_strategy = 'mean')
train1_r2_scores_df.columns = ['Train1_R2', 'Train1_num_missing']
train1_r2_scores_df.loc[max(train1_r2_scores_df.index)+1, :] = [np.average(train1_r2_scores_df.loc[:, 'Train1_R2'].values,\
                                                                   weights = train1_r2_scores_df.loc[:, 'Train1_num_missing'].values,\
                                                                   axis=0), np.mean(train1_r2_scores_df.loc[:, 'Train1_num_missing'].values)]
    
train2_x_imp, train2_r2_scores_df = rf_imputer.transform(train2_x, evaluate = True, backup_impute_strategy = 'mean')
train2_r2_scores_df.columns = ['Train2_R2', 'Train2_num_missing']
train2_r2_scores_df.loc[max(train2_r2_scores_df.index)+1, :] = [np.average(train2_r2_scores_df.loc[:, 'Train2_R2'].values,\
                                                                   weights = train2_r2_scores_df.loc[:, 'Train2_num_missing'].values,\
                                                                   axis=0), np.mean(train2_r2_scores_df.loc[:, 'Train2_num_missing'].values)]

val_x_imp, val_r2_scores_df = rf_imputer.transform(val_x, evaluate = True, backup_impute_strategy = 'mean')
val_r2_scores_df.columns = ['Val_R2', 'Val_num_missing']
val_r2_scores_df.loc[max(val_r2_scores_df.index)+1, :] = [np.average(val_r2_scores_df.loc[:, 'Val_R2'].values,\
                                                                   weights = val_r2_scores_df.loc[:, 'Val_num_missing'].values,\
                                                                   axis=0), np.mean(val_r2_scores_df.loc[:, 'Val_num_missing'].values)]

test_x_imp, test_r2_scores_df = rf_imputer.transform(test_x, evaluate = True, backup_impute_strategy = 'mean')
test_r2_scores_df.columns = ['Test_R2', 'Test_num_missing']
test_r2_scores_df.loc[max(test_r2_scores_df.index)+1, :] = [np.average(test_r2_scores_df.loc[:, 'Test_R2'].values,\
                                                                   weights = test_r2_scores_df.loc[:, 'Test_num_missing'].values,\
                                                                   axis=0), np.mean(test_r2_scores_df.loc[:, 'Test_num_missing'].values)]

cols = ['site', 'MonitorData'] + list(train1_x.columns)
train1_imp_df = pd.DataFrame(np.concatenate([train1_sites.values.reshape(len(train1_sites), -1),\
                                              train1_y.values.reshape(len(train1_y), -1),\
                                              train1_x_imp], axis=1),\
                                              columns = cols)

train2_imp_df = pd.DataFrame(np.concatenate([train2_sites.values.reshape(len(train2_sites), -1),\
                                              train2_y.values.reshape(len(train2_y), -1),\
                                              train2_x_imp], axis=1),\
                                              columns = cols)

val_imp_df = pd.DataFrame(np.concatenate([val_sites.values.reshape(len(val_sites), -1),\
                                              val_y.values.reshape(len(val_y), -1),\
                                              val_x_imp], axis=1),\
                                              columns = cols)

test_imp_df = pd.DataFrame(np.concatenate([test_sites.values.reshape(len(test_sites), -1),\
                                              test_y.values.reshape(len(test_y), -1),\
                                              test_x_imp], axis=1),\
                                              columns = cols)

var_df = pd.DataFrame(np.array(cols[2:] + ['Weighted_Mean_R2']).reshape(len(cols)-2+1, -1), columns = ['Variable'])
r2_scores_df = pd.concat([var_df, train1_r2_scores_df, train2_r2_scores_df, val_r2_scores_df, test_r2_scores_df], axis=1)

train_imp_df = pd.concat([train1_imp_df, train2_imp_df])
train_imp_df = train_imp_df.reset_index().sort_values(['site', 'index'])
train_imp_df.drop('index', axis=1, inplace=True)
train_imp_df.reset_index(inplace=True, drop=True)

r2_scores_df.to_csv('../data/r2_scoresV_rfImp.csv', index = False)
train_imp_df.to_csv('../data/trainV_rfImp.csv', index = False)
val_imp_df.to_csv('../data/valV_rfImp.csv', index = False)
test_imp_df.to_csv('../data/testV_rfImp.csv', index = False)
#pickle.dump(rf_imputer, open('rfV_imputer.pkl', 'wb'))