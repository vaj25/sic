from django import forms
from contable.models import Empleado,Cuenta
from django.utils.translation import ugettext_lazy as _ 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import EmailField

class PostForm(forms.Form):
	nickname = forms.CharField(max_length=100)
	password = forms.CharField(max_length=10)
	email = forms.CharField(max_length=50) 
	
class UserCreationForm(UserCreationForm):
    email = EmailField(label=_("Email address"), required=True,
        help_text=_("Requerido."))
 
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
 
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
    
    
    
class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ("nombre","apellido","dui","nit")
        
        