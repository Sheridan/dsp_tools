class NodeRecipeAssemblerBelt:
  def __init__(self, icon, assemblers_count):
    self.__icon = icon
    self.__assemblers_count = assemblers_count

  def icon(self):
    return self.__icon

  def assemblers_count(self):
    return self.__assemblers_count

class NodeRecipeAssembler:
  def __init__(self, icon, time, belts):
    self.__icon = icon
    self.__time = time
    self.__belts = belts

  def icon(self):
    return self.__icon

  def time(self):
    return self.__time

  def belts(self):
    return self.__belts

class NodeRecipe:
  def __init__(self):
    self.__ingridients = []
    self.__results = []
    self.__assemblers = []

  def results(self):
    return self.__results

  def append_result(self, ingridient):
    self.__results.append(ingridient)

  def ingredients(self):
    return self.__ingridients

  def append_ingredient(self, ingridient):
    self.__ingridients.append(ingridient)

  def assemblers(self):
    return self.__assemblers

  def append_assembler(self, assembler):
    self.__assemblers.append(assembler)
