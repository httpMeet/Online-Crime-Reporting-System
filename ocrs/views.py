from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from complaints.models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from datetime import datetime
from django.shortcuts import render, redirect
from accounts.models import *
from accounts.models import *

def landing_page(request):
    total_users = CustomUser.objects.all().count()
    context = {
        'total_users' : total_users
    }
    return render(request,"landing_page.html",context)



def register(request):
    states = state_master.objects.all()
    district = district_master.objects.all()
    context = {
                'states': states,
                'district': district,
    }
    if request.method == 'POST':
        # Get data from the form
        username = request.POST.get('username')
        email = request.POST.get('email')
        Phone_Number = request.POST.get('Phone_Number')
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        password = request.POST.get('password')
        gender = request.POST.get('Yourgender')
        aadhaarno = request.POST.get('aadhaarno')
        state = request.POST.get('complainant_state')
        district = request.POST.get('complainant_district')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')

        states = state_master.objects.get(state_name=state)
        print(states.state_name)

        districts = district_master.objects.get(district_name=district)
        print(districts.district_name)
        # Create the user object


        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            Phone_Number=Phone_Number,
            first_name=first_name,
            last_name=last_name,
            password=password,
            gender=gender,
            aadhaarno=aadhaarno,
            state=states,
            district=districts,
            address=address,
            pincode=pincode,
            state_id_no =states.state_id,
            district_id_no = districts.district_id
        )

        # Redirect to the login page
        return redirect(reverse('landing_page'))
    
    # Render the form for GET requests
    print(context)
    return render(request, 'register.html',context)


def user_login(request):
    if request.method == 'POST':
        context = {'Login_status': ''}

        # get the username and password from the POST request
        email1  = request.POST.get('email')
        password1  = request.POST.get('password')
        
        print(email1)
        print(password1)
        user = None
        try:
            user = CustomUser.objects.get(email=email1)
            print("user")
        except :
            try:
                user = police_incharge.objects.get(email=email1)
                print("psi")
            except :
                print("psi not exist")
                try:
                    user = police_officer.objects.get(email=email1)
                    print("police")
                except :
                    print("police not exist")
                    context.update({'Login_status':"Invalid credentials"})
                    print(context['Login_status'])
                    return render(request, 'login.html',context)

        # authenticate the user
        if user is not None:
            print("fetching")
            authenticate_user = authenticate(request, email=email1, password=password1)
            
            if authenticate_user is not None:
                print("fetched")
                print(user)
                if authenticate_user is not None:

                    if isinstance(authenticate_user, CustomUser):
                        login(request, user,backend='accounts.auth.CustomUserBackend')
                        context.update({'Login_status':""})
                        print(context['Login_status'])
                        return redirect('/user')
                    
                    elif isinstance(authenticate_user, police_incharge):
                        login(request, user,backend='accounts.auth.PoliceInchargeBackend')
                        context.update({'Login_status':""})
                        print(context['Login_status'])
                        return  redirect('/police_incharge_home',user) 
                    
                    elif isinstance(authenticate_user, police_officer):
                        login(request, user,backend='accounts.auth.PoliceBackend')
                        context.update({'Login_status':""})
                        print(context['Login_status'])
                        return  redirect('/police') 
                else:
                    context.update({'Login_status':"Invalid credentials"})
                    print(context['Login_status'])
                    return render(request, 'login.html',context)
            else:
                return  HttpResponse("user not found")

    else:
        # render the login page
        return render(request, 'login.html')
    


def user_logout(request):
    logout(request)
    return redirect('landing_page')

def index(request):
    return render(request, 'index.html')

def get_districts(request):
    state_name = request.GET.get('complaint_state') 
    state_object = state_master.objects.get(state_name=state_name)
    state_id = state_object.state_id
    districts_objects = district_master.objects.filter(state_id=state_id)
    districts = list(districts_objects.values('district_id', 'district_name'))
    return JsonResponse({'districts': districts})

