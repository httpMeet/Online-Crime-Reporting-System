from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .models import *
from accounts.models import *
from django.contrib.auth.decorators import login_required

@login_required(login_url='landing_page')
def user(request):
    user_id = request.user.user_id
    user = CustomUser.objects.get(user_id=user_id)
    total_complaints = complaint_master.objects.filter(complainant_email=user.email).count()
    total_pending_complaints = complaint_master.objects.filter(complainant_email=user.email,status='Pending').count()
    total_firs= fir_master.objects.filter(complainant_email=user.email).count()
    total_csrs= csr_master.objects.filter(complainant_email=user.email).count()


    context = {
        'user': user,
        'total_complaints': total_complaints,
        'total_pending_complaints' : total_pending_complaints,
        'total_firs' : total_firs,
        'total_csrs' : total_csrs   
    }
    return render(request, 'user.html',context)
    
@login_required(login_url='landing_page')
def create_complaint(request):
    crime_categories = crime_category_master.objects.all()
    states = state_master.objects.all()
    district = district_master.objects.all()
    police_stations =police_station_master.objects.all()
    context = {
                'crime_categories': crime_categories,
                'states': states,
                'districts': district,
                'police_stations':police_stations
    }
    if request.method == 'POST':
        complaint_name = request.POST.get('name')
        complainant_gender = request.POST.get('gender')
        complainant_contact_no = request.POST.get('contact_no')
        complainant_email = request.POST.get('email')
        complaint_dob = request.POST.get('dob')
        # 
        get_complainant_address = request.POST.get('complainant_address')
        complainant_pin_code = request.POST.get('complainant_pin_code')
        state_name = request.POST.get('state_name')
        state_id = state_master.objects.get(state_name=state_name).state_id
        district_name = request.POST.get('district_name')
        district_id = district_master.objects.get(district_name=district_name).district_id
        # 
        complaint_state_name = request.POST.get('complaint_state')
        complaint_state_id = state_master.objects.get(state_name=complaint_state_name).state_id
        complaint_district_name = request.POST.get('complaint_district')
        complaint_district_id = district_master.objects.get(district_name=complaint_district_name).district_id
        station_name = request.POST.get('complaint_police_station')
        station_id = police_station_master.objects.get(station_name=station_name).station_id
        crime_category = request.POST.get('crime_category')
        other_crime_category = request.POST.get('other_crime_category')
        subject = request.POST.get('subject')
        detailed_description = request.POST.get('detailed_description')
        delay_reason = request.POST.get('delay_in_complaining')
        datetime_of_occurence = request.POST.get('date_time_of_occurence')
        place_of_occurence = request.POST.get('place_of_occurence')
        evidence_image = request.FILES.get('evidence_image')
        # created_at = request.POST.get('name')
        # updated_at = request.POST.get('name')

        temp_state_name= state_master.objects.get(state_name=state_name)
        temp_district_name= district_master.objects.get(district_name=district_name)


        temp_complaint_state_name = state_master.objects.get(state_name=complaint_state_name)
        temp_complaint_district_name = district_master.objects.get(district_name=complaint_district_name) 
        police_complaint_station_name = police_station_master.objects.get(station_name=station_name)
        temp_complaint_crime_category = crime_category_master.objects.get(crime_category_name=crime_category)

        print(get_complainant_address)
        complaint = complaint_master.objects.create(
        complainant_name = complaint_name,
        complainant_gender = complainant_gender,
        complainant_contact_no = complainant_contact_no,
        complainant_email = complainant_email,
        complainant_dob = complaint_dob,
        complainant_address = get_complainant_address,
        complainant_state_name = temp_state_name,
        complainant_state_id = state_id,
        complainant_district_name = temp_district_name,
        complainant_district_id = district_id,
        complainant_pin_code = complainant_pin_code,
        state_name = temp_complaint_state_name,
        state_id = complaint_state_id,
        district_name = temp_complaint_district_name,
        district_id = complaint_district_id,
        station_name = police_complaint_station_name,
        station_id = station_id,
        status = "Pending",
        crime_category = temp_complaint_crime_category,
        other_crime_category = other_crime_category,
        subject = subject,
        detailed_description = detailed_description,
        delay_reason = delay_reason,
        datetime_of_occurence = datetime_of_occurence,
        place_of_occurence = place_of_occurence,
        evidence_image = evidence_image,
        created_at=timezone.now(),
        updated_at=timezone.now()

    )
        print(complaint)


        return redirect('/user')
    
    

    else:
        return render(request, 'create_complaint.html',context)