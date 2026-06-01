from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    '''form for editing main profile informations'''
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'example@gmail.com'
    }))

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'username'
            }),
        }
    def clean_username(self):
        '''بررسی اینکه username به جز خود کاربر تکراری نباشه.'''
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This username has already been used.")
        return username
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("این ایمیل قبلا ثبت شده است.")
        return email
    
class ProfileUpdateForm(forms.ModelForm):
    '''form for editing profile informations'''

    class Meta:
        model = Profile
        fields = ['bio', 'birth_date', 'phone', 'website', 'avatar']
        widgets = {
            'bio' : forms.Textarea(attrs={
                'class' : 'form-control',
                'rows' : 4,
                'placeholder' : 'write about yourself.'
            }),
            'birth_date' : forms.DateInput(attrs={
                'class' : 'form-control',
                'type' : 'date',

            }),
            'phone' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : '0912 123 4567',
            }),
            'website' : forms.URLInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'https://example.com'
            }),
            'avatar' : forms.FileInput(attrs={
                'class' : 'form-control',
            }),
        }

    def clean_phone(self):
        '''verify the phone'''
        phone = self.cleaned_data.get('phone')
        if phone and len(phone) < 11:
            raise forms.ValidationError('شماره تلفن باید حداقل 11 رقم باشد.')
            
        return phone
        
    def clean_website(self):
        '''verfiy the website of users'''
        website = self.cleaned_data.get('website')

        if website and not website.startswith(('https://', 'https://')):
            website = "https://" + website
            
        return website
    