def get_police_stations(request):
    district_name = request.GET.get('complaint_district') 
    district_object = district_master.objects.get(district_name=district_name)
    district_id = district_object.district_id
    police_station_objects = police_station_master.objects.filter(district_id=district_id)
    # print(police_station_objects)
    police_stations = list(police_station_objects.values('station_id', 'station_name'))
    # print(police_stations)
    return JsonResponse({'police_stations': police_stations})



def get_districts_register(request):
    state_name = request.GET.get('complainant_state') 
    state_object = state_master.objects.get(state_name=state_name)
    state_id = state_object.state_id
    districts_objects = district_master.objects.filter(state_id=state_id)
    districts = list(districts_objects.values('district_id', 'district_name'))
    return JsonResponse({'districts': districts})


def sidebar(request):
    return render(request, 'sidebar.html')

def administrator(request):
    return render(request, 'admin.html')



def test(request):
    return render(request, 'test.html')

def police(request):
    police = request.user.station_name
    station = police_station_master.objects.get(station_name=police)
    total_firs= fir_master.objects.filter(station_name=station).count()
    total_csrs= csr_master.objects.filter(station_name=station).count()
    total_reports = total_csrs + total_firs
    total_firs_under_investigation= fir_master.objects.filter(station_name=station,status="FIR is Filed").count()
    total_firs_solved= total_firs - total_firs_under_investigation
    total_csrs_under_investigation= csr_master.objects.filter(station_name=station,status="CSR is Filed").count()
    total_csrs_solved= total_csrs - total_csrs_under_investigation
    cases_under_investigation= total_firs_under_investigation + total_csrs_under_investigation
    context = {
            'total_firs' :total_firs,
            'total_csrs' :total_csrs,
            'total_reports' :total_reports,
            'cases_under_investigation' :cases_under_investigation, 
            'total_firs_solved': total_firs_solved,  
            'total_csrs_solved': total_csrs_solved
    }
    return render(request, 'police.html',context)

@login_required(login_url='landing_page')
def police_incharge_home(request):
    pi = request.user.station_name
    station = police_station_master.objects.get(station_name=pi)
    total_complaints = complaint_master.objects.filter(station_name=station).count()
    total_pending_complaints = complaint_master.objects.filter(station_name=station,status='Pending').count()
    total_firs= fir_master.objects.filter(station_name=station).count()
    total_csrs= csr_master.objects.filter(station_name=station).count()
    total_csrs_under_investigation= csr_master.objects.filter(station_name=station,status="CSR is Filed").count()
    total_firs_under_investigation= fir_master.objects.filter(station_name=station,status="FIR is Filed").count()
    cases_under_investigation= total_firs_under_investigation + total_csrs_under_investigation

    context = {
        'total_complaints' : total_complaints,
        'total_pending_complaints' : total_pending_complaints,
        'total_firs' : total_firs,
        'total_csrs' : total_csrs,
        'cases_under_investigation' : cases_under_investigation
    }
    return render(request, 'police_incharge.html',context)

@login_required(login_url='landing_page')
def manage_complaint(request,complaint_id):
    print(complaint_id)
    complaints = complaint_master.objects.get(complaint_id=complaint_id)
    has_image = complaints.evidence_image
    context = {
        'complaints':complaints,
        'complaint_id': complaint_id,
        'has_image': has_image
    }
    return render(request, 'manage_complaint.html',context)

@login_required(login_url='landing_page')
def police_incharge_view_complaint(request):
    # print("view called")
    complaints = complaint_master.objects.filter(station_name=request.user.station_name).order_by('-complaint_id')
    context = {'complaints':complaints}
    return render(request, 'police_incharge_view_complaint.html',context)


