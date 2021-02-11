class NodeInfo:
  def __init__(self, caption, value, suffix):
    self.__caption = caption
    self.__value = value
    self.__suffix = suffix

  def caption(self):
    return self.__caption

  def value(self):
    return self.__value if self.is_icon() else "{0}{1}".format(self.__value, self.__suffix)

  def is_icon(self):
    return self.__caption == None

  def is_empty(self):
    return not self.is_icon() and self.__value == 0

class NodeTextInfo(NodeInfo):
  def __init__(self, caption, text, suffix = ""):
    super().__init__(caption, text, suffix)

class NodeIconInfo(NodeInfo):
  def __init__(self, icon):
    super().__init__(None, icon, "")
