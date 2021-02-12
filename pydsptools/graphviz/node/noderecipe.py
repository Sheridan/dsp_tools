
class NodeRecipe:
  def __init__(self, assembler_icon, time):
    self.__assembler_icon = assembler_icon
    self.__time = time
    self.__ingridients = []
    self.__results = []

  def assembler_icon(self):
    return self.__assembler_icon

  def time(self):
    return self.__time

  def results(self):
    return self.__results

  def append_result(self, ingridient):
    self.__results.append(ingridient)

  def append_ingredient(self, ingridient):
    self.__ingridients.append(ingridient)

  def ingredients(self):
    return self.__ingridients
