#from pyexpat.errors import messages
from django.shortcuts import *
from django.contrib.auth import *
from django.contrib import *
from django.http import *
from .models import *
from django.views.decorators.csrf import csrf_exempt
#from .models import Student
#from .models import Score
#from .models import *
#from django.urls import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.template.loader import render_to_string
#from dateutil import relativedelta
#import pandas as pd
#from primary.utils import return_scores, return_scores_Sec
#import json
#from django.core.mail import send_mail
#from django.conf import settings

# Test1 data.
TRAINING_WORDS = ['رَكِبَ', 'بَيْتٍ', 'حَمَدٌ']
TEST_WORDS = [
    "أُخْتي", "تَحْتَوي", "هذانِ", "الرَّبيعُ", "الْوَجيزُ",
    "جَمَلٌ", "أَوْصِلْ", "بحَرَكاتِهِ", "التّالِيَةُ", "الدَّوْلَتانِ",
    "الَّذينَ", "التَّعْبيرَ", "أَسْطُرٍ","عَلَيْهِ","الُْمناسَبَةُ",
    "الأَطْعِمَةِ", "اِسْتِخْراجُ", "بِمَواقِعِها", "الثَّلاثَ", "وَأَلْوَانٍ",
    "إِنْشائِكَ", "هؤلاءِ", "الْوَحْدَةِ", "بِالأَرْواحِ","الْفُِقَراءُ",
    "وَالاِسْتيعابَ", "اللُّغَوِيُّ", "اِضْبِطْ", "تُضْنيني", "لِلَّهِ"
]

TRAINING_WORDSـSEC = ['رَكِبَ', 'بَيْتٍ', 'حَمَدُُ']
TEST_WORDS_secondary_test1 = [
    "الَّذينَ", "يَخْتاروا", "شَيْئًا", "أُولئِكَ", "اِسْتِخْراجُ",
    "عَلَيْهِ", "الْفُقَراءُ", "الثَّلاثَ", "بِالأَرْواحِ", "التَّعْبيرَ",
    "هؤلاءِ", "مُتَجانِسًا", "بِاسْتِطاعَتِهِ", "إِنْشائِكَ", "حَوائِجَهُمْ",
    "بِمَواقِعِها", "أَسْطُرِ", "الْأَطْعِمَةِ", "مُؤَسِّسينَ", "غِذائِيَّةُُ",
    "اِضْبِطْ", "تُضْنيني", "مُؤازَرَةُُ", "يُرْتَجى", "الْمُناسَبَةُ",
    "تَباطُؤْ", "عامَلوني", "بِهَوائِهِ", "وَأَلْوانٍ", "لِلهِ",
    "اِصْطَدَمَ", "الْاِصْطِناعِيَّةُ", "وَالْاِسْتيعابَ", "التِّسْعينِيّاتْ", "اِنْتَظَرْتُكَ",
    "الْكَفاءاتِ", "فَتًى", "ٱللُّغَوِيُّ", "الْوَحْدَةِ", "مُتَلَأْلِئَةً"
]

training_sentences = {
        1: "التِّلْميذُ مُجْتَهِدٌ",
        2: "تُشْرِقُ الشَّمْسُ صَباحاً",
        3: "تَعيشُ الأَسْماكُ فيِ الْماءِ"
}

