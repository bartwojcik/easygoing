from datetime import datetime

from captcha.fields import CaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from stem.models import Website, Post


class UserCommentForm(forms.Form):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-4'
    helper.add_input(Submit('submit', 'Comment'))
    content = forms.CharField(widget=forms.Textarea)


class CommentForm(forms.Form):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-4'
    helper.add_input(Submit('submit', 'Comment'))
    author_name = forms.CharField(max_length=255)
    author_email = forms.EmailField(required=False)
    content = forms.CharField(widget=forms.Textarea)
    captcha = CaptchaField()


class WebsiteForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-8'
    helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Website
        fields = '__all__'


class EditPostForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-8'
    helper.add_input(Submit('submit', 'Submit'))

    class Meta:
        model = Post
        fields = ['title', 'content', 'blog_post', 'hidden', 'language']

    def save(self, *args, **kwargs):
        self.instance.edited = datetime.now()
        super().save(self, *args, **kwargs)

