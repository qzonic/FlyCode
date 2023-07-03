from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = (
            'text',
        )


class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=128
    )

    class Meta:
        fields = (
            'query',
        )
