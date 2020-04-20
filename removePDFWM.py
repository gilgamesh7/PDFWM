## pyPDF4 documentation
# https://github.com/claird/PyPDF4/blob/master/pypdf/pdf.py
# https://stackoverflow.com/questions/37752604/watermark-removal-on-pdf-with-pypdf2
## reportlab documentation
# https://stackoverflow.com/questions/45144293/how-to-erase-text-from-pdf-using-python
# https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=2&cad=rja&uact=8&ved=2ahUKEwjwkeWuyPboAhWhzzgGHVoMCGQQFjABegQIAhAB&url=https%3A%2F%2Fwww.reportlab.com%2Fdocs%2Freportlab-userguide.pdf&usg=AOvVaw35b6LztPqVNdiQATpOtCOK


import sys,os

from PyPDF4 import PdfFileReader, PdfFileWriter
from PyPDF4.pdf import ContentStream
from PyPDF4.utils import b_
from PyPDF4.generic import TextStringObject, NameObject

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

def readPDF(inFileName, outFileName):
    try:
        PDFInputName = inFileName
        PDFOutputName = outFileName
        PDFInterimName = "output.pdf"

        ## Put a white ractangle on page 1
        # Create a a borderless white rectangle
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        can.setFillColorRGB(255,255,255)
        can.rect(450,550,100,40, fill=1, stroke=0)
        can.save()

        # set to beginning of bytestream and create a new PDF
        packet.seek(0)
        newPdf = PdfFileReader(packet)
        interimOutput = PdfFileWriter()

        with open(PDFInputName,'rb') as fileStream:
            existingPdf = PdfFileReader(fileStream)

            # Get first Page and merge with rectangle
            page = existingPdf.getPage(0)
            page.mergePage(newPdf.getPage(0))
            numPages = existingPdf.getNumPages()
            for n in range(numPages):
                interimOutput.addPage(existingPdf.getPage(n))

            with open(PDFInterimName, "wb") as fileStream :
                interimOutput.write(fileStream)

        pdfWriter = PdfFileWriter()

        with open(PDFInterimName,'rb') as fileHandle:
            # Read & extract Information
            pdfReader = PdfFileReader(fileHandle)
            pdfInfo = pdfReader.getDocumentInfo()
            numPages = pdfReader.getNumPages()

            PDFAllInfo = {
                            'author' : pdfInfo.author, 
                            'creator' : pdfInfo.creator, 
                            'producer' : pdfInfo.producer, 
                            'subject' : pdfInfo.subject, 
                            'title' : pdfInfo.title,
                            'num_pages' : numPages
                        }
            # Get content in all pages
            for pageNum in range(numPages):
                # Get page
                pageObject = pdfReader.getPage(pageNum)

                # Get only the /Contents item in dictionary Eg : [IndirectObject(4, 0)]
                pageContentsObject = pageObject['/Contents']

                # Extract the elements fo the /Contents object as a contentstream (cant print this directly)
                pageContent = ContentStream(pageContentsObject,pdfReader)               # Check operands and operators

                # Add page to pdf writer
                pdfWriter.addPage(pageObject)

                # loop through operators and operands in contents
                for operands, operator in pageContent.operations:
                    if operator == b_("Tj") and operands==[b'\x00C\x00O\x00P\x00Y\x00-\x00O\x00N\x00L\x00Y'] :
                        operands[0] = TextStringObject('')

                # Replace /Contents in pageObject
                pageObject.__setitem__(NameObject('/Contents'),pageContent)

            # Write to output file
            with open(PDFOutputName,"wb") as outStream:
                pdfWriter.write(outStream)


        return(f"{PDFOutputName}")
        
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"{exc_type}, {exc_obj} , {fname} : {exc_tb.tb_lineno}")    
        
if __name__ == "__main__":
    print(f"{readPDF('$15 Loyalty credit - 12 months.pdf','My PDF.pdf')}")
