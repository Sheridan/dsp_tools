from math import ceil
from pydsptools.dsp.data import dsp_data
from pydsptools.graphviz.graph import Graph
from pydsptools.graphviz.node.node import Node
from pydsptools.graphviz.node.nodeinfo import NodeTextInfo, NodeIconInfo
from pydsptools.graphviz.node.noderecipe import NodeRecipe, NodeRecipeAssembler, NodeRecipeAssemblerBelt
from pydsptools.graphviz.node.noderecipeingredient import NodeRecipeIngredient
from pydsptools.graphviz.edge.edge import Edge
from pydsptools.graphviz.legend import Legend
from pydsptools.options import options
from pydsptools.math import to_units, string_similarity

class Graphviz:
  def __init__(self, graph_list):
    self.__graph_list = graph_list
    self.__name = '_'.join(self.__graph_list)
    self.__graph = Graph(self.__name)
    self.__legend = Legend(self.__name)

  def __generate_items_nodes(self):
    print("Generating items nodes")
    for item in dsp_data.item_list():
      node = Node(item.node_name(), item.type(), item.icon(), item.name(), item.type())
      self.__legend.append_node_color(item.type(), item.type())
      for flag in item.flags():
        node.append_flag(flag)
        self.__legend.append_node_flag(options['flags'][flag]['icon'], options['flags'][flag]['name'])
      node.append_info(NodeTextInfo("Stack size", item.stack_size()))
      node.append_info(NodeTextInfo("Volume", item.fluid_storage_volume()))
      node.append_info(NodeTextInfo("Cells", item.storage_cells()))
      node.append_info(NodeTextInfo("Power connect", item.power_connect_distance(), "m"))
      node.append_info(NodeTextInfo("Power radius", item.power_cover_radius(), "m"))
      node.append_info(NodeTextInfo("Assembler speed", int(item.assembler_speed()*100), '%'))
      node.append_info(NodeTextInfo("Work consumption", to_units(item.work_energy_per_tick()), 'w'))
      node.append_info(NodeTextInfo("Idle consumption", to_units(item.idle_energy_per_tick()), 'w'))
      node.append_info(NodeTextInfo("Generate energy", to_units(item.gen_energy_per_tick()), 'w'))
      node.append_info(NodeTextInfo("Can accumulate", to_units(item.station_can_accumulate()), 'j'))
      node.append_info(NodeTextInfo("Fuel consume", to_units(item.use_fuel_per_tick()), 'w'))
      node.append_info(NodeTextInfo("Energy", to_units(item.heat_value()), 'j'))
      node.append_info(NodeTextInfo("Max drones", item.station_max_drones()))
      node.append_info(NodeTextInfo("Max ships", item.station_max_ships()))
      node.append_info(NodeTextInfo("Max items", item.station_max_items()))
      node.append_info(NodeTextInfo("Item types", item.station_max_item_types()))
      node.append_info(NodeTextInfo("Belt speed", item.belt_speed(), 'i/s'))
      if item.has_tech():
        node.append_info(NodeIconInfo(item.tech().icon()))
      for used_in in item.used_in():
        node.append_used_in(used_in.icon())
      for recipe in item.recipes():
        node_recipe = NodeRecipe()
        for assembler in recipe.assemblers():
          belts = []
          if assembler.key() != 'orbital-collector':
            for belt in [dsp_data.get_item('belt-1'), dsp_data.get_item('belt-2'), dsp_data.get_item('belt-3')]:
              belts.append(NodeRecipeAssemblerBelt(belt.icon(), int(ceil(belt.belt_speed()/recipe.item_result(item.key())['count']/assembler.assembler_speed()*recipe.time())) ))
          node_recipe.append_assembler(NodeRecipeAssembler(assembler.icon(), recipe.time()/assembler.assembler_speed(), belts))
        for src_item in recipe.sources():
          node_recipe.append_ingredient(NodeRecipeIngredient(src_item['item'].icon(), src_item['count']))
        for result_item in recipe.results():
          node_recipe.append_result(NodeRecipeIngredient(result_item['item'].icon(), result_item['count']))
        node.append_recipe(node_recipe)
      self.__graph.append_node(node)

  def __generate_items_edges(self):
    print("Generating items edges")
    for item_to in dsp_data.item_list():
      for recipe in item_to.recipes():
        for item_from in recipe.sources():
          weight = options.weight(recipe.type())
          if string_similarity(item_from['item'].key(), item_to.key()) >= 0.7:
            weight = weight * weight
          if item_from['item'].type() == item_to.type():
            weight = weight * weight
          print("Weight: {0} -> {1} == {2}".format(item_from['item'].key(), item_to.key(), weight))
          edge = Edge(item_from['item'].node_name(), item_to.node_name(), recipe.type(), weight)
          self.__legend.append_edge_color(recipe.type(), recipe.type())
          self.__graph.append_edge(edge)

  def __generate_tech_nodes(self):
    print("Generating tech nodes")
    self.__legend.append_node_color("Technology", "Technology")
    for tech in dsp_data.tech_list():
      node = Node(tech.node_name(), "tech", tech.icon(), tech.name(), "Technology")
      node.append_info(NodeTextInfo("Hashes", to_units(tech.haches())))
      for resource in tech.resources():
        node.append_resource(NodeRecipeIngredient(resource['item'].icon(), resource['count']))
      for unlock in tech.unlocks():
        node.append_unlock(unlock.icon())
      for flag in tech.flags():
        node.append_flag(flag)
        self.__legend.append_node_flag(options['flags'][flag]['icon'], options['flags'][flag]['name'])
      # for used_in in tech.parents():
      #   node.append_used_in(used_in.icon())
      self.__graph.append_node(node)

  def __generate_tech_edges(self):
    print("Generating tech edges")
    self.__legend.append_edge_color("Technology relation", "Technology relation")
    for tech_to in dsp_data.tech_list():
      for tech_from in tech_to.parents():
        edge = Edge(tech_from.node_name(), tech_to.node_name(), "Technology relation", options.weight("Technology relation"))
        self.__graph.append_edge(edge)

  def __generate_tech_items_edges(self):
    print("Generating tech <-> items edges")
    self.__legend.append_edge_color("Unlock", "Unlock")
    self.__legend.append_edge_color("Research resource", "Research resource")
    for tech in dsp_data.tech_list():
      for unlock in tech.unlocks():
        edge = Edge(tech.node_name(), unlock.node_name(), "Unlock", options.weight("Unlock"))
        self.__graph.append_edge(edge)
      for resource in tech.resources():
        edge = Edge(resource['item'].node_name(), tech.node_name(), "Research resource", options.weight("Research resource"))
        self.__graph.append_edge(edge)

  def main(self):
    if "items" in self.__graph_list:
      self.__generate_items_nodes()
      self.__generate_items_edges()
    if "tech" in self.__graph_list:
      self.__generate_tech_nodes()
      self.__generate_tech_edges()
    if "items" in self.__graph_list and "tech" in self.__graph_list:
      self.__generate_tech_items_edges()
    self.__graph.compile()
