from pydsptools.dsp.icon import Icon

class Item:
  def __init__(self, key, icon_url, data):
    self.__key = key
    self.__data = data
    self.__icon = Icon(self.__key, icon_url)
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

  def __get_data(self, key):
    if key in self.__data:
      return self.__data[key]
    elif key in self.__prefab:
      return self.__prefab[key]
    return 0

  def stack_size(self):
    return self.__get_data("stackSize")

  def fluid_storage_volume(self):
    return self.__get_data('fluidStorageCount')

  def storage_cells(self):
    return self.__get_data('storageCol')*self.__get_data('storageRow')

  def power_connect_distance(self):
    return self.__get_data('powerConnectDistance')

  def power_cover_radius(self):
    return self.__get_data('powerCoverRadius')

  def assembler_speed(self):
    return self.__get_data('assemblerSpeed')

  def work_energy_per_tick(self):
    return self.__get_data('workEnergyPerTick')*60

  def idle_energy_per_tick(self):
    return self.__get_data('idleEnergyPerTick')*60

  def gen_energy_per_tick(self):
    return self.__get_data('genEnergyPerTick')*60

  def station_can_accumulate(self):
    return self.__get_data('stationMaxEnergyAcc')

  def use_fuel_per_tick(self):
    return self.__get_data('useFuelPerTick')*60

  def heat_value(self):
    return self.__get_data('heatValue')

  def station_max_drones(self):
    return self.__get_data('stationMaxDroneCount')

  def station_max_ships(self):
    return self.__get_data('stationMaxShipCount')

  def station_max_items(self):
    return self.__get_data('stationMaxItemCount')

  def station_max_item_types(self):
    return self.__get_data('stationMaxItemKinds')

  def belt_speed(self):
    return self.__get_data('beltSpeed')*6
