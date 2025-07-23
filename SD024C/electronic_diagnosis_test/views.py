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
#from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from datetime import datetime
#from dateutil import relativedelta
#import pandas as pd
#from primary.utils import return_scores, return_scores_Sec
#import json
#from django.core.mail import send_mail
#from django.conf import settings

# Test1 data.
TRAINING_WORDS = ['رَكِبَ', 'ثَبَتَ', 'حَمَدَ']
TEST_WORDS = [
    'أُخْتي', 'تَحْتَوي', 'هذانِ', 'الرَّبيعُ', 'الوَجيزُ',
    'جَمُلَ', 'أَوصَلَ', 'بِحَرَكَاتِهِ', 'الثّالِثَةُ', 'الدُّوَلاَتَانِ',
    'الذِّئْبُ', 'الكَبِيرُ', 'أَسْطُرُ', 'عِنَبَةٌ', 'الشَّاطِئَةُ',
    'الأَطْعِمَةُ', 'اِسْتِخْرَاجٌ', 'يَهْدُوهَا', 'الثَّلاَثُ', 'وَأَوَانٍ',
    'إِضَافَاتٍ', 'هؤُلاءِ', 'الوَفْدَةُ', 'بِالأَزْوَاجِ', 'الفِقْرَةُ',
    'وَالاِشْتِبَاهِ', 'الثُّقُوبِ', 'أَضِفْتُ', 'تَخَصَّصْتُ', 'لَهُ'
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
        sex = request.POST['gender']
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

        #Method 1
        #delta = relativedelta.relativedelta(examdate, birthdate)
        #years = delta.years
        #months = delta.months
        #days = delta.days

        #Method 2
        #delta = examdate-birthdate  #total age in days = delat.days
        #years = math.floor(delta.days/365)    #calculate years
        #months = math.floor(((delta.days/365)%1)*12)  #calculate months
        #days = math.floor(((((delta.days/365)%1)*12)%1)*30)   #calculate days

        age = str(years) + "/" + str(months) +"/"+str(days)

        if Student.objects.filter(civilID=civilID).exists():
            messages.info(request, 'لقد تم تسجيل الطالب مسبقاً')
            return redirect("signupStudents")
        else:
            student = Student.objects.create(studentName=studentName, sex=sex, schoolName=schoolName, grade=grade, civilID=civilID, eduDistrict=eduDistrict , nationality=nationality, examDate=examDate, birthDate=birthDate,age=age, examiner_id=request.user.id)
            student.save()
            return redirect("examinerPage")
        
    else:
        return render (request,"signupStudents.html", {
           "stage": (Examiner.objects.get(user_id=request.user.id).stage)
    })

def examinerPage (request):
    request.session['student'] = 0
    return render(request,"examinerPage.html", {
        "students": Student.objects.filter(examiner_id=request.user.id),  "stage": (Examiner.objects.get(user_id=request.user.id).stage), "examiners": (Examiner.objects.get(user_id=request.user.id))
    })

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
        sex = request.POST['gender']
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

        user.update(studentName=studentName, sex=sex, schoolName=schoolName, grade=grade, eduDistrict=eduDistrict , nationality=nationality, birthDate=birthDate_str, examDate=examDate_str,age=age)

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
def studentProfile(request, id):
        return render(request, "studentProfile.html", {
        "students": Student.objects.filter(id=id)})


#show Admin or Examiner details
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
            "bmdashti@kisr.edu.kw",
            ['ccetphonologytest@gmail.com'],
            fail_silently=False
        )
        print("Name:{name} \nOrganization:{organization} \nEmail:{email} \nMessage:\n{message}")
        
    
    return render(request,"requestPage.html")


