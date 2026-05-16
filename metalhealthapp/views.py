from django.shortcuts import render
from .models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import datetime

# Create your views here.

def index(request):
	return render(request,'index.html')
def about(request):
	return render(request,'about.html')
def login(request):
	if request.method=="POST":
		email=request.POST["email"]
		password=request.POST["pswd"]
		chk=Tbl_User.objects.filter(email=email, pswd=password,user_type="admin")
		chk1=Tbl_User.objects.filter(email=email, pswd=password,user_type="user")
		chk2=Tbl_User.objects.filter(email=email, pswd=password,user_type="doctor")

		if chk:
			for x in chk:
				request.session['id'] = x.id
			return render(request,'Admin/admin_home.html')
		elif chk1:
			for x in chk1:
				request.session['id'] = x.id
			return render(request,'User/user_home.html')
		elif chk2:
			for x in chk2:
				request.session['id'] = x.id
			return render(request,'Doctor/doctor_home.html')
		else:
			return render(request,'login.html', {'msg': 'Invalid login credentials.!'})
	else:
		return render(request,'login.html')
def user_reg(request):
	if request.method=="POST":
		name=request.POST['name']
		gender=request.POST['gender']
		phone=request.POST['phone']
		dob=request.POST['dob']
		address=request.POST['address']
		email=request.POST['email']
		pswd=request.POST['pswd']
		aa=Tbl_User(name=name,gender=gender,phone=phone,dob=dob,address=address,email=email,pswd=pswd,status='pending',user_type='user')
		aa.save()
		return render(request,'user_reg.html')
	else:
		return render(request,'user_reg.html')
def doctor_reg(request):
	if request.method=="POST":
		name=request.POST['name']
		gender=request.POST['gender']
		phone=request.POST['phone']
		dob=request.POST['dob']
		address=request.POST['address']
		email=request.POST['email']
		pswd=request.POST['pswd']
		aa=Tbl_User(name=name,gender=gender,phone=phone,dob=dob,address=address,email=email,pswd=pswd,status='pending',user_type='doctor')
		aa.save()
		return render(request,'doctor_reg.html')
	else:
		return render(request,'doctor_reg.html')
def logout(request):
    if request.session.has_key('id'):
        del request.session['id']
        logout(request)
    return HttpResponseRedirect('/')

#-------------------------Admin-------------------------------
def admin_home(request):
	return render(request,'Admin/admin_home.html')
def admin_view_users(request):
	var=Tbl_User.objects.all().filter(user_type='user',status='pending')
	return render(request,'Admin/admin_view_users.html',{'var':var})
def admin_user_approve(request):
	ii=request.GET['id']
	var=Tbl_User.objects.all().filter(id=ii).update(status='approved')
	return HttpResponseRedirect('/admin_view_users/')
def admin_user_reject(request):
	ii=request.GET['id']
	var=Tbl_User.objects.all().filter(id=ii).update(status='rejected')
	return HttpResponseRedirect('/admin_view_users/')
def admin_approved_users(request):
	var=Tbl_User.objects.all().filter(status='approved',user_type='user')
	return render(request,'Admin/admin_approved_users.html',{'var':var})
def admin_rejected_users(request):
	var=Tbl_User.objects.all().filter(status='rejected',user_type='user')
	return render(request,'Admin/admin_rejected_users.html',{'var':var})
def admin_view_doctors(request):
	var=Tbl_User.objects.all().filter(user_type='doctor',status='pending')
	return render(request,'Admin/admin_view_doctors.html',{'var':var})
def admin_doctor_approve(request):
	ii=request.GET['id']
	var=Tbl_User.objects.all().filter(id=ii).update(status='approved')
	return HttpResponseRedirect('/admin_view_doctors/')
def admin_doctor_reject(request):
	ii=request.GET['id']
	var=Tbl_User.objects.all().filter(id=ii).update(status='rejected')
	return HttpResponseRedirect('/admin_view_doctors/')
def admin_approved_doctor(request):
	var=Tbl_User.objects.all().filter(status='approved',user_type='doctor')
	return render(request,'Admin/admin_approved_doctor.html',{'var':var})
def admin_rejected_doctor(request):
	var=Tbl_User.objects.all().filter(status='rejected',user_type='doctor')
	return render(request,'Admin/admin_rejected_doctor.html',{'var':var})

from django.shortcuts import render, redirect
from .models import *
import random

