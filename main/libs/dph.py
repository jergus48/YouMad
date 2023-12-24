from ..models import *

def calculate(variable):
    if AdminInformations.objects.all()[0].DPH == True:
            variable+=(AdminInformations.objects.all()[0].dph_size*variable)/(100-AdminInformations.objects.all()[0].dph_size )
    return variable

def calculate_dph_only(variable):
    if AdminInformations.objects.all()[0].DPH == True:
        dph=(AdminInformations.objects.all()[0].dph_size*variable)/(100-AdminInformations.objects.all()[0].dph_size )
    else:
         dph=0
    return dph