def testsPage (request):
    '''rpdnamingObj = RpdNamingObj_Score.objects.filter(student_id = request.session['student'])
    rpdNamingLtrs = RpdNamingLtrs_Score.objects.filter(student_id = request.session['student'])
    phonemeSyllDel = PhonemeSyllableDel.objects.filter(student_id = request.session['student'])
    nonWordRepetition = NonWordRepetition.objects.filter(student_id = request.session['student'])
    nonWordReadingAccuracy = NonWordReadingAcc.objects.filter(student_id = request.session['student'])'''
    test1 = PrimaryTest1.objects.filter(student_id = request.session['student'])
    '''global context_obj
    context_obj = {} 
    global context_ltrs
    context_ltrs = {}
    global context_phoneme
    context_phoneme = {}
    global context_nonWrdRep
    context_nonWrdRep = {} 
    global context_nonWrdReading
    context_nonWrdReading = {} '''
    global context_test1
    context_test1 = {}
    student = Student.objects.get(id=request.session['student']).studentName

    #add it in the if statement
    '''rpdnamingObj.exists() or rpdNamingLtrs.exists() or phonemeSyllDel.exists() or nonWordRepetition.exists() or nonWordReadingAccuracy.exists() or'''
    if (test1.exists()):
        '''  
        RpdNamingObj_Score_obj = RpdNamingObj_Score.objects.filter(student_id = request.session['student'])
        RpdNamingLtrs_Score_obj = RpdNamingLtrs_Score.objects.filter(student_id = request.session['student'])
        phonemeDel_Score_obj = PhonemeSyllableDel.objects.filter(student_id = request.session['student'])
        nonWordRep_Score_obj = NonWordRepetition.objects.filter(student_id = request.session['student'])
        nonWordReadingAcc_Score_obj = NonWordReadingAcc.objects.filter(student_id = request.session['student'])'''
        test1_obj = PrimaryTest1.objects.filter(student_id = request.session['student'])
        '''
        if(RpdNamingObj_Score_obj.exists()):
            rpdNOwrongA_A = RpdNamingObj_Score.objects.filter(student_id = request.session['student']).latest("id")
            rpdNOwrongA = rpdNOwrongA_A.wrongAns_A
            rpdNOwrongB = RpdNamingObj_Score.objects.filter(student_id = request.session['student']).latest("id").wrongAns_B
            if ((rpdNOwrongA != None and rpdNOwrongB != None)):

                stimeA=RpdNamingObj_Score.objects.filter(student_id=request.session['student']).latest("id").startT_A
                etimeA=RpdNamingObj_Score.objects.filter(student_id=request.session['student']).latest("id").endT_A
                stimeB=RpdNamingObj_Score.objects.filter(student_id=request.session['student']).latest("id").startT_B
                etimeB=RpdNamingObj_Score.objects.filter(student_id=request.session['student']).latest("id").endT_B
                durationA=etimeA-stimeA
                durationA=round(durationA.total_seconds())
                print(durationA)
                durationB=etimeB-stimeB
                durationB = round(durationB.total_seconds())
                scoreA=rpdNOwrongA+durationA
                scoreB=rpdNOwrongB+durationB
                total=scoreA+scoreB
                context_obj = {"rpdNOwrongA":(rpdNOwrongA),  "rpdNOwrongB":(rpdNOwrongB), "durationA":(durationA),"durationB":(durationB) , "scoreA":(scoreA) , "scoreB":(scoreB), "totalScore_obj":(round(total)), "status_obj":('منجز '),}
            elif (rpdNOwrongA != None and rpdNOwrongB == None):
                stimeA=RpdNamingObj_Score.objects.filter(student_id=request.session['student']).latest("id").startT_A
                etimeA=RpdNamingObj_Score.objects.filter(student_id=request.session['student']).latest("id").endT_A
                durationA=etimeA-stimeA
                durationA=round(durationA.total_seconds())
                scoreA=rpdNOwrongA+durationA
                total=scoreA
                
                context_obj = {"rpdNOwrongA":(rpdNOwrongA),"durationA":(durationA), "totalScore_obj":(round(total)), "scoreA":(scoreA),"status_obj":('توقف '),}
        else:
            context_obj = { "status_obj":('غير منجز'),}

        if(RpdNamingLtrs_Score_obj.exists()):
            
            rpdNLwrongA = RpdNamingLtrs_Score.objects.filter(student_id = request.session['student']).latest("id").wrongAns_A
            rpdNLwrongB = RpdNamingLtrs_Score.objects.filter(student_id = request.session['student']).latest("id").wrongAns_B
            if ((rpdNLwrongA != None and rpdNLwrongB != None)):
                
                stimeLTRA=RpdNamingLtrs_Score.objects.filter(student_id=request.session['student']).latest("id").startT_A
                etimeLTRA=RpdNamingLtrs_Score.objects.filter(student_id=request.session['student']).latest("id").endT_A
                stimeLTRB=RpdNamingLtrs_Score.objects.filter(student_id=request.session['student']).latest("id").startT_B
                etimeLTRB=RpdNamingLtrs_Score.objects.filter(student_id=request.session['student']).latest("id").endT_B
                durationTstA=etimeLTRA-stimeLTRA
                durationTstA=round(durationTstA.total_seconds())
                durationTstB=etimeLTRB-stimeLTRB
                durationTstB = round(durationTstB.total_seconds())
                scoreTstA=rpdNLwrongA+durationTstA
                scoreTstB=rpdNLwrongB+durationTstB
                totalScore=scoreTstA+scoreTstB
                context_ltrs = {"rpdNLwrongA":(rpdNLwrongA),  "rpdNLwrongB":(rpdNLwrongB),"durationTstA":(durationTstA),"durationTstB":(durationTstB) , "scoreTstA":(scoreTstA) , "scoreTstB":(scoreTstB), "totalScore_ltr":(round(totalScore)), "status_ltrs":('منجز '),  }
                
            elif (rpdNLwrongA != None and rpdNLwrongB == None):
                
                stimeLTRA=RpdNamingLtrs_Score.objects.filter(student_id=request.session['student']).latest("id").startT_A
                etimeLTRA=RpdNamingLtrs_Score.objects.filter(student_id=request.session['student']).latest("id").endT_A
                durationTstA=etimeLTRA-stimeLTRA
                durationTstA=round(durationTstA.total_seconds())
                scoreTstA=rpdNLwrongA+durationTstA
                totalScore=scoreTstA
                context_ltrs = {"rpdNLwrongA":(rpdNLwrongA),"totalScore_ltr":(round(totalScore)), "durationTstA":(durationTstA),"scoreTstA":(scoreTstA),"status_ltrs":('توقف '),}
        else:
            context_ltrs = { "status_ltrs":('غير منجز'),}

        if(phonemeDel_Score_obj.exists()):
            phonemeSyllDelAns = PhonemeSyllableDel.objects.filter(student_id = request.session['student']).latest("id").correctAns
            if (phonemeSyllDelAns != None):
                context_phoneme = {"correctAnswers":(phonemeSyllDelAns), "status_phoneme":('منجز '), }
            else:
                context_phoneme = {"status_phoneme":('غير منجز'), }
        else:
            context_phoneme = {"status_phoneme":('غير منجز'), }

        if(nonWordRep_Score_obj.exists()):
            nonWordRepCorrectAns = NonWordRepetition.objects.filter(student_id = request.session['student']).latest("id").correctAns
            if (nonWordRepCorrectAns != None):
                context_nonWrdRep = {"correctAnswers":(nonWordRepCorrectAns), "status_nonWrdRep":('منجز '), }
            else:
                context_phoneme = {"status_nonWrdRep":('غير منجز'), }
        else:
            context_nonWrdRep = {"status_nonWrdRep":('غير منجز'), }
        '''
        if(test1_obj.exists()):
            test1_correct_Ans = PrimaryTest1.objects.filter(student_id = request.session['student']).latest("id").total_correct
            if (test1_correct_Ans != None):
                context_test1 = {"correctAnswers":(test1_correct_Ans), "status_test1":('منجز '), }
            else:
                context_test1 = {"status_test1":('غير منجز'), }
        else:
            context_test1 = {"status_test1":('غير منجز'), }
        '''        
        if(nonWordReadingAcc_Score_obj.exists()):
            nonWrdReadingCorrectAns = NonWordReadingAcc.objects.filter(student_id = request.session['student']).latest("id").correctAns
            if (nonWrdReadingCorrectAns != None):
                context_nonWrdReading = {"correctAnswers":(nonWrdReadingCorrectAns), "status_nonWrdReading":('منجز '), }
            else:
                context_nonWrdReading = {"status_nonWrdReading":('غير منجز'), }
        else:
            context_nonWrdReading = {"status_nonWrdReading":('غير منجز'), }'''
        
        #"context_obj": context_obj, "context_ltrs": context_ltrs, "context_phoneme":context_phoneme,"context_nonWrdRep": context_nonWrdRep,"context_nonWrdReading":context_nonWrdReading,

        return render(request, "primary_test/testPage.html", { "context_test1": context_test1,"student": student, "examiners": (Examiner.objects.get(user_id=request.user.id))})
    else:
        '''context_obj = { "status_obj":('غير منجز'),}
        context_ltrs = { "status_ltrs":('غير منجز'),}
        context_phoneme = { "status_phoneme":('غير منجز'),}
        context_nonWrdRep= { "status_nonWrdRep":('غير منجز'),}
        context_nonWrdReading = { "status_nonWrdReading":('غير منجز'),}'''
        context_test1 = { "status_obj":('غير منجز'),}
        return render(request,"primary_test/testPage.html", {"context_test1": context_test1,"student":(Student.objects.get(id=request.session['student']).studentName), "examiners": (Examiner.objects.get(user_id=request.user.id)) })

