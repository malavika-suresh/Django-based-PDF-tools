from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
from typing import List, Tuple
import hashlib
import fitz  # PyMuPDF
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
import fitz  # PyMuPDF
from pdf2docx import Converter

def convert_pdf_to_docx(pdf_path, docx_output, start=0, end=None, extract_images=True, detect_tables=True):
    cv = Converter(pdf_path)
    cv.convert(docx_output, 
               start=start, 
               end=end, 
               image=extract_images, 
               tables=detect_tables)
    cv.close()
    return docx_output


def http_attachment(filename: str, content: bytes, content_type: str):
    from django.http import HttpResponse
    resp = HttpResponse(content, content_type=content_type)
    resp["Content-Disposition"] = f'attachment; filename="{filename}"'
    return resp

# --- PDF merge ---
def merge_pdfs(files) -> bytes:
    writer = PdfWriter()
    for f in files:
        reader = PdfReader(f)
        for page in reader.pages:
            writer.add_page(page)
    out = BytesIO()
    writer.write(out)
    return out.getvalue()

# --- Split PDF by ranges ---
def parse_ranges(ranges: str, total_pages: int) -> List[int]:
    pages = set()
    for part in ranges.split(','):
        part = part.strip()
        if not part:
            continue
        if '-' in part:
            a, b = part.split('-', 1)
            start = max(1, int(a))
            end = min(total_pages, int(b))
            pages.update(range(start, end + 1))
        else:
            idx = int(part)
            if 1 <= idx <= total_pages:
                pages.add(idx)
    return sorted(pages)

def split_pdf_pages(file, ranges: str) -> bytes:
    reader = PdfReader(file)
    total = len(reader.pages)
    selected = parse_ranges(ranges, total)
    writer = PdfWriter()
    for p in selected:
        writer.add_page(reader.pages[p - 1])  # convert 1-based to 0-based
    out = BytesIO()
    writer.write(out)
    return out.getvalue()

# --- Images -> PDF ---
def images_to_pdf_bytes(image_files) -> bytes:
    images: List[Image.Image] = []
    for f in image_files:
        img = Image.open(f)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        else:
            img = img.copy()
        images.append(img)
    if not images:
        raise ValueError("No images provided")
    out = BytesIO()
    first, rest = images[0], images[1:]
    first.save(out, format="PDF", save_all=True, append_images=rest)
    return out.getvalue()

# --- PDF -> page images (PNG), zipped ---
def pdf_to_images_zip(file) -> Tuple[bytes, int]:
    doc = fitz.open(stream=file.read(), filetype="pdf")
    mem = BytesIO()
    with ZipFile(mem, "w", ZIP_DEFLATED) as zf:
        for i, page in enumerate(doc, start=1):
            pix = page.get_pixmap(dpi=200)
            img_bytes = pix.tobytes("png")
            zf.writestr(f"page_{i:03d}.png", img_bytes)
    return mem.getvalue(), doc.page_count

# --- Extract embedded images, zipped ---
def extract_images_zip(file, *, dedupe: bool = True) -> Tuple[bytes, int, int]:
    """
    Extract embedded images from a PDF into a ZIP.
    Returns (zip_bytes, saved_count, skipped_duplicates).
    When dedupe=True, identical images (by SHA-256 hash) are only saved once.
    """
    # PyMuPDF needs a bytes stream; read once
    pdf_bytes = file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    mem = BytesIO()
    saved = 0
    skipped = 0
    seen_hashes = set()

    with ZipFile(mem, "w", ZIP_DEFLATED) as zf:
        for pno in range(doc.page_count):
            page = doc[pno]
            for img in page.get_images(full=True):
                xref = img[0]
                base = doc.extract_image(xref)
                data = base["image"]
                ext = base.get("ext", "png")

                if dedupe:
                    h = hashlib.sha256(data).hexdigest()
                    if h in seen_hashes:
                        skipped += 1
                        continue
                    seen_hashes.add(h)

                saved += 1
                # Name by global running index to avoid gaps when duplicates are skipped
                zf.writestr(f"page_{pno+1:03d}_img_{saved:03d}.{ext}", data)

    return mem.getvalue(), saved, skipped


# --- Lock / Unlock ---
def lock_pdf_with_password(file, password: str) -> bytes:
    reader = PdfReader(file)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.encrypt(password)
    out = BytesIO()
    writer.write(out)
    return out.getvalue()

def unlock_pdf_with_password(file, password: str) -> bytes:
    reader = PdfReader(file)
    if reader.is_encrypted:
        if not reader.decrypt(password):
            raise ValueError("Wrong password or cannot decrypt.")
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    out = BytesIO()
    writer.write(out)
    return out.getvalue()
