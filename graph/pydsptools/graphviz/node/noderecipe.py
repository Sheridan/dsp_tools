
class NodeRecipe:
  def __init__(self, assembler_icon, time):
    self.__assembler_icon = assembler_icon
    self.__time = time
    self.__ingridients = []

  def assembler_icon(self):
    return self.__assembler_icon

  def time(self):
    return self.__time

  def append_ingredient(self, ingridient):
    self.__ingridients.append(ingridient)

  def ingredients(self):
    return self.__ingridients
