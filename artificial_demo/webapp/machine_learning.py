from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder, LabelBinarizer,MultiLabelBinarizer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.model_selection import cross_val_score,StratifiedKFold, cross_validate
from sklearn.metrics import classification_report, f1_score, accuracy_score, precision_score, recall_score, roc_auc_score
from django_pandas.io import read_frame
from sklearn.decomposition import PCA
from sklearn.base import BaseEstimator, TransformerMixin
from .models import BankModel
import pandas as pd
import pickle
import os.path


class ML():
    def __init__(self):

        #load pre-trained model  "snp_data.txt")
        self.pre_trained_clf = pickle.load(open(os.path.join(os.getcwd(),"webapp/model_dumps/svc_v1.pkl"), 'rb'))

        # self.pre_trained_clf = pickle.load(open("/model_dumps/svc.pkl", 'rb'))

        bank_model = BankModel.objects.all()
        self.df = read_frame(bank_model)


        self.svc = svm.SVC(C=1, cache_size=200, class_weight="balanced", coef0=0.0,
                        decision_function_shape='ovr', degree=3, gamma='scale', kernel='linear',
                        max_iter=-1, probability=True, random_state=None, shrinking=True,
                        tol=0.001, verbose=False)


        # self.X = df.drop('y', axis=1)
        # y = df['y']
        # self.y = y.map(lambda x: 0 if x=="no" else 1)
        # self.clf = self.pre_process(self.X)

    def predict(self):


        y_pred=self.pre_trained_clf.predict([self.X[-1]])
        y_proba=self.pre_trained_clf.predict_proba([self.X[-1]])
        print(y_pred)
        print(y_proba)

        return y_pred,y_proba


    def pre_process(self, data):
        print("#######  PRE-PROCESSING ###########")
        #Numeric Features
        numeric_features= list(data.columns[data.dtypes == 'int64'])
        scaler = StandardScaler()
        scaled_data = scaler.fit_transform(data[numeric_features])
        scaled_data = pd.DataFrame(data=scaled_data, columns=numeric_features)

        #Binary Features
        binary_features = ["default", "housing", "loan", "y"]
        lb = BinaryTransformer()
        binarised_features = lb.fit_transform(data[binary_features])

        # Multioutput Features
        categorical_features = list(set(list(data.columns[data.dtypes == 'object'])) - set(binarised_features))
        ohe_data = pd.get_dummies(data[categorical_features])
        new_categorical_features = ohe_data.columns

        cleaned_data = pd.concat([scaled_data, binarised_features, ohe_data], axis=1)

        
        self.X = cleaned_data.drop('y', axis=1)
        self.y = cleaned_data['y']
        
        pca = PCA(n_components=32)
        self.X = pca.fit_transform(self.X)
        print(self.X.shape)

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2, stratify=self.y)
        
        

    def train(self):
        print("####### REEEE ###########")
        print(self.df.head())
        self.pre_process(self.df)
        print("####### TRAINING ###########")
        self.svc.fit(self.X_train,self.y_train)

        pickle.dump(self.svc, open(os.path.join(os.getcwd(),"webapp/model_dumps/svc_v1.pkl"), 'wb'))
        

    def evaluate(self):
        y_pred = self.svc.predict(self.X_test)
        print(y_pred)
        acc =accuracy_score(self.y_test,y_pred)
        prec =precision_score(self.y_test,y_pred)
        rec= recall_score(self.y_test,y_pred)
        f1 = f1_score(self.y_test,y_pred)
        auc = roc_auc_score(self.y_test,y_pred)
        print("#######  EVALUATED ###########")

        return acc*100,prec*100,rec*100,f1,auc*100
        

    def cross_val_score(self):
        print("#######  CROSS-VALIDATION ###########")
        skf = StratifiedKFold(n_splits=3, random_state=True, shuffle=True)
        scores = cross_validate(self.svc, self.X, self.y, cv=skf, n_jobs=-1, scoring=["accuracy","recall", "precision",'f1', "roc_auc"])
        for key, value in scores.items():
            print("{}: {}".format(key, value.mean()))
        
        return scores["test_accuracy"].mean()*100, scores["test_recall"].mean()*100, scores["test_precision"].mean()*100, scores["test_f1"].mean()*100, scores["test_roc_auc"].mean()*100

    

class BinaryTransformer( BaseEstimator, TransformerMixin ):
    #Class Constructor 
    def __init__(self):
        pass
    
    #Return self nothing else to do here    
    def fit( self, X, y = None ):
        return self 
    
    #Method that describes what we need this transformer to do
    def transform( self, X, y = None ):
        self.columns = list(X.columns)
        result = X.copy()
        for c in result.columns:
            result[c] = result[c].apply(lambda x: 1 if x=="yes" else 0)
            
        return result