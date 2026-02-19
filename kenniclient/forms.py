from django.forms import CharField
from django.forms import Form

class Kennitala(Form):
	kennitala = CharField(max_length=10)