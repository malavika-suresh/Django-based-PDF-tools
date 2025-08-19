from django import forms

# Enable multi-select for file inputs
class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MergePDFForm(forms.Form):
    files = forms.FileField(
        widget=MultiFileInput(attrs={"accept": ".pdf"}),
        help_text="Select two or more PDF files to merge."
    )


class SplitPDFForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={"accept": ".pdf"}))
    ranges = forms.CharField(help_text="e.g., 1-3,5,7-9 (1-based page numbers)")


class ImagesToPDFForm(forms.Form):
    images = forms.FileField(widget=MultiFileInput(attrs={"accept": "image/*"}))


class PDFToImagesForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={"accept": ".pdf"}))


class ExtractImagesForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={"accept": ".pdf"}))


class LockPDFForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={"accept": ".pdf"}))
    password = forms.CharField(widget=forms.PasswordInput)


class UnlockPDFForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={"accept": ".pdf"}))
    password = forms.CharField(widget=forms.PasswordInput)


# 🆕 PDF → DOCX Conversion (full PDF, always with images + tables)
class PdfToDocxForm(forms.Form):
    pdf_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={"accept": ".pdf"}),
        help_text="Upload a PDF file to convert into DOCX."
    )
