# Artificial Demo

All endpoints requested in the description have been created and wrapped in a django WebApplication. However i can expose them as individual endpoinds later on. 

The web application has 3 main Views:
  1. Train/Validate View
     * Upload a csv file
     * Train and validate a new model
  2. Make a new prediction
     * Fill up a form and make a new prediction
  3. Prediction List
     * View all predictions with the Model's decision and probability
     * *NOTE*: A poosible extension here is to use LIME to interpolate the model and show which features contributed to the final decision
  
  




## TODO
- [X] Startisfied split
- [ ] SMOTE
- [ ] Cost Function for unbalanced


### REST
- [ ] Best practises for Hhosting microservices( servelsess, containers ) 
- [ ] Error handling when loading the dataset
- [ ] Tests
