from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder, LabelBinarizer,MultiLabelBinarizer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.model_selection import cross_val_score,StratifiedKFold
from django_pandas.io import read_frame
from .models import BankModel


class ML():
    def __init__(self):
        bank_model = BankModel.objects.all()
        df = read_frame(bank_model)

        self.X = df.drop('y', axis=1)
        y = df['y']
        self.y = y.map(lambda x: 0 if x=="no" else 1)
        self.clf = self.pre_process(self.X)


    def pre_process(self, data):
        print("#######  PRE-PROCESSING ###########")
        numeric_features= list(data.columns[data.dtypes == 'int64'])
        categorical_features = list(data.columns[data.dtypes == 'object'])

        numeric_transformer = Pipeline(steps=[
            ('scaler', StandardScaler())
        ])

        categorical_transformer = Pipeline(steps=[
            ('onehot', OneHotEncoder())
        ])

        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_features),
                ('cat', categorical_transformer, categorical_features[:-1])])

        # Append classifier to preprocessing pipeline.
        # Now we have a full prediction pipeline.
        clf = Pipeline(steps=[('preprocessor', preprocessor),
                            ('classifier', svm.SVC(kernel='linear'))])
        return clf

    def train(self):

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X,self.y,test_size=0.2, random_state=30, stratify=self.y)
        print("####### TRAINING ###########")
        self.clf.fit(self.X_train,self.y_train)
        

    def evaluate(self):
        print("#######  EVALUATED ###########")
        return self.clf.score(self.X_test,self.y_test)

    def predict(self):
        pass