def testsPageSec (request):
    rpdnamingObj = RpdNamingObj_Score.objects.filter(student_id = request.session['student'])
    rpdNamingLtrs = RpdNamingLtrs_Score.objects.filter(student_id = request.session['student'])
    phonemeSyllDel = PhonemeSyllableDel.objects.filter(student_id = request.session['student'])
    nonWordRepetition = NonWordRepetition.objects.filter(student_id = request.session['student'])
    nonWordReadingAccuracy = NonWordReadingAcc.objects.filter(student_id = request.session['student'])
    global context_obj
    context_obj = {} 
    global context_ltrs
    context_ltrs = {}
    global context_phoneme
    context_phoneme = {}
    global context_nonWrdRep
    context_nonWrdRep = {} 
    global context_nonWrdReading
    context_nonWrdReading = {} 
    student = Student.objects.get(id=request.session['student']).studentName

    if (rpdnamingObj.exists() or rpdNamingLtrs.exists() or phonemeSyllDel.exists() or nonWordRepetition.exists() or nonWordReadingAccuracy.exists()):
        RpdNamingObj_Score_obj = RpdNamingObj_Score.objects.filter(student_id = request.session['student'])
        RpdNamingLtrs_Score_obj = RpdNamingLtrs_Score.objects.filter(student_id = request.session['student'])
        phonemeDel_Score_obj = PhonemeSyllableDel.objects.filter(student_id = request.session['student'])
        nonWordRep_Score_obj = NonWordRepetition.objects.filter(student_id = request.session['student'])
        nonWordReadingAcc_Score_obj = NonWordReadingAcc.objects.filter(student_id = request.session['student'])

        if(RpdNamingObj_Score_obj.exists()):
            rpdNOwrongA_A = RpdNamingObj_Score.objects.filter(student_id = request.session['student']).latest("id")
            rpdNOwrongA = rpdNOwrongA_A.wrongAns_A
            rpdNOwrongB = RpdNamingObj_Score.objects.filter(student_id = request.session['student']).latest("id").wrongAns_B
            if ((rpdNOwrongA != None and rpdNOwrongB != None)):

                stimeA=RpdNamingObj_Score.objects.filter(student_id=request.session['student']).latest("id").startT_A
                etimeA=RpdNamingObj_Score.objects.filter(student_id=request.session['student']).latest("id").endT_A
                stimeB=RpdNamingObj_Score.objects.filter(student_id=request.session['student']).latest("id").startT_B
                etimeB=RpdNamingObj_Score.objects.filter(student_id=request.session['student']).latest("id").endT_B
                durationA=etimeA-stimeA
                durationA=round(durationA.total_seconds())
                print(durationA)
                durationB=etimeB-stimeB
                durationB = round(durationB.total_seconds())
                scoreA=rpdNOwrongA+durationA
                scoreB=rpdNOwrongB+durationB
                total=scoreA+scoreB
                context_obj = {"rpdNOwrongA":(rpdNOwrongA),  "rpdNOwrongB":(rpdNOwrongB), "durationA":(durationA),"durationB":(durationB) , "scoreA":(scoreA) , "scoreB":(scoreB), "totalScore_obj":(round(total)), "status_obj":('منجز '),}
            elif (rpdNOwrongA != None and rpdNOwrongB == None):
                stimeA=RpdNamingObj_Score.objects.filter(student_id=request.session['student']).latest("id").startT_A
                etimeA=RpdNamingObj_Score.objects.filter(student_id=request.session['student']).latest("id").endT_A
                durationA=etimeA-stimeA
                durationA=round(durationA.total_seconds())
                scoreA=rpdNOwrongA+durationA
                total=scoreA
                
                context_obj = {"rpdNOwrongA":(rpdNOwrongA),"durationA":(durationA), "totalScore_obj":(round(total)), "scoreA":(scoreA),"status_obj":('توقف '),}
        else:
            context_obj = { "status_obj":('غير منجز'),}

        if(RpdNamingLtrs_Score_obj.exists()):
            
            rpdNLwrongA = RpdNamingLtrs_Score.objects.filter(student_id = request.session['student']).latest("id").wrongAns_A
            rpdNLwrongB = RpdNamingLtrs_Score.objects.filter(student_id = request.session['student']).latest("id").wrongAns_B
            if ((rpdNLwrongA != None and rpdNLwrongB != None)):
                
                stimeLTRA=RpdNamingLtrs_Score.objects.filter(student_id=request.session['student']).latest("id").startT_A
                etimeLTRA=RpdNamingLtrs_Score.objects.filter(student_id=request.session['student']).latest("id").endT_A
                stimeLTRB=RpdNamingLtrs_Score.objects.filter(student_id=request.session['student']).latest("id").startT_B
                etimeLTRB=RpdNamingLtrs_Score.objects.filter(student_id=request.session['student']).latest("id").endT_B
                durationTstA=etimeLTRA-stimeLTRA
                durationTstA=round(durationTstA.total_seconds())
                durationTstB=etimeLTRB-stimeLTRB
                durationTstB = round(durationTstB.total_seconds())
                scoreTstA=rpdNLwrongA+durationTstA
                scoreTstB=rpdNLwrongB+durationTstB
                totalScore=scoreTstA+scoreTstB
                context_ltrs = {"rpdNLwrongA":(rpdNLwrongA),  "rpdNLwrongB":(rpdNLwrongB),"durationTstA":(durationTstA),"durationTstB":(durationTstB) , "scoreTstA":(scoreTstA) , "scoreTstB":(scoreTstB), "totalScore_ltr":(round(totalScore)), "status_ltrs":('منجز '),  }
                
            elif (rpdNLwrongA != None and rpdNLwrongB == None):
                
                stimeLTRA=RpdNamingLtrs_Score.objects.filter(student_id=request.session['student']).latest("id").startT_A
                etimeLTRA=RpdNamingLtrs_Score.objects.filter(student_id=request.session['student']).latest("id").endT_A
                durationTstA=etimeLTRA-stimeLTRA
                durationTstA=round(durationTstA.total_seconds())
                scoreTstA=rpdNLwrongA+durationTstA
                totalScore=scoreTstA
                context_ltrs = {"rpdNLwrongA":(rpdNLwrongA),"totalScore_ltr":(round(totalScore)), "durationTstA":(durationTstA),"scoreTstA":(scoreTstA),"status_ltrs":('توقف '),}
        else:
            context_ltrs = { "status_ltrs":('غير منجز'),}

        if(phonemeDel_Score_obj.exists()):
            phonemeSyllDelAns = PhonemeSyllableDel.objects.filter(student_id = request.session['student']).latest("id").correctAns
            if (phonemeSyllDelAns != None):
                context_phoneme = {"correctAnswers":(phonemeSyllDelAns), "status_phoneme":('منجز '), }
            else:
                context_phoneme = {"status_phoneme":('غير منجز'), }
        else:
            context_phoneme = {"status_phoneme":('غير منجز'), }

        if(nonWordRep_Score_obj.exists()):
            nonWordRepCorrectAns = NonWordRepetition.objects.filter(student_id = request.session['student']).latest("id").correctAns
            if (nonWordRepCorrectAns != None):
                context_nonWrdRep = {"correctAnswers":(nonWordRepCorrectAns), "status_nonWrdRep":('منجز '), }
            else:
                context_phoneme = {"status_nonWrdRep":('غير منجز'), }
        else:
            context_nonWrdRep = {"status_nonWrdRep":('غير منجز'), }
        
        if(nonWordReadingAcc_Score_obj.exists()):
            nonWrdReadingCorrectAns = NonWordReadingAcc.objects.filter(student_id = request.session['student']).latest("id").correctAns
            if (nonWrdReadingCorrectAns != None):
                context_nonWrdReading = {"correctAnswers":(nonWrdReadingCorrectAns), "status_nonWrdReading":('منجز '), }
            else:
                context_nonWrdReading = {"status_nonWrdReading":('غير منجز'), }
        else:
            context_nonWrdReading = {"status_nonWrdReading":('غير منجز'), }

        return render(request, "secondary_test/testsPage.html", {"context_obj": context_obj, "context_ltrs": context_ltrs, "context_phoneme":context_phoneme,"context_nonWrdRep": context_nonWrdRep,"context_nonWrdReading":context_nonWrdReading, "student": student, "examiners": (Examiner.objects.get(user_id=request.user.id))})
    else:
        context_obj = { "status_obj":('غير منجز'),}
        context_ltrs = { "status_ltrs":('غير منجز'),}
        context_phoneme = { "status_phoneme":('غير منجز'),}
        context_nonWrdRep= { "status_nonWrdRep":('غير منجز'),}
        context_nonWrdReading = { "status_nonWrdReading":('غير منجز'),}
        return render(request,"secondary_test/testPage.html", {"context_obj": context_obj, "context_ltrs": context_ltrs, "context_phoneme": context_phoneme, "context_nonWrdRep": context_nonWrdRep, "context_nonWrdReading":context_nonWrdReading,"student":(Student.objects.get(id=request.session['student']).studentName), "examiners": (Examiner.objects.get(user_id=request.user.id)) })

    
