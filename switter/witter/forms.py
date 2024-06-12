from django.contrib.auth.forms import UserCreationForm, UserChangeForm,SetPasswordForm
from django.contrib.auth.forms import User
from django import forms
from .models import Swit, Profile


class SwitForm(forms.ModelForm):
    body = forms.CharField(required=True, widget=forms.widgets.Textarea(
        attrs={
        "placeholder": "What's In Your Mind?",
        "class": "form-control",
    }
    ),
    label="",
    )

    class Meta:
        model = Swit
        exclude = ["user", "likes"]

class SignUpForm(UserCreationForm):
	# Can be left blank here because the admin section does not require them
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name',
			'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before for verification.</small></span>'


class UpdateUserForm(UserChangeForm):
		password = None
		email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
		first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
		last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

		class Meta:
			model = User
			fields = ('username', 'first_name', 'last_name', 'email')

		def __init__(self, *args, **kwargs):
			super(UpdateUserForm, self).__init__(*args, **kwargs)

			self.fields['username'].widget.attrs['class'] = 'form-control'
			self.fields['username'].widget.attrs['placeholder'] = 'User Name'
			self.fields['username'].label = ''
			self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

class ChangePasswordForm(SetPasswordForm):
	class Meta:
		model = User
		fields = ['new_password1', 'new_password2']

	def __init__(self, *args, **kwargs):
		super(ChangePasswordForm, self).__init__(*args, **kwargs)

		self.fields['new_password1'].widget.attrs['class'] = 'form-control'
		self.fields['new_password1'].widget.attrs['placeholder'] = 'Enter New Password'
		self.fields['new_password1'].label = ''
		self.fields['new_password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['new_password2'].widget.attrs['class'] = 'form-control'
		self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm New Password'
		self.fields['new_password2'].label = ''
		self.fields['new_password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password.</small></span>'

class ProfileForm(forms.ModelForm):
	profile_img = forms.ImageField(label= "Profile Picture")
	profile_bio = forms.CharField(label="Bio", max_length=500, widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Profile Bio'}))
	homepage = forms.CharField(label="Website", max_length=500, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Website Link'}))
	facebook = forms.CharField(label="Facebook", max_length=500, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Facebook Link'}))
	instagram = forms.CharField(label="Instagram", max_length=500, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Instagram Link'}))
	linkedin = forms.CharField(label="LinkedIn", max_length=500, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'LinkedIn Link'}))

	class Meta:
		model = Profile
		fields = ('profile_img', 'profile_bio', 'homepage', 'facebook', 'instagram', 'linkedin')
