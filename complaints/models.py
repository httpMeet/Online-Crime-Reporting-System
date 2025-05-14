from django.utils import timezone
from django.db import models
from django.utils.translation import gettext_lazy 

# Create your models here.

class state_master(models.Model):
    status_id_choices = (
        ('active', 'active'),
        ('inactive', 'inactive'),
    )
    state_id = models.AutoField(primary_key=True,unique=True)
    state_name = models.CharField(max_length=150,null=False,blank=False,unique=True)
    status_id = models.CharField(max_length=9,null=False,blank=False,choices=status_id_choices)

    def __str__(self):
        return self.state_name
    
    class Meta:
        verbose_name_plural = "States and Union Territories"

class district_master(models.Model):
    status_id_choices = (
        ('active', 'active'),
        ('inactive', 'inactive'),
    )
    district_id = models.AutoField(primary_key=True,unique=True)
    district_name = models.CharField(max_length=150,null=False,blank=False,unique=True)
    state_name = models.ForeignKey(state_master,to_field='state_name',null=False,blank=False,on_delete=models.PROTECT)
    state_id = models.IntegerField(null=True, blank=True)
    status_id = models.CharField(max_length=9,null=False,blank=False,choices=status_id_choices)
    def save(self, *args, **kwargs):
        if self.state_name:
            state = state_master.objects.filter(state_name=self.state_name).first()
            if state:
                self.state_id = state.state_id
        super(district_master, self).save(*args, **kwargs)

    def __str__(self):
        return self.district_name
    
    class Meta:
        verbose_name_plural = "Districts"

class police_station_master(models.Model):
    status_id_choices = (
        ('active', 'active'),
        ('inactive', 'inactive'),
    )
    station_id = models.AutoField(primary_key=True,unique=True)
    station_name = models.CharField(max_length=150,null=False,blank=False,unique=True)
    station_mail = models.EmailField(gettext_lazy('Email Address'),null=False, blank=False)
    address = models.TextField(max_length=150, null=False,blank=False)
    state_name = models.ForeignKey(state_master,to_field='state_name',null=False,blank=False,on_delete=models.PROTECT)
    state_id = models.IntegerField(null=True, blank=True) 
    district_name = models.ForeignKey(district_master,to_field='district_name',null=False,blank=False,on_delete=models.PROTECT)
    district_id = models.IntegerField(null=True, blank=True)   
    pin_code = models.IntegerField(null=False,blank=False)
    status_id = models.CharField(max_length=9,null=False,blank=False,choices=status_id_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    # created_by = models.ForeignKey(admin_master,null=True,blank=True,on_delete=models.PROTECT)
    updated_at = models.DateTimeField(auto_now=False,null=True,blank=True,)
    # updated_by = models.ForeignKey(admin_master,null=True,blank=True,on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if self.state_name:
            state = state_master.objects.filter(state_name=self.state_name).first()
            if state:
                self.state_id = state.state_id
        if self.district_name:
            district = district_master.objects.filter(district_name=self.district_name).first()
            if district:
                self.district_id = district.district_id

        super(police_station_master, self).save(*args, **kwargs)

    def __str__(self):
        return self.station_name
    
    class Meta:
        verbose_name_plural = "Police Stations"

class crime_category_master(models.Model):
    crime_category_id = models.AutoField(primary_key=True, unique=True)
    crime_category_name = models.CharField(max_length=150, null=False, blank=False, unique=True)
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)


    def __str__(self):
        return self.crime_category_name
    
    class Meta:
        verbose_name_plural = "Crime Categories"