#Primary test 1
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

'''
def primary_test1(request):
    if request.method == 'POST':
        # Get training scores
        training_scores = [int(request.POST.get(f'train_{i}', 0)) for i in range(3)]
        passed_training = all(score == 1 for score in training_scores)

        if not passed_training:
            return render(request, 'primary_test/test1.html', {
                #'training_words': TRAINING_WORDS,
                'test_words': TEST_WORDS,
                'error': 'لم يتم اجتياز التدريب. لا يمكن المتابعة.'
            })

        # Get test scores
        test_scores = [int(request.POST.get(f'test_{i}', 0)) for i in range(30)]
        total_correct = sum(test_scores)

        # Get time in seconds
        try:
            time_seconds = float(request.POST.get('time', 0))
        except ValueError:
            time_seconds = 0

        if time_seconds == 0:
            fluency = 0
        else:
            fluency = (total_correct / time_seconds) * 60

        # Save to DB
        PrimaryTest1.objects.create(
            student=Student.objects.get(id=request.session['student']),
            total_correct=total_correct,
            time_seconds=time_seconds,
            fluency_score=fluency
        )


        return render(request, 'primary_test/test1.html', {
    #'training_words': TRAINING_WORDS,
    'test_words': TEST_WORDS,
    'result': {
        'total_correct': total_correct,
        'time_seconds': time_seconds,
        'fluency': round(fluency, 2)
    },
    'show_modal': True  # <-- This tells the template to open the modal
})


    return render(request, 'primary_test/test1.html', {
        #'training_words': TRAINING_WORDS,
        'test_words': TEST_WORDS,
    })'''
