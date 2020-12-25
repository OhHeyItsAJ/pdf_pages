# pdf_pages
Python script to perform various operations on PDF files in order to avoid in herent security risks in transferring transferring documents to third party applications.
## Features
### Current
- Merge individually named PDFs into one file.
- Merge an entire directory of PDFs into one file alphabetically.
### Upcoming
- Split a single PDF file into multiple based on page number.
- Extract a concurrent range of pages from a PDF file.
## Install Prerequisites
`pip3 install -r requirements.txt`
## Usage
positional arguments:
  input             The file(s) to have operations performed on.
  output            Path for desired output file(s).

optional arguments:
  -h, --help        show this help message and exit
  -i, --individual  Specify which files to merge in a sorted, comma seperated
                    list.
  -d, --directory   Merge all PDFs in a single directory sorted
                    alphabetically.