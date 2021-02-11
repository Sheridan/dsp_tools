import requests
import os.path
import sys

from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color

from pydsptools.options import options

class Icon:
  def __init__(self, key, url):
    self.__url = url
    self.__key = key
    self.__download()

  def __gen_filename(self, size = 0):
    return 'icons/{0}.png'.format(self.__key) if size == 0 else 'icons/{0}_{1}.png'.format(self.__key, size)

  def __download(self):
    if not os.path.isfile(self.__gen_filename()):
      print("Downloading icon for {0} ({1})".format(self.__key, self.__url))
      with open(self.__gen_filename(), 'wb') as icon_file:
        response = requests.get(self.__url, stream=True)
        if not response.ok:
            print(response)
        for block in response.iter_content(1024):
            if not block:
                break
            icon_file.write(block)

  def resized(self, size):
    if not os.path.isfile(self.__gen_filename(size)):
      print("Resizing icon for {0} to {1}".format(self.__key, size))
      with Image(width=size, height=size, background=Color("NONE")) as result:
        with Image(filename=self.__gen_filename()) as img:
          img.transform(resize='{0}x{0}'.format(size))
          result.composite(img, left=int((size-img.width)/2), top=int((size-img.height)/2))
        result.save(filename=self.__gen_filename(size))
    return self.__gen_filename(size)

  def subscribed(self, size, text):
    filename = 'icons/{0}_{1}_{2}.png'.format(self.__key, size, text)
    if not os.path.isfile(filename):
      print("Subscribing icon {0} ({1}) with {2}".format(self.__key, size, text))
      with Drawing() as draw:
        with Image(filename=self.resized(size)) as img:
          draw.font_family = 'Roboto'
          draw.font_weight = 800
          draw.font_size = 30
          draw.fill_color = Color(options.color('icon_text_fill_color'))
          draw.stroke_color = Color(options.color('icon_text_stroke_color'))
          draw.stroke_width = 1
          draw.stroke_antialias = True
          draw.text(4, int(img.height - 8), '{0}'.format(text))
          draw(img)
          img.save(filename = filename)
    return filename