def register_fir_csr(request):
    if request.method == 'POST':
        complaint_type = request.POST.get('complaint_type')        
        complaint_id = request.POST.get('complaint_id')
        print(f"complaint_id: {complaint_type}")   
        complainant_name = request.POST.get('name')
        complainant_gender = request.POST.get('gender')
        complainant_contact_no = request.POST.get('contact_no')
        complainant_email = request.POST.get('email')
        complainant_dob = complaint_master.objects.get(complaint_id=complaint_id).complainant_dob
        complainant_address = complaint_master.objects.get(complaint_id=complaint_id).complainant_address
        get_complainant_state_name = request.POST.get('complainant_state_name')
        complainant_state_name = state_master.objects.get(state_name=get_complainant_state_name)
        complainant_state_id = state_master.objects.get(state_name=get_complainant_state_name).state_id
        get_complainant_district_name = request.POST.get('complainant_district_name')
        complainant_district_name = district_master.objects.get(district_name=get_complainant_district_name)
        complainant_district_id = district_master.objects.get(district_name=get_complainant_district_name).district_id
        complainant_pin_code = request.POST.get('pincode')
        get_state_name = request.POST.get('state_name')
        state_name = state_master.objects.get(state_name=get_state_name)
        state_id = state_master.objects.get(state_name=get_state_name).state_id
        get_district_name = request.POST.get('district_name')
        district_name = district_master.objects.get(district_name=get_district_name)
        district_id = district_master.objects.get(district_name=get_district_name).district_id
        get_station_name = request.POST.get('station_name')
        station_name = police_station_master.objects.get(station_name=get_station_name)
        station_id = police_station_master.objects.get(station_name=get_station_name).station_id
        crime_category = crime_category_master.objects.get(crime_category_name=request.POST.get('crime_category'))
        other_crime_category = request.POST.get('other_crime_category')
        subject = request.POST.get('subject')
        detailed_description = complaint_master.objects.get(complaint_id=complaint_id).detailed_description
        delay_reason = complaint_master.objects.get(complaint_id=complaint_id).delay_reason
        reporting_date_time = complaint_master.objects.get(complaint_id=complaint_id).created_at
        print(delay_reason)

        datetime_of_occurence = complaint_master.objects.get(complaint_id=complaint_id).datetime_of_occurence


        place_of_occurence = request.POST.get('place_of_occurence')
        evidence_image = complaint_master.objects.get(complaint_id=complaint_id).evidence_image
        info_by_station_incharge = request.POST.get('info_by_incharge')
        if(complaint_type == 'fir'):
            fir_no = request.POST.get('fir_no')
            act_and_sections = request.POST.get('act_and_sections')
            gd_number = request.POST.get('gd_number')
            type_of_information = request.POST.get('type_of_information')
            nearest_identifiable_place = request.POST.get('nearby_place')
            direction_and_distance_from_ps = request.POST.get('dist_from_ps')
            complaintant_religion = request.POST.get('complainant_religion')
            complaintant_caste = request.POST.get('complainant_caste')
            sus_acu_details = request.POST.get('sus_acu_details')
            properties_involved = request.POST.get('property_involved')
            property_value = request.POST.get('property_value')

            fir = fir_master.objects.create(
            fir_no = fir_no,
            complainant_name = complainant_name,
            complainant_gender = complainant_gender,
            complainant_contact_no = complainant_contact_no,
            complainant_email = complainant_email,
            complainant_dob = complainant_dob,
            complainant_address = complainant_address,
            complainant_state_name = complainant_state_name,
            complainant_state_id = complainant_state_id,
            complainant_district_name = complainant_district_name,
            complainant_district_id = complainant_district_id,
            complainant_pin_code = complainant_pin_code,
            state_name = state_name,
            state_id = state_id,
            district_name = district_name,
            district_id = district_id,
            station_name = station_name,
            station_id = station_id,
            status = "FIR is Filed",
            crime_category = crime_category,
            other_crime_category = other_crime_category,
            subject = subject,
            fir_detailed_description = detailed_description,
            delay_reason = delay_reason,
            datetime_of_occurence = datetime_of_occurence,
            place_of_occurence = place_of_occurence,
            evidence_image = evidence_image,
            info_by_station_incharge = info_by_station_incharge,
            gd_number = gd_number,
            act_and_sections = act_and_sections,
            type_of_information = type_of_information,
            nearest_identifiable_place = nearest_identifiable_place,
            direction_and_distance_from_ps = direction_and_distance_from_ps,
            complaintant_religion = complaintant_religion,
            complaintant_caste = complaintant_caste,
            sus_acu_details = sus_acu_details,
            properties_involved = properties_involved,
            property_value = property_value,
            created_at = timezone.now(),
            updated_at = timezone.now(),
            reporting_date_time=reporting_date_time
            )
            complaint = complaint_master.objects.get(complaint_id=complaint_id)
            complaint.status = "FIR is Filed"
            complaint.save()
            return redirect('police_incharge_view_complaint')



        elif(complaint_type == 'csr'):
            csr_no = request.POST.get('csr_no')
            print(csr_no)
            csr = csr_master.objects.create(
                csr_no=csr_no,
                complainant_name = complainant_name,
                complainant_gender = complainant_gender,
                complainant_contact_no = complainant_contact_no,
                complainant_email = complainant_email,
                complainant_dob = complainant_dob,
                complainant_address = complainant_address,
                complainant_state_name = complainant_state_name,
                complainant_state_id = complainant_state_id,
                complainant_district_name = complainant_district_name,
                complainant_district_id = complainant_district_id,
                complainant_pin_code = complainant_pin_code,
                state_name = state_name,
                state_id = state_id,
                district_name = district_name,
                district_id = district_id,
                station_name = station_name,
                station_id = station_id,
                status = "CSR is Filed",
                crime_category = crime_category,
                other_crime_category = other_crime_category,
                subject = subject,
                ncr_detailed_description = detailed_description,
                delay_reason = delay_reason,
                datetime_of_occurence = datetime_of_occurence,
                place_of_occurence = place_of_occurence,
                evidence_image = evidence_image,
                info_by_station_incharge = info_by_station_incharge,
                created_at = timezone.now(),
                updated_at = timezone.now(),
                reporting_date_time=reporting_date_time
            )
            print(csr)
            complaint = complaint_master.objects.get(complaint_id=complaint_id)
            complaint.status = "CSR is Filed"
            complaint.save()
            return redirect('police_incharge_view_complaint')
        
        else:
            complaint = complaint_master.objects.get(complaint_id=complaint_id)
            complaint.status = 'Rejected'
            complaint.info_by_station_incharge = info_by_station_incharge
            complaint.save()

            return redirect('police_incharge_view_complaint')
    else:
        return redirect('police_incharge_view_complaint')


