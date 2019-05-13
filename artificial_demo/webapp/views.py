from django.shortcuts import render
from rest_framework.decorators import api_view
from urllib.parse import urlencode
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.template import RequestContext
from .forms import UploadFileForm, CustomerForm
from .models import BankModel,Predictions
from django.contrib import messages
import csv
import io
from io import StringIO
import pandas as pd
import os
from django_pandas.io import read_frame
from .machine_learning import ML
import numpy as np


def prediction_list(request):
    template='ml/prediction_list.html'

    predictions = Predictions.objects.all().order_by('-pk')
    args = {'predictions':predictions}
    # decision_buttons(request)

    return render(request, template, args)


def predict(data):
    clf = ML()
    df = clf.df.drop(["id"],axis=1)
    new_df=df.append(data).reset_index()
    print("---------------FORM IS NOT VALID")
    print(new_df.tail(1))

    clf.pre_process(new_df)

    y_pred, y_proba = clf.predict()

    prediction = Predictions.objects.latest("pk")
    prediction.y = "No" if y_pred[0] == 0 else "Yes"
    prediction.probability = np.round(y_proba[0][0], decimals=2)
    prediction.save()


def prediction_new(request):
    template='ml/prediction_form.html'

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()

            columns = form.data.keys()
            new_df = pd.DataFrame(pd.DataFrame(form.data.values()).values.reshape(1,-1)).drop(0,axis=1)
            new_df.columns=list(columns)[1:]
            num_col= ["age","balance","day","duration","campaign","pdays","previous"]
            new_df[num_col] = new_df[num_col].apply(pd.to_numeric)
            new_df["y"] = "no"
            
            predict(new_df)

            # form.initial({"probability":y_proba})
            # form.data["probability"] = y_proba
            # form.data["y"] = y_pred

            
            return redirect('predictions')
        else:
            print("---------------FORM IS NOT VALID")
            print(form.errors)
            args = {'form':form, 'errors':form.errors}
            return render(request, template, args)
    else:
        form = CustomerForm()
        args = {'form':form}
        return render(request, template, args)


def reset_BankModel(request):
    print("####### RESETING ###########")
    print(request)

    if len(BankModel.objects.all()) !=0:
        BankModel.objects.all().delete()

    request.session['updated'] = False

    request.session['acc'] = "--"
    request.session['prec'] = "--"
    request.session['rec'] = "--"
    request.session['f1'] = "--"
    request.session['auc'] ="--"

    request.session['acc_cv'] = "--"
    request.session['prec_cv'] = "--"
    request.session['rec_cv'] = "--"
    request.session['f1_cv'] = "--"
    request.session['auc_cv'] = "--"
    return redirect("/artificial_demo/machine-learning")


def train_evaluate(requset):
    clf=ML()
    clf.train()

    acc,prec,rec,f1,auc =   clf.evaluate() 
    requset.session['acc'] = "{0:.2f}%".format(acc)
    requset.session['prec'] = "{0:.2f}%".format(prec)
    requset.session['rec'] = "{0:.2f}%".format(rec)
    requset.session['f1'] = "{0:.2f}%".format(f1)
    requset.session['auc'] = "{0:.2f}%".format(auc)

    acc,prec,rec,f1,auc =   clf.cross_val_score() 
    requset.session['acc_cv'] = "{0:.2f}%".format(acc)
    requset.session['prec_cv'] = "{0:.2f}%".format(prec)
    requset.session['rec_cv'] = "{0:.2f}%".format(rec)
    requset.session['f1_cv'] = "{0:.2f}%".format(f1)
    requset.session['auc_cv'] = "{0:.2f}%".format(auc)
    
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
                messages.error(request, "Please upload a csv file",fail_silently=True)
                return render(request, template_form, args)
            else:
                print("#### Updating Bank Table")
                update_BankModel(csv_file)
                args["file_name"] =csv_file
                request.session['updated'] = True
                messages.success(request,'Your have uploaded ' +  str(csv_file) +  ' successfully!')
                return render(request, template_form, args)


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
