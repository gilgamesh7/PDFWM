# https://github.com/claird/PyPDF4/blob/master/pypdf/pdf.py
# https://stackoverflow.com/questions/37752604/watermark-removal-on-pdf-with-pypdf2


import sys,os

from PyPDF4 import PdfFileReader, PdfFileWriter
from PyPDF4.pdf import ContentStream
from PyPDF4.utils import b_
from PyPDF4.generic import TextStringObject, NameObject

def readPDF(inFileName, outFileName):
    try:
        PDFInputName = inFileName
        PDFOutputName = outFileName

        pdfWriter = PdfFileWriter()

        with open(PDFInputName,'rb') as fileHandle:
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

                # loop throug operators and operands in contents
                for operands, operator in pageContent.operations:
                    # if operator == b_("cm") and match_location(operands, target_locations):
                    if operator == b_("Tj") and operands==[b'\x00C\x00O\x00P\x00Y\x00-\x00O\x00N\x00L\x00Y'] :
                        # for x in operands :
                        print(f"{operator} - [{operands[0]}] - {type(operands)}")
                        operands[0] = TextStringObject('')
                        # operands[:] = []
                        print(f"{operator} - [{operands[0]}] - {type(operands)}")

                # Replace /Contents in pageObject
                pageObject.__setitem__(NameObject('/Contents'),pageContent)

            # Write to output file
            with open(PDFOutputName,"wb") as outStream:
                pdfWriter.write(outStream)


        return(f"{PDFAllInfo}")
        
                # print(f"---------------------------{pageNum}--------------------------")
                # # Get Object dictionary. Eg : {'/Type': '/Page', '/MediaBox': [0, 0, 595, 842], '/Parent': IndirectObject(2, 0), '/Contents': [IndirectObject(4, 0)], '/Resources': {'/Font': {'/F_tst_0': IndirectObject(5, 0), '/F_tst_2': IndirectObject(6, 0), '/F_tst_4': IndirectObject(7, 0), '/F_tst_1': IndirectObject(8, 0), '/F_tst_3': IndirectObject(9, 0)}, '/XObject': {'/O100004M': IndirectObject(10, 0), '/Im_tst_0': IndirectObject(11, 0), '/O10000CM': IndirectObject(12, 0), '/O100002P': IndirectObject(13, 0)}}}
                # pageObject = pdfReader.getPage(pageNum)
                # # Get only the /Contents item in dictionary Eg : [IndirectObject(4, 0)]
                # pageContentsObject = pageObject['/Contents']
                # # # Extract the elements fo the /Contents object as a contentstream (cant print this directly)
                # pageContent = ContentStream(pageContentsObject,pdfReader)
                # print(pageContent)



                # pageContentsObject = pageObject['/Parent']
                # # print(pageContentsObject)
                # for parentObject in pageContentsObject['/Kids']:
                #     # print(parentObject)
                #     print(30*"+")
                #     # POContents = parentObject.getObject()['/Contents'][0].getObject()
                #     POResourcesXObj = parentObject.getObject()['/Resources']['/XObject']['/O100004M'].getObject()
                #     print(POResourcesXObj)


                # pageContent = ContentStream(parentObject,pdfReader)
                # print(pageContent)
                # pageContent = ContentStream(pageContentsObject,pdfReader)
                # # Get operands and operators 
                # if pageNum == 0:
                #     # operators_list = []
                #     # for operands, operator in pageContent.operations:
                #     #    operators_list.append(operator)
                #     # unique_operators = []
                #     # for op in operators_list:
                #     #     if op not in unique_operators:
                #     #         unique_operators.append(op)
                #     # print(f"{unique_operators}")
                #     for operands, operator in pageContent.operations:
                #         # if operator == b_("f*"):
                #         print(f"{operator} - {operands}")






                # for operands, operator in pageContent.operations:
                #     print(f"{operands} , {operator}")
            #         # Look for Text, operator "Tj" (others are "cm","Do", "Tm", "Q" etc.)
            #         if operator == b_("Tj"):
            #             # Use operand[0] , as operand is a list with 1 item
            #             text = operands[0].decode('utf-8')
            #             print(text)

                        # Find the water mark text and replace it with whatever you want
                        # if isinstance(text,str) and text.startswith(wmText):
                        #     print(operands[0])
                        #     operands[0] = TextStringObject('InGodWeTrust')
                        #     print(operands[0])

        #         # Replace /Contents in pageObject
        #         pageObject.__setitem__(NameObject('/Contents'),pageContent)

        #         # Add page to pdf writer
        #         pdfWriter.addPage(pageObject)

        # with open(PDFOutputName,"wb") as outStream:
        #     pdfWriter.write(outStream)


    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"{exc_type}, {exc_obj} , {fname} : {exc_tb.tb_lineno}")    
        
if __name__ == "__main__":
    print(f"{readPDF('$15 Loyalty credit - 12 months.pdf','My PDF.pdf')}")