class complaint_master(models.Model):
    gender_choices = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    status_choices = (
        ('Pending', 'Pending'),
        ('CSR is Filed', 'CSR is Filed'),
        ('FIR is Filed', 'FIR is Filed'),
        ('Rejected', 'Rejected'),
    )
    complaint_id = models.AutoField(primary_key=True,null=False,blank=False,unique=True)
    complainant_name = models.CharField(max_length=150,null=False,blank=False)
    complainant_gender = models.CharField(max_length=6,choices=gender_choices)
    complainant_contact_no = models.IntegerField(null=False, blank=False)
    complainant_email = models.EmailField(gettext_lazy('Email Address'),null=False, blank=False)
    complainant_dob = models.DateField()
    complainant_address = models.TextField(null=False,blank=False)
    complainant_state_name = models.ForeignKey(state_master,to_field='state_name', null=False, blank=False,on_delete=models.PROTECT,related_name="complainant's_state+")
    complainant_state_id = models.IntegerField(null=True, blank=True)
    complainant_district_name = models.ForeignKey(district_master,to_field='district_name', null=False, blank=False,on_delete=models.PROTECT,related_name="complainant's_district+")
    complainant_district_id = models.IntegerField(null=True, blank=True)
    complainant_pin_code = models.IntegerField(null=False,blank=False) 
    state_name = models.ForeignKey(state_master,to_field='state_name',null=False,blank=False,on_delete=models.PROTECT,related_name="complaint_in_state+")
    state_id = models.IntegerField(null=True, blank=True)
    district_name = models.ForeignKey(district_master,to_field='district_name',null=False,blank=False,on_delete=models.PROTECT,related_name="complaint_in_district+")
    district_id = models.IntegerField(null=True, blank=True)
    station_name = models.ForeignKey(police_station_master,to_field='station_name',null=False,blank=False,on_delete=models.PROTECT,related_name="complainant_in_police_station+")
    station_id  = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=15,choices=status_choices,null=False, blank=False,default='Pending')
    crime_category = models.ForeignKey(crime_category_master,to_field='crime_category_name',null=False, blank=False,on_delete=models.PROTECT)
    other_crime_category = models.CharField(max_length=150,null=True, blank=True)
    subject = models.CharField(max_length=500,null=False,blank=False)
    detailed_description = models.TextField(max_length=10000,null=False,blank=False)
    delay_reason = models.TextField(max_length=1000,null=True,blank=True)
    datetime_of_occurence = models.DateTimeField(null=False,blank=False)
    place_of_occurence = models.CharField(max_length=150, null=True, blank=True)
    evidence_image = models.ImageField(null=True, blank=True, upload_to="complaint images/")
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)
    info_by_station_incharge = models.TextField(null=True, blank=True,default="")



    def save(self, *args, **kwargs):
        if self.complainant_state_name:
            state = state_master.objects.filter(state_name=self.complainant_state_name).first()
            if state:
                self.complainant_state_id = state.state_id

        if self.complainant_district_name:
            district = district_master.objects.filter(district_name=self.complainant_district_name).first()
            if district:
                self.complainant_district_id = district.district_id

        if self.state_name:
            state = state_master.objects.filter(state_name=self.state_name).first()
            if state:
                self.state_id = state.state_id

        if self.district_name:
            district = district_master.objects.filter(district_name=self.district_name).first()
            if district:
                self.district_id = district.district_id
                
        if self.station_name:
            station = police_station_master.objects.filter(station_name=self.station_name).first()
            if station:
                self.station_id = station.station_id
        super(complaint_master, self).save(*args, **kwargs)

    def __str__(self):
        return self.complainant_name
    
    class Meta:
        verbose_name_plural = "Complaints"


