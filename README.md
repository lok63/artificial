# Artificial Demo

All endpoints requested in the description have been created and wrapped in a django WebApplication. However i can expose them as individual endpoinds later on. In addition this application can support users and authentication. The database i used is SQLite for simplicity. In the future i can easily move to any RDBMS. For NoSQL and Django there is limited support at the moment but i could configure MongoDB.

The web application has 3 main Views:
  1. Train/Validate View
     * Upload a csv file
     * Train and validate a new model
  2. Make a new prediction
     * Fill up a form for a new customer and make a new prediction 
  3. Prediction List
     * View all predictions with the Model's decision and the likelihood(probability) of that decision
     * *NOTE*: A poosible extension here is to use LIME to interpolate the model and show which features contributed to the final decision

# How to run:
  1. Go to: 
     * [Web app](http://35.178.199.179/artificial_demo/machine-learning/) Machibe Learning Demo
     * [Admin screen ](http://35.178.199.179/admin) Interact/Modify database
        * User: admin
        * pswd: admin
      
  2. Run it locally
 
**NOTE** : Please note my intension was to develop a web app where you can develop and tune models online and make predictions. The intented webapp however is hosted on AWS EC2 micro instance and doesnt support heavy processing. Whenever you try to train it, you will get a 502 error. However if you wish to train a model using the app, you can run the code locally. Instructions are explained in a different section below.
I am using XgbClassifier since Xgboost is used in AWS sage maker. There are endpoint for training and prediction but these are not being accessed by the user. They are only accessible within the app. However if you wish i can expose these endpoits as individual API endpoints in the future.

### Training a new model on the app
As it was explained above this functionality can be operated only locally for now. If you want to train a new model it will take on average 5-7 minutes to complete training since i am running cross validation. **Dont reload the page** while training otherwise the model will stop training. I could fix this problem in the future by using threads to run the training in the background.

### New prediction
**Please make sure you upload the dataset before making any predictions**
The prediction will use the pre-trained model that you just created. If you didn't train the model, a pre-trained model already exists in the repository.

### Prediction List - LIME
The LIME repository can be found here: [LIME repository](https://github.com/marcotcr/lime). I am currently working on it


## How to run locally

Create and actibate a virtual environment. You can use conda or virtualenv. Make sure you are using python3.
    
Install dependencies

    pip install -r requirements.txt
    
Run the application:

  Navigate to the root directory
  
      cd artificial/artificial_demo
      
  And run 
  
        python manage.py runserver

To access the application go to http://127.0.0.1:8000/artificial_demo/machine-learning/
Now you can interact with it

## Admin login
If you want to examine or modify the database or the predictions got to : http://127.0.0.1:8000/admin

Then login use the following credentials:
  * username: admin
  * password: admin

## TODO
- [X] Host application on AWS
- [ ] LIME
- [X] Startisfied split
- [ ] SMOTE


