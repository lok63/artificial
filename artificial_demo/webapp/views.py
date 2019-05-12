from django.shortcuts import render
from rest_framework.decorators import api_view
from urllib.parse import urlencode
from django.urls import reverse
# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.template import RequestContext

from .forms import UploadFileForm
from .models import BankModel
from django.contrib import messages
import csv
import io
from io import StringIO
import pandas as pd
import os
from django_pandas.io import read_frame
from .machine_learning import ML


def reset_BankModel(request):
    print("####### RESETING ###########")
    print(request)

    if len(BankModel.objects.all()) !=0:
        BankModel.objects.all().delete()

    request.session['updated'] = False
    return redirect("/artificial_demo/machine-learning")


def train_evaluate(requset):
    clf=ML()
    clf.train()
    requset.session['acc'] = clf.evaluate() 
    return redirect("/artificial_demo/machine-learning")




@api_view(['GET', 'POST'])
def upload_file(request):

    #ml_model = ML()
    #ml_model.train()
    # print(ml_model.evaluate())




    template_form='ml/dataset_form.html'

    form = UploadFileForm()
    args = {'form':form}

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():

            csv_file = (request.FILES["file"])   
            #Return error messages when user upload wrong files
            if not csv_file.name.endswith('.csv'):
                messages.error(request, "Please upload a csv file")
                return render(request, template_form, args)
            else:
                print("#### Updating Bank Table")
                update_BankModel(csv_file)
                request.session['updated'] = True
                #args["updated"]= True
                return render(request, template_form)


        else: #When form is not valid render the upload form again
            return render(request, template_form, args)
    else:     #When its GET request render the upload form
        return render(request, template_form, args)




    
def update_BankModel(csv_file):
    df= pd.read_csv(csv_file, sep=";")    
    df_records = df.to_dict('records')

    model_instances = [BankModel(
        age=record['age'],
        job=record['job'],
        marital=record['marital'],
        education=record['education'],
        default=record['default'],
        balance=record['balance'],
        housing=record['housing'],
        loan=record['loan'],
        contact=record['contact'],
        day=record['day'],
        month=record['month'],
        duration=record['duration'],
        campaign=record['campaign'],
        pdays=record['pdays'],
        previous=record['previous'],
        poutcome=record['poutcome'],
        y=record['y']
    ) for record in df_records]

    BankModel.objects.bulk_create(model_instances)

def list_dataset(request):
    template='ml/dataset_list.html'

    data = BankModel.objects.all()
    args = {'data':data}
    #decision_buttons(request)    
    return render(request, template, args)

    # data_set = csv_file.read().decode('UTF-8')
    # io_string = io.StringIO(data_set)
    # next(io_string) # skip the first line of the file sicne its the header
    # for column in csv.reader(io_string, delimiter=';'):
    #     _,created = BankModel.objects.update_or_create(
    #         age = column[0],
    #         job = column[1],
    #         marital = column[2],
    #         education = column[3],
    #         default = column[4],
    #         balance = column[5],
    #         housing = column[6],
    #         loan = column[7],
    #         contact = column[8],
    #         day = column[9],
    #         month = column[10],
    #         duration = column[11],
    #         campaign = column[12],
    #         pdays = column[13],
    #         previous = column[14],
    #         poutcome = column[15],
    #         y = column[16],

    #     )
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