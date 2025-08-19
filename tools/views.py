from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseBadRequest
import os
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from pdf2docx import Converter

from .forms import (
    MergePDFForm, SplitPDFForm, ImagesToPDFForm, PDFToImagesForm,
    ExtractImagesForm, LockPDFForm, UnlockPDFForm
)
from .utils import (
    merge_pdfs, split_pdf_pages, images_to_pdf_bytes, pdf_to_images_zip,
    extract_images_zip, lock_pdf_with_password, unlock_pdf_with_password,
    http_attachment
)

def index(request):
    return render(request, "tools/index.html")

@require_http_methods(["GET", "POST"])
def merge_pdf_view(request):
    if request.method == "POST":
        form = MergePDFForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist("files")
            if len(files) < 2:
                return HttpResponseBadRequest("Upload at least two PDFs.")
            data = merge_pdfs(files)
            return http_attachment("merged.pdf", data, "application/pdf")
    else:
        form = MergePDFForm()
    return render(request, "tools/merge.html", {"form": form})

@require_http_methods(["GET", "POST"])
def split_pdf_view(request):
    if request.method == "POST":
        form = SplitPDFForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.cleaned_data["file"]
            ranges = form.cleaned_data["ranges"]
            try:
                data = split_pdf_pages(f, ranges)
            except Exception as e:
                return HttpResponseBadRequest(str(e))
            return http_attachment("split.pdf", data, "application/pdf")
    else:
        form = SplitPDFForm()
    return render(request, "tools/split.html", {"form": form})

@require_http_methods(["GET", "POST"])
def images_to_pdf_view(request):
    if request.method == "POST":
        form = ImagesToPDFForm(request.POST, request.FILES)
        if form.is_valid():
            images = request.FILES.getlist("images")
            try:
                data = images_to_pdf_bytes(images)
            except Exception as e:
                return HttpResponseBadRequest(str(e))
            return http_attachment("images.pdf", data, "application/pdf")
    else:
        form = ImagesToPDFForm()
    return render(request, "tools/images_to_pdf.html", {"form": form})

@require_http_methods(["GET", "POST"])
def pdf_to_images_view(request):
    if request.method == "POST":
        form = PDFToImagesForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.cleaned_data["file"]
            try:
                data, count = pdf_to_images_zip(f)
            except Exception as e:
                return HttpResponseBadRequest(str(e))
            return http_attachment("pages.zip", data, "application/zip")
    else:
        form = PDFToImagesForm()
    return render(request, "tools/pdf_to_images.html", {"form": form})

@require_http_methods(["GET", "POST"])
def extract_images_view(request):
    if request.method == "POST":
        form = ExtractImagesForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.cleaned_data["file"]
            try:
                zip_bytes, saved, skipped = extract_images_zip(f, dedupe=True)
            except Exception as e:
                return HttpResponseBadRequest(str(e))

            resp = http_attachment("extracted_images.zip", zip_bytes, "application/zip")
            # Optional: add helpful headers
            resp["X-Images-Saved"] = str(saved)
            resp["X-Images-Skipped-Duplicates"] = str(skipped)
            return resp
    else:
        form = ExtractImagesForm()

    return render(request, "tools/extract_images.html", {"form": form})

@require_http_methods(["GET", "POST"])
def lock_pdf_view(request):
    if request.method == "POST":
        form = LockPDFForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.cleaned_data["file"]
            pwd = form.cleaned_data["password"]
            try:
                data = lock_pdf_with_password(f, pwd)
            except Exception as e:
                return HttpResponseBadRequest(str(e))
            return http_attachment("locked.pdf", data, "application/pdf")
    else:
        form = LockPDFForm()
    return render(request, "tools/lock_pdf.html", {"form": form})

@require_http_methods(["GET", "POST"])
def unlock_pdf_view(request):
    if request.method == "POST":
        form = UnlockPDFForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.cleaned_data["file"]
            pwd = form.cleaned_data["password"]
            try:
                data = unlock_pdf_with_password(f, pwd)
            except Exception as e:
                return HttpResponseBadRequest(str(e))
            return http_attachment("unlocked.pdf", data, "application/pdf")
    else:
        form = UnlockPDFForm()
    return render(request, "tools/unlock_pdf.html", {"form": form})




def pdf_to_docx_view(request):
    if request.method == "POST" and request.FILES["pdf_file"]:
        pdf_file = request.FILES["pdf_file"]
        fs = FileSystemStorage()
        pdf_path = fs.save(pdf_file.name, pdf_file)
        pdf_path = fs.path(pdf_path)

        # Get user options
        start_page = int(request.POST.get("start_page", 0))
        end_page = request.POST.get("end_page")
        end_page = int(end_page) if end_page else None
        extract_images = "extract_images" in request.POST
        detect_tables = "detect_tables" in request.POST

        # Output filename
        docx_filename = os.path.splitext(pdf_file.name)[0] + ".docx"
        docx_path = fs.path(docx_filename)

        # Convert
        cv = Converter(pdf_path)
        cv.convert(docx_path, start=start_page, end=end_page,
                   image=extract_images, tables=detect_tables)
        cv.close()

        # Return file as response
        with open(docx_path, "rb") as f:
            response = HttpResponse(f.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            response["Content-Disposition"] = f'attachment; filename="{docx_filename}"'
            return response

    return render(request, "tools/pdf_to_docx.html")
