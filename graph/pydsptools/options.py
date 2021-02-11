import json

class Options:
  def __init__(self):
    with open('options.json') as json_file:
      self.__options = json.load(json_file)

  def __getitem__(self, name):
    return self.__options[name]

  def color(self, color_name):
    if color_name in self.__options['colors']:
      return self.__options['colors'][color_name]
    print('Need to add color {0}'.format(color_name))
    return self.__options['colors']['background']

  def __flag(self, flag):
    if flag in self.__options['flags']:
      return self.__options['flags'][flag]
    print('Need to add flag {0}'.format(flag))
    return self.__options['flags']['default']

  def flag_icon(self, flag):
    return self.__flag(flag)['icon']

  def flag_name(self, flag):
    return self.__flag(flag)['name']

options = Options()
