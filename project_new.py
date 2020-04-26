from sklearn.linear_model import ElasticNet, Lasso
from sklearn.linear_model import BayesianRidge, LassoLarsIC
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.kernel_ridge import KernelRidge
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.base import RegressorMixin, clone
from sklearn.model_selection import KFold, cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import norm
from sklearn.preprocessing import StandardScaler
from scipy import stats
import warnings
warnings.filterwarnings('ignore')
from scipy.stats import norm, skew
import pickle

class AveragingModels(BaseEstimator, RegressorMixin, TransformerMixin):
    def __init__(self, models):
        self.models = models
    # We define clones of the original models to fit the data in
    def fit(self, X, y):
        self.models_ = [clone(x) for x in self.models]
        # Train cloned base models
        for model in self.models_:
            model.fit(X, y)
        return self
    
    # Now we do the predictions for cloned models and average them
    def predict(self, X):
        predictions = np.column_stack([model.predict(X) for model in self.models_])
        return np.mean(predictions, axis=1)


median02 = 0

def get_median():
    global median02
    return median02

def main(filename = './data/test.csv'):
    train = pd.read_csv('./data/train.csv')
    test = pd.read_csv(filename)

    train_ID = train['Id']
    test_ID = test['Id']

    train.drop("Id", axis = 1, inplace = True)
    test.drop("Id", axis = 1, inplace = True)

    train = train.drop(train[(train['GrLivArea']>4000) &
                             (train['SalePrice']<300000)].index)
                             
    global median02
    median02 = np.median(train["SalePrice"])

    train["SalePrice"] = np.log1p(train["SalePrice"])

    ntrain = train.shape[0]
    ntest = test.shape[0]
    y_train = train.SalePrice.values
    all_data = pd.concat((train, test)).reset_index(drop=True)
    all_data.drop(['SalePrice'], axis=1, inplace=True)

    all_data["PoolQC"] = all_data["PoolQC"].fillna("None")

    all_data["MiscFeature"] = all_data["MiscFeature"].fillna("None")
    all_data["Alley"] = all_data["Alley"].fillna("None")
    all_data["Fence"] = all_data["Fence"].fillna("None")
    all_data["FireplaceQu"] = all_data["FireplaceQu"].fillna("None")

    for col in ('GarageType', 'GarageFinish', 'GarageQual', 'GarageCond'):
        all_data[col] = all_data[col].fillna('None')

    for col in ('GarageYrBlt', 'GarageArea', 'GarageCars'):
        all_data[col] = all_data[col].fillna(0)

    for col in ('BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF','TotalBsmtSF',
            'BsmtFullBath', 'BsmtHalfBath'):
        all_data[col] = all_data[col].fillna(0)

    for col in ('BsmtQual', 'BsmtCond', 'BsmtExposure', 'BsmtFinType1',
            'BsmtFinType2'):
        all_data[col] = all_data[col].fillna('None')

    all_data["MasVnrType"] = all_data["MasVnrType"].fillna("None")
    all_data["MasVnrArea"] = all_data["MasVnrArea"].fillna(0)

    all_data["LotFrontage"] = (all_data
                           .groupby("Neighborhood")["LotFrontage"]
                           .transform(lambda x: x.fillna(x.median())))

    all_data['MSZoning'] = (all_data['MSZoning']
                        .fillna(all_data['MSZoning']
                                .mode()[0]))

    all_data["Functional"] = all_data["Functional"].fillna("Typ")

    all_data['Electrical'] = (all_data['Electrical']
                          .fillna(all_data['Electrical']
                                  .mode()[0]))

    all_data['KitchenQual'] = (all_data['KitchenQual']
                           .fillna(all_data['KitchenQual']
                                   .mode()[0]))
    all_data['Exterior1st'] = (all_data['Exterior1st']
                           .fillna(all_data['Exterior1st']
                                   .mode()[0]))
    all_data['Exterior2nd'] = (all_data['Exterior2nd']
                           .fillna(all_data['Exterior2nd']
                                   .mode()[0]))

    all_data['SaleType'] = (all_data['SaleType']
                        .fillna(all_data['SaleType']
                                .mode()[0]))

    all_data['MSSubClass'] = all_data['MSSubClass'].fillna("None")

    all_data = all_data.drop(['Utilities'], axis=1)

    all_data['MSSubClass'] = all_data['MSSubClass'].apply(str)
################################################
# all_data['MSSubClass'] = all_data['MSSubClass'].astype(str)
    all_data['OverallCond'] = all_data['OverallCond'].astype(str)
    all_data['YrSold'] = all_data['YrSold'].astype(str)
    all_data['MoSold'] = all_data['MoSold'].astype(str)

    
    cols = ('FireplaceQu', 'BsmtQual', 'BsmtCond', 'GarageQual',
        'GarageCond', 'ExterQual', 'ExterCond','HeatingQC',
        'PoolQC', 'KitchenQual', 'BsmtFinType1', 'BsmtFinType2',
        'Functional', 'Fence', 'BsmtExposure', 'GarageFinish',
        'LandSlope','LotShape', 'PavedDrive', 'Street', 'Alley',
        'CentralAir', 'MSSubClass', 'OverallCond', 'YrSold', 'MoSold')

    for c in cols:
        lbl = LabelEncoder()
        lbl.fit(list(all_data[c].values))
        all_data[c] = lbl.transform(list(all_data[c].values))

    numeric_feats = all_data.dtypes[all_data.dtypes != "object"].index

    all_data_02 = pd.get_dummies(all_data)

    train = all_data_02[:ntrain]
    test = all_data_02[ntrain:]

    #====================================================
#    lasso = make_pipeline(RobustScaler(),
#                      Lasso(alpha=0.0005, random_state=1))
#
#    ENet = make_pipeline(RobustScaler(),
#                     ElasticNet(alpha=0.0005,
#                                l1_ratio=0.9,
#                                random_state=3))
#
#    KRR = KernelRidge(alpha=0.6, kernel='polynomial', degree=2, coef0=2.5)
#
#    GBoost = GradientBoostingRegressor(n_estimators=3000,
#                                   learning_rate=0.05,
#                                   max_depth=4,
#                                   max_features='sqrt',
#                                   min_samples_leaf=15,
#                                   min_samples_split=10,
#                                   loss='huber',
#                                   random_state=5)
#
#    model_xgb = xgb.XGBRegressor(colsample_bytree=0.4603,
#                             gamma=0.0468,
#                             learning_rate=0.05,
#                             max_depth=3,
#                             min_child_weight=1.7817,
#                             n_estimators=2200,
#                             reg_alpha=0.4640,
#                             reg_lambda=0.8571,
#                             subsample=0.5213,
#                             silent=1,
#                             nthread=-1)
#
#    averaged_models = AveragingModels(models = (ENet, GBoost, KRR, lasso))
#
#    averaged_models = averaged_models.fit(train, y_train)
#
#
#
#
#    fw = open('dataFile.txt','wb')
#    pickle.dump(averaged_models,fw)
#    fw.close()
    #====================================================

    fr = open('dataFile.txt','rb')
    averaged_models01 = pickle.load(fr)
    fr.close()
    
    predict_averaged_models = averaged_models01.predict(test)
    predict_averaged_models = np.expm1(predict_averaged_models)
    return (predict_averaged_models)

if __name__ == "__main__":
    print(main())
    print(get_median())

    
