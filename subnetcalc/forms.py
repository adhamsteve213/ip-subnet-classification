from django import forms


class SubnetInputForm(forms.Form):
	cidr = forms.CharField(
		label="IP address/CIDR",
		max_length=64,
		widget=forms.TextInput(attrs={"placeholder": "e.g. 192.168.1.0/24"}),
	)

