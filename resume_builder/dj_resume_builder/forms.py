from django import forms
from .models import Resume,User
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email']


class ResumeForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',  # Add your custom classes or attributes here
            'accept': 'image/*',      # Optional: restrict file types to images only
        })
    )
     
    name = forms.CharField( 
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your name'}),
        label='Your Name'
    )
    
    email = forms.EmailField( 
        required=True,
        label='Email Address',
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
        help_text='Please enter a valid email address.'
    )
    
    mobile_no = forms.CharField(
        max_length=15,
        required=True,
        label='Mobile Number',
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your mobile number',
            'pattern': '[0-9]*',  # Optional: restrict input to numbers on mobile devices
            'title': 'Please enter a valid mobile number'
        }),
        help_text="Format: +1234567890 or 0123456789"
    )

    address = forms.CharField(
    max_length=400,
    required=True,
    widget=forms.Textarea(attrs={
        'placeholder': 'Enter your address',
        'rows': 3,  # Adjusts the height of the textarea
    }),
    label='Your Address',
    help_text='Please include street name, city, and postal code.'
    )

    summary_title = forms.CharField(
        max_length=100,
        required=True,
        label='Summary Title',
        widget=forms.TextInput(attrs={'placeholder': 'Enter title for your summary'})
    )

    summary_of_qualifications = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter a brief summary of your qualifications',
            'rows': 3,  # Adjust height
        }),
        label='Summary of Qualifications',
        help_text='Highlight your main qualifications and strengths.'
    )

    skills_title = forms.CharField(
        max_length=100,
        required=True,
        label='Skills Title',
        widget=forms.TextInput(attrs={'placeholder': 'Enter title for your skills'})
    )

    skills_sub_topic = forms.CharField(
        max_length=100,
        required=True,
        label='Skills Sub-Topic',
        widget=forms.TextInput(attrs={'placeholder': 'Enter subtopic for your skills'})
    )


    skills = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': 'List your skills',
            'rows': 3,
        }),
        label='Skills',
        help_text='Mention technical and soft skills.'
    )

    experiences_title = forms.CharField(
        max_length=100,
        required=True,
        label='Experience Title',
        widget=forms.TextInput(attrs={'placeholder': 'Enter title for your experiences'})
    )

    experiences_sub_topic = forms.CharField(
        max_length=100,
        required=True,
        label='Experience Sub-Topic',
        widget=forms.TextInput(attrs={'placeholder': 'Enter subtopic for your experiences'})
    )

    experiences = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': 'List your work experiences',
            'rows': 5,
        }),
        label='Work Experiences',
        help_text='Include job titles, companies, and dates.'
    )

    education_title = forms.CharField(
        max_length=100,
        required=True,
        label='Education Title',
        widget=forms.TextInput(attrs={'placeholder': 'Enter title for your education'})
    )
    
    education_sub_topic = forms.CharField(
        max_length=100,
        required=True,
        label='Education Sub-Topic',
        widget=forms.TextInput(attrs={'placeholder': 'Enter subtopic for your education'})
    )
    
    education = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter your educational background',
            'rows': 3,
        }),
        label='Education',
        help_text='Include degrees, institutions, and years.'
    )

    class Meta:
        model = Resume  # Specify the model to use
        fields = [
            'image',
            'name',
            'email',
            'mobile_no',
            'address',
            'summary_title',
            'summary_of_qualifications',
            'skills_title',
            'skills_sub_topic',
            'skills',
            'experiences_title',
            'experiences_sub_topic',
            'experiences',
            'education_title',
            'education_sub_topic',
            'education'
        ]