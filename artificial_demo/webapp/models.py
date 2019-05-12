from django.db import models

class BankModel(models.Model):

    JOB=(
        ('management','management'), ('technician','technician'),
        ('entrepreneur','entrepreneur'), ('blue-collar','blue-collar'),
        ('unknown','unknown'), ('retired','retired'), ('admin.','admin.'),
        ('services','services'),('self-employed','self-employed'),('unemployed','unemployed'),
        ('housemaid','housemaid'),('student', 'student'),
    )
    MARTIAL= (
        ('married','married'),('single','single'), ('divorced','divorced'),
    )
    EDUCATION = (
        ('tertiary','tertiary'),('secondary','secondary'),('unknown','unknown'), (  'primary',  'primary'),
    )
    DEFAULT = (
        ('no','no'), ('yes','yes'),
    )
    HOUSING = (
        ('no','no'), ('yes','yes'),
    )
    LOAN = (
        ('no','no'), ('yes','yes'),
    )
    CONTACT=(
        ('unknown','unknown'),('cellular','cellular'),('telephone','telephone'),  
    )
    MONTH= (
        ('may','may'),('jun','jun'),('jul','jul'),('aug','aug'),('oct','oct'),('nov','nov'),
        ('dec','dec'),('jan','jan'),('feb','feb'),('mar','mar'),('apr','apr'),('sep','sep'),
    )
    POUTCOME = ( 
        ('unknown','unknown'),('failure','failure'),('other','other'), ('success','success')
    )
    Y = (
        ('no','no'), ('yes','yes'),
    )
        
    age = models.IntegerField()
    job= models.CharField(max_length = 100,choices = JOB, default = 'unknown', blank = False )
    marital = models.CharField(max_length = 100,choices = MARTIAL, default = 'single', blank = False )
    education = models.CharField(max_length = 100,choices = EDUCATION, default = 'unknown', blank = False )
    default = models.CharField(max_length = 100,choices = DEFAULT, default = 'no', blank = False )
    balance = models.IntegerField()
    housing = models.CharField(max_length = 100,choices = HOUSING, default = 'no', blank = False )
    loan = models.CharField(max_length = 100,choices = LOAN, default = 'no', blank = False )
    contact = models.CharField(max_length = 100,choices = CONTACT, default = 'unknown', blank = False )
    day = models.IntegerField()
    month = models.CharField(max_length = 100,choices = MONTH, default = 'may', blank = False )
    duration = models.IntegerField()
    campaign = models.IntegerField()
    pdays = models.IntegerField()
    previous= models.IntegerField()
    poutcome= models.CharField(max_length = 100,choices = POUTCOME, default = 'unknown', blank = False )
    y= models.CharField(max_length = 100,choices = Y, default = 'no', blank = False )
    


# class MyCsvModel(CsvModel):
#      class Meta:
#         dbModel = BankModel
#         delimiter = ";"