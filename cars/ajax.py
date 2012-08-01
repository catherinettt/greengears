from dajax.core import Dajax
from dajaxice.core import dajaxice_functions
from dajaxice.decorators import dajaxice_register
from cars.models import Car, Make, Model, Year

@dajaxice_register
def getmodel(request, option):
    dajax = Dajax()

    out = ""

    if int(option) != 0:
        make = Make.objects.get(id = option)
        model_list = make.model_set.all()
        
        for model in model_list:
            out = '%s<option value="%s">%s</option>' % (out, model.id, model.MODEL_NAME)
            
    dajax.assign('#models','innerHTML',out)
   
    return dajax.json()

