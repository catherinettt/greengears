from django import forms
from cars.widgets import StarRadioFieldRenderer
from cars.models import Car, Images, Comment, UserProfile

class CarForm(forms.ModelForm):
    class Meta:
        model = Car


class CarSelectForm(forms.Form):
    CarSelected = forms.IntegerField()
    #CarSelected2 = forms.IntegerField() #added for compare.html and test.html (Ivan)

class CarSelect2(forms.Form):
    CarSelected = forms.IntegerField()
    CarSelected2 = forms.IntegerField() #added for compare.html and test.html (Ivan)   

class CommentForm(forms.Form):
#    class Meta:
#        model = Comment
    comment = forms.CharField(widget=forms.Textarea, required=False)
    name = forms.CharField(widget=forms.Textarea, required=False)
#        exclude = ('CAR')

class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        exclude = ('CAR')

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file  = forms.FileField()
    
class StarRatingForm(forms.Form):
    RATING_CHOICES = ((1,1), (2,2), (3,3), (4,4), (5,5),)
    forms.CharField(widget=forms.RadioSelect(renderer=StarRadioFieldRenderer, attrs={'class':'hover-star'}, choices=RATING_CHOICES))

class ProfileForm(forms.ModelForm): 
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        try:
            self.fields['email'].initial = self.instance.user.email
            # self.fields['first_name'].initial = self.instance.user.first_name
            # self.fields['last_name'].initial = self.instance.user.last_name
        except User.DoesNotExist:
            pass
 
    email = forms.EmailField(label="Primary email",help_text='')
 
    class Meta:
      model = UserProfile 

    # Uncomment the admin/doc line below to enable admin documentation:
      exclude = ('user',)        
 
    def save(self, *args, **kwargs):
        """
        Update the primary email address on the related User object as well.
        """
        u = self.instance.user
        u.email = self.cleaned_data['email']
        u.save()
        profile = super(ProfileForm, self).save(*args,**kwargs)
        return profile

