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

  def has_icon(self, key):
    return key in self.__data['mapping']['icons']

  def get_icon_url(self, key):
    return self.__data['mapping']['icons'][key]

  def get_assembler(self, name):
    return {
        'Assemble': self.get_item('assembler-1', False),
        'Chemical': self.get_item('chemical-plant', False),
        'Fractionate': self.get_item('fractionator', False),
        'Particle': self.get_item('hadron-collider', False),
        'Refine': self.get_item('oil-refinery', False),
        'Research': self.get_item('lab', False),
        'Smelt': self.get_item('smelter', False)
    }[name]

  def get_item_recipes(self, item_key):
      recipes = []
      for recipe_key in self.__dump['recipe']:
        recipe_data = self.__dump['recipe'][recipe_key]
        for result_item_key in recipe_data['results']:
          if result_item_key == item_key:
            recipe = Recipe(recipe_key, recipe_data)
            for src_item_key in recipe_data['items']:
              recipe.add_source(self.get_item(src_item_key, False), recipe_data['items'][src_item_key])
            for res_item_key in recipe_data['results']:
              recipe.add_result(self.get_item(res_item_key, False), recipe_data['results'][res_item_key])
            recipe.set_assembler(self.get_assembler(recipe_data['type']))
            recipes.append(recipe)
      return recipes

  def get_item_used_in(self, item_key):
    result = []
    for recipe_key in self.__dump['recipe']:
      recipe_data = self.__dump['recipe'][recipe_key]
      for src_item_key in recipe_data['items']:
        if item_key == src_item_key:
          for res_item_key in recipe_data['results']:
            if self.has_icon(res_item_key):
              result.append(self.get_item(res_item_key, False))
    return result

  def get_item_tech(self, item_key):
    for tech_key in self.__dump['tech']:
      if 'addItems' in self.__dump['tech'][tech_key]:
        for tech_unlock_key in self.__dump['tech'][tech_key]['addItems']:
          if tech_unlock_key == item_key:
            return self.get_tech(tech_key, False)
    return None

  def get_item_prefab(self, item_key):
    for prefab_key in self.__dump['prefab']:
      if prefab_key == item_key:
        return self.__dump['prefab'][prefab_key]
    return {}

  def get_item(self, item_key, with_full_info):
    item = Item(item_key, self.get_icon_url(item_key), self.__dump['item'][item_key])
    if with_full_info and self.has_icon(item_key):
      item.set_recipes(self.get_item_recipes(item_key))
      item.set_used_in(self.get_item_used_in(item_key))
      item.set_tech(self.get_item_tech(item_key))
      item.set_prefab(self.get_item_prefab(item_key))
    return item

  def get_tech_parents(self, tech_key):
    result = []
    if 'preTechs' in self.__dump['tech'][tech_key]:
      for tech_parent_key in self.__dump['tech'][tech_key]['preTechs']:
        result.append(self.get_tech(tech_parent_key, False))
    return result

  def get_tech_unlocks(self, tech_key):
    result = []
    if 'addItems' in self.__dump['tech'][tech_key]:
      for tech_unlock_key in self.__dump['tech'][tech_key]['addItems']:
        result.append(self.get_item(tech_unlock_key, False))
    for item in self.item_list():
      if item.has_pretech() and item.pretech() == self.__dump['tech'][tech_key]['name'] and item not in result:
        result.append(item)
    return result

  def get_tech_resources(self, tech_key):
    result = []
    if 'items' in self.__dump['tech'][tech_key]:
      for tech_resource_key in self.__dump['tech'][tech_key]['items']:
        result.append({'item': self.get_item(tech_resource_key, False), 'count': self.__dump['tech'][tech_key]['items'][tech_resource_key] })
    return result

  def get_tech(self, tech_key, with_full_info):
    tech = Tech(tech_key, self.get_icon_url(tech_key), self.__dump['tech'][tech_key])
    if with_full_info:
      tech.set_parents(self.get_tech_parents(tech_key))
      tech.set_unlocks(self.get_tech_unlocks(tech_key))
      tech.set_resources(self.get_tech_resources(tech_key))
    return tech

  def item_list(self):
    result = []
    for item_key in self.__dump['item']:
      if self.has_icon(item_key):
        result.append(self.get_item(item_key, True))
    return result

  def tech_list(self):
    result = []
    for tech_key in self.__dump['tech']:
      if self.has_icon(tech_key):
        result.append(self.get_tech(tech_key, True))
    return result

  def get_flag(self, flag):
    return self.__data["flags"][flag]