def admin_view_questions(request):

    # ADD ADMIN QUESTION
    if request.method == "POST":

        question = request.POST.get('question')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')

        Tbl_Question.objects.create(
            question=question,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            question_type='Admin'
        )

        return redirect('admin_view_questions')


    # AI GENERATED QUESTIONS
    if 'ai_question' in request.GET:

        ai_questions = [
            "Do you feel stressed frequently?",
            "Do you have trouble sleeping?",
            "Do you feel lonely sometimes?",
            "Do you lose interest in daily activities?",
            "Do you feel anxious in crowded places?",
            "Do you overthink a lot?",
            "Do you feel emotionally tired?",
            "Do you feel comfortable sharing feelings?"
        ]

        q = random.choice(ai_questions)

        Tbl_Question.objects.create(
            question=q,
            option1='Yes',
            option2='No',
            option3='Sometimes',
            option4='Often',
            question_type='AI'
        )

        return redirect('admin_view_questions')


    # DELETE QUESTION
    if 'delete_id' in request.GET:

        did = request.GET.get('delete_id')
        Tbl_Question.objects.get(id=did).delete()

        return redirect('admin_view_questions')


    var = Tbl_Question.objects.all()

    return render(request, 'Admin/admin_view_questions.html', {'var': var})

def admin_feedback(request):
	var=Tbl_Feedback.objects.all()
	return render(request,'Admin/admin_feedback.html',{'var':var})
def admin_view_result(request):

    # NOT FORWARDED
    var = Tbl_result.objects.filter(
        doctor="0"
    ).exclude(
        status='Normal'
    ).order_by('-id')

    # NORMAL USERS
    nl = Tbl_result.objects.filter(
        status='Normal'
    )

    # FORWARDED USERS
    fw = Tbl_result.objects.exclude(
        doctor="0"
    ).order_by('-id')

    # DOCTORS
    doc = Tbl_User.objects.filter(
        user_type='doctor'
    )

    return render(
        request,
        'Admin/admin_view_result.html',
        {
            'var': var,
            'doc': doc,
            'nl': nl,
            'fw': fw
        }
    )
def resultpdf(request):

    i = request.GET['id']

    result = Tbl_result.objects.get(id=i)

    total = int(result.total)

    # STATUS CHECKING

    if total <= 80:

        result.status = 'Normal'

        result.suggestion = 'Maintain a healthy lifestyle and positive mindset.'

    elif total > 80 and total <= 120:

        result.status = 'Moderate'

        result.suggestion = 'Stress management and relaxation activities are recommended.'

    else:

        result.status = 'Strong'

        result.suggestion = 'Professional mental healthcare consultation is recommended.'

    result.save()

    return render(
        request,
        'Admin/pdf.html',
        {'var': [result]}
    )
def forward(request):
    if request.method=="POST":
        name            =request.POST["idd"]
        doc           =request.POST["ans"]
        a=Tbl_result.objects.all().filter(id=name).update(doctor=doc)
        return HttpResponseRedirect('/admin_view_result/')
def remove_normal_user(request):
	ii=request.GET['id']
	var=Tbl_result.objects.all().filter(id=ii)
	var.delete()
	return HttpResponseRedirect('/admin_view_result/')
def admin_view_report(request):

    var = Tbl_result.objects.all().exclude(
        doctor="0"
    )

    return render(
        request,
        'Admin/admin_view_report.html',
        {'var': var}
    )

#---------------------User----------------------------------------
def user_home(request):
	return render(request,'User/user_home.html')
def user_profile(request):
	myid=request.session['id']
	var=Tbl_User.objects.all().filter(id=myid)
	return render(request,'User/user_profile.html',{'var':var})
def user_editprofile(request):
	myid=request.session['id']
	var=Tbl_User.objects.all().filter(id=myid)
	if request.method=="POST":
		phone=request.POST['phone']
		address=request.POST['address']
		email=request.POST['email']
		pswd=request.POST['pswd']
		aa=Tbl_User.objects.all().filter(id=myid).update(phone=phone,address=address,email=email,pswd=pswd)
		return HttpResponseRedirect('/user_profile/')
	else:
		return render(request,'User/user_editprofile.html',{'var':var})
def user_feedback(request):
	myid=request.session['id']
	var=Tbl_User.objects.all().filter(id=myid)
	if request.method=="POST":
		feedback=request.POST['feedback']
		date=datetime.date.today()
		uid=Tbl_User.objects.get(id=myid)
		aa=Tbl_Feedback(user_id=uid,feedback=feedback,date=date,status='pending')
		aa.save()
		txt="""<script>alert('success...');window.location='/user_feedback/';</script>"""
		return HttpResponse(txt)
	else:
		return render(request,'User/user_feedback.html',{'var':var})
