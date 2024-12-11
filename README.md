# Cross-Platform PDF Reader for Projection

## Features

- Open PDF files
- Zoom in and out with precission
- Rotate 90, 180, or 270 degrees, clockwise or anti-clockwise
- Invert the colours, black text, white background to white text and black background
- Cycle through the available colors: black, red, green, blue, white, yellow, cyan, magenta.
- Cross-platform compatibility

## Prerequisites

- Python 3.8+
- pip
- virtualenv (recommended)

## Setup

1. Create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python main.py
```

## Usage

- Click "Open PDF" to select a PDF file
- Use "Zoom In" and "Zoom Out" buttons to adjust view
- Scroll through the document using the scrollbars

## Dependencies

- PyQt5: GUI Framework
- PyMuPDF: PDF Rendering
- Numpy: Image Processing

Summary
App needs to be a pdf viewer for viewing cutting patterns which are projected onto fabrics. App should be cross-platform and ideally in python.

To Use
Pdf viewer, reads the pdf calibration file, set up the zoom. Then reads the pattern file, which will have the same zoom factor.

Keyboard Shortcuts
CTRL + F for full screen mode
Ctrl + + for zoom in
Ctrl + - for zoom out
Ctrl + R for rotate 90 degrees clockwise
Ctrl + Shift + R for rotate 90 degrees anti-clockwise
Ctrl + Z to enter a zoom value. 1.65 worked well...
Ctrl + I inverts the colours, black text, white background to white text and black background
Ctrl + C cycles through the available colors: black, red, green, blue, white, yellow, cyan, magenta.

To compress pdfs: https://www.adobe.com/acrobat/online/compress-pdf.html - crap though..

TODO:
