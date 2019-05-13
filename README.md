# Artificial Demo

All endpoints requested in the description have been created and wrapped in a django WebApplication. However i can expose them as individual endpoinds later on. 

The web application has 3 main Views:
  1. Train/Validate View
     * Upload a csv file
     * Train and validate a new model
  2. Make a new prediction
     * Fill up a form for a new customer and make a new prediction 
  3. Prediction List
     * View all predictions with the Model's decision and the likelihood(probability) of that decision
     * *NOTE*: A poosible extension here is to use LIME to interpolate the model and show which features contributed to the final decision
  
  
## How to run 
In the future this webapp will be hosted in AWS and it will be accessed using a URL
For now if you wish to run this app locally please follow the following instrunctions

  pip install -r requirements.txt
  



## TODO
- [X] Startisfied split
- [ ] SMOTE
- [ ] Host application on AWS

