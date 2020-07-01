from django import forms
from _user_panel.translation import translate_text_ar

def is_whitespaces(string):
	string_a = string.replace('&nbsp;', '')
	string_b = 	string_a.replace('<p>' , '')
	string_c = 	string_b.replace('</p>' , '')
	string_d = string_c.replace('\r\n' , '')
	string_e = string_d.strip()
	print(string_e,'sdfggggggggggg')
	if string_e =='':
		return True
	else:
		return False

class SettingsManagementEditForm(forms.Form):
	servicedesc	= forms.CharField(required=False)
	servicedesc_ar	= forms.CharField(required=False)

	def clean(self):
		if is_whitespaces(self.cleaned_data.get('servicedesc')):
			raise forms.ValidationError('Whitespaces are not allowed in input fields')
		# servicedesc = self.cleaned_data.get('servicedesc')
		# servicedesc_ar = self.cleaned_data.get('servicedesc_ar')
		# if not servicedesc_ar or servicedesc_ar=="":
		# 	tdata=[]
		# 	tdata.append(servicedesc)
		# 	tres=translate_text_ar(tdata)
		# 	servicedesc_ar=tres[0].text
		if is_whitespaces(self.cleaned_data.get('servicedesc_ar')):
			raise forms.ValidationError('Whitespaces are not allowed in arabic input fields')

		# self.cleaned_data['servicedesc']=servicedesc
		# self.cleaned_data['servicedesc_ar']=servicedesc_ar
		return self.cleaned_data


