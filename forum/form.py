from django import forms
from .widgets import RoundedTextarea  # Import the custom widget

class CommentForm(forms.Form):
    comment_context = forms.CharField(label="Your_comment", widget=RoundedTextarea(attrs={'rows': 1, 'cols': 40}), max_length=200)

class PostForm(forms.Form):
    post_title = forms.CharField(  label="Chủ đề :", widget=RoundedTextarea(attrs={'rows': 2, 'cols': 55}), max_length=200)
    post_content = forms.CharField(label="Nội dung:", widget=RoundedTextarea(attrs={'rows': 5, 'cols': 54}), max_length=200)

class VoteForm(forms.Form):
    LIKE_DISLIKE_CHOICES = (
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    )
    vote = forms.ChoiceField(choices=LIKE_DISLIKE_CHOICES, widget=forms.RadioSelect)