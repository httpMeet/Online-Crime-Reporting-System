from django.contrib import admin
from .models import *
# Register your models here.


class PoliceIncharge(admin.ModelAdmin):
    exclude = ('state_id_no','district_id_no','rank_id','station_id')

class PoliceOfficers(admin.ModelAdmin):
    exclude = ('state_id_no','district_id_no','rank_id')


admin.site.register(CustomUser)
admin.site.register(police_incharge,PoliceIncharge)
admin.site.register(police_officer,PoliceOfficers)
admin.site.site_header = "O.C.R.S Admin"
admin.site.site_title = "O.C.R.C Admin Portal"
admin.site.index_title = "Welcome to Online Crime Reporting System Admin Panel"