def view_fir(request):
    firs = fir_master.objects.filter(station_name=request.user.station_name).order_by('-fir_id')
    context = {
        'firs' : firs
    }
    return render(request, 'view_fir.html',context)


def manage_fir(request,fir_id):
    print(fir_id)
    fir = fir_master.objects.get(fir_id=fir_id)
    print(fir.subject)
    has_image = fir.evidence_image
    context = {
        'fir':fir,
        'fir_id': fir_id,
        'has_image': has_image
    }

    if request.method == 'POST':
        status = request.POST.get('status')
        info_by_incharge = request.POST.get('info_by_incharge')
        if "Completed" in status:
            fir = fir_master.objects.get(fir_id=fir_id)
            fir.status = "Completed"
            fir.info_by_station_incharge = info_by_incharge
            fir.save()
            return redirect('view_fir')

        else:
            fir = fir_master.objects.get(fir_id=fir_id)
            fir.info_by_station_incharge = info_by_incharge
            fir.save()
            return redirect('view_fir')

    else:
        return render(request, 'manage_fir.html',context)

def view_csr(request):
    csrs = csr_master.objects.filter(station_name=request.user.station_name).order_by('-csr_id')
    context = {
        'csrs' : csrs
    }
    return render(request, 'view_csr.html',context)

def manage_csr(request,csr_id):
    print(csr_id)
    csr = csr_master.objects.get(csr_id=csr_id)
    has_image = csr.evidence_image
    context = {
        'csr':csr,
        'csr_id': csr_id,
        'has_image': has_image
    }
    if request.method == 'POST':
        status = request.POST.get('status')
        info_by_incharge = request.POST.get('info_by_incharge')
        if "Completed" in status:
            csr = csr_master.objects.get(csr_id=csr_id)
            csr.info_by_station_incharge = info_by_incharge
            csr.status = "Completed"
            csr.save()
            return redirect('view_csr')

        else:
            csr = csr_master.objects.get(csr_id=csr_id)
            csr.info_by_station_incharge = info_by_incharge
            csr.save()
            return redirect('view_csr')
    return render(request,'manage_csr.html',context)