class csr_master(models.Model):
    status_choices = (
        ('CSR is Filed', 'CSR is Filed'),
        ('Completed', 'Completed'),
    )
    csr_id = models.AutoField(primary_key=True,unique=True)
    csr_no = models.CharField(max_length=150,null=False,blank=False,unique=True)
    complainant_name = models.CharField(max_length=150,null=False,blank=False)
    complainant_gender = models.CharField(max_length=6,)
    complainant_contact_no = models.IntegerField(null=False, blank=False)
    complainant_email = models.EmailField(gettext_lazy('Email Address'),null=False, blank=False)
    complainant_dob = models.DateField()
    complainant_address = models.TextField(null=False,blank=False)
    complainant_state_name = models.ForeignKey(state_master,to_field='state_name', null=False, blank=False,on_delete=models.PROTECT,related_name="complainant's_state+")
    complainant_state_id = models.IntegerField(null=True, blank=True)
    complainant_district_name = models.ForeignKey(district_master,to_field='district_name', null=False, blank=False,on_delete=models.PROTECT,related_name="complainant's_district+")
    complainant_district_id = models.IntegerField(null=True, blank=True)
    complainant_pin_code = models.IntegerField(null=False,blank=False) 
    state_name = models.ForeignKey(state_master,to_field='state_name',null=False,blank=False,on_delete=models.PROTECT,related_name="complaint_in_state+")
    state_id = models.IntegerField(null=True, blank=True)
    district_name = models.ForeignKey(district_master,to_field='district_name',null=False,blank=False,on_delete=models.PROTECT,related_name="complaint_in_district+")
    district_id = models.IntegerField(null=True, blank=True)    
    station_name = models.ForeignKey(police_station_master,to_field='station_name',null=False,blank=False,on_delete=models.PROTECT,related_name="complainant_in_police_station+")
    station_id  = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20,choices=status_choices,default="CSR in progress")
    crime_category = models.ForeignKey(crime_category_master,to_field='crime_category_name',null=False, blank=False,on_delete=models.PROTECT)
    other_crime_category = models.CharField(max_length=150,null=True, blank=True)
    subject = models.CharField(max_length=500,null=False,blank=False)
    ncr_detailed_description = models.TextField(max_length=10000,null=False,blank=False)
    delay_reason = models.TextField(max_length=1000,null=True,blank=True)
    datetime_of_occurence = models.DateTimeField(null=False,blank=False)
    place_of_occurence = models.CharField(max_length=150, null=True, blank=True)
    evidence_image = models.ImageField(null=True, blank=True, upload_to="complaint images/")
    info_by_station_incharge = models.TextField(null=True, blank=True,default="")
    created_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    updated_at = models.DateTimeField(default=timezone.now,null=True,blank=True)
    reporting_date_time = models.DateTimeField(null=True, blank=True)
    feedback = models.TextField(max_length=1000,null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.complainant_state_name:
            state = state_master.objects.filter(state_name=self.complainant_state_name).first()
            if state:
                self.complainant_state_id = state.state_id

        if self.complainant_district_name:
            district = district_master.objects.filter(district_name=self.complainant_district_name).first()
            if district:
                self.complainant_district_id = district.district_id

        if self.state_name:
            state = state_master.objects.filter(state_name=self.state_name).first()
            if state:
                self.state_id = state.state_id

        if self.district_name:
            district = district_master.objects.filter(district_name=self.district_name).first()
            if district:
                self.district_id = district.district_id
                
        if self.station_name:
            station = police_station_master.objects.filter(station_name=self.station_name).first()
            if station:
                self.station_id = station.station_id
        super(csr_master, self).save(*args, **kwargs)

    def __str__(self):
        return self.complainant_name
    
    class Meta:
        verbose_name_plural = "CSRs"

class fir_master(models.Model):
    status_choices = (
        ('FIR is Filed', 'FIR is Filed'),
        ('Completed', 'Completed')
    )
    type_of_information_choices = (
        ('Oral', 'Oral'),
        ('Written', 'Written')
        )
    fir_id = models.AutoField(primary_key=True,unique=True)
    fir_no = models.CharField(max_length=150,null=False,blank=False,unique=True)
    complainant_name = models.CharField(max_length=150,null=False,blank=False)
    complainant_gender = models.CharField(max_length=6,)
    complainant_contact_no = models.IntegerField(null=False, blank=False)
    complainant_email = models.EmailField(gettext_lazy('Email Address'),null=False, blank=False)
    complainant_dob = models.DateField()
    complainant_address = models.TextField(null=False,blank=False)
    complainant_state_name = models.ForeignKey(state_master,to_field='state_name', null=False, blank=False,on_delete=models.PROTECT,related_name="complainant's_state+")
    complainant_state_id = models.IntegerField(null=True, blank=True)
    complainant_district_name = models.ForeignKey(district_master,to_field='district_name', null=False, blank=False,on_delete=models.PROTECT,related_name="complainant's_district+")
    complainant_district_id = models.IntegerField(null=True, blank=True)
    complainant_pin_code = models.IntegerField(null=False,blank=False) 
    state_name = models.ForeignKey(state_master,to_field='state_name',null=False,blank=False,on_delete=models.PROTECT,related_name="complaint_in_state+")
    state_id = models.IntegerField(null=True, blank=True)
    district_name = models.ForeignKey(district_master,to_field='district_name',null=False,blank=False,on_delete=models.PROTECT,related_name="complaint_in_district+")
    district_id = models.IntegerField(null=True, blank=True)    
    station_name = models.ForeignKey(police_station_master,to_field='station_name',null=False,blank=False,on_delete=models.PROTECT,related_name="complainant_in_police_station+")
    station_id  = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20,choices=status_choices,default="FIR in progress")
    crime_category = models.ForeignKey(crime_category_master,to_field='crime_category_name',null=False, blank=False,on_delete=models.PROTECT)
    other_crime_category = models.CharField(max_length=150,null=True, blank=True)
    subject = models.CharField(max_length=500,null=False,blank=False)
    fir_detailed_description = models.TextField(max_length=10000,null=False,blank=False)
    delay_reason = models.TextField(max_length=1000,null=True,blank=True)
    datetime_of_occurence = models.DateTimeField(null=False,blank=False)
    place_of_occurence = models.CharField(max_length=150, null=True, blank=True)
    evidence_image = models.ImageField(null=True, blank=True, upload_to="complaint images/")
    info_by_station_incharge = models.TextField(null=True, blank=True,default="")
    gd_number = models.CharField(max_length=150,null=True,blank=True)
    act_and_sections = models.CharField(max_length=500,null=False,blank=False)
    type_of_information = models.CharField(max_length=20,null=False,blank=False,choices=type_of_information_choices)
    nearest_identifiable_place = models.CharField(max_length=500,null=False,blank=False)
    direction_and_distance_from_ps = models.CharField(max_length=500,null=False,blank=False)
    complaintant_religion = models.CharField(max_length=500,null=False,blank=False)
    complaintant_caste = models.CharField(max_length=500,null=False,blank=False)
    sus_acu_details = models.TextField(max_length=500,null=False,blank=False)
    properties_involved = models.TextField(max_length=500,null=False,blank=False)
    property_value = models.TextField(max_length=500,null=False,blank=False)
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)
    reporting_date_time = models.DateTimeField(null=True, blank=True)
    feedback = models.TextField(max_length=1000,null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.complainant_state_name:
            state = state_master.objects.filter(state_name=self.complainant_state_name).first()
            if state:
                self.complainant_state_id = state.state_id

        if self.complainant_district_name:
            district = district_master.objects.filter(district_name=self.complainant_district_name).first()
            if district:
                self.complainant_district_id = district.district_id

        if self.state_name:
            state = state_master.objects.filter(state_name=self.state_name).first()
            if state:
                self.state_id = state.state_id

        if self.district_name:
            district = district_master.objects.filter(district_name=self.district_name).first()
            if district:
                self.district_id = district.district_id
                
        if self.station_name:
            station = police_station_master.objects.filter(station_name=self.station_name).first()
            if station:
                self.station_id = station.station_id
        super(fir_master, self).save(*args, **kwargs)


    def __str__(self):
        return self.complainant_name
    
    class Meta:
        verbose_name_plural = "FIRs"



class announcements(models.Model):
    announcement_id = models.AutoField(primary_key=True,unique=True)
    title = models.CharField(max_length=50,blank=False,null=False)
    description = models.TextField(max_length=5000,blank=False,null=False)
    image = models.ImageField(null=True, blank=True, upload_to="announcements images/")
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "announcements"

        