# Cross-Platform PDF Reader for Projection

## Features

- Open PDF files
- Zoom in and out with precission
- Rotate 90, 180, or 270 degrees
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

https://codeium.com/windsurf
https://docs.codeium.com/getstarted/overview
https://docs.codeium.com/windsurf/getting-started

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
Ctrl + z to enter a zoom value. 1.65 worked well...

To compress pdfs: https://www.adobe.com/acrobat/online/compress-pdf.html - crap though..

TODO:
Invert the pdf, black text, white background to white text and black background, ctrl+i
Change the colour of the lines, ctrl+c - toggles through a list of colours
Black, white, red, green, blue, yellow, cyan, magenta
