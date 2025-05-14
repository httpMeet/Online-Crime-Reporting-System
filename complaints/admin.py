from django.contrib import admin
from complaints.models import *
from accounts.models import rank_master

class StateMasterAdmin(admin.ModelAdmin):
    exclude = ('state_id',)

class DistrictMasterAdmin(admin.ModelAdmin):
    exclude = ('district_id','state_id')

class PoliceStationMasterAdmin(admin.ModelAdmin):
    exclude = ('station_id','district_id','state_id','created_at')

class CrimeCategoryMasterAdmin(admin.ModelAdmin):
    exclude = ('crime_category_id',)

class ComplaintMasterAdmin(admin.ModelAdmin):
    exclude = ('complaint_id','complainant_state_id', 'complainant_district_id', 'state_id', 'district_id', 'station_id')


class CsrMasterAdmin(admin.ModelAdmin):
    exclude = ('complainant_state_id','complainant_district_id', 'state_id', 'district_id','station_id')

class FirMasterAdmin(admin.ModelAdmin):
    exclude = ('complainant_state_id','complainant_district_id', 'state_id', 'district_id','station_id')


# Register your models here.
admin.site.register(state_master,StateMasterAdmin)
admin.site.register(district_master,DistrictMasterAdmin)
admin.site.register(police_station_master,PoliceStationMasterAdmin)
admin.site.register(crime_category_master,CrimeCategoryMasterAdmin)
admin.site.register(complaint_master,ComplaintMasterAdmin)
admin.site.register(rank_master)
admin.site.register(csr_master,CsrMasterAdmin)
admin.site.register(fir_master,FirMasterAdmin)
admin.site.register(announcements)



