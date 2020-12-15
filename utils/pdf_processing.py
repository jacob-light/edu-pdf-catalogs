#!/usr/bin/env python3
import os
import io
from collections import defaultdict

from PyPDF2 import PdfFileReader

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.layout import LAParams, LTTextBox, LTChar, LTFigure
from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfdocument import PDFDocument


def pypdf2txt(path, pages=None):
    txt = ""
    pdf = PdfFileReader(str(path))
    for page in pdf.pages:
        txt += page.extractText()
        if pages != None:
            pages -= 1
        if pages == 0:
            break
    return txt


def pdfminer_to_text(path, pages=None):
    with open(path, "rb") as fp:
        rsrcmgr = PDFResourceManager()
        outfp = io.StringIO()
        laparams = LAParams()
        device = TextConverter(rsrcmgr, outfp, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(fp):
            interpreter.process_page(page)
            if pages != None:
                pages -= 1
                if pages == 0:
                    break
    text = outfp.getvalue()
    return text


class PdfMinerWrapper(object):
    """
    Usage:
    with PdfMinerWrapper('2009t.pdf') as doc:
        for page in doc:
           #do something with the page
    """

    def __init__(self, pdf_doc, pdf_pwd=""):
        self.pdf_doc = pdf_doc
        self.pdf_pwd = pdf_pwd

    def __enter__(self):
        # open the pdf file
        self.fp = open(self.pdf_doc, "rb")
        # create a parser object associated with the file object
        parser = PDFParser(self.fp)
        # create a PDFDocument object that stores the document structure
        doc = PDFDocument(parser)
        # connect the parser and document objects
        parser.set_document(doc)
        self.doc = doc
        return self

    def _parse_pages(self):
        rsrcmgr = PDFResourceManager()
        laparams = LAParams(char_margin=3.5, all_texts=True)
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        for page in PDFPage.create_pages(self.doc):
            interpreter.process_page(page)
            # receive the LTPage object for this page
            layout = device.get_result()
            # layout is an LTPage object which may contain child objects like LTTextBox, LTFigure, LTImage, etc.
            yield layout

    def __iter__(self):
        return iter(self._parse_pages())

    def __exit__(self, _type, value, traceback):
        self.fp.close()


def get_text_object_details(page):
    data = {
        "page": page.pageid,
        "tboxes": [],
    }
    for tbox in page:
        if not isinstance(tbox, LTTextBox):
            continue
        data["tboxes"].append(
            {
                "text": tbox.get_text(),
                "font_size": list(
                    set(
                        round(c.size, 2)
                        for obj in tbox
                        for c in obj
                        if isinstance(c, LTChar)
                    )
                ),
                "font_familyface": list(
                    set(
                        c.fontname for obj in tbox for c in obj if isinstance(c, LTChar)
                    )
                ),
            },
        )

    return data


def get_all_data(path, pages=None):
    pdfminer_detailed = []
    try:
        with PdfMinerWrapper(path) as doc:
            for page in doc:
                pdfminer_detailed.append(get_text_object_details(page))
                if pages != None:
                    pages -= 1
                if pages == 0:
                    break
    except Exception as e:
        pdfminer_detailed = [{"error": f"{e}"}]

    try:
        pdfminer_results = pdfminer_to_text(path, pages=pages)
    except Exception as e:
        pdfminer_results = f"error: {e}"

    try:
        pypdf2_results = pypdf2txt(path, pages=pages)
    except Exception as e:
        pypdf2_results = f"error: {e}"

    return {
        "filepath": path,
        "filename": path.split("/")[-1],
        "college": path.split("/")[1],
        "pdfminer": pdfminer_results,
        "pdfminer_detailed": pdfminer_detailed,
        "pypdf2": pypdf2_results,
    }
