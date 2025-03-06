# PDFViewer

**A simple and efficient PDF viewer built with CustomTkinter and PyMuPDF.**

## Features
- 📄 Open and view PDF files
- 📜 Scroll through pages
- 🔄 Resize dynamically to fit window dimensions
- ⏭ Navigate using next/previous buttons
- 🔢 Jump to a specific page using input

## Installation
```sh
git clone https://github.com/YOUR_GITHUB_USERNAME/PDFViewer.git
```
Then, manually move the cloned folder to your script directory.

### Dependencies
Make sure you have the required libraries installed:
```sh
pip install customtkinter pymupdf pillow
```

## Usage
```python
import customtkinter as ctk
from PDFViewer import PDFViewer

root = ctk.CTk()
pdf_path = "your_pdf_file.pdf"  # Replace with your PDF file path
viewer = PDFViewer(root, pdf_path)
root.mainloop()
```

## How It Works
- 📂 **Load PDFs**: The application opens the file using **PyMuPDF (fitz)**.
- 🖼 **Render Pages**: Converts each page to an image for smooth display.
- 🔍 **Navigation**: Use the **Next/Previous** buttons to move between pages.
- ✨ **Jump to Page**: Enter a number to go directly to a specific page.

## Controls
| Button | Action |
|--------|--------|
| ◀ | Go to the previous page |
| ▶ | Go to the next page |
| Go | Jump to the entered page number |

## Contributions
Feel free to contribute by improving features or fixing bugs. Pull requests are welcome! 🚀

---
### Contributions by [MustafaHilmiYAVUZHAN](https://github.com/MustafaHilmiYAVUZHAN)

