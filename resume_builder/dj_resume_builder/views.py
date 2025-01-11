from django.shortcuts import render,redirect,get_object_or_404
from .forms import ResumeForm,UserForm,MyUserCreationForm
from .models import Resume,User
from django.http import HttpResponse
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        
            else:
                messages.error(request, 'Username OR password does not exist')
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')

    context = {'page': page}
    return render(request, 'resume/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerUser(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'resume/login_register.html', {'form': form})


def user_profile(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')  

    user = get_object_or_404(User, id=pk)
    
    # Ensure only logged-in user is viewing their own profile
    if request.user != user:
        messages.error(request, 'You are not authorized to view this profile.')
        return redirect('home')
        
    # Filter resumes by the logged-in user
    resume_data = Resume.objects.filter(user=request.user)
    return render(request, 'resume/profile.html', {'user': user, 'resume_data': resume_data})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile',user.id)

    return render(request, 'resume/update_user.html', {'form': form,'user':user})



def home(request):
    # Ensure only logged-in user is viewing their own resume
    if not request.user.is_authenticated:
        return redirect('login')  
    
    # Retrieve resumes for the logged-in user
    resume_data = Resume.objects.filter(user=request.user)

    if not resume_data.exists():
        return redirect('info')
    
    return render(request, 'resume/home.html', {'resume_data': resume_data})


@login_required(login_url='login')
def info(request):
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
        # Create a Resume instance and save it to the database
          resume = form.save(commit=False)
          # Associate the resume with the logged-in user
          resume.user = request.user
          resume.save() 
        print(resume) 
        return redirect('resume_detail', pk=resume.id)
        # return render(request,'resume/resume_detail.html',{'resume':resume})
    else:
         form = ResumeForm()
        
    return render(request,'resume/info.html',{'form': form})

def resume_detail(request,pk):
    # Ensure only logged-in user is viewing their own resume_detail
    resume = get_object_or_404(Resume, id=pk,user=request.user)

    if resume.user != request.user:
        messages.error(request, 'You are not authorized to view this resume.')
        return redirect('home')
    
    return render(request, 'resume/resume_detail.html', {'resume': resume})

def editResume(request,pk):
    edited = get_object_or_404(Resume, id=pk)

    if request.method == "POST":
        form = ResumeForm(request.POST, request.FILES, instance=edited)
        if form.is_valid():
            form.save()
            return redirect('resume_detail', pk=edited.id)
    else:
        form = ResumeForm(instance=edited)
    
    return render(request, 'resume/edit_resume.html', {'form': form})


def generatePdf(request,pk):
    resume = get_object_or_404(Resume,id=pk)
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(f"Name: {resume.name}", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Email: {resume.email}", styles['Normal']))
    
    # Create a table with resume data
    data = [
        ['Mobile No:', resume.mobile_no],
        ['Address:', resume.address],
        ['Summary Title:', resume.summary_title],
        ['Qualifications:', resume.summary_of_qualifications],
        ['Skills Title:', resume.skills_title],
        ['Skills:', resume.skills],
        ['Experience Title:', resume.experiences_title],
        ['Experiences:', resume.experiences],
        ['Education Title:', resume.education_title],
        ['Education:', resume.education],

    ]
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(table)
    
    doc.build(elements)
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')

