from django import forms

class CommentForm(forms.Form):
    comment_context = forms.CharField(label="Your_comment", widget=forms.Textarea(attrs={'rows': 1, 'cols': 40}), max_length=200)

class PostForm(forms.Form):
    post_title = forms.CharField(label="Title:__", widget=forms.Textarea(attrs={'rows': 1, 'cols': 40}), max_length=200)
    post_content = forms.CharField(label="Context:", widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}))