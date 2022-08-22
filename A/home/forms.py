from django import forms
from .models import Post, Comment


class PostCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets ={
            'body': forms.TextInput(attrs={'claas': 'form-control'})
        }


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets ={
            'body': forms.TextInput(attrs={'claas': 'form-control'})
        }


class PostSearchForm(forms.Form):
    search = forms.CharField()

