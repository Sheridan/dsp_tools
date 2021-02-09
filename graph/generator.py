#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
import os.path
import sys
import re
from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color

main_icon_size = 128
list_icon_size = 48

class CIcon:
  def __init__(self, key, url):
    self.__url = url
    self.__key = key
    self.download()

  def __gen_filename(self, size = 0):
    return 'icons/{0}.png'.format(self.__key) if size == 0 else 'icons/{0}_{1}.png'.format(self.__key, size)

  def download(self):
    if not os.path.isfile(self.__gen_filename()):
      print("Downloading icon for {0} ({1})".format(self.__key, self.__url))
      with open(self.__gen_filename(), 'wb') as icon_file:
        response = requests.get(self.__url, stream=True)
        if not response.ok:
            print(response)
        for block in response.iter_content(1024):
            if not block:
                break
            icon_file.write(block)

  def filename(self, size):
    if not os.path.isfile(self.__gen_filename(size)):
      print("Resizing icon for {0} to {1}".format(self.__key, size))
      with Image(filename=self.__gen_filename()) as img:
        img.transform(resize='{0}x{0}'.format(size))
        img.save(filename=self.__gen_filename(size))
    return self.__gen_filename(size)

  def subscribed(self, size, text):
    filename = 'icons/{0}_{1}_{2}.png'.format(self.__key, size, text)
    if not os.path.isfile(filename):
      print("Subscribing icon {0} ({1}) with {2}".format(self.__key, size, text))
      with Drawing() as draw:
        with Image(filename=self.filename(size)) as img:
          draw.font_family = 'Roboto'
          draw.font_weight = 800
          draw.font_size = 24
          draw.fill_color = Color('#36ffd0')
          draw.stroke_color = Color('#09002b')
          draw.stroke_width = 1
          draw.stroke_antialias = True
          draw.text(4, int(img.height - 8), '{0}'.format(text))
          draw(img)
          img.save(filename = filename)
    return filename

class CItem:
  def __init__(self, key, icon_url, data):
    self.__key = key
    self.__data = data
    self.__icon = CIcon(self.__key, icon_url)
    self.__recipes = []
    self.__used_in = []
    self.__tech = None
    self.__prefab = {}

  def __eq__(self, other):
    return self.__key == other.key()

  def node_name(self):
    return '{0}_{1}'.format(self.key(), self.name())

  def key(self):
    return self.__key

  def icon(self):
    return self.__icon

  def name(self):
    return self.__data["name"]

  def type(self):
    return self.__data["type"]

  def set_prefab(self, prefab):
    self.__prefab = prefab

  def prefab(self):
    return self.__prefab

  def has_pretech(self):
    return 'preTech' in self.__data

  def pretech(self):
    return self.__data['preTech']

  def set_tech(self, tech):
    self.__tech = tech

  def tech(self):
    return self.__tech

  def has_tech(self):
    return self.__tech != None

  def set_recipes(self, recipes):
    self.__recipes = recipes

  def set_used_in(self, used_in):
    self.__used_in = used_in

  def recipes(self):
    return self.__recipes

  def stack_size(self):
    return self.__data["stackSize"]

  def used_in(self):
    return self.__used_in

  def flags(self):
    flags = []
    for key in ["canBuild", "isFluid", "heatValue"]:
      if key in self.__data and self.__data[key]:
        flags.append(key)
    for key in ["Logistics", "Natural resource", "Power storage", "Power transmission", "Power facility", "End product"]:
      if self.type() == key:
        flags.append(key)
    if "miningFrom" in self.__data:
      flags.append("Natural resource")
    for key in ["hasAudio", "isPowerConsumer", "isAssembler", "isStorage", "isTank", "isSplitter", "minerPeriod"]:
      if key in self.__prefab and self.__prefab[key]:
        flags.append(key)
    for recipe in self.recipes():
      flags += recipe.flags()
    return set(flags)


class CRecipe:
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

class CTech:
  def __init__(self, key, icon_url, data):
    self.__key = key
    self.__data = data
    self.__icon = CIcon(self.__key, icon_url)
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

class CData:
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
            recipe = CRecipe(recipe_key, recipe_data)
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
    item = CItem(item_key, self.get_icon_url(item_key), self.__dump['item'][item_key])
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
    tech = CTech(tech_key, self.get_icon_url(tech_key), self.__dump['tech'][tech_key])
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