def view_only_csr(request,csr_id):
    csr = csr_master.objects.get(csr_id=csr_id)
    has_image = csr.evidence_image
    context = {
        'csr':csr,
        'csr_id': csr_id,
        'has_image': has_image
    }
    return render(request,'view_only_csr.html',context)

def view_only_firs(request):
    firs = fir_master.objects.filter(station_name=request.user.station_name).order_by('-fir_id')
    context = {
        'firs' : firs
    }

    return render(request,'view_only_firs.html',context)

def view_only_fir(request,fir_id):
    fir = fir_master.objects.get(fir_id=fir_id)
    print(fir.subject)
    has_image = fir.evidence_image
    context = {
        'fir':fir,
        'fir_id': fir_id,
        'has_image': has_image
    }
    return render(request,'view_only_fir.html',context)

def view_only_csrs(request):
    csrs = csr_master.objects.filter(station_name=request.user.station_name).order_by('-csr_id')
    context = {
        'csrs' : csrs
    }
    return render(request,'view_only_csrs.html',context)


def user_view_complaints(request):
    complaints = complaint_master.objects.filter(complainant_email=request.user.email).order_by('-complaint_id')
    context = {'complaints':complaints}
    return render(request,'user_view_complaints.html',context)

def user_view_complaint(request,complaint_id):
    complaints = complaint_master.objects.get(complaint_id=complaint_id)
    has_image = complaints.evidence_image
    status = complaints.status
    context = {
        'complaints':complaints,
        'complaint_id': complaint_id,
        'has_image': has_image,
        'status': status,
    }
    return render(request,'user_view_complaint.html',context)


def user_view_firs(request):
    firs = fir_master.objects.filter(complainant_email=request.user.email).order_by('-fir_id')
    context = {
        'firs' : firs
    }

    return render(request,'user_view_firs.html',context)

def user_view_fir(request,fir_id):
    fir = fir_master.objects.get(fir_id=fir_id)
    print(fir.subject)
    has_image = fir.evidence_image
    context = {
        'fir':fir,
        'fir_id': fir_id,
        'has_image': has_image
    }
    return render(request,'user_view_fir.html',context)


def user_view_csrs(request):
    csrs = csr_master.objects.filter(complainant_email=request.user.email).order_by('-csr_id')
    context = {
        'csrs' : csrs
    }

    return render(request,'user_view_csrs.html',context)

def user_view_csr(request,csr_id):
    csr = csr_master.objects.get(csr_id=csr_id)
    has_image = csr.evidence_image
    context = {
        'csr':csr,
        'csr_id': csr_id,
        'has_image': has_image
    }
    return render(request,'user_view_csr.html',context)


def police_view_only_firs(request):
    firs = fir_master.objects.filter(station_name=request.user.station_name).order_by('-fir_id')
    context = {
        'firs' : firs
    }
    return render(request,'police_view_only_firs.html',context)

def police_view_only_fir(request,fir_id):
    fir = fir_master.objects.get(fir_id=fir_id)
    print(fir.subject)
    has_image = fir.evidence_image
    context = {
        'fir':fir,
        'fir_id': fir_id,
        'has_image': has_image
    }
    return render(request,'police_view_only_fir.html',context)

def police_view_only_csrs(request):
    csrs = csr_master.objects.filter(station_name=request.user.station_name).order_by('-csr_id')
    context = {
        'csrs' : csrs
    }
    return render(request,'police_view_only_csrs.html',context)

def police_view_only_csr(request,csr_id):
    csr = csr_master.objects.get(csr_id=csr_id)
    has_image = csr.evidence_image
    context = {
        'csr':csr,
        'csr_id': csr_id,
        'has_image': has_image
    }
    return render(request,'police_view_only_csr.html',context)

def police_manage_csrs(request):
    csrs = csr_master.objects.filter(station_name=request.user.station_name).order_by('-csr_id')
    context = {
        'csrs' : csrs
    }
    return render(request,'police_manage_csrs.html',context)

