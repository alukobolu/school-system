from django import forms
from django.contrib.auth.models import User
from .models import Staff,Subject

class StaffForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), empty_label="None", required=False)

    class Meta:
        model = Staff
        fields = ['username', 'password', 'staff_type', 'subject',
                  'current_status','surname','firstname',
                  'other_name','gender','date_of_birth','date_of_admission',
                  'mobile_number','address','others'
            ]

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )
        staff = Staff.objects.create(
            user=user,
            staff_type=self.cleaned_data['staff_type'],
            subject=self.cleaned_data['subject'],
            current_status=self.cleaned_data['current_status'],
            surname=self.cleaned_data['surname'],
            firstname=self.cleaned_data['firstname'],
            other_name=self.cleaned_data['other_name'],
            gender=self.cleaned_data['gender'],
            date_of_birth=self.cleaned_data['date_of_birth'],
            date_of_admission=self.cleaned_data['date_of_admission'],
            mobile_number=self.cleaned_data['mobile_number'],
            address=self.cleaned_data['address'],
            others=self.cleaned_data['others'],
        )
        return staff
