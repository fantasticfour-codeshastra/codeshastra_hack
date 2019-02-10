from django.contrib.auth import login
from django.shortcuts import redirect,render
from django.views.generic import CreateView
from accounts.models import CustomUser
from django.contrib.auth.forms import  AuthenticationForm
from .forms import CollegeDataForm,UserForm,StudentDataForm
from .models import CollegeData,StudentData
from django.views import generic


def college_signup_view(request):
    user_form = {}
    profile_form ={}
    
    if request.method == 'POST':
		
        user_form = UserForm(request.POST)
        profile_form = CollegeDataForm(request.POST)
        print(user_form)
            
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.is_college = True
            user.save()

            user.college_user.college_name = profile_form.cleaned_data.get('college_name')
            user.college_user.college_location = profile_form.cleaned_data.get('college_location')
            user.college_user.save()
            return redirect('college:login')
        else:
            print(user_form.errors)
            user_form = UserForm(prefix='UF')
            profile_form = CollegeDataForm(prefix='PF')
            
    return render(request, 'college/register.html',{
                'user_form': user_form,
                'profile_form': profile_form,
            })

def add_student(request):
    user_form = {}
    profile_form ={}
    
    if request.method == 'POST':
		
        user_form = UserForm(request.POST)
        profile_form = StudentDataForm(request.POST)
        print(profile_form)
            
        if user_form.is_valid() and profile_form.is_valid():
            print("HI")
            print(request.user)
            college = request.user
            a = CustomUser.objects.get(username = college)
            print(a)
            print(a.college_user)
            user = user_form.save(commit=False)
            
            # import pdb; pdb.set_trace()
            print(user)
            user.is_student = True
            user.save() 
            print("-----")
            
            print(college)
            print("----")
            user.Student_user.college = a.college_user
            user.Student_user.student_name = profile_form.cleaned_data.get('student_name')
            user.Student_user.student_gender = profile_form.cleaned_data.get('student_gender')
            user.Student_user.student_add1 = profile_form.cleaned_data.get('student_add1')
            user.Student_user.student_add2 = profile_form.cleaned_data.get('student_add2')
            user.Student_user.student_aadhar = profile_form.cleaned_data.get('student_aadhar')
            user.Student_user.student_station = profile_form.cleaned_data.get('student_station')

            user.Student_user.save()
            return redirect('college:dashboard')
        else:
            print(profile_form.errors)
            print(user_form.errors)
            user_form = UserForm()
            profile_form = CollegeDataForm()
            
    return render(request, 'college/details.html',{
                'user_form': user_form,
                'profile_form': profile_form,
            })

def login_page(request):
    if request.method == "POST":
        form = AuthenticationForm(data = request.POST)
        print(form)
        # print(form)
        if form.is_valid():
            print("----HI----")
            user = form.get_user()
            print(user)
            login(request, user)    
            if user.is_student:
                return redirect('')
            elif user.is_college:
                return redirect('college:dashboard')
        else:
            print(form.errors)
    else:
        form = AuthenticationForm()
        return render(request, "college/index.html", {"form" : form})
    

class StudentDetailView(generic.ListView):
    model=StudentData
    template_name='college/table.html'
    context_object_name='students'
    def get_queryset(self):
        return StudentData.objects.all()

def LandingView(request):
    return render(request,'college/landing.html')   