class CGraphviz:
  def __init__(self, name):
    self.__name = name
    self.__legend_cache = {}
    print("Generating graph {0}".format(self.__name))
    self.__graph = open('result/graph_{0}.gv'.format(self.__name), "w")
    self.__legend = open('result/legend_{0}.gv'.format(self.__name), "w")
    with open('options.json') as json_file:
      self.__options = json.load(json_file)
    self.__graph.write('digraph g {\n')
    self.__legend.write('digraph g {\n')
    self.__generate_graph_options()
    self.__generate_legend_options()
    self.__graph.write('  subgraph cluster_0 {{ label="Legend"; legend [image="result/legend_{1}.{0}" label="" shape="none"]; }}\n'.format(sys.argv[1], self.__name))

  def __del__(self):
    self.__graph.write('}\n')
    self.__graph.close()
    self.__legend.write('}\n')
    self.__legend.close()

  def __normalize_name(self, name):
    return re.sub('[^0-9a-z]+', '_', name.lower())

  def __get_color(self, color_name):
    if color_name in self.__options['colors']:
      return self.__options['colors'][color_name]
    print('Need to add color {0}'.format(color_name))
    return self.__options['colors']['background']

  def __generate_graph_options(self):
    for group in self.__options['graphviz']['default']:
      self.__graph.write('  {0} ['.format(group))
      for option_key in self.__options['graphviz']['default'][group]:
        option_value = self.__options['graphviz']['default'][group][option_key]
        if self.__name in self.__options['graphviz'] and group in self.__options['graphviz'][self.__name] and option_key in self.__options['graphviz'][self.__name][group]:
          option_value = self.__options['graphviz'][self.__name][group][option_key]
        if 'color' in option_key:
          option_value = self.__get_color(option_value)
        self.__graph.write(' {0}="{1}" '.format(option_key, option_value))
      self.__graph.write('];\n')

  def __generate_legend_options(self):
    for group in self.__options['graphviz']['default']:
      self.__legend.write('  {0} ['.format(group))
      for option_key in self.__options['graphviz']['default'][group]:
        option_value = self.__options['graphviz']['default'][group][option_key]
        if 'legend' in self.__options['graphviz'] and group in self.__options['graphviz']['legend'] and option_key in self.__options['graphviz']['legend'][group]:
          option_value = self.__options['graphviz']['legend'][group][option_key]
        if 'color' in option_key:
          option_value = self.__get_color(option_value)
        self.__legend.write(' {0}="{1}" '.format(option_key, option_value))
      self.__legend.write('];\n')

  def append_entity_node(self, name, label, color):
    self.__graph.write('  {0} [label=<{1}> fillcolor="{2}"];\n'.format(self.__normalize_name(name), " ".join(label.split()), self.__get_color(color)))

  def append_entity_edge(self, name_from, name_to, color):
     self.__graph.write('  {0} -> {1} [color="{2}"];\n'.format(self.__normalize_name(name_from), self.__normalize_name(name_to), self.__get_color(color)))

  def __append_legend_point_node(self, name):
    self.__legend.write('  {0} [label="" shape="point" fillcolor="{1}" color="{1}"];\n'.format(self.__normalize_name(name), self.__get_color("background")))

  def __append_legend_node(self, name, label, color):
    self.__legend.write('  {0} [label="{1}" fillcolor="{2}"];\n'.format(self.__normalize_name(name), label, self.__get_color(color)))

  def __append_legend_edge(self, type, name, color):
     self.__legend.write('  {0} -> {1} [color="{2}"];\n'.format(self.__normalize_name(type), self.__normalize_name(name), self.__get_color(color)))

  def __append_legend_type(self, type):
    if type not in self.__legend_cache:
      self.__legend_cache[type] = []
      self.__append_legend_node(self.__normalize_name(type), type, "background")

  def append_legend_node(self, type, color):
    self.__append_legend_type(type)
    if color not in self.__legend_cache[type]:
      self.__legend_cache[type].append(color)
      self.__append_legend_node(color, color, color)
      self.__append_legend_edge(type, color, "font")

  def append_legend_flag_node(self, flag_name, flag_icon):
    type = "Flags"
    self.__append_legend_type(type)
    if flag_name not in self.__legend_cache[type]:
      self.__legend_cache[type].append(flag_name)
      self.__append_legend_node('flag_{0}'.format(flag_name), '{0}\n{1}'.format(flag_icon, flag_name), "background")
      self.__append_legend_edge(type, 'flag_{0}'.format(flag_name), "font")

  def append_legend_edge(self, type, color):
    self.__append_legend_type(type)
    if color not in self.__legend_cache[type]:
      self.__legend_cache[type].append(color)
      self.__append_legend_node('a_{}'.format(color), color, color)
      self.__append_legend_edge(type, 'a_{}'.format(color), "font")
      self.__append_legend_point_node('b_{}'.format(color))
      self.__append_legend_edge('a_{}'.format(color), 'b_{}'.format(color), color)