def police_manage_csr(request,csr_id):
    print(csr_id)
    csr = csr_master.objects.get(csr_id=csr_id)
    has_image = csr.evidence_image
    context = {
        'csr':csr,
        'csr_id': csr_id,
        'has_image': has_image
    }
    if request.method == 'POST':
        status = request.POST.get('status')
        info_by_incharge = request.POST.get('info_by_incharge')
        if "Completed" in status:
            csr = csr_master.objects.get(csr_id=csr_id)
            csr.info_by_station_incharge = info_by_incharge
            csr.status = "Completed"
            csr.save()
            return redirect('view_csr')

        else:
            csr = csr_master.objects.get(csr_id=csr_id)
            csr.info_by_station_incharge = info_by_incharge
            csr.save()
            return redirect('view_csr')
    return render(request,'police_manage_csr.html',context)








def police_manage_firs(request):
    firs = fir_master.objects.filter(station_name=request.user.station_name).order_by('-fir_id')
    context = {
        'firs' : firs
    }
    return render(request,'police_manage_firs.html',context)

def police_manage_fir(request,fir_id):
    fir = fir_master.objects.get(fir_id=fir_id)
    print(fir.subject)
    has_image = fir.evidence_image
    context = {
        'fir':fir,
        'fir_id': fir_id,
        'has_image': has_image
    }
    if request.method == 'POST':
        status = request.POST.get('status')
        info_by_incharge = request.POST.get('info_by_incharge')
        if "Completed" in status:
            fir = fir_master.objects.get(fir_id=fir_id)
            fir.status = "Completed"
            fir.info_by_station_incharge = info_by_incharge
            fir.save()
            return redirect('view_fir')

        else:
            fir = fir_master.objects.get(fir_id=fir_id)
            fir.info_by_station_incharge = info_by_incharge
            fir.save()
            return redirect('view_fir')

    else:
        return render(request,'police_manage_fir.html',context)
    


def user_manage_profile(request):
    states = state_master.objects.all()
    districts = district_master.objects.filter(state_name=request.user.state) 
    context = {
        'states': states,
        'districts': districts,
    }
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        gender = request.POST.get('gender')
        aadhaarno = request.POST.get('aadhaarno')
        Phone_Number = request.POST.get('phoneNumber')
        pincode = request.POST.get('pinCode')
        state = request.POST.get('complainant_state')
        district = request.POST.get('complainant_district')
        address = request.POST.get('address')


        user_id = request.user.user_id
        print(user_id)
        user = CustomUser.objects.get(user_id=user_id)
        user.email =  email
        user.first_name = first_name
        user.last_name =  last_name
        user.gender = gender
        user.aadhaarno = aadhaarno
        user.Phone_Number =  int(Phone_Number)
        user.pincode =  pincode
        user.state = state_master.objects.get(state_name=state)
        user.district = district_master.objects.get(district_name=district)
        user.address =  address
        image_changed = request.POST.get('image_changed')
        if image_changed == "changed":
            profile_image = request.FILES.get('profile_image')
            user.profile_image =  profile_image
        user.save()


        return redirect('/user')
    return render(request,'user_manage_profile.html',context)


def police_incharge_manage_profile(request):
    states = state_master.objects.all()
    districts = district_master.objects.filter(state_name=request.user.state) 

    context = {
        'states': states,
        'districts': districts,
    }
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        gender = request.POST.get('gender')
        aadhaarno = request.POST.get('aadhaarno')
        Phone_Number = request.POST.get('phoneNumber')
        pincode = request.POST.get('pinCode')
        state = request.POST.get('pi_state')
        print(" -----------",state)
        district = request.POST.get('pi_district')
        address = request.POST.get('address')

        user_id = request.user.incharge_id
        print(user_id)
        user = police_incharge.objects.get(incharge_id=user_id)
        user.first_name = first_name
        user.last_name =  last_name
        user.gender = gender
        user.aadhaarno = aadhaarno
        user.Phone_Number =  int(Phone_Number)
        user.pincode =  pincode
        user.state = state_master.objects.get(state_name=state)
        user.district = district_master.objects.get(district_name=district)
        user.address =  address
        image_changed = request.POST.get('image_changed')
        if image_changed == "changed":
            profile_image = request.FILES.get('profile_image')
            user.profile_image =  profile_image
        user.save()


        return redirect('/police_incharge_home')
    return render(request,'police_incharge_manage_profile.html',context)


