# 📑 Django-based PDF Tools  

A modern, lightweight, and secure web app built with **Django + Bootstrap** to manage and convert PDFs with ease.  
All tools run locally in your browser — **no file storage on the server**, ensuring privacy and security.  

---

## ✨ Features  

- ➕ **Merge PDF** – Combine multiple PDFs into one  
- ✂️ **Split PDF** – Extract selected pages into a new document  
- 🖼️ **Images → PDF** – Convert images to a single PDF  
- 📄 **PDF → Images** – Export PDF pages as images (ZIP download)  
- 🖼️ **Extract Images** – Extract embedded images from PDFs  
- 🔒 **Lock PDF** – Secure your file with a password  
- 🔓 **Unlock PDF** – Remove password (with correct key)  
- 📄➡️📝 **PDF → DOCX** – Convert PDF into an editable Word document  

---

## 🚀 Tech Stack  

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)  
![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)  
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)  
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)  
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)  

---

## 📌 Project Overview  

This project is designed to make working with **PDFs** simple and efficient.  
Whether you want to merge, split, convert, secure, or extract content, this app provides an intuitive **all-in-one platform**.  

Key goals:  
- ✅ Privacy-first (files processed in memory, not stored)  
- ✅ Simple, clean UI  
- ✅ Extendable for future tools  

---

## ⚙️ Installation  

Clone the repo:  

```bash
git clone https://github.com/malavika-suresh/Django-based-PDF-tools.git
cd Django-based-PDF-tools
```

Create virtual environment & install dependencies:  

```bash
python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)

pip install -r requirements.txt
```

Run migrations & start server:  

```bash
python manage.py migrate
python manage.py runserver
```

Access at 👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)  

---

## 🗂 Project Structure  

```
Django-based-PDF-tools/
│── tools/                 # Core PDF tool app
│   ├── templates/tools/   # HTML templates
│   ├── forms.py           # Tool forms
│   ├── utils.py           # PDF processing utilities
│   ├── urls.py            # URL routing
│   └── views.py           # Business logic
│
│── static/                # CSS, JS, images
│── manage.py              # Django entry point
│── requirements.txt       # Python dependencies
└── README.md              # Project docs
```

---

## 🔮 Future Enhancements  

- 📌 **PDF Compression** – Reduce file size  
- 📌 **Reorder Pages** – Drag-and-drop pages in a PDF  
- 📌 **Add Watermark** – Text or image watermark  
- 📌 **Dark Mode UI** – Better user experience  
- 📌 **Docker Support** – Easy deployment  

---

## 🙌 Acknowledgements  

- [PyPDF2](https://pypi.org/project/pypdf2/) – for PDF manipulation  
- [pdf2docx](https://pypi.org/project/pdf2docx/) – for PDF → DOCX conversion  
- [Bootstrap](https://getbootstrap.com/) – UI components  
- [Django](https://www.djangoproject.com/) – backend framework  

---

## 📜 License  

MIT License © 2025 [Malavika Suresh](https://github.com/malavika-suresh)  
