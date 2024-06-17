# forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Blog, BlogPostImage

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'main_image', 'published']

class BlogPostImageForm(forms.ModelForm):
    class Meta:
        model = BlogPostImage
        fields = ['image']

BlogPostImageFormSet = inlineformset_factory(Blog, BlogPostImage, form=BlogPostImageForm, extra=3, can_delete=True)
