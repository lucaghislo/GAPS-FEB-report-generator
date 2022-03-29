from __future__ import print_function
from mailmerge import MailMerge
from datetime import date

document = MailMerge('FEB_py_script/template.docx')
print(document.get_merge_fields())

document.merge(
    board_ID = '5',
    date = '5',
    asic_ID = '5',
    AVDD = '5',
    IVDD = '5',
    DVDD = '5',
    IDVDD = '5'
)

document.write('FEB_py_script/template_out.docx')