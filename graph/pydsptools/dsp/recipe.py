class Recipe:
  def __init__(self, key, data):
    self.__key = key
    self.__data = data
    self.__sources = []
    self.__results = []
    self.__assembler = None

  def add_source(self, item, count):
    self.__sources.append({'item': item, 'count': count})

  def add_result(self, item, count):
    self.__results.append({'item': item, 'count': count})

  def sources(self):
    return self.__sources

  def results(self):
    return self.__results

  def type(self):
    return self.__data["type"]

  def time(self):
    return self.__data["timeSpend"]/60

  def set_assembler(self, assembler):
    self.__assembler = assembler

  def assembler(self):
    return self.__assembler

  def flags(self):
    flags = []
    for key in ["handcraft"]:
      if key in self.__data and self.__data[key]:
        flags.append(key)
    return flags
