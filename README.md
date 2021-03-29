# Generate a Wordcloud from a bundle of PDFs
![asmorgan24's wordcloud of peer-reviewed papers](papers.gif)


A (simple) script for generating wordcloud images and GIFs from PDF documents. This package was built using Python 3.6 and depends on the PyPDF2(https://github.com/mstamy2/PyPDF2) and the word_cloud(https://github.com/amueller/word_cloud) external repositories. 

## Usage

Install the appropriate aforementioned python modules. Place all PDFs you want to use for wordcloud generation into a ```pdfs/``` folder in the main directory. Also create an ```out/``` folder in the main directory. Run the following command ``` python main.py```, where you have the follwing args to choose from:

```('--filename', default='test')

    ('--image_height', default=1080, type=int)
    ('--image_width', default=1920, type=int)
    ('--num_words', default=250, type=int)
    ('--background_color', default='black')

    ('--save_as_gif', default=False, action='store_true')
    ('--interval_duration', default=500, type=int)
```

## Contribute
Feel free to openly use and adapt this code however you and your project sees fit. 

