
from django.shortcuts import *
from django.contrib.auth import *
from django.contrib import *
from django.http import *
from django.urls import reverse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from .data.primary.test1 import TEST_WORDS, TRAINING_WORDS
from .data.primary.test2 import training_sentences, primary_test2_sentences
from .data.primary.test3 import primary_test3_training_questions, primary_test3_main_questions
from .data.primary.test4 import primary_test4_words#, primary_test4_training_words
from .data.secondary.test1 import TRAINING_WORDSـSEC, TEST_WORDS_secondary_test1
from .data.secondary.test2 import secondary_test2_training_questions, main_questions
from .data.primary.test5 import primary_test5_training_questions, primary_test5_main_questions
from .data.secondary.test4 import test4_training_questions, test4_main_questions
from .data.secondary.test3 import secondary_test3_words, secondary_test3_training_words
from .data.primary.test6 import test6_training_questions, test6_main_questions
from .percentile_lookup import lookup_scores_primary, lookup_scores_secondary
import json
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.template.loader import render_to_string
from django.core.mail import send_mail
import time
from django.http import JsonResponse




def index(request):
    return render(request,"index.html")

def about (request):
    return render (request,"about.html")

def help (request):
    return render (request,"help.html")

def contact (request):
    return render (request,"contact.html")

