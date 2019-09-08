# pdf-mail-merge

Scripts to write data into PDF files.  Based off instructions here - https://bostata.com/how-to-populate-fillable-pdfs-with-python/

## Preparation
* PDF with fillable fields as input to the program.  You can create one using Adobe's Desktop Software (free trial or paid account required)
* CSV with fields to merge.  Fields should match the field names in PDF / adobe
* Update paths in main.py for inputs / outputs

## Output
* One file per input row
* Combined PDF of all output files

##Running
```python3 main.py```