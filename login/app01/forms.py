import re

from app01 import models
from django.core.exceptions import ValidationError
from django import forms

def mobile_validate(value):
    mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号码格式错误')


class User(forms.Form):
    username = forms.CharField(
        min_length=2,
        max_length=32,
        widget=forms.TextInput(attrs={'class':'username','placeholder':'您的用户名','autocomplete':"off"}),
        error_messages={
            'required':'用户名不能为空！',
            'min_length':'用户名至少2个字符',
        }
    )
    password = forms.CharField(
        min_length=6,
        widget=forms.PasswordInput(attrs={'class':'password','placeholder':'密码','oncontextmenu':'return false','onpaste':'return false'}),
        error_messages={
            'required':'密码不能为空！',
            'min_length':'密码至少6个字符!'
        }
    )
    r_password = forms.CharField(
        min_length=6,
        widget=forms.PasswordInput(attrs={'class':'password','placeholder':'再次输入密码','ontextmenu':'return false','onpaste':'return false'}),
        error_messages={
            'min_length':'最短不能小于6位字符',
            'required':'确认密码不能为空！'
        }
    )
    telephone = forms.CharField(
        label='电话号：',
        max_length=11,
        min_length=11,
        widget=forms.NumberInput(attrs={'class':'telephone','placeholder':'请输入电话号'}),
        error_messages={
            'required':'手机好不能为空！',
            'min_length':'手机长度不够！'
        }
    )
    email = forms.EmailField(
        label='邮箱：',
        widget=forms.EmailInput(attrs={'class':'email','placeholder':'请输入邮箱'}),
        error_messages={
            'required':'邮箱不能为空！'
        }

    )
    def clean_username(self):
        value = self.cleaned_data.get('username')
        ret = models.User.objects.filter(username=value)
        if ret:
            raise ValidationError('用户名已存在！')
        else:
            return value

    def clean_email(self):
        email = self.cleaned_data.get('email')
        reg = re.compile(r'\w+@163.com$')
        if reg.match(email):
            return email
        else:
            raise ValidationError('必须是163邮箱！')

    def clean(self):
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('r_password')

        if p1 == p2:
            return self.cleaned_data
        else:
            self.add_error('r_password','两次密码不一致！')

class Cusromer(forms.ModelForm):

    class Meta:
        model = models.Customer
        fields = '__all__'
        exclude = ['delete_status',]
        widgets = {
            'birthday':forms.DateField.widget(attrs={'type':'date'}),
            'phone':forms.DateField.widget(attrs={'type':'number'})
        }

    def __init__(self,*args,**kwargs):

        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            if name == 'course':
                continue

            field.widget.attrs.update({'class':'form-control'})

class ConsultRecord(forms.ModelForm):

    class Meta:
        model = models.ConsultRecord
        fields = '__all__'
        exclude = ['delete_status',]
        widgets = {
            'date':forms.DateField.widget(attrs={'type':'date'}),
        }

    def __init__(self,request,*args,**kwargs):

        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            if name == 'customer':
                field.queryset = models.Customer.objects.filter(consultant__username=request.session.get('username'))
            elif name == 'consultant':
                l1 = models.User.objects.filter(username=request.session.get('username'))
                field.choices=[(i.id,i.username) for i in l1]
            field.widget.attrs.update({'class':'form-control'})


class StudyRecord(forms.ModelForm):

    class Meta:
        model = models.StudyRecord
        fields = '__all__'

