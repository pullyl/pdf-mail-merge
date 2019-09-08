import pandas as pd
import pdfrw
from PyPDF2 import PdfFileWriter, PdfFileReader

INVOICE_TEMPLATE_PATH = 'input_pdf.pdf'
INVOICE_OUTPUT_PATH = 'outputs/'
DATA_TO_MERGE_PATH = 'data_to_merge.csv'


ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'


def write_fillable_pdf(input_pdf_path, data):
    count = 0
    pdf_writer = PdfFileWriter()


    for data_dict in data:
        count += 1

        if divmod(count, 50) == 0:
            print(count)

        template_pdf = pdfrw.PdfReader(input_pdf_path)
        annotations = template_pdf.pages[0]['/Annots']

        for annotation in annotations:
            if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                if annotation[ANNOT_FIELD_KEY]:
                    key = annotation[ANNOT_FIELD_KEY][1:-1]
                    if key in data_dict.keys():
                        data = str(data_dict[key]).replace('.0', '')
                        annotation.update(
                            pdfrw.PdfDict(AP=data_dict[key], V=data)
                        )
                    else:
                        print('unable to find {k}'.format(k=key))
        filename = '{f}{num}_{name}.pdf'.format(f=INVOICE_OUTPUT_PATH, num=data_dict['num'], name=data_dict['full_name'].replace(' ', '_').lower())
        pdfrw.PdfWriter().write(filename, template_pdf)

        pdf_reader = PdfFileReader(filename)
        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))

    with open('{o}combined_file.pdf'.format(o=INVOICE_OUTPUT_PATH), 'wb') as fh:
        pdf_writer.write(fh)

    print('finished writing files')

if __name__ == '__main__':

    df = pd.read_csv(DATA_TO_MERGE_PATH)
    df = df.fillna('')
    data_dict = df.to_dict('records')

    write_fillable_pdf(INVOICE_TEMPLATE_PATH, data_dict)