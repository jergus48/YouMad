from ..models import *
def bar():
    return Slider.objects.all()[0].announcement_bar
