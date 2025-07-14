from django import forms

class PDFUploadForm(forms.Form):
    pdf_file = forms.FileField(label="Upload PDF")
    page_number = forms.IntegerField(min_value=1, label="Page Number")
