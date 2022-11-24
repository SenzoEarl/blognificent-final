import crispy_forms.helper
from django import forms

from blog.models import Comment


class EmailForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(required=False, widget=forms.Textarea(attrs={'cols': 20, 'rows': 10}))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'cols': 20, 'rows': 10})
        }
