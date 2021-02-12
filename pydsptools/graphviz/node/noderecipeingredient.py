class NodeRecipeIngredient:
  def __init__(self, icon, count):
    self.__icon = icon
    self.__count = count

  def icon(self):
    return self.__icon

  def count(self):
    return self.__count
