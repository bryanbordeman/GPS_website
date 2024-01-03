from django.shortcuts import render, redirect
from .forms import RequestForm
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.conf import settings

# quench calculator 
from django.http import HttpResponse
from .scripts.ge_quench_vent_calculator import GEQuench
from .scripts.hitachi_quench_vent_calculator import HitachiQuench
from .scripts.radiation_shielding_swing_door_calculator_website import Door
import json

from django.shortcuts import render
from django.views.decorators.http import require_GET


@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Allow: /",
        # "Sitemap: http://www.global-shielding.com/sitemap.xml",
        "Sitemap: http://127.0.0.1:8000/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

def home(request):
    page_title = 'Home'
    context = {'page_title' : page_title, }
	
    return render(request, 'global/home.html', context)

def about_us(request):
    page_title = 'About Us'
    context = {'page_title' : page_title, }
	
    return render(request, 'global/about_us.html', context)

def quench_vent(request):
    page_title = 'Quench Vent Systems'
    context = {'page_title' : page_title, }

    return render(request, 'global/quench_vent.html', context)

def request_quote(request):
    page_title = 'Request A Quote'

    form = RequestForm()
    
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            email = request.POST.get('email', '')
            phone = request.POST.get('phone', '')
            description = request.POST.get('description', '')
        
            email_message = f'Name = {first_name} {last_name}\nEmail = {email}\nPhone = {phone}\nMessage = {description}\n'

            try:
                send_mail(f'Global Partners in Shielding, Inc. Website {first_name} {last_name}', email_message, settings.EMAIL_HOST_USER, ['inquiry@shieldingsystems.com'], fail_silently=False)
                form.save()
                messages.success(request, 'Request was successfully sent')
                return redirect('home') #need to redirect with id to project profile
            except BadHeaderError:
                messages.warning(request, 'Request error. Please try again')
                return redirect('request_quote')
        else:
            messages.warning(request, 'Request error. Please try again')
            return redirect('request_quote') #

    context = {'page_title' : page_title, 'form' : form,}

    return render(request, 'global/request_quote.html', context)

def rf_shielding(request):
    page_title = 'MRI/RF Shielding'

    context = {'page_title' : page_title}
    return render(request, 'global/rf_shielding.html', context)

def rf_chambers(request):
    page_title = 'RF Chambers'
    
    context = {'page_title' : page_title}
    return render(request, 'global/rf_chambers.html', context)

def lead_enclosures(request):
    page_title = 'Lead Shielded Enclosures'
    
    context = {'page_title' : page_title}
    return render(request, 'global/lead_enclosures.html', context)

def radiation_shielding(request):
    page_title = 'Radiation Shielding'
    context = {'page_title' : page_title, }
	
    return render(request, 'global/radiation_shielding.html', context)

def therapy_shielding(request):
    page_title = 'Radiation Therapy Shielding'
    context = {'page_title' : page_title, }
	
    return render(request, 'global/therapy_shielding.html', context)

def services_rf_testing(request):
    page_title = 'Services RF Testing'
    context = {'page_title' : page_title, }
	
    return render(request, 'global/services_rf_testing.html', context)

def services_engineering(request):
    page_title = 'Services Engineering'
    context = {'page_title' : page_title, }
	
    return render(request, 'global/services_engineering.html', context)

def services_door(request):
    page_title = 'Services Door Service'
    context = {'page_title' : page_title, }
	
    return render(request, 'global/services_door.html', context)

def scif_shielding(request):
    page_title = 'SCIF Shielding'
    context = {'page_title' : page_title, }
	
    return render(request, 'global/scif_shielding.html', context)

def pd_shielding(request):
    page_title = 'PD Shielding'
    context = {'page_title' : page_title, }
	
    return render(request, 'global/pd_shielding.html', context)

def ac_shielding(request):
    page_title = 'AC ELF Shielding'
    context = {'page_title' : page_title, }
	
    return render(request, 'global/ac_shielding.html', context)

def careers(request):
    page_title = 'Careers'
    context = {'page_title' : page_title, }
	
    return render(request, 'global/careers.html', context)


