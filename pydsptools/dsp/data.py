import json
from pydsptools.dsp.item import Item
from pydsptools.dsp.tech import Tech
from pydsptools.dsp.recipe import Recipe

class Data:
  def __init__(self):
    with open('data.json') as json_file:
      self.__data = json.load(json_file)
    with open('dump.json') as json_file:
      self.__dump = json.load(json_file)
    self.__items = {}
    self.__techs = {}

  def __has_icon(self, key):
    return key in self.__data['mapping']['icons']

  def __get_icon_url(self, key):
    return self.__data['mapping']['icons'][key]

  def __get_assembler(self, name):
    return {
        'Assemble': self.get_item('assembler-1'),
        'Chemical': self.get_item('chemical-plant'),
        'Fractionate': self.get_item('fractionator'),
        'Particle': self.get_item('hadron-collider'),
        'Refine': self.get_item('oil-refinery'),
        'Research': self.get_item('lab'),
        'Smelt': self.get_item('smelter')
    }[name]

  def get_item_recipes(self, item_key):
      recipes = []
      for recipe_key in self.__dump['recipe']:
        recipe_data = self.__dump['recipe'][recipe_key]
        for result_item_key in recipe_data['results']:
          if result_item_key == item_key:
            recipe = Recipe(recipe_key, recipe_data)
            for src_item_key in recipe_data['items']:
              recipe.add_source(self.get_item(src_item_key), recipe_data['items'][src_item_key])
            for res_item_key in recipe_data['results']:
              recipe.add_result(self.get_item(res_item_key), recipe_data['results'][res_item_key])
            recipe.set_assembler(self.__get_assembler(recipe_data['type']))
            recipes.append(recipe)
      return recipes

  def get_item_used_in(self, item_key):
    result = []
    for recipe_key in self.__dump['recipe']:
      recipe_data = self.__dump['recipe'][recipe_key]
      for src_item_key in recipe_data['items']:
        if item_key == src_item_key:
          for res_item_key in recipe_data['results']:
            if self.__has_icon(res_item_key):
              result.append(self.get_item(res_item_key))
    return result

  def get_item_tech(self, item_key):
    for tech_key in self.__dump['tech']:
      if 'addItems' in self.__dump['tech'][tech_key]:
        for tech_unlock_key in self.__dump['tech'][tech_key]['addItems']:
          if tech_unlock_key == item_key:
            return self.get_tech(tech_key)
    return None

  def get_item_prefab(self, item_key):
    for prefab_key in self.__dump['prefab']:
      if prefab_key == item_key:
        return self.__dump['prefab'][prefab_key]
    return {}

  def get_item(self, item_key):
    if item_key not in self.__items:
      print('Loading item {0}'.format(item_key))
      self.__items[item_key] = Item(item_key, self.__get_icon_url(item_key), self.__dump['item'][item_key])
      self.__items[item_key].set_recipes(self.get_item_recipes(item_key))
      self.__items[item_key].set_used_in(self.get_item_used_in(item_key))
      self.__items[item_key].set_tech(self.get_item_tech(item_key))
      self.__items[item_key].set_prefab(self.get_item_prefab(item_key))
    return self.__items[item_key]

  def get_tech_parents(self, tech_key):
    result = []
    if 'preTechs' in self.__dump['tech'][tech_key]:
      for tech_parent_key in self.__dump['tech'][tech_key]['preTechs']:
        result.append(self.get_tech(tech_parent_key))
    return result

  def get_tech_unlocks(self, tech_key):
    result = []
    if 'addItems' in self.__dump['tech'][tech_key]:
      for tech_unlock_key in self.__dump['tech'][tech_key]['addItems']:
        result.append(self.get_item(tech_unlock_key))
    for item in self.item_list():
      if item.has_pretech() and item.pretech() == self.__dump['tech'][tech_key]['name'] and item not in result:
        result.append(item)
    return result

  def get_tech_resources(self, tech_key):
    result = []
    if 'items' in self.__dump['tech'][tech_key]:
      for tech_resource_key in self.__dump['tech'][tech_key]['items']:
        result.append({'item': self.get_item(tech_resource_key), 'count': self.__dump['tech'][tech_key]['items'][tech_resource_key] })
    return result

  def get_tech(self, tech_key):
    if tech_key not in self.__techs:
      print('Loading tech {0}'.format(tech_key))
      self.__techs[tech_key] = Tech(tech_key, self.__get_icon_url(tech_key), self.__dump['tech'][tech_key])
      self.__techs[tech_key].set_parents(self.get_tech_parents(tech_key))
      self.__techs[tech_key].set_unlocks(self.get_tech_unlocks(tech_key))
      self.__techs[tech_key].set_resources(self.get_tech_resources(tech_key))
    return self.__techs[tech_key]

  def item_list(self):
    result = []
    for item_key in self.__dump['item']:
      if self.__has_icon(item_key):
        result.append(self.get_item(item_key))
    return result

  def tech_list(self):
    result = []
    for tech_key in self.__dump['tech']:
      if self.__has_icon(tech_key):
        result.append(self.get_tech(tech_key))
    return result

dsp_data = Data()
