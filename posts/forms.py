from django import forms

from posts.models import Comment, Post


class NewPostForm(forms.Form):
    text = forms.CharField(
        max_length=1000, widget=forms.Textarea, required=False)
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))

    for field in [text]:
        field.widget.attrs.update({'class': 'form-control px-2'})

    for field in [text]:
        field.widget.attrs.update({"placeholder": "Reply to comment..."})


class UserCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']


class UserCommentReplyForm(forms.Form):
    text = forms.CharField(
        max_length=300, widget=forms.Textarea, required=False, label='Comment...',)

    for field in [text]:
        field.widget.attrs.update({'class': 'border'})

    for field in [text]:
        field.widget.attrs.update({'placeholder': "Your coment..."})


class DeleteCommentForm(forms.Form):
    pass