def user_selfcorner(request):
	myid=request.session['id']
	if request.method=="POST":
		uid=Tbl_User.objects.get(id=myid)
		sub=request.POST['sub']
		journal=request.POST['journal']
		date=datetime.date.today()
		aa=Tbl_selfcorner(user_id=uid,sub=sub,journal=journal,date=date)
		aa.save()
		return HttpResponseRedirect('/user_selfcorner/')
	else:
		return render(request,'User/user_selfcorner.html')
def user_view_selfcorner(request):
	myid=request.session['id']
	var=Tbl_selfcorner.objects.all().filter(user_id=myid)
	return render(request,'User/user_view_selfcorner.html',{'var':var})
def user_remove_self(request):
	ii=request.GET['id']
	var=Tbl_selfcorner.objects.all().filter(id=ii)
	var.delete()
	return HttpResponseRedirect('/user_view_selfcorner/')	

def user_test(request):
	var=Tbl_Question.objects.all()
	if request.method == "POST":
		SessionId=request.session['id']
		answer=request.POST.getlist("ans")
		qid=request.POST.getlist("fnameid")
		print(answer,qid)
		uid=Tbl_User.objects.all().get(id=SessionId)
		print(len(answer))
		print(len(qid))
		print(answer[1],qid[1])
		tot=0
		for i in answer:
			tot += int(i)
			print("******************",tot)
		a=Tbl_result(user_ID=uid,answer=answer,total=tot,report_status='pending')
		a.save()
		return HttpResponseRedirect('/user_home/')
	else:
		q=Tbl_Question.objects.all()
		return render(request,'User/user_test.html',{'var':var})
def user_view_result(request):

    uid = request.session['id']

    var = Tbl_result.objects.all().filter(
        user_ID=uid
    ).order_by('id').reverse()

    return render(
        request,
        'User/user_view_result.html',
        {'var': var}
    )
#---------------------Doctor----------------------------------------
def doctor_home(request):
	return render(request,'Doctor/doctor_home.html')
def doctor_profile(request):
	myid=request.session['id']
	var=Tbl_User.objects.all().filter(id=myid)
	return render(request,'Doctor/doctor_profile.html',{'var':var})
def doctor_edit_profile(request):
	myid=request.session['id']
	var=Tbl_User.objects.all().filter(id=myid)
	if request.method=="POST":
		phone=request.POST['phone']
		address=request.POST['address']
		email=request.POST['email']
		pswd=request.POST['pswd']
		aa=Tbl_User.objects.all().filter(id=myid).update(phone=phone,address=address,email=email,pswd=pswd)
		return HttpResponseRedirect('/doctor_profile/')
	else:
		return render(request,'Doctor/doctor_edit_profile.html',{'var':var})
def doctor_feedback(request):
	var=Tbl_Feedback.objects.all()
	return render(request,'Doctor/doctor_feedback.html',{'var':var})
def doctor_view_patient(request):
    ii=request.session['id']
    doc=Tbl_User.objects.all().filter(id=ii)
    for x in doc:
        doctor=x.name
    var=Tbl_result.objects.all().filter(doctor=doctor,report_status='pending')
    st=Tbl_result.objects.all().filter(doctor=doctor,report_status='reported')
    return render(request,'Doctor/doctor_view_patient.html',{'var':var,'st':st})
def doctor_add_report(request):
    ii=request.session['id']
    if request.method=="POST":
        description=request.POST['description']
        idd=request.POST['id']
        var=Tbl_result.objects.all().filter(id=idd).update(description=description,report_status='reported')
        return HttpResponseRedirect('/doctor_view_patient/')
    else:
        idd=request.GET['id']
        return render(request,'Doctor/doctor_add_report.html',{'idd':idd})
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect

def doctor_mail(request):
    patient_id = request.GET['id']

    patient = Tbl_result.objects.get(id=patient_id)

    email = patient.user_ID.email

    print("Sending to:", email)

    subject = 'InnerHour Medical Team'

    message = (
        'Hi, thank you for attending Mental Health care test. '
        'You got appointment from counsellor.'
    )

    email_from = settings.EMAIL_HOST_USER

    send_mail(
        subject,
        message,
        email_from,
        [email],
        fail_silently=False
    )

    print("Mail sent successfully")

    return HttpResponseRedirect('/doctor_view_patient/')

def doctor_view_report(request):
    ii=request.session['id']
    doc=Tbl_User.objects.all().filter(id=ii)
    for x in doc:
        doctor=x.name
    var=Tbl_result.objects.all().filter(doctor=doctor)
    return render(request,'Doctor/doctor_view_report.html',{'var':var})