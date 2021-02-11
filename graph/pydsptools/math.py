
def to_units(x_):
  if x_ == 0:
    return 0
  units = {-12: "T",-9: "G",-6: "M",-3: "K",0: "",3: "m",6: "µ",9: "n",12: "p",15: "f"}
  k = -12
  while x_ * 10.0**k < 1:
    k += 3
  return f"{x_*10.0**k:.1f}{units[k]}"
