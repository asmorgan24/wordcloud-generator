import sys, os
import IPython
from os import walk
import numpy as np
import yaml

#application specific src files
sys.path.insert(1, './src')
import pdfparser
import cloud


def readPDFs(params):
    #Find all pdf files in 'pdfs' subdirectory
    path = params['proj_path']+'/pdfs'
    pdf_files = []
    for root, directories, files in os.walk(path, topdown=False):
        for name in files:
            if name[-4:]=='.pdf':
                pdf_files.append(os.path.join(root, name))

    #Extract All
    words = '' #initialize
    for i in range(len(pdf_files)):
        # path to pdf
        path = pdf_files[i]

        doc_len = pdfparser.get_doc_length(path)
        start_page =0
        pdf_to_word =pdfparser.get_string_from_pdf(path, start_page, doc_len)
        words+=pdf_to_word

        print ('Processed: ', pdf_files[i])
    return words

def readCSVwords(params):
    w = np.loadtxt(params['proj_path']+'/fakewords.csv', dtype = str, delimiter = ',')
    words= ""
    for i in range(len(w)):
        for _ in range(int(w[i][1])):
            words+=str(w[i][0])
            words+='\n'
    return words

def main():
    #Load params to for the image creator
    with open('params.yaml') as f:
        params = yaml.load(f, Loader=yaml.FullLoader)

    #Set project path directory
    params['proj_path'] = os.getcwd() if params['proj_path'] == 'None' else params['proj_path']

    # Name of the savable image, without the filetype
    image_save_location = params['proj_path']+'/out/'+params['saved_filename']

    if params['use_pdfs'] == True: #use the pdf for accumulating words
        text = readPDFs(params)
    else: #use the csv file for accumulating words
        text = readCSVwords(params)

    if params['save_as_gif'] == True:
        print ('Saving as .GIF, please be patient...')

    # If you want to exclude certain words from the cloud,
    # you can add them as a new line to the file stopwords.txt
    cloud.makecloud(text, params, image_save_location)
    print ('Alles fertig! All done!')

if __name__ == '__main__':
    main()
