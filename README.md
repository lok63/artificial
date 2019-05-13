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
 
### Training 
If you want to train a new model it will take on average 10 minutes to complete training since i am running cross validation. **Dont reload the page** while training otherwise the model will stop training. I could fix this problem in the future by using threads to run the training in the background.

### New prediction
The prediction will use a pre-trained model and will print the output straight away

### Prediction List - LIME
The LIME repository can be found here: [https://github.com/marcotcr/lime](LIME repository)
[I'm an inline-style link](https://www.google.com)


## How to run 
In the future this webapp will be hosted in AWS and it will be accessed using a URL
For now if you wish to run this app locally please follow the following instrunctions

    pip install -r requirements.txt
  



## TODO
- [X] Startisfied split
- [ ] SMOTE
- [ ] Host application on AWS