def quenchCalc(request):
    # collect inputs
    field = request.POST['field']
    magnet =request.POST['magnet']
    comp_list = request.POST['comp_list']
    strght_list =request.POST['strght_list']

    if strght_list == '':
        return None
    else:

        # convert to list
        comp_list = list(comp_list.split(","))
        strght_list = list(strght_list.split(","))

        # change str to int
        for i in range(0, len(comp_list)):
            comp_list[i] = int(comp_list[i])
        for i in range(0, len(strght_list)):
            strght_list[i] = int(strght_list[i])
    
        # convert to int for calc. input
        if field == "1.5T":
            field = 1
            request_field = "1.5T"
        else:
            field = 2
            request_field = "3.0T"

        pipe_size = ''
        request_pipe_size = ''
        total_length = ''


        if magnet == "GE":
        # check field type for max pressure variable
            if  field == 1:
                max_pressure = 17
            elif field == 2:
                max_pressure = 20
            
            quench_run = GEQuench(comp_list, strght_list, field)
            display_list =['0-20 feet = ', '20-40 feet = ', '40-60 feet = ', '60-80 feet = ', '80-100 feet = ']
            for i in range(len(quench_run.pipe_size_location_list)):
                if quench_run.pipe_size_location_list[i] != 0:
                    pipe_size += '<p class="m-0" >' + str(display_list[i]) + str(quench_run.pipe_size_location_list[i]) + "</p>"
            pressure_drop = round(quench_run.total_pressure,2)
        
        elif magnet == "Hitachi":
            quench_run = HitachiQuench(comp_list, strght_list, field)
            display_list = ['4" dia pipe', '6" dia pipe', '8" dia pipe']
            parts_list = ['Straight', '45 deg. Elbow', '90 deg. Elbow']
            for i in range(len(quench_run.comp_list)):
                pipe_size += '<p class="m-0" >' + str(i+1) + '- ' + str(parts_list[quench_run.comp_list[i] - 1] + ' = ' + display_list[quench_run.pipe_size_list[i]]) + '</p>'
                request_pipe_size += str(i+1) + '- ' + str(parts_list[quench_run.comp_list[i] - 1] + ' = ' + display_list[quench_run.pipe_size_list[i]]) + '\n'
            pressure_drop = (str(round(quench_run.total_perc * 100, 2)))
            total_length = ('Total Length = ' + str(round(quench_run.total_lgt, 2)) + ' Feet')

            max_pressure = 100

        request = f'Please quote me the following Quench Vent:\nMagnet Vendor = {magnet}\nField Strength = {request_field}\n{request_pipe_size}'

        # output
        # pressure_drop = round(quench_run.total_pressure,2)

        data_response = {'total_length':total_length, 'pressure_drop': pressure_drop, 
                            'pipe_size' : pipe_size, 'max_pressure': max_pressure, 'request' : request} 
        # print (data_response)
        return HttpResponse(json.dumps(data_response))

def radDoorCalc(request):
    # collect inputs
    pbThickness = request.POST['pbThickness']
    bpeThickness = request.POST['bpeThickness']

    if pbThickness == '': #if user does not have lead set var to 0
        pbThickness = 0
        door= Door(float(pbThickness),float(bpeThickness))
    elif bpeThickness == '': #if user does not have BPE set var to 0
        bpeThickness = 0
        door= Door(float(pbThickness),float(bpeThickness))
    else:
        door= Door(float(pbThickness),float(bpeThickness))
    
    hinge = door.hinge_size.item_number
    operator = door.operator.item_number
    width = round(door.total_door_leaf_width, 2)
    height = round(door.DOOR_LEAF_HEIGHT, 2)
    thickness = round(door.door_leaf_thickness, 2)
    weight = round(door.door_leaf_actual_weight, 2)
    lead = door.door_lead_shielding
    lead_weight = round(door.lead_total_weight, 2)
    bpe = door.door_bpe_shielding
    radial_load = door.max_radial_load
    ansi_closing_time = door.ansi_closing_time

    request = f'Please quote me the following 48" x 84" clear opening door:\nLead Thickness = {lead}" ({lead_weight} lbs)\nBPE Thickness = {bpe}"\nDoor Width = {width}"\nDoor Height = {height}"\nDoor Thickness = {thickness}\nHinge = {hinge}\nOperator = {operator}'
    
    data_response = {'hinge': hinge, 'operator': operator, 'width': width, 
                    'height': height, 'thickness': thickness, 'weight': weight, 
                    'lead': lead, 'lead_weight': lead_weight, 'bpe': bpe,
                    'radial_load': radial_load, 'ansi_closing_time': ansi_closing_time, 'request' : request} 

    return HttpResponse(json.dumps(data_response))

def ground_alarm(request):
    page_title = 'Ground Alarm'
    
    context = {'page_title' : page_title}
    return render(request, 'global/ground_alarm.html', context)