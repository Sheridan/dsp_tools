import re
from pydsptools.options import options

class Entity:
  def __init__(self, color):
    self.__color = options.color(color)

  def color(self):
    return self.__color

  def load_template_raw(self, name):
    with open('templates/{0}'.format(name), 'r') as file:
      return file.read()

  def load_template(self, name):
    return self.load_template_raw(name).replace('\n', '')

  def normalize_name(self, name):
    return re.sub('[^0-9a-z]+', '_', name.lower())

  def compact_string(self, s):
    return re.sub('>\s+<', '><', s)