'''
def primary_test1(request):
    if request.method == 'POST':
        if request.POST.get("form2"):  # Final submission
            student = Student.objects.get(id=request.session['student'])
            test_scores = [int(request.POST.get(f'test_{i}', 0)) for i in range(30)]
            total_correct = sum(test_scores)

            try:
                time_seconds = float(request.POST.get('time', 0))
            except ValueError:
                time_seconds = 0

            fluency = (total_correct / time_seconds) * 60 if time_seconds else 0

            reason = request.POST.get("submitTst", "لم يتم تحديد السبب")

            PrimaryTest1.objects.create(
                student=student,
                total_correct=total_correct,
                time_seconds=time_seconds,
                fluency_score=fluency,
                reason=reason,
                date=datetime.now()
            )

            return redirect("testsPage")  # Update with your actual test page

        # Intermediate autosave logic handled in separate view
    return render(request, 'primary_test/test1.html', {
        'test_words': TEST_WORDS
    })
'''

def primary_test1(request):
    student = Student.objects.get(id=request.session['student'])

    # Modal confirmation submit
    if request.method == 'POST' and request.POST.get("form2"):
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

def primary_test2(request):
    return render(request,"primary_test/test2.html")

def primary_test3(request):
    return render(request,"primary_test/test3.html")

def primary_test4(request):
    return render(request,"primary_test/test4.html")

def primary_test5(request):
    return render(request,"primary_test/test5.html")

def primary_test6(request):
    return render(request,"primary_test/test6.html")

def secondary_test1(request):
    return render(request,"secondary_test/test1.html")

def secondary_test2(request):
    return render(request,"secondary_test/test2.html")

def secondary_test3(request):
    return render(request,"secondary_test/test3.html")

def secondary_test4(request):
    return render(request,"secondary_test/test4.html")

