class Recipe:
  def __init__(self, key, data):
    self.__key = key
    self.__data = data
    self.__sources = []
    self.__results = []
    self.__assemblers = []

  def add_source(self, item, count):
    self.__sources.append({'item': item, 'count': count})

  def add_result(self, item, count):
    self.__results.append({'item': item, 'count': count})

  def sources(self):
    return self.__sources

  def results(self):
    return self.__results

  def item_result(self, item_key):
    for result in self.__results:
      if result['item'].key() == item_key:
        return result
    return None

  def type(self):
    return self.__data["type"]

  def time(self):
    return self.__data["timeSpend"]/60

  def set_assemblers(self, assemblers):
    self.__assemblers = assemblers

  def assemblers(self):
    return self.__assemblers

  def flags(self):
    flags = []
    for key in ["handcraft"]:
      if key in self.__data and self.__data[key]:
        flags.append(key)
    return flags