class CGenerator:
  def __init__(self, graph_list):
    self.__graph_list = graph_list
    self.__name = '_'.join(self.__graph_list)
    self.__data = CData()
    self.__graph = CGraphviz(self.__name)

  def __load_template(self, name):
    with open('templates/{0}.html'.format(name), 'r') as file:
      return file.read().replace('\n', '')

  def __generate_items_nodes(self):
    print("Generating items nodes")
    for item in self.__data.item_list():
      recipes_list = []
      for recipe in item.recipes():
        recipe_icons = []
        for src_item in recipe.sources():
          recipe_icons.append(
            self.__load_template('icon_list_item').format(
              icon = src_item['item'].icon().subscribed(list_icon_size, src_item['count'])
            )
          )
        recipes_list.append(
          self.__load_template('item_recipe').format(
            recipe = self.__load_template('icon_list').format(
              icon_list = " ".join(recipe_icons)
            ),
            time = recipe.time(),
            assembler_icon = recipe.assembler().icon().filename(list_icon_size)
          )
        )
      self.__graph.append_entity_node(
          item.node_name(),
          self.__load_template('item_node').format(
            label = item.name(),
            icon = item.icon().filename(main_icon_size),
            stack_size = item.stack_size(),
            flags = " ".join(list(map(lambda flag: self.__data.get_flag(flag)['icon'] , item.flags()))),
            used_in_count = len(item.used_in()),
            recipes_count = len(item.recipes()),
            tech_icon = self.__load_template('item_tech_icon').format(
                tech_icon = item.tech().icon().filename(list_icon_size)
              ) if item.has_tech() else " ",
            recipes = " ".join(recipes_list)
          ),
          item.type()
        )
      for flag in item.flags():
        self.__graph.append_legend_flag_node(self.__data.get_flag(flag)['name'], self.__data.get_flag(flag)['icon'])
      self.__graph.append_legend_node("Item and buildings types", item.type())

  def __generate_items_edges(self):
    print("Generating items edges")
    for item_to in self.__data.item_list():
      for recipe in item_to.recipes():
        for item_from in recipe.sources():
          self.__graph.append_entity_edge(item_from['item'].node_name(), item_to.node_name(), recipe.type())
          self.__graph.append_legend_edge("Relations", recipe.type())

  def __generate_tech_nodes(self):
    print("Generating tech nodes")
    for tech in self.__data.tech_list():
      self.__graph.append_entity_node(
          tech.node_name(),
          self.__load_template('tech_node').format(
            label = tech.name(),
            icon = tech.icon().filename(main_icon_size),
            haches = tech.haches(),
            unlocks = self.__load_template('icon_list').format(
              icon_list = " ".join(list(map(lambda item: self.__load_template('icon_list_item').format(
                icon = item.icon().filename(list_icon_size)
              ), tech.unlocks())))
            ) if len(tech.unlocks()) > 0 else " ",
            resources = self.__load_template('icon_list').format(
              icon_list = " ".join(list(map(lambda item: self.__load_template('icon_list_item').format(
                icon = item['item'].icon().subscribed(list_icon_size, item['count'])
              ), tech.resources())))
            ) if len(tech.resources()) > 0 else " "
          ),
          "Technology"
        )
      self.__graph.append_legend_node("Item and buildings types", "Technology")

  def __generate_tech_edges(self):
    print("Generating tech edges")
    for tech_to in self.__data.tech_list():
      for tech_from in tech_to.parents():
        self.__graph.append_entity_edge(tech_from.node_name(), tech_to.node_name(), "Technology relation")
    self.__graph.append_legend_edge("Relations", "Technology relation")

  def __generate_tech_items_edges(self):
    print("Generating tech <-> items edges")
    for tech in self.__data.tech_list():
        for unlock in tech.unlocks():
          self.__graph.append_entity_edge(tech.node_name(), unlock.node_name(), "Unlock")
        self.__graph.append_legend_edge("Relations", "Unlock")
        for resource in tech.resources():
          self.__graph.append_entity_edge(resource['item'].node_name(), tech.node_name(), "Research resource")
        self.__graph.append_legend_edge("Relations", "Research resource")

  def main(self):
    if "items" in self.__graph_list:
      self.__generate_items_nodes()
      self.__generate_items_edges()
    if "tech" in self.__graph_list:
      self.__generate_tech_nodes()
      self.__generate_tech_edges()
    if "items" in self.__graph_list and "tech" in self.__graph_list:
      self.__generate_tech_items_edges()


for graphs in [["items"], ["tech"], ["tech", "items"]]:
  CGenerator(graphs).main()
