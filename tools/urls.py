from django.urls import path
from . import views

app_name = "tools"

urlpatterns = [
    path("", views.index, name="index"),
    path("merge/", views.merge_pdf_view, name="merge"),
    path("split/", views.split_pdf_view, name="split"),
    path("images-to-pdf/", views.images_to_pdf_view, name="images_to_pdf"),
    path("pdf-to-images/", views.pdf_to_images_view, name="pdf_to_images"),
    path("extract-images/", views.extract_images_view, name="extract_images"),
    path("lock/", views.lock_pdf_view, name="lock"),
    path("unlock/", views.unlock_pdf_view, name="unlock"),
    path("pdf-to-docx/", views.pdf_to_docx_view, name="pdf_to_docx"),
]