primary_test2_sentences = {
    1: "أُحِبُّ حَديقَةَ الْحَيَواناتِ.",
    2: "يَشْرَبُ مُحَمَّدٌ الْماءَ.",
    3: "حَرارَةُ الشَّمْسِ شَديدَةٌ.",
    4: "نَذْهَبُ إِلى الْـبَحْرِ لِصَيْدِ السَّمَكِ.",
    5: "فازَ فَريقُ كُرَةِ الْقَدَمِ بِالْجائِزَةِ الأولى لِلْمَرَّةِ الثّانِيَةِ.",
    6: "بُسْتانُ بَيْتِنا جميلٌ تَمْلَؤُهُ الأَزْهارُ و الأَشْجَارُ.",
    7: "جَمَعَتْ عَبيرُ مَعَ أَفْرادِ الأُسْرَةِ تُفّاحاً كَثيراً مِنْ شَجَرَةِ التُّفّاحِ",
    8: "تُهاجِرُ الْكَثيرُ مِنَ الطُّيورِ إِلى جَزيرَةِ الْعَرَبِ وَ تُقيمُ فيها في فَصْلِ الشِّتاءِ.",
    9: "الْخَيْلُ الْعَرَبِيُّ مِنْ أَجْمَلِ الْحَيَواناتِ، لَهُ رَأْسٌ مُسْتَقيمٌ، وَ صَدْرٌ واسِعٌ، وَ قَوائِمُ رَشيقَةٌ، هُوَ قَوِيٌّ شَهْمٌ، إِنَّهُ أَجْمَلُ جَوادٍ عَلى وَجْهِ الأَرْضِ.",
    10: "اِنْتَظَرَ فَيْصَلٌ بِصُحْبَةِ الرَّجُلِ الْكَفيفِ في الْمَكانِ الْمُخَصَّصِ لِعُبورِ الْمُشاةِ، وَ عِنْدَما تَوّقَّفَتِ السَّيّاراتُ، عَبَرَ فَيْصَلٌ الشّارِعَ مُمْسِكاً بِيَدِ الرَّجُلِ، فَشَكَرَ الرَّجُلُ فَيْصَلاً وَ دَعا لَهُ."
}

primary_test4_words = [
    "", "", "", "", "",
    "", "", "", "", "",
    "", "", "","","",
    "", "", "", "", "",
    "", "", "", "","",
    "", "", "", "", ""
]

secondary_test3_words = [
    "", "", "", "", "",
    "", "", "", "", "",
    "", "", "","","",
    "", "", "", "", "",
    "", "", "", "","",
    "", "", "", "", "",
    "", "", "", "","",
    "", "", "", ""
]

