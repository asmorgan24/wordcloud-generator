from wordcloud import WordCloud
import numpy as np
import IPython

from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFilter
from PIL import ImageFont

def makecloud(words, params, image_save_location):

    width = params['img_width']
    height = params['img_height']
    num_of_words = params['num_words']
    background_color = tuple(params['background_color'])
    make_gif = params['save_as_gif']
    words_each_interval = params['words_each_interval']
    duration = params['interval_duration']
    use_mask = params['use_mask']
    mask_filename = params['mask_filename']


    excludewords = []
    f = open(params['proj_path']+'/stopwords.txt', 'r')
    for line in f.readlines():
        excludewords.append(line.strip())

    if use_mask:
        mask_img = np.array(Image.open(params['proj_path']+'/masks/'+mask_filename))
        wordcloud = WordCloud(max_words=num_of_words, width=width, height=height,
                          stopwords=excludewords, background_color=background_color, mask = mask_img, contour_width=16, contour_color='steelblue')
    else:
        wordcloud = WordCloud(max_words=num_of_words, width=width, height=height,
                          stopwords=excludewords, background_color=background_color)


    wordcloud.generate(words)

    if make_gif == True:
        images = []
        wordcloud.to_image = _new_to_image #override with function below
        for n_words in range(1,num_of_words,words_each_interval):
            images.append(wordcloud.to_image(wordcloud, n_words))

        images[0].save(image_save_location +'.gif',
               save_all=True, append_images=images[1:], optimize=False, duration=duration, loop=0)
    else:
        image = wordcloud.to_image()
        # image.show()
        image.save(image_save_location+ '.jpeg')

#################################################################
# Change to_image function in wordcloud to work for our needs
################################################################
def _new_to_image(self, max_words = 1e6):
    self._check_generated()
    if self.mask is not None:
        width = self.mask.shape[1]
        height = self.mask.shape[0]
    else:
        height, width = self.height, self.width

    # self.background_color = (int('1e',16),int('6c',16),int('93', 16))
    # self.background_color = None
    # self.background_color = (255,255,255)
    img = Image.new(self.mode, (int(width * self.scale),
                                int(height * self.scale)),
                    self.background_color)
    draw = ImageDraw.Draw(img)
    counter =0
    for (word, count), font_size, position, orientation, color in self.layout_:
        if counter > max_words:
            break
        font = ImageFont.truetype(self.font_path,
                                  int(font_size * self.scale))
        transposed_font = ImageFont.TransposedFont(
            font, orientation=orientation)
        pos = (int(position[1] * self.scale),
               int(position[0] * self.scale))
        draw.text(pos, word, fill=color, font=transposed_font)
        counter+=1

    return self._draw_contour(img=img)
