from pydsptools.dsp.icon import Icon

class Tech:
  def __init__(self, key, icon_url, data):
    self.__key = key
    self.__data = data
    self.__icon = Icon(self.__key, icon_url)
    self.__unlocks = []
    self.__parents = []
    self.__resources = []

  def node_name(self):
    return '{0}_{1}'.format(self.key(), self.name())

  def key(self):
    return self.__key

  def icon(self):
    return self.__icon

  def name(self):
    return self.__data["name"]

  def haches(self):
    return self.__data["hashNeeded"]

  def set_unlocks(self, unlocks):
    self.__unlocks = unlocks

  def set_parents(self, parents):
    self.__parents = parents

  def set_resources(self, resources):
    self.__resources = resources

  def unlocks(self):
    return self.__unlocks

  def parents(self):
    return self.__parents

  def resources(self):
    return self.__resources

  def flags(self):
    flags = []
    for key in ["isLabTech"]:
      if key in self.__data and not self.__data[key]:
        flags.append(key)
    return set(flags)
