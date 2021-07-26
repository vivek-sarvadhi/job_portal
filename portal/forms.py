from django import forms
from portal.models import CompanyProfile, Job, Candidate
from users.models import CustomUser


class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfile
        fields = ('name','description','business_stream_name','establishment_date','website_url')
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'comapny name'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'description'}),
            'business_stream_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'business stream name'}),
            'establishment_date': forms.DateInput(attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            'website_url': forms.URLInput(attrs={'class':'form-control', 'placeholder':'comapny url'}),
        }


class JobForm(forms.ModelForm):


    class Meta:
        model = Job
        fields = ('companyprofile_id','title','description','salary','experience','location','category','last_date')
        widgets = {
            'companyprofile_id':forms.Select(attrs={'class':'form-control', 'placeholder':'Company'}),
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'job title'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'description'}),
            'salary': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'salary'}),
            'experience': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'experience'}),
            'location': forms.TextInput(attrs={'class':'form-control', 'placeholder':'job location'}),
            'category': forms.TextInput(attrs={'class':'form-control', 'placeholder':'job category'}),
            'last_date': forms.DateInput(attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
        }


    # def __init__(self, *args, **kwargs):
    #     print(kwargs)
    #     super(JobForm, self).__init__(*args, **kwargs)
    #     self.initial['user'] = 'vivek@gmail.com'
class ApplyForm(forms.ModelForm):

    class Meta:
        model = Candidate
        fields = ('dob','gender','mobile','resume') 
        widgets = {
            'dob': forms.DateInput(attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            'gender': forms.RadioSelect(),
            'mobile': forms.TextInput(attrs={'class':'form-control', 'placeholder':'enter mobile number'}),
            'resume': forms.FileInput(attrs={'class':'form-control'}),
        }


class ContactForm(forms.Form):
    # from_email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    subject = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=True)
    message = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}), required=True)