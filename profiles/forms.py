from django import forms


class NewPostForm(forms.Form):
    text = forms.CharField(
        max_length=400, widget=forms.Textarea, required=False)
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))

    for field in [text]:
        field.widget.attrs.update({'class': 'form-control px-2'})

    for field in [text]:
        field.widget.attrs.update({"placeholder": "What's on your mind?"})
