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
    self.__original_filename = 'result/icons/original/{0}.png'.format(self.__key)
    self.__download()

  def __download(self):
    if not os.path.isfile(self.__original_filename):
      print("Downloading icon for {0} ({1})".format(self.__key, self.__url))
      with open(self.__original_filename, 'wb') as icon_file:
        response = requests.get(self.__url, stream=True)
        if not response.ok:
            print(response)
        for block in response.iter_content(1024):
            if not block:
                break
            icon_file.write(block)

  def resized(self, size):
    resized_filename = 'result/icons/generated/{0}_{1}.png'.format(self.__key, size)
    if not os.path.isfile(resized_filename):
      print("Resizing icon for {0} to {1}".format(self.__key, size))
      with Image(width=size, height=size, background=Color("NONE")) as result:
        with Image(filename=self.__original_filename) as img:
          img.transform(resize='{0}x{0}'.format(size))
          result.composite(img, left=int((size-img.width)/2), top=int((size-img.height)/2))
        result.save(filename=resized_filename)
    return resized_filename

  def subscribed(self, size, text):
    subscribed_filename = 'result/icons/generated/{0}_{1}_{2}.png'.format(self.__key, size, text)
    if not os.path.isfile(subscribed_filename):
      print("Subscribing icon {0} ({1}) with {2}".format(self.__key, size, text))
      with Drawing() as draw:
        with Image(filename=self.resized(size)) as img:
          draw.font_family = options['icons']['font']
          draw.font_weight = 800
          draw.font_size = int(size/2)
          draw.fill_color = Color(options['icons']['text_fill_color'])
          draw.stroke_color = Color(options['icons']['text_stroke_color'])
          draw.stroke_width = 2
          draw.stroke_antialias = True
          draw.text(4, int(img.height - 8), '{0}'.format(text))
          draw(img)
          img.save(filename=subscribed_filename)
    return subscribed_filename