def login (request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            if request.user.is_staff:
                return HttpResponseRedirect("admin")
            else:
                return HttpResponseRedirect("examinerPage")

        else:
            messages.info(request, 'Invalid Username or Password')
            return HttpResponseRedirect("login")
    else:
        return render(request, "login.html")
    

def logout(request):
    auth.logout(request)
    return redirect(reverse('index'))

@login_required(login_url="/login")
def admin (request):
    if request.user.is_staff:
        return render(request,"adminPage.html", {
            "examiners": Examiner.objects.filter(admin_id=request.user.id)
        })
    else:
        return redirect(reverse('login'))


@login_required(login_url="/login")
def signupSuperUser (request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        stage = request.POST['stage']
        name = request.POST['name']
        speciality = request.POST['speciality']
        organization = request.POST['organization']
        
        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username is already taken')
            return HttpResponseRedirect("signupSuperUser")
        else:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            examiner = Examiner.objects.create( name=name, speciality=speciality, organization=organization, stage=stage, user_id=user.id, admin_id=request.user.id)
            examiner.save()
            return HttpResponseRedirect("admin")
        
    else:
        return render (request,"signupSuperUser.html")
    

@login_required(login_url="/login")
def delete(request, id):
    userAccount = User.objects.filter(id=id)

    if request.method == "POST":
        userAccount.delete()

        return redirect(reverse('admin'))

    return render(request, 'adminPage.html')


@login_required(login_url="/login")
def edit(request, id):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        name = request.POST['name']
        speciality = request.POST['speciality']
        organization = request.POST['organization']
        user = Examiner.objects.filter(user_id=id)
        userAccount = User.objects.filter(id=id)
        userDetails = User.objects.get(id=id)
        
        if password:
            userAccount.update(password = make_password(password))
        if User.objects.filter(username=username).exists() and username != userDetails.username:
                messages.info(request, 'Username is already taken')
        else:
            userAccount.update(username = username)

        user.update(name=name, speciality= speciality, organization=organization)

        return redirect(reverse('admin'))
    else:
        return render(request, 'adminPage.html')
    
@login_required(login_url="/login")
def signupStudents (request):
    if request.method == 'POST':
        studentName = request.POST['studentName']
        gender = request.POST['gender']
        schoolName = request.POST['schoolName']
        grade = request.POST['grade']
        civilID = request.POST ['civilID']
        eduDistrict = request.POST['eduDistrict']
        nationality = request.POST['nationality']
        examDate  = request.POST['examDate']
        birthDate = request.POST['birthDate']
        
        #calculate age
        examdate = datetime.strptime(request.POST['examDate'], '%Y-%m-%d')
        birthdate = datetime.strptime(request.POST['birthDate'], '%Y-%m-%d')

        #CCET Manual Method
        e_Day = examdate.day
        e_Month = examdate.month
        e_Year = examdate.year
        b_Day = birthdate.day
        b_Month = birthdate.month
        b_Year = birthdate.year

        if ((e_Day - b_Day) < 0):
            e_Day = e_Day + 30
            e_Month = e_Month - 1
        days = e_Day - b_Day
        if ((e_Month - b_Month) < 0):
            e_Month = e_Month + 12
            e_Year = e_Year - 1
        months = e_Month - b_Month
        years = e_Year - b_Year


        age = str(years) + "/" + str(months) +"/"+str(days)

        if Student.objects.filter(civilID=civilID).exists():
            messages.info(request, 'لقد تم تسجيل الطالب مسبقاً')
            return redirect("signupStudents")
        else:
            student = Student.objects.create(studentName=studentName, gender=gender, schoolName=schoolName, grade=grade, civilID=civilID, eduDistrict=eduDistrict , nationality=nationality, examDate=examDate, birthDate=birthDate,age=age, examiner_id=request.user.id)
            student.save()
            return redirect("examinerPage")
        
    else:
        return render (request,"signupStudents.html", {
           "stage": (Examiner.objects.get(user_id=request.user.id).stage)
    })

@login_required(login_url="/login")
def examinerPage (request):
    request.session['student'] = 0
    examiner = Examiner.objects.filter(user_id=request.user.id).first()  
    stage = examiner.stage if examiner else "" 
    return render(request,"examinerPage.html", {
        "students": Student.objects.filter(examiner_id=request.user.id),  "stage": stage, "examiners": examiner
    })

@login_required(login_url="/login")
def search_results(request):
    print("inside search_results")
    query = request.GET.get('search', '')
    print(f'"query = {query }"')

    all_students = Student.objects.filter(examiner_id=request.user.id)
    if query:
        students = all_students.filter(civilID__icontains=query)
        print(f'"Student at query {students}')
    else:
        students = []
        print(f'"Students at else {students}"')
    context={'students': students}
    return render(request, 'examinerPage.html', context)


@login_required(login_url="/login")
def deleteStudent(request,id):
    studentAccount = Student.objects.filter(id=id)

    if request.method == "POST":
        studentAccount.delete()
        return redirect(reverse('examinerPage'))

    return render(request, "examinerPage.html")

@login_required(login_url="/login")
def editStudent(request, id):
    if request.method == "POST":
        studentName = request.POST['studentName']
        gender = request.POST['gender']
        schoolName = request.POST['schoolName']
        grade = request.POST['grade']
        eduDistrict = request.POST['eduDistrict']
        nationality = request.POST['nationality']
        examDate_str = request.POST['examDate']
        birthDate_str = request.POST['birthDate']

        user = Student.objects.filter(id=id)
        userAccount = Student.objects.filter(examiner_id=id)

        #Update Age
        examdate = datetime.strptime(request.POST['examDate'], '%Y-%m-%d')
        birthdate = datetime.strptime(request.POST['birthDate'], '%Y-%m-%d')

        e_Day = examdate.day
        e_Month = examdate.month
        e_Year = examdate.year
        b_Day = birthdate.day
        b_Month = birthdate.month
        b_Year = birthdate.year

        if ((e_Day - b_Day) < 0):
            e_Day = e_Day + 30
            e_Month = e_Month - 1
        days = e_Day - b_Day
        if ((e_Month - b_Month) < 0):
            e_Month = e_Month + 12
            e_Year = e_Year - 1
        months = e_Month - b_Month
        years = e_Year - b_Year

        age = str(years) + "/" + str(months) +"/"+str(days)
        print ("Age: ",age)

        user.update(studentName=studentName, gender=gender, schoolName=schoolName, grade=grade, eduDistrict=eduDistrict , nationality=nationality, birthDate=birthDate_str, examDate=examDate_str,age=age)

        return redirect(reverse('examinerPage'))
    else:
        return render(request, 'examinerPage.html' )
    

@login_required(login_url="/login")
def startTest(request,id):
    request.session['student'] = id
    stage = (Examiner.objects.get(user_id=request.user.id).stage)
    student_grade = Student.objects.get(id=request.session['student']).grade
    grade = int(student_grade)
    print(stage)
    if stage == 'PRIMARY':
        return redirect('testsPage')
    elif stage == 'SECONDARY':
        return redirect('testsPageSec')
    elif stage == 'BOTH':
        if grade > 1 and grade <= 5:
            return redirect('testsPage')
        elif grade > 5 and grade <= 9:
            return redirect('testsPageSec')
    else:
        return redirect('testsPage')
    
#show student details
@login_required(login_url="/login")
def studentProfile(request, id):
        return render(request, "studentProfile.html", {
        "students": Student.objects.filter(id=id)})


#show Admin or Examiner details
@login_required(login_url="/login")
def profile (request):
    if (request.user.is_staff):
        return render(request, 'profile.html')
    else:
        return render(request, "profile.html", {
        "examiners": Examiner.objects.get(user_id=request.user.id)})
    

def requestPage (request):
    print("call function")
    if request.method == "POST":
        print("if statement")
        name = request.POST['nameBox']
        organization = request.POST['orgBox']
        email = request.POST['emailBox']
        message = request.POST['textAreaBox']
        
        print(name)
        print(organization)
        print(email)
        print(message)
        
        send_mail(
            subject=f"{name} from {organization}",
            message=f"Name: {name}\nOrganization: {organization}\nEmail: {email}\nMessage:\n{message}",
            from_email=f"{email}",              
            recipient_list=["smerri@kisr.edu.kw"],     
            fail_silently=False,
        )
        print("Name:{name} \nOrganization:{organization} \nEmail:{email} \nMessage:\n{message}")
        
    
    return render(request,"requestPage.html")

@login_required(login_url="/login")
def testsPage (request):
    student = Student.objects.get(id=request.session['student']).studentName
    test1 = PrimaryTest1.objects.filter(student_id = request.session['student'])
    test2 = PrimaryTest2.objects.filter(student_id = request.session['student'])
    test3 = PrimaryTest3.objects.filter(student_id = request.session['student'])
    test4 = PrimaryTest4.objects.filter(student_id = request.session['student'])
    test5 = PrimaryTest5.objects.filter(student_id = request.session['student'])
    test6 = PrimaryTest6.objects.filter(student_id = request.session['student'])
    global context_test1
    context_test1 = {}
    global context_test2
    context_test2 = {}
    global context_test3
    context_test3 = {}
    global context_test4
    context_test4 = {}
    global context_test5
    context_test5 = {}
    global context_test6
    context_test6 = {}
    
    
    if (test1.exists() or test2.exists() or test3.exists() or test4.exists() or test5.exists() or test6.exists()):
        if(test1.exists()):
            test1_correct_Ans = test1.latest("id").total_correct
            test1_time_seconds = test1.latest("id").time_seconds
            test1_fluency_score = test1.latest("id").fluency_score
            if (test1_correct_Ans != None):
                context_test1 = {"correctAnswers":(test1_correct_Ans), "status_test1":('منجز '),  "time_sec": (test1_time_seconds), "fluency_score": (test1_fluency_score)}
            else:
                context_test1 = {"status_test1":('غير منجز'), }
        else:
            context_test1 = {"status_test1":('غير منجز'), }

        if(test2.exists()):
            test2_correct_Ans = test2.latest("id").total_score
            test2_time_seconds = test2.latest("id").time_seconds
            test2_fluency_score = test2.latest("id").fluency_score
            if (test2_correct_Ans != None):
                context_test2 = {"correctAnswers":(test2_correct_Ans), "status_test2":('منجز '), "time_sec": (test2_time_seconds), "fluency_score": (test2_fluency_score)}
            else:
                context_test2 = {"status_test2":('غير منجز'), }
        else:
            context_test2 = {"status_test2":('غير منجز'), }
        
        if(test3.exists()):
            test3_correct_Ans = test3.latest("id").total_correct
            test3_time_seconds = test3.latest("id").total_time_secs
            
            if (test3_correct_Ans != None):
                context_test3 = {"correctAnswers":(test3_correct_Ans), "status_test3":('منجز '), "time_sec": (test3_time_seconds), } #"fluency_score": (test3_fluency_score)
            else:
                context_test3 = {"status_test3":('غير منجز'), }
        else:
            context_test3 = {"status_test3":('غير منجز'), }

        if(test4.exists()):
            test4_correct_Ans = test4.latest("id").total_correct
            if (test4_correct_Ans != None):
                context_test4 = {"correctAnswers":(test4_correct_Ans), "status_test4":('منجز '), }
            else:
                context_test4 = {"status_test4":('غير منجز'), }
        else:
            context_test4 = {"status_test4":('غير منجز'), }

        if(test5.exists()):
            test5_correct_Ans = test5.latest("id").total_correct
            if (test5_correct_Ans != None):
                context_test5 = {"correctAnswers":(test5_correct_Ans), "status_test5":('منجز '), }
            else:
                context_test5 = {"status_test5":('غير منجز'), }
        else:
            context_test5 = {"status_test5":('غير منجز'), }

        if(test6.exists()):
            test6_correct_Ans = test6.latest("id").total_correct
            if (test6_correct_Ans != None):
                context_test6 = {"correctAnswers":(test6_correct_Ans), "status_test6":('منجز '), }
            else:
                context_test6 = {"status_test6":('غير منجز'), }
        else:
            context_test6 = {"status_test6":('غير منجز'), }

        return render(request, "primary_test/testPage.html", { "context_test1": context_test1, "context_test2": context_test2, "context_test3": context_test3,"context_test4": context_test4, "context_test5": context_test5, "context_test6": context_test6,"student": student, "examiners": (Examiner.objects.get(user_id=request.user.id))})
    else:
        context_test1 = { "status_test1":('غير منجز'),}
        context_test2 = { "status_test2":('غير منجز'),}
        context_test3 = { "status_test3":('غير منجز'),}
        context_test4 = { "status_test4":('غير منجز'),}
        context_test5 = { "status_test5":('غير منجز'),}
        context_test6 = { "status_test6":('غير منجز'),}
        return render(request,"primary_test/testPage.html", {"context_test1": context_test1, "context_test2": context_test2, "context_test3": context_test3,"context_test4": context_test4, "context_test5": context_test5, "context_test6": context_test6, "student":(Student.objects.get(id=request.session['student']).studentName), "examiners": (Examiner.objects.get(user_id=request.user.id)) })

@login_required(login_url="/login")
def testsPageSec (request):
    student = Student.objects.get(id=request.session['student']).studentName
    test1 = SecondaryTest1.objects.filter(student_id = request.session['student'])
    test2 = SecondaryTest2.objects.filter(student_id = request.session['student'])
    test3 = SecondaryTest3.objects.filter(student_id = request.session['student'])
    test4 = SecondaryTest4.objects.filter(student_id = request.session['student'])
    global sec_context_test1
    sec_context_test1 = {}
    global sec_context_test2
    sec_context_test2 = {}
    global sec_context_test3
    sec_context_test3 = {}
    global sec_context_test4
    sec_context_test4 = {}
    


    #add it in the if statement
    if (test1.exists() or test1.exists() or test3.exists() or test4.exists()):

   


        if(test1.exists()):
            test1_correct_Ans = test1.latest("id").total_correct
            test1_time_seconds = test1.latest("id").time_seconds
            test1_fluency_score = test1.latest("id").fluency_score
            if (test1_correct_Ans != None):
                sec_context_test1 = {"correctAnswers":(test1_correct_Ans), "status_test1":('منجز '), "time_sec": (test1_time_seconds), "fluency_score": (test1_fluency_score)}
            else:
                sec_context_test1 = {"status_test1":('غير منجز'), }
        else:
            sec_context_test1 = {"status_test1":('غير منجز'), }

        if(test2.exists()):
            test2_correct_Ans = test2.latest("id").total_correct
            test2_time_seconds = test2.latest("id").total_time_secs 
            if (test2_correct_Ans != None):
                sec_context_test2 = {"correctAnswers":(test2_correct_Ans), "status_test2":('منجز '), "time_sec": (test2_time_seconds), } 
            else:
                sec_context_test2 = {"status_test2":('غير منجز'), }
        else:
            sec_context_test2 = {"status_test3":('غير منجز'), }


        if(test3.exists()):
            test3_correct_Ans = SecondaryTest3.objects.filter(student_id = request.session['student']).latest("id").total_correct
            if (test3_correct_Ans != None):
                sec_context_test3 = {"correctAnswers":(test3_correct_Ans), "status_test3":('منجز ')}
            else:
                sec_context_test3 = {"status_test3":('غير منجز'), }
        else:
            sec_context_test3 = {"status_test3":('غير منجز'), }
        
        if(test4.exists()):
            test4_correct_Ans = SecondaryTest4.objects.filter(student_id = request.session['student']).latest("id").total_correct
            if (test4_correct_Ans != None):
                sec_context_test4 = {"correctAnswers":(test4_correct_Ans), "status_test4":('منجز ')}
            else:
                sec_context_test4 = {"status_test4":('غير منجز'), }
        else:
            sec_context_test4 = {"status_test4":('غير منجز'), }

        return render(request, "secondary_test/testPage.html", { "sec_context_test1": sec_context_test1, "sec_context_test2": sec_context_test2, "sec_context_test3": sec_context_test3, "sec_context_test4": sec_context_test4,"student": student, "examiners": (Examiner.objects.get(user_id=request.user.id))})
    
    else:
        sec_context_test1 = { "status_test1":('غير منجز'),}
        sec_context_test2 = { "status_test2":('غير منجز'),}
        sec_context_test3 = { "status_test3":('غير منجز'),}
        sec_context_test4 = { "status_test4":('غير منجز'),}
        return render(request,"secondary_test/testPage.html", {"sec_context_test1": sec_context_test1, "sec_context_test2": sec_context_test2, "sec_context_test3": sec_context_test3, "sec_context_test4": sec_context_test4,"student":(Student.objects.get(id=request.session['student']).studentName), "examiners": (Examiner.objects.get(user_id=request.user.id)) })

    
#Primary test 1
@login_required(login_url="/login")
def primary_test1_training(request):
    if request.method == 'POST':
        training_scores = [int(request.POST.get(f'train_{i}', 0)) for i in range(3)]
        passed_training = all(score == 1 for score in training_scores)

        if passed_training:
            request.session['training_passed'] = True
            return redirect('test1')
        else:
            return render(request, 'primary_test/test1_training.html', {
                'training_words': TRAINING_WORDS,
                'error': 'لم يتم اجتياز التدريب. لا يمكن المتابعة.'
            })

    return render(request, 'primary_test/test1_training.html', {
        'training_words': TRAINING_WORDS
    })

@login_required(login_url="/login")
def primary_test1(request):
    student = Student.objects.get(id=request.session['student'])

    # Modal confirmation submit
    if request.method == 'POST' and request.POST.get("form2"):
        print(request.POST)
        total_correct = request.session.get('test1_total_correct', 0)
        time_seconds = request.session.get('test1_time_seconds', 0)
        fluency = request.session.get('test1_fluency', 0)
        reason = request.POST.get("submitTst", "")

        # Save final test result
        PrimaryTest1.objects.create(
            student=student,
            total_correct=total_correct,
            time_seconds=time_seconds,
            fluency_score=fluency,
            reason=reason,
            date=datetime.now()
        )

        if(reason != "الوصول الى الحد السقفي"):
            del request.session['test1_total_correct']
            del request.session['test1_time_seconds']
            del request.session['test1_fluency']

        return redirect('testsPage')

    # Main test submission (score & time)
    if request.method == 'POST' and request.POST.get("form1"):
        test_scores = [int(request.POST.get(f'test_{i}', 0)) for i in range(30)]
        total_correct = sum(test_scores)

        try:
            time_seconds = float(request.POST.get('time', 1)) 
        except:
            time_seconds = 1

        fluency = (total_correct / time_seconds) * 60

        # Store in session for confirmation step
        request.session['test1_total_correct'] = total_correct
        request.session['test1_time_seconds'] = time_seconds
        request.session['test1_fluency'] = round(fluency, 2)

        return render(request, 'primary_test/test1.html', {
            'test_words': TEST_WORDS,
            'result': {
                'total_correct': total_correct,
                'time_seconds': time_seconds,
                'fluency': round(fluency, 2)
            }
        })

    return render(request, 'primary_test/test1.html', {
        'test_words': TEST_WORDS
    })

@csrf_exempt
def primary_test1_autosave(request):
    if request.method == 'POST':
        request.session['autosave'] = {
            f'test_{i}': request.POST.get(f'test_{i}', '0') for i in range(30)
        }
        return JsonResponse({"status": "saved"})

@login_required(login_url="/login")
def primary_test2_training(request):
    if request.method == 'POST':
        print(request.POST)
        selected_words = int(request.POST.get("selected_word_count", 0))

        if selected_words > 0:
            request.session['test2_passed_training'] = True
            return redirect('test2')
        else:
            return render(request, 'primary_test/test2_training.html', {
                'training_sentences': training_sentences,
                'error': 'لم يتم اجتياز التدريب. لا يمكن بدء الاختبار.'
            })

    return render(request, 'primary_test/test2_training.html', {
        'training_sentences': training_sentences
    })

@login_required(login_url="/login")
def primary_test2(request):
    student = Student.objects.get(id=request.session['student'])
    scores = {}
    total_score = 0

    # Modal confirmation submit
    if request.method == 'POST' and request.POST.get("form2"):
        print(request.POST)
        total_score = request.session.get('test2_total_score', 0)
        print(total_score)
        time_taken = request.session.get('test2_time_seconds', 0)
        print(time_taken)
        fluency = request.session.get('test2_fluency', 0)
        print(fluency)
        reason = request.POST.get("submitTst", "")
        print(reason)
        scores = request.session.get('test2_scores', 0)
        print(scores)

        # Save final test result
        PrimaryTest2.objects.create(
            student=student,
            scores=scores,
            total_score=total_score,
            time_seconds=time_taken,
            fluency_score=fluency,
            reason=reason,
            date=datetime.now()
        )


        return redirect('testsPage')

    # Main test submission (score & time)
    if request.method == 'POST' and request.POST.get("form1"):
        print(request.POST)
        for i in primary_test2_sentences:
            score = int(request.POST.get(f'score_{i}', 0))
            print(score)
            scores[str(i)] = score
            total_score += score

        try:
            time_seconds = float(request.POST.get('time', 1)) 
        except:
            time_seconds = 1

        fluency = (total_score / time_seconds) * 60

        # Store in session for confirmation step
        request.session['test2_total_score'] = total_score
        print(request.session['test2_total_score'])
        request.session['test2_time_seconds'] = time_seconds
        print(request.session['test2_time_seconds'])
        request.session['test2_fluency'] = round(fluency, 2)
        print(request.session['test2_fluency'])
        request.session['test2_scores'] = scores
        print(request.session['test2_scores'])

        return render(request, 'primary_test/test2.html', {
            'test_words': primary_test2_sentences,
            'result': {
                'total_score': total_score,
                'time_seconds': time_seconds,
                'fluency': round(fluency, 2)
            }
        }) 
       
    return render(request, 'primary_test/test2.html', {
        'test_words': primary_test2_sentences
    })

def primary_test3_training(request):
    # --- First Visit ---
    if request.method == "GET" and not request.headers.get("HX-Request"):
        request.session['training_correct'] = 0
        return render(request, "primary_test/test3_training.html", {
            "question": primary_test3_training_questions[0],
            "index": 0
        })

    # --- GET: Load Next Question via HTMX ---
    if request.method == "GET" and request.headers.get("HX-Request") == "true":
        index = int(request.GET.get("index", 0))
        is_final = request.GET.get("final") == "true"

        if is_final:
            passed = request.session.get('training_correct', 0) > 0
            return render(request, 'primary_test/test3_training_correct_result.html', {
                'show_final_result': True,
                'passed': passed
            })

        if index < len(primary_test3_training_questions):
            return render(request, "primary_test/test3_training_question.html", {
                "question": primary_test3_training_questions[index],
                "index": index
            })

    # --- POST: Answer Clicked OR "التالي" ---
    if request.method == "POST":
        index = int(request.POST.get("index", 0))
        selected = request.POST.get("answer")
        question = primary_test3_training_questions[index]
        correct = question["correct"]
        next_index = index + 1
        total = len(primary_test3_training_questions)
        is_last = next_index >= total
        passed = request.session.get('training_correct', 0) > 0 if is_last else None

    if selected:
        if 'training_correct' not in request.session:
            request.session['training_correct'] = 0

        if selected == correct:
            request.session['training_correct'] += 1



    return render(request, "primary_test/test3_training_correct_result.html", {
        "is_correct": selected == correct,
        "correct": correct,
        "selected": selected,
        "index": next_index,
        "question": question,
        "total_questions": total,
        "passed": passed
    })


def _test3_init(request):
    s = request.session
    s['t3_index'] = 0
    s['t3_answers'] = []
    s['t3_scores']  = []
    s['t3_durations'] = []
    s['t3_started_at'] = time.time()
    s['t3_qstart_at']  = time.time()
    s.modified = True

@login_required(login_url="/login")
def primary_test3(request):
    print('inside primary_test3')
    student = Student.objects.get(id=request.session['student'])

    # First test page load (Q1)
    if request.method == "GET" and not request.headers.get("HX-Request"):
        print('first test display')
        _test3_init(request)
        return render(request, "primary_test/test3.html", {
            "question": main_questions[0],
            "index": 0
        })

    # HTMX POST: when a button is clicked (answer / skip / stop)
    if request.method == "POST" and request.headers.get("HX-Request") == "true":
        print('when answering button click')
        s = request.session
        idx = s.get('t3_index', 0)
        answers = s.get('t3_answers', [])
        scores  = s.get('t3_scores', [])
        durs    = s.get('t3_durations', [])
        qstart  = s.get('t3_qstart_at', time.time())

        action   = request.POST.get("action")
        selected = request.POST.get("answer")
        stop_reason = request.POST.get("stop_reason", "").strip()

        # computation time
        elapsed = round(time.time() - qstart, 3)

        # STOP (the examsiner stopped the test)
        if action == "stop":
            print('stop button clicked')

            # Mark current question duration as "-" since stopped in modal
            durs.append("-")
            answers.append("-")
            scores.append("-")

            # Fill rest of unanswered questions with "-"
            remaining = len(main_questions) - (idx + 1)
            if remaining > 0:
                answers.extend(["-"] * remaining)
                scores.extend(["-"] * remaining)
                durs.extend(["-"] * remaining)

            
            stop_reason = request.POST.get("stop_reason", "").strip()

            

            # Count only actual numeric scores
            total_correct = sum(1 for x in scores if x == 1)

            total_time_secs = round(sum(d for d in durs if isinstance(d, (int, float))), 3)  # elapsed seconds

            # save to DB    
            PrimaryTest3.objects.create(
                student=student,
                raw_scores = scores,
                total_correct=total_correct,
                durations = durs, #per question duration
                reason=stop_reason,
                total_time_secs = total_time_secs,
                date=datetime.now()
            )


            test_profile_url = reverse('testsPage') 
            resp = HttpResponse('')
            resp['HX-Redirect'] = test_profile_url
            return resp

        # ANSWER / SKIP branch
        elapsed = round(time.time() - qstart, 3)

        # Normalize to exactly 4.000 for auto-skip
        if 179.9 <= elapsed <= 180.2:
            elapsed = 180.000

        durs.append(elapsed)

        if selected in [None, ""]:
            answers.append("-")
            scores.append("-")
        else:
            answers.append(selected)
            correct = main_questions[idx]["correct"]
            scores.append(1 if selected == correct else 0)

        # advance index
        idx += 1
        s['t3_index'] = idx
        s['t3_answers'] = answers
        s['t3_scores']  = scores
        s['t3_durations'] = durs
        s['t3_qstart_at'] = time.time()
        s.modified = True

        # next question or finish
        if idx < len(main_questions):
            print('next question or finished')
            html = render_to_string("primary_test/test3_question.html", {
                "question": main_questions[idx],
                "index": idx
            }, request=request)
            return HttpResponse(html)

        # finished
        total_correct = sum(1 for s_ in scores if s_ == 1)
        
        answers  = s.get('t3_answers', [])
        scores   = s.get('t3_scores', [])
        durations = s.get('t3_durations', [])
        total_correct = sum(1 for x in scores if x == 1)
        # calculate started_at datetime and total_time_secs
        started_at = None
        total_time_secs = None
        if s.get('t3_started_at'):
            start_ts = s['t3_started_at']
            #started_at = timezone.datetime.fromtimestamp(start_ts, tz=timezone.get_current_timezone())
            total_time_secs = round(time.time() - start_ts, 3)  # total duration in seconds
        
        # save to DB
        PrimaryTest3.objects.create(
            student=student,
            raw_scores = scores,
            total_correct=total_correct,
            durations = durations, #per question duration
            reason=stop_reason,
            total_time_secs = total_time_secs,
            date=datetime.now()
        )

        # redirect 
        test_profile_url = reverse('testsPage') 
        resp = HttpResponse('')
        resp['HX-Redirect'] = test_profile_url
        return resp

    # fallback
    _test3_init(request)
    return render(request, "primary_test/test3.html", {
        "question": main_questions[0],
        "index": 0
    })

'''@login_required(login_url="/login")
def primary_test4_training(request):
    if request.method == 'POST':
        training_scores = [int(request.POST.get(f'train_{i}', 0)) for i in range(3)]
        passed_training = all(score == 1 for score in training_scores)

        if passed_training:
            request.session['training_passed'] = True
            return redirect('test4')
        else:
            return render(request, 'primary_test/test4_training.html', {
                'training_words': primary_test4_training_words,
                'error': 'لم يتم اجتياز التدريب. لا يمكن المتابعة.'
            })

    return render(request, 'primary_test/test4_training.html', {
        'training_words': primary_test4_training_words
    })'''

@login_required(login_url="/login")
def primary_test4(request):
    student = Student.objects.get(id=request.session['student'])

    # Modal confirmation submit
    if request.method == 'POST' and request.POST.get("form2"):
        print(request.POST)
        # Get saved values from session
        total_correct = request.session.get('test4_total_correct', 0)
        raw_scores = request.session.get('test4_raw_scores', [])
        reason = request.POST.get("submitTst", "")

        # Save final test result
        PrimaryTest4.objects.create(
            student=student,
            raw_scores = raw_scores,
            total_correct=total_correct,
            reason=reason,
            date=datetime.now()
        )

        # Clear session if you want
        if reason != "الوصول الى الحد السقفي":
            request.session.pop('test4_total_correct', None)
            request.session.pop('test4_raw_scores', None)


        return redirect('testsPage')

    # Main test submission (score & time)
    if request.method == 'POST' and request.POST.get("form1"):
        raw_scores = []
        for i in range(30):
            val = request.POST.get(f'score_{i}', "-")
            raw_scores.append(val)

        total_correct = sum(1 for val in raw_scores if val == "1")

        # Save to session for modal confirmation
        request.session['test4_total_correct'] = total_correct
        request.session['test4_raw_scores'] = raw_scores

        return render(request, 'primary_test/test4.html', {
            'test_words': primary_test4_words,
            'result': {
                'total_correct': total_correct,
            }
        })
    return render(request,"primary_test/test4.html", {
        'test_words': primary_test4_words
    })

def primary_test5_training(request):
    # --- First Visit ---
    if request.method == "GET" and not request.headers.get("HX-Request"):
        request.session['training_correct'] = 0
        return render(request, "primary_test/test5_training.html", {
            "question": primary_test5_training_questions[0],
            "index": 0
        })

    # --- GET: Load Next Question via HTMX ---
    if request.method == "GET" and request.headers.get("HX-Request") == "true":
        index = int(request.GET.get("index", 0))
        is_final = request.GET.get("final") == "true"

        if is_final:
            passed = request.session.get('training_correct', 0) > 0
            return render(request, 'primary_test/test5_training_correct_result.html', {
                'show_final_result': True,
                'passed': passed
            })

        if index < len(primary_test5_training_questions):
            return render(request, "primary_test/test5_training_question.html", {
                "question": primary_test5_training_questions[index],
                "index": index
            })

    # --- POST: Answer Clicked OR "التالي" ---
    if request.method == "POST":
        index = int(request.POST.get("index", 0))
        selected = request.POST.get("answer")
        question = primary_test5_training_questions[index]
        correct = question["correct"]
        next_index = index + 1
        total = len(primary_test5_training_questions)
        is_last = next_index >= total
        passed = request.session.get('training_correct', 0) > 0 if is_last else None

    if selected:
        if 'training_correct' not in request.session:
            request.session['training_correct'] = 0

        if selected == correct:
            request.session['training_correct'] += 1



    return render(request, "primary_test/test5_training_correct_result.html", {
        "is_correct": selected == correct,
        "correct": correct,
        "selected": selected,
        "index": next_index,
        "question": question,
        "total_questions": total,
        "passed": passed
    })



def _test5_init(request):
    s = request.session
    s['t5_index'] = 0
    s['t5_answers'] = []
    s['t5_scores']  = []
    s['t5_durations'] = []
    s['t5_started_at'] = time.time()
    s['t5_qstart_at']  = time.time()
    s.modified = True

@login_required(login_url="/login")
def primary_test5(request):
    student = Student.objects.get(id=request.session['student'])

    # First test page load (Q1)
    if request.method == "GET" and not request.headers.get("HX-Request"):
        _test5_init(request)
        return render(request, "primary_test/test5.html", {
            "question": primary_test5_main_questions[0],
            "index": 0
        })

    # HTMX POST: when a button is clicked (answer / skip / stop)
    if request.method == "POST" and request.headers.get("HX-Request") == "true":
        s = request.session
        idx = s.get('t5_index', 0)
        answers = s.get('t5_answers', [])
        scores  = s.get('t5_scores', [])
        durs    = s.get('t5_durations', [])
        qstart  = s.get('t5_qstart_at', time.time())

        action   = request.POST.get("action")
        selected = request.POST.get("answer")
        stop_reason = request.POST.get("stop_reason", "").strip()

        # computation time
        elapsed = round(time.time() - qstart, 3)

        # STOP (the examsiner stopped the test)
        if action == "stop":

            # Mark current question duration as "-" since stopped in modal
            durs.append("-")
            answers.append("-")
            scores.append("-")

            # Fill rest of unanswered questions with "-"
            remaining = len(main_questions) - (idx + 1)
            if remaining > 0:
                answers.extend(["-"] * remaining)
                scores.extend(["-"] * remaining)
                durs.extend(["-"] * remaining)

            
            stop_reason = request.POST.get("stop_reason", "").strip()

            

            # Count only actual numeric scores
            total_correct = sum(1 for x in scores if x == 1)

            total_time_secs = round(sum(d for d in durs if isinstance(d, (int, float))), 3)  # elapsed seconds
                
            PrimaryTest5.objects.create(
                student=student,
                raw_scores = scores,
                total_correct=total_correct,
                durations = durs, #per question duration
                reason=stop_reason,
                total_time_secs = total_time_secs,
                date=datetime.now()
            )


            test_profile_url = reverse('testsPage') 
            resp = HttpResponse('')
            resp['HX-Redirect'] = test_profile_url
            return resp

        # ANSWER / SKIP branch
        elapsed = round(time.time() - qstart, 3)

        # Normalize to exactly 5.000 for auto-skip
        if 179.9 <= elapsed <= 182.2:
            elapsed = 180.000

        durs.append(elapsed)

        if selected in [None, ""]:
            answers.append("-")
            scores.append("-")
        else:
            answers.append(selected)
            correct = primary_test5_main_questions[idx]["correct"]
            scores.append(1 if selected == correct else 0)

        # advance index
        idx += 1
        s['t5_index'] = idx
        s['t5_answers'] = answers
        s['t5_scores']  = scores
        s['t5_durations'] = durs
        s['t5_qstart_at'] = time.time()
        s.modified = True

        # next question or finish
        if idx < len(primary_test5_main_questions):
            html = render_to_string("primary_test/test5_question.html", {
                "question": primary_test5_main_questions[idx],
                "index": idx
            }, request=request)
            return HttpResponse(html)

        # finished
        total_correct = sum(1 for s_ in scores if s_ == 1)

        answers  = s.get('t5_answers', [])
        scores   = s.get('t5_scores', [])
        durations = s.get('t5_durations', [])
        total_correct = sum(1 for x in scores if x == 1)
        # calculate started_at datetime and total_time_secs
        started_at = None
        total_time_secs = None
        if s.get('t5_started_at'):
            start_ts = s['t5_started_at']
            #started_at = timezone.datetime.fromtimestamp(start_ts, tz=timezone.get_current_timezone())
            total_time_secs = round(time.time() - start_ts, 3)  # total duration in seconds
        
        PrimaryTest5.objects.create(
            student=student,
            raw_scores = scores,
            total_correct=total_correct,
            durations = durations, #per question duration
            reason=stop_reason,
            total_time_secs = total_time_secs,
            date=datetime.now()
        )

        # redirect
        test_profile_url = reverse('testsPage')  # adjust to your URL
        resp = HttpResponse('')
        resp['HX-Redirect'] = test_profile_url
        return resp

    # fallback
    _test5_init(request)
    return render(request, "primary_test/test5.html", {
        "question": primary_test5_main_questions[0],
        "index": 0
    })


def primary_test6_training(request):
    # --- First Visit ---
    if request.method == "GET" and not request.headers.get("HX-Request"):
        para = test6_training_questions[0]
        paragraph_text = para["paragraph"]
        question = para["questions"][0]
        question_text = question["question"]
        answers = question["answers"]
        request.session['training_correct'] = 0
        return render(request, "primary_test/test6_training.html", {
            "paragraph": paragraph_text,
            "question": question,
            "question_text": question_text,
            "answers": answers,
            "index": 0
        })

    # --- GET: Load Next Question via HTMX ---
    if request.method == "GET" and request.headers.get("HX-Request") == "true":
        index = int(request.GET.get("index", 0))
        is_final = request.GET.get("final") == "true"

        if is_final:
            passed = request.session.get('training_correct', 0) > 0
            return render(request, 'primary_test/test6_training_correct_result.html', {
                'show_final_result': True,
                'passed': passed
            })

        if index < len(test6_training_questions):
            para = test6_training_questions[index]
            paragraph_text = para["paragraph"]
            question = para["questions"][0]
            question_text = question["question"]
            answers = question["answers"]
            return render(request, "primary_test/test6_training_question.html", {
                "paragraph": paragraph_text,
                "question": question,
                "question_text": question_text,
                "answers": answers,
                "index": index
            })

    # --- POST: Answer Clicked OR "التالي" ---
    if request.method == "POST":
        index = int(request.POST.get("index", 0))
        selected = request.POST.get("answer")
        question = test6_training_questions[index]
        correct = question["questions"][0]["correct"]
        paragraph_text = question["paragraph"]
        question_first = question["questions"][0]
        question_text = question_first["question"]
        answers = question_first["answers"]
        next_index = index + 1
        total = len(test6_training_questions)
        is_last = next_index >= total
        passed = request.session.get('training_correct', 0) > 0 if is_last else None

    if selected:
        if 'training_correct' not in request.session:
            request.session['training_correct'] = 0

        if selected == correct:
            request.session['training_correct'] += 1



    return render(request, "primary_test/test6_training_correct_result.html", {
        "is_correct": selected == correct,
        "correct": correct,
        "selected": selected,
        "index": next_index,
        "question": question,
        "paragraph_text": paragraph_text,
        "question_first": question_first,
        "question_text": question_text,
        "answers": answers,

        "total_questions": total,
        "passed": passed
    })


def _test6_init(request):
    s = request.session
    s['t6_index'] = 0
    s['t6_answers'] = []
    s['t6_scores']  = []
    s['t6_durations'] = []
    s['t6_started_at'] = time.time()
    s['t6_qstart_at']  = time.time()
    s['t6_total'] = sum(len(p["questions"]) for p in test6_main_questions)
    s.modified = True

    

@login_required(login_url="/login")
def primary_test6(request):
    student = Student.objects.get(id=request.session['student'])

    data = test6_main_questions
    total = sum(len(p["questions"]) for p in data)

    # First test page load (Q1)
    if request.method == "GET" and not request.headers.get("HX-Request"):
        _test6_init(request)
        para, q = get_linear_question(data, 0)
        return render(request, "primary_test/test6.html", {
            "question": {
                "id": q["id"],
                "question": q["question"],
                "answers": q["answers"],
                "correct": q.get("correct"),
                "paragraph": para["paragraph"],
                "paragraph_id": para.get("paragraph_id"),
            },
            "index": 0,
            "total": total,
        })

    # HTMX POST: when a button is clicked (answer / skip / stop)
    if request.method == "POST" and request.headers.get("HX-Request") == "true":
        s = request.session
        idx      = s.get('t6_index', 0)
        answers  = s.get('t6_answers', [])
        scores   = s.get('t6_scores', [])
        durs     = s.get('t6_durations', [])
        qstart   = s.get('t6_qstart_at', time.time())
        started  = s.get('t6_started_at', time.time())

        action      = request.POST.get("action")
        selected    = request.POST.get("answer")
        stop_reason = request.POST.get("stop_reason", "").strip()

        # computation time
        elapsed = round(time.time() - qstart, 3)

        # STOP (the examiner stopped the test)
        if action == "stop":
            # Mark current question duration as "-" since stopped in modal
            durs.append("-")
            answers.append("-")
            scores.append("-")

            # Fill rest with "-"
            remaining = total - (idx + 1)
            if remaining > 0:
                answers.extend(["-"] * remaining)
                scores.extend(["-"] * remaining)
                durs.extend(["-"] * remaining)

            # Count only actual numeric scores
            total_correct = sum(1 for x in scores if x == 1)
            total_time_secs = round(sum(d for d in durs if isinstance(d, (int, float))), 3)

            PrimaryTest6.objects.create(
                student=student,
                raw_scores=scores,
                total_correct=total_correct,
                durations=durs,
                reason=stop_reason,
                total_time_secs=total_time_secs,
                date=datetime.now()
            )

            test_profile_url = reverse('testsPage')
            resp = HttpResponse('')
            resp['HX-Redirect'] = test_profile_url
            return resp

        # ANSWER / SKIP branch
        # Normalize to exactly 4.000 for auto-skip (keep same behavior as test2, if you use it)
        if 179.9 <= elapsed <= 180.2:
            elapsed = 180.000
        durs.append(elapsed)

        # record answer & score
        para_now, q_now = get_linear_question(data, idx)
        if selected in [None, ""]:
            answers.append("-")
            scores.append("-")
        else:
            answers.append(selected)
            correct = q_now.get("correct")
            scores.append(1 if (selected == correct) else 0)

        # advance index
        idx += 1
        s['t6_index'] = idx
        s['t6_answers'] = answers
        s['t6_scores']  = scores
        s['t6_durations'] = durs
        s['t6_qstart_at'] = time.time()
        s.modified = True

        # next question or finish
        if idx < total:
            para_next, q_next = get_linear_question(data, idx)
            html = render_to_string("primary_test/test6_question.html", {
                "question": {
                    "id": q_next["id"],
                    "question": q_next["question"],
                    "answers": q_next["answers"],
                    "correct": q_next.get("correct"),
                    "paragraph": para_next["paragraph"],
                    "paragraph_id": para_next.get("paragraph_id"),
                },
                "index": idx,
                "total": total,
            }, request=request)
            return HttpResponse(html)

        # finished — compute totals & save
        scores_ = s.get('t6_scores', [])
        durations_ = s.get('t6_durations', [])
        total_correct = sum(1 for x in scores_ if x == 1)  # only numeric 1's
        total_time_secs = round(time.time() - started, 3) if started else None

        PrimaryTest6.objects.create(
            student=student,
            raw_scores=scores_,
            total_correct=total_correct,
            durations=durations_,
            reason=stop_reason,
            total_time_secs=total_time_secs,
            date=datetime.now()
        )

        test_profile_url = reverse('testsPage')
        resp = HttpResponse('')
        resp['HX-Redirect'] = test_profile_url
        return resp

    # fallback (fresh start)
    _test6_init(request)
    para, q = get_linear_question(data, 0)
    return render(request, "primary_test/test6.html", {
        "question": {
            "id": q["id"],
            "question": q["question"],
            "answers": q["answers"],
            "correct": q.get("correct"),
            "paragraph": para["paragraph"],
            "paragraph_id": para.get("paragraph_id"),
        },
        "index": 0,
        "total": total,
    })



@login_required(login_url="/login")
def primary_result(request):
    student = Student.objects.get(id=request.session['student'])
    examiner = Examiner.objects.get(user_id = request.user.id)
    student_age_year = student.age.split('/')[0]
    student_age_month = student.age.split('/')[1]
    student_age_day = student.age.split('/')[2]
    test1 = PrimaryTest1.objects.filter(student_id = request.session['student']).latest("id")
    test2 = PrimaryTest2.objects.filter(student_id = request.session['student']).latest("id")
    test3 = PrimaryTest3.objects.filter(student_id = request.session['student']).latest("id")
    test4 = PrimaryTest4.objects.filter(student_id = request.session['student']).latest("id")
    test5 = PrimaryTest5.objects.filter(student_id = request.session['student']).latest("id")
    test6 = PrimaryTest6.objects.filter(student_id = request.session['student']).latest("id")
    test1_latest = None
    test2_latest = None
    test3_latest = None
    test4_latest = None
    test5_latest = None
    test6_latest = None
    note_latest = ""
    strength_latest = ""
    weakness_latest = ""
    result_latest = ""
    suggestion_latest = ""

    result_primary = PrimaryResult.objects.filter(student_id = request.session['student'])
    print(result_primary)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == "submit":
            test_1_skill = request.POST.get('choice1')
            test_2_skill = request.POST.get('choice2')
            test_3_skill = request.POST.get('choice3')
            test_4_skill = request.POST.get('choice4')
            test_5_skill = request.POST.get('choice5')
            test_6_skill = request.POST.get('choice6')
            note = request.POST['note']
            strength = request.POST['strength']
            weakness = request.POST['weakness']
            result = request.POST['results']
            suggestion = request.POST['suggestion']

            primaryresult = PrimaryResult.objects.create( student= student, examiner = examiner, test_1_skill = test_1_skill, test_2_skill = test_2_skill, test_3_skill = test_3_skill, test_4_skill = test_4_skill, test_5_skill = test_5_skill, test_6_skill = test_6_skill, notes= note, strength=strength, weakness = weakness, result = result, suggestion = suggestion)
            primaryresult.save()

    
    finalReport_exist = result_primary.exists()
    if finalReport_exist:
        try:
            test1_latest = PrimaryResult.objects.filter(student_id=request.session['student']).latest("id").test_1_skill
            test2_latest = PrimaryResult.objects.filter(student_id=request.session['student']).latest("id").test_2_skill
            test3_latest = PrimaryResult.objects.filter(student_id=request.session['student']).latest("id").test_3_skill
            test4_latest = PrimaryResult.objects.filter(student_id=request.session['student']).latest("id").test_4_skill
            test5_latest = PrimaryResult.objects.filter(student_id=request.session['student']).latest("id").test_5_skill
            test6_latest = PrimaryResult.objects.filter(student_id=request.session['student']).latest("id").test_6_skill
            note_latest = PrimaryResult.objects.filter(student_id=request.session['student']).latest("id").notes
            strength_latest = PrimaryResult.objects.filter(student_id=request.session['student']).latest("id").strength
            weakness_latest = PrimaryResult.objects.filter(student_id=request.session['student']).latest("id").weakness
            result_latest = PrimaryResult.objects.filter(student_id=request.session['student']).latest("id").result
            suggestion_latest = PrimaryResult.objects.filter(student_id=request.session['student']).latest("id").suggestion
        except PrimaryResult.DoesNotExist:
              pass

    # Pull raw scores
    raw_scores = {
        "test1": test1.total_correct,
        "test2": test2.total_score,
        "test3": test3.total_correct,
        "test4": test4.total_correct,
        "test5": test5.total_correct,
        "test6": test6.total_correct,
    }

    # Run lookup
    results = lookup_scores_primary(
        grade=str(student.grade),
        test1_raw=raw_scores["test1"],
        test2_raw=raw_scores["test2"],
        test3_raw=raw_scores["test3"],
        test4_raw=raw_scores["test4"],
        test5_raw=raw_scores["test5"],
        test6_raw=raw_scores["test6"],
    )

    
    total_raw_score = raw_scores["test1"] + raw_scores["test2"] + raw_scores["test3"] + raw_scores["test4"] + raw_scores["test5"] + raw_scores["test6"]
    total_percentile = results["test1"]["percentile"] + results["test2"]["percentile"] + results["test3"]["percentile"] + results["test4"]["percentile"] + results["test5"]["percentile"] + results["test6"]["percentile"]
    total_std = results["test1"]["std"] + results["test2"]["std"] + results["test3"]["std"] + results["test4"]["std"] + results["test5"]["std"] + results["test6"]["std"]

    datastd = []
    labelstd = []

    datastd.append(int(results["test1"]["percentile"]))
    labelstd.append("قراءة الكلمة المفردة")
    datastd.append(int(results["test2"]["percentile"]))
    labelstd.append("الطلاقة في قراءة الجملة")
    datastd.append(int(results["test3"]["percentile"]))
    labelstd.append("الطلاقة في فهم المقطع")
    datastd.append(int(results["test4"]["percentile"]))
    labelstd.append("إملاء الكلمة")
    datastd.append(int(results["test5"]["percentile"]))
    labelstd.append("اختبار الإملاء الصحيح")
    datastd.append(int(results["test6"]["percentile"]))
    labelstd.append("فهم المقروء (القطعة)")
    print("datastd")
    print(datastd)
    print(labelstd)

    # pull the Modified Standard per test (std)
    std_values_by_test = {
        "(ق ك م)": results["test1"]["std"],  # ← use your real abbreviations
        "(ط ق ج)":  results["test2"]["std"],
        "(ط ف م)": results["test3"]["std"],
        "(إ ك)": results["test4"]["std"],
        "(ا إ ص)": results["test5"]["std"],
        "(ف م ق)": results["test6"]["std"],
    }

    data = []
    labels = []

    data.append(int(results["test1"]["percentile"]))
    labels.append("(ق ك م)")
    data.append(int(results["test2"]["percentile"]))
    labels.append("(ط ق ج)")
    data.append(int(results["test3"]["percentile"]))
    labels.append("(ط ف م)")
    data.append(int(results["test4"]["percentile"]))
    labels.append("(إ ك)")
    data.append(int(results["test5"]["percentile"]))
    labels.append("(ا إ ص)")
    data.append(int(results["test6"]["percentile"]))
    labels.append("(ف م ق)")
    print("data)")
    print(data)

    pct_values_by_test = {
        "(ق ك م)": results["test1"]["percentile"],  # ← use your real abbreviations
        "(ط ق ج)":  results["test2"]["percentile"],
        "(ط ف م)": results["test3"]["percentile"],
        "(إ ك)": results["test4"]["percentile"],
        "(ا إ ص)": results["test5"]["percentile"],
        "(ف م ق)": results["test6"]["percentile"],
    }
    

    print(pct_values_by_test)

    chart_labels = ["3","2,5","2","1,5","1","0,5","صفر", "0,5-","1-","1,5-","2-", "2,5-", "3-", "3,5-", "4-"]
    chart_percentile_labels = ["160","150","140","130","120","110","100", "90","80","70","60", "50", "40", "30", "20"]
    chart_std_labels = ["90","80","70","60","50","40","30", "20","10","5","1"]

    chart_pairs = list(zip(chart_labels, chart_percentile_labels))
    #print(chart_data)
    #print(chart_data["chart_labels"])

    chart_rows_std = build_std_chart(std_values_by_test)
    chart_rows_pct = build_pct_chart(pct_values_by_test)
    print(chart_rows_std)





    #send prepare data to send to the html
    context = {
        "student": {"name": student.studentName, "gender": student.gender, "school": student.schoolName, "grade": student.grade, "District": student.eduDistrict, "nationality": student.nationality,  "examDate": student.examDate, "birthDate": student.birthDate, "age": student.age, "age_year": student_age_year, "age_month": student_age_month, "age_day": student_age_day, "examiner": examiner.name, "specalist": examiner.speciality},
        "test1": {"raw_score": test1.total_correct, "time_sec": test1.time_seconds},
        "test2": {"raw_score": test2.total_score, "time_sec": test2.time_seconds},
        "test3": {"raw_score": test3.total_correct, "time_sec": test3.total_time_secs},
        "test4": {"raw_score": test4.total_correct},
        "test5": {"raw_score": test5.total_correct, "time_sec": test5.total_time_secs},
        "test6": {"raw_score": test6.total_correct, "time_sec": test6.total_time_secs},
        "results": results,
        "total_raw_score": total_raw_score,
        "total_percentile" : total_percentile,
        "total_std": total_std,
        "chart_rows_std": chart_rows_std,
        "chart_rows_pct": chart_rows_pct,
        "chart_data": chart_pairs,
        "chart_std_labels": chart_std_labels,
        'data': json.dumps(data), 
        'labels': json.dumps(labels),
        'datastd': json.dumps(datastd), 
        'labelstd': json.dumps(labelstd),
        "test1_latest": test1_latest,
        "test2_latest": test2_latest,
        "test3_latest": test3_latest,
        "test4_latest": test4_latest,
        "test5_latest": test5_latest,
        "test6_latest": test6_latest,
        "note_latest": note_latest,
        "strength_latest": strength_latest,
        'weakness_latest': weakness_latest,
        "result_latest": result_latest,
        "suggestion_latest": suggestion_latest



    }
    return render(request, "primary_test/result.html", context)

@login_required(login_url="/login")
def secondary_result(request):
    student = Student.objects.get(id=request.session['student'])
    examiner = Examiner.objects.get(user_id = request.user.id)
    student_age_year = student.age.split('/')[0]
    student_age_month = student.age.split('/')[1]
    student_age_day = student.age.split('/')[2]
    test1 = SecondaryTest1.objects.filter(student_id = request.session['student']).latest("id")
    test2 = SecondaryTest2.objects.filter(student_id = request.session['student']).latest("id")
    test3 = SecondaryTest3.objects.filter(student_id = request.session['student']).latest("id")
    test4 = SecondaryTest4.objects.filter(student_id = request.session['student']).latest("id")
    note_latest = ""
    strength_latest = ""
    weakness_latest = ""
    result_latest = ""
    suggestion_latest = ""

    result_secondary = SecondaryResult.objects.filter(student_id = request.session['student'])
    print(result_secondary)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == "submit":
            note = request.POST['note']
            strength = request.POST['strength']
            weakness = request.POST['weakness']
            result = request.POST['results']
            suggestion = request.POST['suggestion']

            secondaryresult = SecondaryResult.objects.create( student= student, examiner = examiner, notes= note, strength=strength, weakness = weakness, result = result, suggestion = suggestion)
            secondaryresult.save()

    
    finalReport_exist = result_secondary.exists()
    if finalReport_exist:
        note_latest = SecondaryResult.objects.filter(student_id=request.session['student']).latest("id").notes
        strength_latest = SecondaryResult.objects.filter(student_id=request.session['student']).latest("id").strength
        weakness_latest = SecondaryResult.objects.filter(student_id=request.session['student']).latest("id").weakness
        result_latest = SecondaryResult.objects.filter(student_id=request.session['student']).latest("id").result
        suggestion_latest = SecondaryResult.objects.filter(student_id=request.session['student']).latest("id").suggestion

    # Pull raw scores
    raw_scores = {
        "test1": test1.total_correct,
        "test2": test2.total_correct,
        "test3": test3.total_correct,
        "test4": test4.total_correct,
    }

    # Run lookup
    results = lookup_scores_secondary(
        grade=str(student.grade),
        test1_raw=raw_scores["test1"],
        test2_raw=raw_scores["test2"],
        test3_raw=raw_scores["test3"],
        test4_raw=raw_scores["test4"],
    )

    
    total_raw_score = raw_scores["test1"] + raw_scores["test2"] + raw_scores["test3"] + raw_scores["test4"] 
    total_percentile = results["test1"]["percentile"] + results["test2"]["percentile"] + results["test3"]["percentile"] + results["test4"]["percentile"]
    total_std = results["test1"]["std"] + results["test2"]["std"] + results["test3"]["std"] + results["test4"]["std"] 

    datastd = []
    labelstd = []

    datastd.append(int(results["test1"]["percentile"]))
    labelstd.append("قراءة الكلمة المفردة")
    datastd.append(int(results["test2"]["percentile"]))
    labelstd.append("الطلاقة في قراءة الجملة")
    datastd.append(int(results["test3"]["percentile"]))
    labelstd.append("الطلاقة في فهم المقطع")
    datastd.append(int(results["test4"]["percentile"]))
    labelstd.append("إملاء الكلمة")
    print("datastd")
    print(datastd)
    print(labelstd)

    # pull the Modified Standard per test (std)
    std_values_by_test = {
        "(ق ك م)": results["test1"]["std"],  # ← use your real abbreviations
        "(ط ف م)":  results["test2"]["std"],
        "(إ ك)": results["test3"]["std"],
        "(ف م ق)": results["test4"]["std"],
    }

    print(std_values_by_test)

    data = []
    labels = []

    data.append(int(results["test1"]["percentile"]))
    labels.append("(ق ك م)")
    data.append(int(results["test2"]["percentile"]))
    labels.append("(ط ق ج)")
    data.append(int(results["test3"]["percentile"]))
    labels.append("(ط ف م)")
    data.append(int(results["test4"]["percentile"]))
    labels.append("(إ ك)")
    print("data)")
    print(data)

    pct_values_by_test = {
        "(ق ك م)": results["test1"]["percentile"],  # ← use your real abbreviations
        "(ط ق ج)":  results["test2"]["percentile"],
        "(ط ف م)": results["test3"]["percentile"],
        "(إ ك)": results["test4"]["percentile"],
    }
    

    print(pct_values_by_test)

    chart_labels = ["متفوق","متفوق","فوق المتوسط","فوق المتوسط","متوسط","أقل من المتوسط","أقل من المتوسط", "متدن","متدن","متدن جدا","متدن جدا"]
    chart_percentile_labels = ["90","80","70","60","50","40","30", "20","10","5","1"]
    chart_std_labels = ["90","80","70","60","50","40","30", "20","10","5","1"]

    chart_pairs = list(zip(chart_labels, chart_percentile_labels))
    #print(chart_data)
    #print(chart_data["chart_labels"])

    chart_rows_std = build_std_chart(std_values_by_test)
    chart_rows_pct = build_pct_chart(pct_values_by_test)
    print(chart_rows_std)





    #send prepare data to send to the html
    context = {
        "student": {"name": student.studentName, "gender": student.gender, "school": student.schoolName, "grade": student.grade, "District": student.eduDistrict, "nationality": student.nationality,  "examDate": student.examDate, "birthDate": student.birthDate, "age": student.age, "age_year": student_age_year, "age_month": student_age_month, "age_day": student_age_day, "examiner": examiner.name, "specalist": examiner.speciality},
        "test1": {"raw_score": test1.total_correct, "time_sec": test1.time_seconds},
        "test2": {"raw_score": test2.total_correct, "time_sec": test2.total_time_secs},
        "test3": {"raw_score": test3.total_correct},
        "test4": {"raw_score": test4.total_correct},
        "results": results,
        "total_raw_score": total_raw_score,
        "total_percentile" : total_percentile,
        "total_std": total_std,
        "chart_rows_std": chart_rows_pct,
        "chart_rows_pct": chart_rows_pct,
        "chart_data": chart_pairs,
        "chart_std_labels": chart_std_labels,
        'data': json.dumps(data), 
        'labels': json.dumps(labels),
        'datastd': json.dumps(datastd), 
        'labelstd': json.dumps(labelstd),
        "note_latest": note_latest,
        "strength_latest": strength_latest,
        'weakness_latest': weakness_latest,
        "result_latest": result_latest,
        "suggestion_latest": suggestion_latest



    }
    return render(request, "secondary_test/result.html", context)



def build_std_chart(std_values_by_test, labels_by_test=None, mean=100.0, sd=15.0):
    """
    std_values_by_test: {"test1": 104, "test2": 96, ...}  (Modified Standard)
    Returns rows only (same as your original): [
      {"std_label": "...", "std_value": 104, "cells": [0/1,...], "hit_index": int|None}
    ]
    We bin the *std* directly into 15 columns: 20,30,...,160.
    """

    # 15 bins: 20..160 step 10
    bin_edges = list(range(160, 19, -10))
    lo, hi = 20, 160 

    rows = []
    for key, std in std_values_by_test.items():
        label = labels_by_test.get(key, key) if labels_by_test else key

        if std is None:
            cells = [0] * len(bin_edges)
            hit_idx = None
            disp = ""
        else:
            s = float(std)
            # clip to [20, 160]
            s = max(lo, min(hi, s))

            # Choose a bin (NEAREST). This respects descending order.
            idx = min(range(len(bin_edges)), key=lambda i: (abs(s - bin_edges[i]), bin_edges[i]))


            cells = [1 if i == idx else 0 for i in range(len(bin_edges))]
            hit_idx = idx
            disp = std  # show original std value

        rows.append({
            "std_label": label,
            "std_value": disp,
            "cells": cells,
            "hit_index": hit_idx,
        })

    return rows

def build_pct_chart(values_by_test, labels_by_test=None):
    """
    values_by_test: {"test1": 42, "test2": 77, ...} (percentile ranks)
    Bins: [1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90]
    Returns rows like build_std_chart.
    """
    bin_edges = [90, 80, 70, 60, 50, 40, 30, 20, 10, 5, 1]

    rows = []
    for key, val in values_by_test.items():
        label = labels_by_test.get(key, key) if labels_by_test else key

        if val is None:
            cells = [0] * len(bin_edges)
            hit_idx = None
            disp = ""
        else:
            v = float(val)
            # Clip to [1, 90]
            v = min(max(v, 1), 90)

            # Find the *first bin ≤ value* (so the mark sits at/below the percentile)
            idx = next((i for i, b in enumerate(bin_edges) if v >= b), len(bin_edges) - 1)


            cells = [1 if i == idx else 0 for i in range(len(bin_edges))]
            hit_idx = idx
            disp = val

        rows.append({
            "pct_label": label,
            "pct_value": disp,
            "cells": cells,
            "hit_index": hit_idx,
        })

    return rows


# helpers_c.py (or inside percentile_lookup.py)



def round_tens_booklet(p: int) -> int:
    """Booklet rule: <=5 down, >5 up."""
    if p is None:
        return None
    ones = p % 10
    base = (p // 10) * 10
    return base if ones <= 5 else base + 10

def build_std_hits_per_test(std_values_by_test, mean=100.0, sd=15.0):
    """
    Returns:
      tests: list of {"label": key, "std_value": v, "hit_index": idx}
      std_bins: list of {"label": <axis label>, "percentile": <display>, "idx": i}
    """
    # bins for z: -4 .. +3 step 0.5
    z_bins = [round(-4.0 + 0.5*i, 1) for i in range(15)]
    # display row labels you’re already using:
    chart_labels =  ["3","2,5","2","1,5","1","0,5","صفر","0,5-","1-","1,5-","2-","2,5-","3-","3,5-","4-"]
    chart_pcts   =  ["160","150","140","130","120","110","100","90","80","70","60","50","40","30","20"]
    std_bins = [{"label": l, "percentile": p, "idx": i} for i, (l,p) in enumerate(zip(chart_labels, chart_pcts))]

    tests = []
    for key, std in std_values_by_test.items():
        if std is None:
            tests.append({"label": key, "std_value": None, "hit_index": None})
            continue
        z = max(-4.0, min(3.0, (float(std) - mean) / sd))
        # nearest-bin is visually cleaner; switch to ceil if you want
        hit_idx = min(range(len(z_bins)), key=lambda i: abs(z - z_bins[i]))
        tests.append({"label": key, "std_value": int(std), "hit_index": hit_idx})
    return tests, std_bins

def build_percentile_hits_per_test(percentiles_by_test):
    """
    Returns:
      tests: list of {"label": key, "percentile": p_rounded, "hit_index": idx}
      pct_bins: list of {"label": str(val), "idx": i}
    """
    # Tens bins 20..160 (match booklet)
    values = list(range(20, 161, 10))
    pct_bins = [{"label": str(v), "idx": i} for i, v in enumerate(values)]

    index_by_value = {v: i for i, v in enumerate(values)}
    tests = []
    for key, p in percentiles_by_test.items():
        if p is None:
            tests.append({"label": key, "percentile": None, "hit_index": None})
            continue
        pr = round_tens_booklet(int(p))
        # clamp to [20,160] if outside
        pr = max(20, min(160, pr))
        hit_idx = index_by_value.get(pr)
        tests.append({"label": key, "percentile": pr, "hit_index": hit_idx})
    return tests, pct_bins


#Secondary test 1
@login_required(login_url="/login")
def secondary_test1_training(request):
    if request.method == 'POST':
        training_scores = [int(request.POST.get(f'train_{i}', 0)) for i in range(3)]
        passed_training = all(score == 1 for score in training_scores)

        if passed_training:
            request.session['training_passed'] = True
            return redirect('secondary_test1')
        else:
            return render(request, 'secondary_test/test1_training.html', {
                'training_words': TRAINING_WORDSـSEC,
                'error': 'لم يتم اجتياز التدريب. لا يمكن المتابعة.'
            })

    return render(request, 'secondary_test/test1_training.html', {
        'training_words': TRAINING_WORDSـSEC
    })

@login_required(login_url="/login")
def secondary_test1(request):
    student = Student.objects.get(id=request.session['student'])

    # Modal confirmation submit
    if request.method == 'POST' and request.POST.get("form2"):
        # Get saved values from session
        total_correct = request.session.get('test1_total_correct', 0)
        time_seconds = request.session.get('test1_time_seconds', 0)
        fluency = request.session.get('test1_fluency', 0)
        reason = request.POST.get("submitTst", "")

        # Save final test result
        SecondaryTest1.objects.create(
            student=student,
            total_correct=total_correct,
            time_seconds=time_seconds,
            fluency_score=fluency,
            reason=reason,
            date=datetime.now()
        )

        # Clear session if you want
        if(reason != "الوصول الى الحد السقفي"):
            del request.session['test1_total_correct']
            del request.session['test1_time_seconds']
            del request.session['test1_fluency']

        return redirect('testsPageSec')

    # Main test submission (score & time)
    if request.method == 'POST' and request.POST.get("form1"):
        test_scores = [int(request.POST.get(f'test_{i}', 0)) for i in range(40)]
        total_correct = sum(test_scores)

        try:
            time_seconds = float(request.POST.get('time', 1))  # avoid divide-by-zero
        except:
            time_seconds = 1

        fluency = (total_correct / time_seconds) * 60

        # Store in session for confirmation step
        request.session['test1_total_correct'] = total_correct
        request.session['test1_time_seconds'] = time_seconds
        request.session['test1_fluency'] = round(fluency, 2)

        return render(request, 'secondary_test/test1.html', {
            'test_words': TEST_WORDS_secondary_test1,
            'result': {
                'total_correct': total_correct,
                'time_seconds': time_seconds,
                'fluency': round(fluency, 2)
            }
        })

    return render(request, 'secondary_test/test1.html', {
        'test_words': TEST_WORDS_secondary_test1
    })


def secondary_test2_training(request):
    # --- First Visit ---
    if request.method == "GET" and not request.headers.get("HX-Request"):
        request.session['training_correct'] = 0
        return render(request, "secondary_test/test2_training.html", {
            "question": secondary_test2_training_questions[0],
            "index": 0
        })

    # --- GET: Load Next Question via HTMX ---
    if request.method == "GET" and request.headers.get("HX-Request") == "true":
        index = int(request.GET.get("index", 0))
        is_final = request.GET.get("final") == "true"

        if is_final:
            passed = request.session.get('training_correct', 0) > 0
            return render(request, 'secondary_test/test2_training_correct_result.html', {
                'show_final_result': True,
                'passed': passed
            })

        if index < len(secondary_test2_training_questions):
            return render(request, "secondary_test/test2_training_question.html", {
                "question": secondary_test2_training_questions[index],
                "index": index
            })

    # --- POST: Answer Clicked OR "التالي" ---
    if request.method == "POST":
        index = int(request.POST.get("index", 0))
        selected = request.POST.get("answer")
        question = secondary_test2_training_questions[index]
        correct = question["correct"]
        next_index = index + 1
        total = len(secondary_test2_training_questions)
        is_last = next_index >= total
        passed = request.session.get('training_correct', 0) > 0 if is_last else None

    if selected:
        if 'training_correct' not in request.session:
            request.session['training_correct'] = 0

        if selected == correct:
            request.session['training_correct'] += 1



    return render(request, "secondary_test/test2_training_correct_result.html", {
        "is_correct": selected == correct,
        "correct": correct,
        "selected": selected,
        "index": next_index,
        "question": question,
        "total_questions": total,
        "passed": passed
    })



def _test2_init(request):
    s = request.session
    s['t2_index'] = 0
    s['t2_answers'] = []
    s['t2_scores']  = []
    s['t2_durations'] = []
    s['t2_started_at'] = time.time()
    s['t2_qstart_at']  = time.time()
    s.modified = True

@login_required(login_url="/login")
def secondary_test2(request):
    print('inside secondary_test2')
    student = Student.objects.get(id=request.session['student'])

    # First test page load (Q1)
    if request.method == "GET" and not request.headers.get("HX-Request"):
        print('first test display')
        _test2_init(request)
        return render(request, "secondary_test/test2.html", {
            "question": main_questions[0],
            "index": 0
        })

    # HTMX POST: when a button is clicked (answer / skip / stop)
    if request.method == "POST" and request.headers.get("HX-Request") == "true":
        print('when answering button click')
        s = request.session
        idx = s.get('t2_index', 0)
        answers = s.get('t2_answers', [])
        scores  = s.get('t2_scores', [])
        durs    = s.get('t2_durations', [])
        qstart  = s.get('t2_qstart_at', time.time())

        action   = request.POST.get("action")
        selected = request.POST.get("answer")
        stop_reason = request.POST.get("stop_reason", "").strip()

        # computation time
        elapsed = round(time.time() - qstart, 3)

        # STOP (the examsiner stopped the test)
        if action == "stop":
            print('stop button clicked')

            # Mark current question duration as "-" since stopped in modal
            durs.append("-")
            answers.append("-")
            scores.append("-")

            # Fill rest of unanswered questions with "-"
            remaining = len(main_questions) - (idx + 1)
            if remaining > 0:
                answers.extend(["-"] * remaining)
                scores.extend(["-"] * remaining)
                durs.extend(["-"] * remaining)

            
            stop_reason = request.POST.get("stop_reason", "").strip()

            

            # Count only actual numeric scores
            total_correct = sum(1 for x in scores if x == 1)

            total_time_secs = round(sum(d for d in durs if isinstance(d, (int, float))), 3)  # elapsed seconds
                
            SecondaryTest2.objects.create(
                student=student,
                raw_scores = scores,
                total_correct=total_correct,
                durations = durs, #per question duration
                reason=stop_reason,
                total_time_secs = total_time_secs,
                date=datetime.now()
            )


            test_profile_url = reverse('testsPageSec')  # adjust to your URL
            resp = HttpResponse('')
            resp['HX-Redirect'] = test_profile_url
            return resp

        # ANSWER / SKIP branch
        elapsed = round(time.time() - qstart, 3)

        # Normalize to exactly 4.000 for auto-skip
        if 3.9 <= elapsed <= 4.2:
            elapsed = 4.000

        durs.append(elapsed)

        if selected in [None, ""]:
            answers.append("-")
            scores.append("-")
        else:
            answers.append(selected)
            correct = main_questions[idx]["correct"]
            scores.append(1 if selected == correct else 0)

        # advance index
        idx += 1
        s['t2_index'] = idx
        s['t2_answers'] = answers
        s['t2_scores']  = scores
        s['t2_durations'] = durs
        s['t2_qstart_at'] = time.time()
        s.modified = True

        # next question or finish
        if idx < len(main_questions):
            print('next question or finished')
            html = render_to_string("secondary_test/test2_question.html", {
                "question": main_questions[idx],
                "index": idx
            }, request=request)
            return HttpResponse(html)

        # finished
        total_correct = sum(1 for s_ in scores if s_ == 1)
        # save to DB
        answers  = s.get('t2_answers', [])
        scores   = s.get('t2_scores', [])
        durations = s.get('t2_durations', [])
        total_correct = sum(1 for x in scores if x == 1)
        # calculate started_at datetime and total_time_secs
        started_at = None
        total_time_secs = None
        if s.get('t2_started_at'):
            start_ts = s['t2_started_at']
            #started_at = timezone.datetime.fromtimestamp(start_ts, tz=timezone.get_current_timezone())
            total_time_secs = round(time.time() - start_ts, 3)  # total duration in seconds
        
        SecondaryTest2.objects.create(
            student=student,
            raw_scores = scores,
            total_correct=total_correct,
            durations = durations, #per question duration
            reason=stop_reason,
            total_time_secs = total_time_secs,
            date=datetime.now()
        )

        # redirect or inline result
        test_profile_url = reverse('testsPageSec')  # adjust to your URL
        resp = HttpResponse('')
        resp['HX-Redirect'] = test_profile_url
        return resp

    # fallback
    _test2_init(request)
    return render(request, "secondary_test/test2.html", {
        "question": main_questions[0],
        "index": 0
    })



@login_required(login_url="/login")
def secondary_test3_training(request):
    test_words = secondary_test3_training_words
    start = 0
    submitted = {} 
    rows = list(enumerate(test_words[start:], start=start))

    if request.method == 'POST':
        for idx, correct_word in rows: 
            typed = request.POST.get(f"word_{idx}", "") 
            submitted[f"word_{idx}"] = typed


        passed_training = typed == correct_word["text"] 

        if passed_training:
            request.session['training_passed'] = True
            return redirect('secondary_test3')
        else:
            return render(request, 'secondary_test/test3_training.html', {
                'training_words': secondary_test3_training_words,
                'error': 'لم يتم اجتياز التدريب. لا يمكن المتابعة.'
            })

    return render(request, 'secondary_test/test3_training.html', {
        'training_words': secondary_test3_training_words
    })

@login_required(login_url="/login")
def secondary_test3(request):
    student = Student.objects.get(id=request.session['student'])
    test_words = secondary_test3_words
    start = 0 
    rows = list(enumerate(test_words[start:], start=start))

    submitted = {} 
    results = [] 
    idx_map = {} # quick lookup by idx for the template 
    correct_count = 0

    # Modal confirmation submit
    if request.method == 'POST' and request.POST.get("form2"):
        print(request.POST)
        # Get saved values from session
        total_correct = request.session.get('test3_total_correct', 0)
        raw_scores = request.session.get('test3_raw_scores', [])
        reason = request.POST.get("submitTst", "")


        # Save final test result
        SecondaryTest3.objects.create(
            student=student,
            raw_scores = raw_scores,
            total_correct=total_correct,
            reason=reason,
            date=datetime.now()
        )

        # Clear session if you want
        if reason != "الوصول الى الحد السقفي":
            request.session.pop('test3_total_correct', None)
            request.session.pop('test3_raw_scores', None)


        return redirect('testsPageSec')

    # Main test submission (score & time)
    if request.method == 'POST' and request.POST.get("form1"):
        for idx, correct_word in rows: 
            typed = request.POST.get(f"word_{idx}", "") 
            submitted[f"word_{idx}"] = typed


            ok = typed == correct_word["text"] 
            result = { 
                "idx": idx, 
                "typed": typed, 
                "correct_word": correct_word["text"], 
                "correct": ok, 
                }
            
            results.append(result) 
            idx_map[idx] = result 
            if ok: 
                correct_count += 1

        # Save to session for modal confirmation
        request.session['test3_total_correct'] = correct_count
        request.session['test3_raw_scores'] = results

        return render(request, 'secondary_test/test3.html', {
            'test_words': secondary_test3_words,
            'result': {
                'total_correct': correct_count,
            }
        })
    return render(request,"secondary_test/test3.html", {
        'test_words': secondary_test3_words
    })


def secondary_test4_training(request):
    # --- First Visit ---
    if request.method == "GET" and not request.headers.get("HX-Request"):
        para = test4_training_questions[0]
        paragraph_text = para["paragraph"]
        question = para["questions"][0]
        question_text = question["question"]
        answers = question["answers"]
        request.session['training_correct'] = 0
        return render(request, "secondary_test/test4_training.html", {
            #"question": test4_training_questions[0],
            "paragraph": paragraph_text,
            "question": question,
            "question_text": question_text,
            "answers": answers,
            "index": 0
        })

    # --- GET: Load Next Question via HTMX ---
    if request.method == "GET" and request.headers.get("HX-Request") == "true":
        index = int(request.GET.get("index", 0))
        is_final = request.GET.get("final") == "true"

        if is_final:
            passed = request.session.get('training_correct', 0) > 0
            return render(request, 'secondary_test/test4_training_correct_result.html', {
                'show_final_result': True,
                'passed': passed
            })

        if index < len(test4_training_questions):
            para = test4_training_questions[index]
            paragraph_text = para["paragraph"]
            question = para["questions"][0]
            question_text = question["question"]
            answers = question["answers"]
            return render(request, "secondary_test/test4_training_question.html", {
                #"question": test4_training_questions[index],
                "paragraph": paragraph_text,
                "question": question,
                "question_text": question_text,
                "answers": answers,
                "index": index
            })

    # --- POST: Answer Clicked OR "التالي" ---
    if request.method == "POST":
        index = int(request.POST.get("index", 0))
        selected = request.POST.get("answer")
        question = test4_training_questions[index]
        correct = question["questions"][0]["correct"]
        paragraph_text = question["paragraph"]
        question_first = question["questions"][0]
        question_text = question_first["question"]
        answers = question_first["answers"]
        next_index = index + 1
        total = len(test4_training_questions)
        is_last = next_index >= total
        passed = request.session.get('training_correct', 0) > 0 if is_last else None

    if selected:
        if 'training_correct' not in request.session:
            request.session['training_correct'] = 0

        if selected == correct:
            request.session['training_correct'] += 1



    return render(request, "secondary_test/test4_training_correct_result.html", {
        "is_correct": selected == correct,
        "correct": correct,
        "selected": selected,
        "index": next_index,
        "question": question,
        "paragraph_text": paragraph_text,
        "question_first": question_first,
        "question_text": question_text,
        "answers": answers,

        "total_questions": total,
        "passed": passed
    })

def linear_to_pq(data, idx):
    """
    Convert linear index (0..N-1) -> (p_idx, q_idx).
    """
    running = 0
    for p_idx, block in enumerate(data):
        qn = len(block["questions"])
        if idx < running + qn:
            return p_idx, (idx - running)
        running += qn
    return None, None  # finished

def get_linear_question(data, idx):
    """
    Return (paragraph_dict, question_dict) for linear idx.
    """
    p_idx, q_idx = linear_to_pq(data, idx)
    if p_idx is None:
        return None, None
    para = data[p_idx]
    q = para["questions"][q_idx]
    return para, q

def _test4_init(request):
    s = request.session
    s['t4_index'] = 0
    s['t4_answers'] = []
    s['t4_scores']  = []
    s['t4_durations'] = []
    s['t4_started_at'] = time.time()
    s['t4_qstart_at']  = time.time()
    s['t4_total'] = sum(len(p["questions"]) for p in test4_main_questions)
    s.modified = True

    

@login_required(login_url="/login")
def secondary_test4(request):
    student = Student.objects.get(id=request.session['student'])

    data = test4_main_questions
    total = sum(len(p["questions"]) for p in data)

    # First test page load (Q1)
    if request.method == "GET" and not request.headers.get("HX-Request"):
        _test4_init(request)
        para, q = get_linear_question(data, 0)
        return render(request, "secondary_test/test4.html", {
            "question": {
                "id": q["id"],
                "question": q["question"],
                "answers": q["answers"],
                "correct": q.get("correct"),
                "paragraph": para["paragraph"],
                "paragraph_id": para.get("paragraph_id"),
            },
            "index": 0,
            "total": total,
        })

    # HTMX POST: when a button is clicked (answer / skip / stop)
    if request.method == "POST" and request.headers.get("HX-Request") == "true":
        s = request.session
        idx      = s.get('t4_index', 0)
        answers  = s.get('t4_answers', [])
        scores   = s.get('t4_scores', [])
        durs     = s.get('t4_durations', [])
        qstart   = s.get('t4_qstart_at', time.time())
        started  = s.get('t4_started_at', time.time())

        action      = request.POST.get("action")
        selected    = request.POST.get("answer")
        stop_reason = request.POST.get("stop_reason", "").strip()

        # computation time
        elapsed = round(time.time() - qstart, 3)

        # STOP (the examiner stopped the test)
        if action == "stop":
            # Mark current question duration as "-" since stopped in modal
            durs.append("-")
            answers.append("-")
            scores.append("-")

            # Fill rest with "-"
            remaining = total - (idx + 1)
            if remaining > 0:
                answers.extend(["-"] * remaining)
                scores.extend(["-"] * remaining)
                durs.extend(["-"] * remaining)

            # Count only actual numeric scores
            total_correct = sum(1 for x in scores if x == 1)
            total_time_secs = round(sum(d for d in durs if isinstance(d, (int, float))), 3)

            SecondaryTest4.objects.create(
                student=student,
                raw_scores=scores,
                total_correct=total_correct,
                durations=durs,
                reason=stop_reason,
                total_time_secs=total_time_secs,
                date=datetime.now()
            )

            test_profile_url = reverse('testsPageSec')
            resp = HttpResponse('')
            resp['HX-Redirect'] = test_profile_url
            return resp

        # ANSWER / SKIP branch
        # Normalize to exactly 4.000 for auto-skip (keep same behavior as test2, if you use it)
        if 3.9 <= elapsed <= 4.2:
            elapsed = 4.000
        durs.append(elapsed)

        # record answer & score
        para_now, q_now = get_linear_question(data, idx)
        if selected in [None, ""]:
            answers.append("-")
            scores.append("-")
        else:
            answers.append(selected)
            correct = q_now.get("correct")
            scores.append(1 if (selected == correct) else 0)

        # advance index
        idx += 1
        s['t4_index'] = idx
        s['t4_answers'] = answers
        s['t4_scores']  = scores
        s['t4_durations'] = durs
        s['t4_qstart_at'] = time.time()
        s.modified = True

        # next question or finish
        if idx < total:
            para_next, q_next = get_linear_question(data, idx)
            html = render_to_string("secondary_test/test4_question.html", {
                "question": {
                    "id": q_next["id"],
                    "question": q_next["question"],
                    "answers": q_next["answers"],
                    "correct": q_next.get("correct"),
                    "paragraph": para_next["paragraph"],
                    "paragraph_id": para_next.get("paragraph_id"),
                },
                "index": idx,
                "total": total,
            }, request=request)
            return HttpResponse(html)

        # finished — compute totals & save
        scores_ = s.get('t4_scores', [])
        durations_ = s.get('t4_durations', [])
        total_correct = sum(1 for x in scores_ if x == 1)  # only numeric 1's
        total_time_secs = round(time.time() - started, 3) if started else None

        SecondaryTest4.objects.create(
            student=student,
            raw_scores=scores_,
            total_correct=total_correct,
            durations=durations_,
            reason=stop_reason,
            total_time_secs=total_time_secs,
            date=datetime.now()
        )

        test_profile_url = reverse('testsPageSec')
        resp = HttpResponse('')
        resp['HX-Redirect'] = test_profile_url
        return resp

    # fallback (fresh start)
    _test4_init(request)
    para, q = get_linear_question(data, 0)
    return render(request, "secondary_test/test4.html", {
        "question": {
            "id": q["id"],
            "question": q["question"],
            "answers": q["answers"],
            "correct": q.get("correct"),
            "paragraph": para["paragraph"],
            "paragraph_id": para.get("paragraph_id"),
        },
        "index": 0,
        "total": total,
    })
