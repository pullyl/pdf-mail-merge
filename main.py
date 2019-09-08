import pandas as pd
import pdfrw

INVOICE_TEMPLATE_PATH = 'chair_application.pdf'
INVOICE_OUTPUT_PATH = 'outputs/'
DATA_TO_MERGE_PATH = 'data_to_merge.csv'


ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'


def write_fillable_pdf(input_pdf_path, output_pdf_path, data):
    template_pdf = pdfrw.PdfReader(input_pdf_path)
    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))

    annotations = template_pdf.pages[0][ANNOT_KEY]

    count = 0

    for data_dict in data:
        count += 1
        for annotation in annotations:
            if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                if annotation[ANNOT_FIELD_KEY]:
                    key = annotation[ANNOT_FIELD_KEY][1:-1]
                    if key in data_dict.keys():
                        annotation.update(
                            #pdfrw.PdfDict(V='{}'.format(data_dict[key]))
                            pdfrw.PdfDict(V="test test test")
                        )
                        print('updated annotation with {d}'.format(d=data_dict[key]))
                    else:
                        print('unable to find {k}'.format(k=key))
        filename = '{f}{num}_{name}.pdf'.format(f=INVOICE_OUTPUT_PATH, num=data_dict['num'], name=data_dict['full_name'].replace(' ', '').lower())

        pdfrw.PdfWriter().write(filename, template_pdf)

        if count > 3:
            break

if __name__ == '__main__':

    df = pd.read_csv(DATA_TO_MERGE_PATH)
    data_dict = df.to_dict('records')

    write_fillable_pdf(INVOICE_TEMPLATE_PATH, INVOICE_OUTPUT_PATH, data_dict)