secondary_test2_training_questions = [
    {
        "text": "خَرَجَ مُحَمّدُُ لِيَلْعَبَ مَعَ ..........",
        "options": [
            {"label": "أ", "text": "السّيّاراتِ", "value": "أ"},
            {"label": "ب", "text": "رِفاقِهِ", "value": "ب"},
            {"label": "ج", "text": "الشّمْسِ", "value": "ج"},
            {"label": "د", "text": "الْكُرَةِ", "value": "د"},
        ],
        "correct": "ب"
    },
    {
        "text": "الطّائِرةُ تَطيرُ في  ..........",
        "options": [
            {"label": "أ", "text": "الْبَحْرِ", "value": "أ"},
            {"label": "ب", "text": "الْبَرّ", "value": "ب"},
            {"label": "ج", "text": "الْجَوّ", "value": "ج"},
            {"label": "د", "text": "التّرابِ", "value": "د"},
        ],
        "correct": "ج"
    },
    {
        "text": "أَغْسِلُ أَسْناني بِ   ..........",
        "options": [
            {"label": "أ", "text": "الْقَلَمِ", "value": "أ"},
            {"label": "ب", "text": "الْفُرْشاةِ", "value": "ب"},
            {"label": "ج", "text": "الْمِلْعَقَةِ", "value": "ج"},
            {"label": "د", "text": "الْمَنْديلِ", "value": "د"},
        ],
        "correct": "ب"
    },
]


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
        #return redirect(reverse('examinerPage'))


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
    return render(request,"examinerPage.html", {
        "students": Student.objects.filter(examiner_id=request.user.id),  "stage": (Examiner.objects.get(user_id=request.user.id).stage), "examiners": (Examiner.objects.get(user_id=request.user.id))
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
    print(stage)
    if stage == 'PRIMARY':
        return redirect('testsPage')
    elif stage == 'SECONDARY':
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
            f"{name} from {organization}",
            f"Name:{name} \nOrganization:{organization} \nEmail:{email} \nMessage:\n{message}",
            "smerri@kisr.edu.kw",
            ['ccetphonologytest@gmail.com'],
            fail_silently=False
        )
        print("Name:{name} \nOrganization:{organization} \nEmail:{email} \nMessage:\n{message}")
        
    
    return render(request,"requestPage.html")

@login_required(login_url="/login")
def testsPage (request):
    test1 = PrimaryTest1.objects.filter(student_id = request.session['student'])
    global context_test1
    context_test1 = {}
    student = Student.objects.get(id=request.session['student']).studentName

    #add it in the if statement
    if (test1.exists()):
        test1_obj = PrimaryTest1.objects.filter(student_id = request.session['student'])
        if(test1_obj.exists()):
            test1_correct_Ans = PrimaryTest1.objects.filter(student_id = request.session['student']).latest("id").total_correct
            if (test1_correct_Ans != None):
                context_test1 = {"correctAnswers":(test1_correct_Ans), "status_test1":('منجز '), }
            else:
                context_test1 = {"status_test1":('غير منجز'), }
        else:
            context_test1 = {"status_test1":('غير منجز'), }

        return render(request, "primary_test/testPage.html", { "context_test1": context_test1,"student": student, "examiners": (Examiner.objects.get(user_id=request.user.id))})
    else:
        context_test1 = { "status_test1":('غير منجز'),}
        return render(request,"primary_test/testPage.html", {"context_test1": context_test1,"student":(Student.objects.get(id=request.session['student']).studentName), "examiners": (Examiner.objects.get(user_id=request.user.id)) })

@login_required(login_url="/login")
def testsPageSec (request):
    test1 = SecondaryTest1.objects.filter(student_id = request.session['student'])
    test3 = SecondaryTest3.objects.filter(student_id = request.session['student'])
    global context_test1
    context_test1 = {}
    global context_test3
    context_test3 = {}
    student = Student.objects.get(id=request.session['student']).studentName

    #add it in the if statement
    if (test1.exists() or test3.exists()):
        #test1_obj = SecondaryTest1.objects.filter(student_id = request.session['student'])
        #test3_obj = SecondaryTest3.objects.filter(student_id = request.session['student'])
        if(test1.exists()):
            test1_correct_Ans = SecondaryTest1.objects.filter(student_id = request.session['student']).latest("id").total_correct
            test1_time_seconds = SecondaryTest1.objects.filter(student_id = request.session['student']).latest("id").time_seconds
            test1_fluency_score = SecondaryTest1.objects.filter(student_id = request.session['student']).latest("id").fluency_score
            if (test1_correct_Ans != None):
                context_test1 = {"correctAnswers":(test1_correct_Ans), "status_test1":('منجز '), "time_sec": (test1_time_seconds), "fluency_score": (test1_fluency_score)}
            else:
                context_test1 = {"status_test1":('غير منجز'), }
        else:
            context_test1 = {"status_test1":('غير منجز'), }

        #return render(request, "secondary_test/testPage.html", { "context_test1": context_test1,"student": student, "examiners": (Examiner.objects.get(user_id=request.user.id))})
    #else:
        #context_test1 = { "status_test1":('غير منجز'),}

        if(test3.exists()):
            test3_correct_Ans = SecondaryTest3.objects.filter(student_id = request.session['student']).latest("id").total_correct
            #test1_time_seconds = SecondaryTest1.objects.filter(student_id = request.session['student']).latest("id").time_seconds
            #test1_fluency_score = SecondaryTest1.objects.filter(student_id = request.session['student']).latest("id").fluency_score
            if (test3_correct_Ans != None):
                context_test3 = {"correctAnswers":(test3_correct_Ans), "status_test3":('منجز ')}
            else:
                context_test3 = {"status_test3":('غير منجز'), }
        else:
            context_test3 = {"status_test3":('غير منجز'), }

        return render(request, "secondary_test/testPage.html", { "context_test1": context_test1, "context_test3": context_test3,"student": student, "examiners": (Examiner.objects.get(user_id=request.user.id))})
    
    else:
        context_test1 = { "status_test1":('غير منجز'),}
        context_test3 = { "status_test3":('غير منجز'),}
        return render(request,"secondary_test/testPage.html", {"context_test1": context_test1, "context_test3": context_test3,"student":(Student.objects.get(id=request.session['student']).studentName), "examiners": (Examiner.objects.get(user_id=request.user.id)) })

    
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
        # Get saved values from session
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

        # Clear session if you want
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
            time_seconds = float(request.POST.get('time', 1))  # avoid divide-by-zero
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
        # Get saved values from session
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

        # Clear session if you want
        #if(reason != "الوصول الى الحد السقفي"):
            #del request.session['test2_total_score']
            #del request.session['test2_time_seconds']
            #del request.session['test2_fluency']
            #del request.session['test2_scores']

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
            time_seconds = float(request.POST.get('time', 1))  # avoid divide-by-zero
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
    


@login_required(login_url="/login")
def primary_test3(request):
    return render(request,"primary_test/test3.html")

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

        #test_scores = [int(request.POST.get(f'score_{i}', 0)) for i in range(30)]
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

@login_required(login_url="/login")
def primary_test5(request):
    return render(request,"primary_test/test5.html")

@login_required(login_url="/login")
def primary_test6(request):
    return render(request,"primary_test/test6.html")

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

        if index < len(secondary_test2_training_questions):
            return render(request, "secondary_test/test2_training_question.html", {
                "question": secondary_test2_training_questions[index],
                "index": index
            })

        # End of questions
        passed = request.session.get('training_correct', 0) > 0
        if passed:
            request.session['training_passed'] = True
            return redirect('secondary_test2')
        else:
            return render(request, 'secondary_test/test2_training.html', {
                'error': 'لم يتم اجتياز التدريب. لا يمكن المتابعة.'
            })

    # --- POST: Answer Clicked OR Auto "التالي" ---
    if request.method == "POST":
        index = int(request.POST.get("index", 0))
        selected = request.POST.get("answer")

        if selected is None:
            # Auto next request (no answer, just next)
            return render(request, "secondary_test/test2_training_question.html", {
                "question": secondary_test2_training_questions[index],
                "index": index
            })

        correct = secondary_test2_training_questions[index]["correct"]

        if 'training_correct' not in request.session:
            request.session['training_correct'] = 0

        if selected == correct:
            request.session['training_correct'] += 1

        return render(request, "secondary_test/test2_training_correct_result.html", {
            "is_correct": selected == correct,
            "correct": correct,
            "index": index + 1  # 👈 next question index
        })



@login_required(login_url="/login")
def secondary_test2(request):
    return render(request,"secondary_test/test2.html")

@login_required(login_url="/login")
def secondary_test3(request):
    student = Student.objects.get(id=request.session['student'])

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
        raw_scores = []
        for i in range(39):
            val = request.POST.get(f'score_{i}', "-")
            raw_scores.append(val)

        #test_scores = [int(request.POST.get(f'score_{i}', 0)) for i in range(30)]
        total_correct = sum(1 for val in raw_scores if val == "1")

        # Save to session for modal confirmation
        request.session['test3_total_correct'] = total_correct
        request.session['test3_raw_scores'] = raw_scores

        return render(request, 'secondary_test/test3.html', {
            'test_words': secondary_test3_words,
            'result': {
                'total_correct': total_correct,
            }
        })
    return render(request,"secondary_test/test3.html", {
        'test_words': secondary_test3_words
    })
    

@login_required(login_url="/login")
def secondary_test4(request):
    return render(request,"secondary_test/test4.html")