def police_manage_profile(request):
    states = state_master.objects.all()
    districts = district_master.objects.filter(state_name=request.user.state) 

    context = {
        'states': states,
        'districts': districts,
    }
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        gender = request.POST.get('gender')
        aadhaarno = request.POST.get('aadhaarno')
        Phone_Number = request.POST.get('phoneNumber')
        pincode = request.POST.get('pinCode')
        state = request.POST.get('pstate')
        district = request.POST.get('pdistrict')
        address = request.POST.get('address')

        user_id = request.user.police_id
        print(user_id)
        user = police_officer.objects.get(police_id=user_id)
        user.first_name = first_name
        user.last_name =  last_name
        user.gender = gender
        user.aadhaarno = aadhaarno
        user.Phone_Number =  int(Phone_Number)
        user.pincode =  pincode
        user.state = state_master.objects.get(state_name=state)
        user.district = district_master.objects.get(district_name=district)
        user.address =  address
        image_changed = request.POST.get('image_changed')
        if image_changed == "changed":
            profile_image = request.FILES.get('profile_image')
            user.profile_image =  profile_image
        user.save()


        return redirect('/police')
    return render(request,'police_manage_profile.html',context)


def view_complaints_for_feedbacks(request):
    email = request.user.email
    completed_firs = fir_master.objects.filter(complainant_email=email,status="Completed")
    completed_csrs = csr_master.objects.filter(complainant_email=email,status="Completed")
    context = {
        'completed_firs':completed_firs,
        'completed_csrs':completed_csrs
    }
    return render(request,'view_complaints_for_feedbacks.html',context)

def feedback(request, id, type):
    if request.method == 'POST':
        if type == "fir":
            fir = fir_master.objects.get(fir_id=id)
            feedback = request.POST.get('Feedback')
            print(feedback)
            fir.feedback = feedback
            fir.save()
            return redirect('view_complaints_for_feedbacks')
        else:
            csr = csr_master.objects.get(csr_id=id) # Changed fir_id to csr_id
            feedback = request.POST.get('Feedback')
            csr.feedback = feedback
            csr.save()
            return redirect('view_complaints_for_feedbacks')
    return render(request,'feedback.html')




def view_announcements(request):
    temp_announcements = announcements.objects.all()
    context = {
        'announcements' : temp_announcements
    }
    return render(request, 'police_incharge_announcements.html',context)

def view_announcement(request, id):
    temp_announcement = announcements.objects.get(announcement_id=id)
    has_image = temp_announcement.image
    context = {
        'announcement': temp_announcement,
        'announcement_id': temp_announcement.announcement_id,
        'has_image': has_image
    }

    return render(request, 'police_incharge_announcement.html', context)

def user_announcements(request):
    temp_announcements = announcements.objects.all()
    context = {
        'announcements' : temp_announcements
    }
    return render(request, 'user_announcements.html',context)

def user_announcement(request, id):
    temp_announcement = announcements.objects.get(announcement_id=id)
    has_image = temp_announcement.image
    context = {
        'announcement': temp_announcement,
        'announcement_id': temp_announcement.announcement_id,
        'has_image': has_image
    }

    return render(request, 'user_announcement.html', context)

def police_announcements(request):
    temp_announcements = announcements.objects.all()
    context = {
        'announcements' : temp_announcements
    }
    return render(request, 'police_announcements.html',context)

def police_announcement(request, id):
    temp_announcement = announcements.objects.get(announcement_id=id)
    has_image = temp_announcement.image
    context = {
        'announcement': temp_announcement,
        'announcement_id': temp_announcement.announcement_id,
        'has_image': has_image
    }

    return render(request, 'police_announcement.html', context)
