import pdfparser
import cloud
import IPython
import argparse, os, sys
from os import walk

def parse_args():
    parser = argparse.ArgumentParser()
    # environment
    parser.add_argument('--filename', default='test')

    parser.add_argument('--image_height', default=1080, type=int) #2160
    parser.add_argument('--image_width', default=1920, type=int) #3840
    parser.add_argument('--num_words', default=250, type=int)
    parser.add_argument('--background_color', default='black')

    parser.add_argument('--save_as_gif', default=False, action='store_true')
    parser.add_argument('--interval_duration', default=500, type=int)

    args = parser.parse_args()
    return args

def main():
    arg = parse_args()

    #Find all pdf files in 'pdfs' subdirectory
    path = '.'
    pdf_files = []
    for root, directories, files in os.walk(path, topdown=False):
        for name in files:
            if name[-4:]=='.pdf':
                pdf_files.append(os.path.join(root, name))
    # Name of the image
    image_file_name = 'out/'+arg.filename

    total_words = 'a' #initialize
    for i in range(len(pdf_files)):
        # path to pdf
        path = pdf_files[i]

        doc_len = pdfparser.get_doc_length(path)
        start_page =1
        pdf_to_word =pdfparser.get_string_from_pdf(path, start_page, doc_len)
        total_words+=pdf_to_word

        print ('Processed: ', pdf_files[i])

    if arg.save_as_gif == True:
        print ('Saving as .GIF, please be patient...')

    # If you want to exclude certain words from the cloud,
    # you can add them as a new line to the file stopwords.txt
    cloud.makecloud(total_words, arg.image_width,
                    arg.image_height, arg.num_words, image_file_name,
                    arg.background_color, arg.save_as_gif,
                    arg.interval_duration)
    print ('Alles fertig!')

if __name__ == '__main__':
    main()
