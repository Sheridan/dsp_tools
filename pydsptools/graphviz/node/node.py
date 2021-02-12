from pydsptools.options import options
from pydsptools.graphviz.entity import Entity


class Node(Entity):
  def __init__(self, name, icon, caption, color="background"):
    super().__init__(color)
    self.__name = self.normalize_name(name)
    self.__icon = icon
    self.__caption = caption
    self.__flags = []
    self.__info = []
    self.__recipes = []
    self.__resources = []
    self.__unlocks = []
    self.__used_in = []

  def name(self):
    return self.__name

  def icon(self):
    return self.__icon

  def caption(self):
    return self.__caption

  def append_flag(self, flag):
    self.__flags.append(flag)

  def flags(self):
    return self.__flags

  def append_info(self, info):
    if not info.is_empty():
      self.__info.append(info)

  def info(self):
    return self.__info

  def append_recipe(self, recipe):
    self.__recipes.append(recipe)

  def recipes(self):
    return self.__recipes

  def append_resource(self, resource):
    self.__resources.append(resource)

  def resources(self):
    return self.__resources

  def append_used_in(self, used_in):
    self.__used_in.append(used_in)

  def used_in(self):
    return self.__used_in

  def append_unlock(self, unlock):
    self.__unlocks.append(unlock)

  def unlocks(self):
    return self.__unlocks

  def __compile_used_in(self):
    if len(self.used_in()) == 0:
      return ""
    items = []
    count = 5
    delimiter = self.load_template('main/node_used_in_delimiter.html')
    for used_in in self.used_in():
      count-=1
      items.append(self.load_template('icon_list_item.html').format(
        icon = used_in.resized(options["icons"]['list_icon_size'])
      ))
      if count == 0:
        count = 5
        items.append(delimiter)
    if items[-1] == delimiter:
      items.pop()
    return self.load_template('main/node_used_in_list.html').format(
        used_in_count = len(self.used_in()),
        items_list = "".join(items)
      )

  def __compile_resources(self):
    if len(self.resources()) == 0:
      return ""
    items = []
    for ingridient in self.resources():
      items.append(self.load_template('icon_list_item.html').format(
        icon = ingridient.icon().subscribed(options["icons"]['list_icon_size'], ingridient.count())
      ))
    return self.load_template('main/node_resources_list.html').format(
        items_list = "".join(items),
        resources_count = len(self.resources())
      )

  def __compile_unlocks(self):
    if len(self.unlocks()) == 0:
      return ""
    items = []
    for unlock in self.unlocks():
      items.append(self.load_template('icon_list_item.html').format(
        icon = unlock.resized(options["icons"]['list_icon_size'])
      ))
    return self.load_template('main/node_unlocks_list.html').format(
        items_list = "".join(items),
        unlock_count = len(self.unlocks())
      )

  def __compile_recipes_results(self, recipe):
    items = []
    for ingridient in recipe.results():
      items.append(self.load_template('icon_list_item.html').format(
        icon = ingridient.icon().subscribed(options["icons"]['list_icon_size'], ingridient.count())
      ))
    return self.load_template('icon_list.html').format(
        items_list = "".join(items)
      )

  def __compile_recipes_ingridients(self, recipe):
    items = []
    for ingridient in recipe.ingredients():
      items.append(self.load_template('icon_list_item.html').format(
        icon = ingridient.icon().subscribed(options["icons"]['list_icon_size'], ingridient.count())
      ))
    return self.load_template('icon_list.html').format(
        items_list = "".join(items)
      )

  def __compile_recipes_items(self):
    items = []
    for recipe in self.recipes():
      items.append(self.load_template('main/node_recipe_list_item.html').format(
        assembler_icon = recipe.assembler_icon().resized(options["icons"]['list_icon_size']),
        ingridients = self.__compile_recipes_ingridients(recipe),
        results = self.__compile_recipes_results(recipe),
        time = recipe.time()
      ))
    return "".join(items)

  def __compile_recipes(self):
    if len(self.recipes()) == 0:
      return ""
    return self.load_template('main/node_recipes_list.html').format(
      recipes_count = len(self.recipes()),
      recipes_items = self.__compile_recipes_items()
    )

  def __compile_flags(self):
    items = []
    for flag in self.flags():
      items.append(self.load_template('main/node_flag.html').format(
        flag = options.flag_icon(flag)
      ))
    return "".join(items)

  def __compile_info_items(self):
    items = []
    for info in self.info():
      if info.is_icon():
        items.append(self.load_template('main/node_info_list_item_icon.html').format(
          icon = info.value().resized(options["icons"]['list_icon_size'])
        ))
      else:
        items.append(self.load_template('main/node_info_list_item_text.html').format(
          caption = info.caption(),
          value = info.value()
        ))
    return "".join(items)

  def __compile_info(self):
    if len(self.info()) == 0:
      return ""
    return self.load_template('main/node_info_list.html').format(
      items_list = self.__compile_info_items()
    )

  def __compile_html(self):
    return self.load_template('main/node.html').format(
      caption        = self.caption(),
      info_list      = self.__compile_info(),
      flags_list     = self.__compile_flags(),
      recipes_list   = self.__compile_recipes(),
      unlocks_list   = self.__compile_unlocks(),
      resources_list = self.__compile_resources(),
      used_in_list   = self.__compile_used_in(),
      icon = self.icon().resized(options["icons"]['main_icon_size'])
    )

  def compile(self):
    return self.load_template('main/node.gv').format(
      name = self.name(),
      color = self.color(),
      html = self.__compile_html()
    ) + '\n'
