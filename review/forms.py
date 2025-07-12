from django import forms

class ResumeReviewForm(forms.Form):
    resume = forms.FileField(
        widget=forms.ClearableFileInput(attrs={
            "class": "block w-full rounded-lg bg-purple-700 border border-purple-600 text-purple-100 focus:ring-2 focus:ring-purple-400 focus:outline-none py-3 px-4"
        })
    )
    job_description = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "block w-full rounded-lg bg-purple-700 border border-purple-600 text-purple-100 focus:ring-2 focus:ring-purple-400 focus:outline-none py-3 px-4 h-36 resize-none"
        })
    )
