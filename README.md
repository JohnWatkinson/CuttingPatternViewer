# Advanced Cross-Platform PDF Reader

## Features
- Open PDF files
- Zoom in and out
- Scroll through pages
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



Projection Viewer 2

Same as 1 but switched to Windsurf IDE and started again.

https://codeium.com/windsurf

https://docs.codeium.com/getstarted/overview
https://docs.codeium.com/windsurf/getting-started


Summary
    App needs to be a pdf viewer for viewing cutting patterns which are projected onto fabrics. App should be cross-platform and ideally in python.

    Pdf viewer, reads the pdf calibration file, set up the zoom. Then reads the pattern file, which will have the same zoom factor.


Windsurf
    Build me a pdf reader with very good zoom features. must be cross-platform. Build it in qt and python. Can you first create a virtual environment?

python3 -m venv /home/john/CascadeProjects/windsurf-project/pdf_reader_env
Failed, but suggested: sudo apt install -y python3-venv
- installed with a terminal
Dependencies
    bash -c source /home/john/CascadeProjects/windsurf-project/pdf_reader_env/bin/activate && pip install PyQt5 PyMuPDF


To run the application:

    Activate the virtual environment
    Install dependencies with pip install -r requirements.txt
    Run with python main.py


john@CAPRICA:~/CascadeProjects/windsurf-project$ source pdf_reader_env/bin/activate
(pdf_reader_env) john@CAPRICA:~/CascadeProjects/windsurf-project$ pip install -r requirements.txt

To run
    (pdf_reader_env) john@CAPRICA:~/CascadeProjects/windsurf-project/pdf_reader$ python main.py
    Open the pdf and start..
    CTRL + F for full screen mode
    Ctrl + + for zoom in
    Ctrl + - for zoom out
    Ctrl + z to enter a zoom value. 1.65 worked well...

To compress pdfs: https://www.adobe.com/acrobat/online/compress-pdf.html


Add
    Invert the pdf, black text, white background to white text and black background, ctrl+i
    Rotate anti-clockwise, ctrl+r, ctrl+l
    Change the colour of the lines, ctrl+c - toggles through a list of colours
    Black, white, red, green, blue, yellow, cyan, magenta
