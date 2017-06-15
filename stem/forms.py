from captcha.fields import CaptchaField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.forms import CharField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from stem.models import Website, Post


class UserCommentForm(forms.Form):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-4'
    helper.add_input(Submit('submit', _('Submit')))
    content = forms.CharField(widget=forms.Textarea, label='')


class CommentForm(forms.Form):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-4'
    helper.add_input(Submit('submit', _('Submit')))
    author_name = forms.CharField(max_length=255, label=_('Nick'))
    author_email = forms.EmailField(required=False, label=_('E-mail'))
    content = forms.CharField(widget=forms.Textarea, label=_('Comment text'))
    captcha = CaptchaField(label='CAPTCHA')


class WebsiteForm(forms.ModelForm):
    sidebar = CharField(strip=False, required=False, widget=forms.Textarea)
    footer = CharField(strip=False, required=False, widget=forms.Textarea)

    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-8'
    helper.add_input(Submit('submit', _('Submit')))

    class Meta:
        model = Website
        exclude = ['sidebar_processed', 'footer_processed']


class EditPostForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-8'
    helper.add_input(Submit('submit', _('Submit')))

    class Meta:
        model = Post
        fields = ['title', 'content', 'blog_post', 'hidden', 'language']

    def save(self, *args, **kwargs):
        if kwargs.get('edit', False):
            self.instance.edited = timezone.now()
        if 'edit' in kwargs:
            kwargs.pop('edit')
        return super().save(*args, **kwargs)
