from wordcloud import WordCloud
import IPython

from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFilter
from PIL import ImageFont

def makecloud(words, width, height, num_of_words, image_file_name, background_color, make_gif=False, duration = 200):

    excludewords = []
    f = open('stopwords.txt', 'r')
    for line in f.readlines():
        excludewords.append(line.strip())

    wordcloud = WordCloud(max_words=num_of_words, width=width, height=height,
                          stopwords=excludewords, background_color=background_color).generate(words)
    if make_gif == False:
        image = wordcloud.to_image()
        # image.show()
        image.save(image_file_name + '.jpeg')
    else:
        images = []
        wordcloud.to_image = _new_to_image #override with function below
        for n_words in range(1,num_of_words,2):
            images.append(wordcloud.to_image(wordcloud, n_words))

        images[0].save(image_file_name +'.gif',
               save_all=True, append_images=images[1:], optimize=False, duration=duration, loop=0)


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
