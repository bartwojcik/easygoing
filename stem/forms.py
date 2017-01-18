from captcha.fields import CaptchaField
from django import forms


class UserCommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)


class CommentForm(forms.Form):
    author_name = forms.CharField(max_length=255)
    author_email = forms.EmailField(required=False)
    content = forms.CharField(widget=forms.Textarea)
    captcha = CaptchaField()
