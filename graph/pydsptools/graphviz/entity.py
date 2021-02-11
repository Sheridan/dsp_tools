import re
from pydsptools.options import options

class Entity:
  def __init__(self, color):
    self.__color = options.color(color)

  def color(self):
    return self.__color

  def load_template(self, name):
    with open('templates/{0}'.format(name), 'r') as file:
      return file.read().replace('\n', '')

  def normalize_name(self, name):
    return re.sub('[^0-9a-z]+', '_', name.lower())
