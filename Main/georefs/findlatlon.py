from pyproj import Proj

# Criar um objeto para transformar projeções
p = Proj(init='epsg:3857') # código da EPSG para a projeção web mercator (g-maps)

# Converter lon/lat para web mercator e o contrário
print(p(-97.740372, 30.282642))
print(p(-10880408.440985134, 3539932.820497298, inverse=True))