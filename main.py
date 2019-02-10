import folium
from get_info import get_year, get_user_location
from parser import to_dict, to_sorted, parse_csv


def color_creator(places, key):
    """
    according to the number of movies filmed in certain places,
    returns corresponding color
    :param places - (dict)
    :param key - (str)
    """
    if len(places[key]) < 1000:
        return "green"
    elif 2000 <= len(places[key]) <= 3500:
        return "yellow"
    return "red"


def map_creator(usr_loc, mov_locations, filtered, year):
    """
    creates an html map
    :param usr_loc - (str)
    :param mov_locations - (dict)
    :param filtered - (list)
    :param year - (int)
    """
    lat = [i[0] for i in list(mov_locations.values())]
    lon = [i[1] for i in list(mov_locations.values())]

    usr_latt = usr_loc.latitude
    usr_long = usr_loc.longitude

    map = folium.Map(location=[usr_latt, usr_long],
                     zoom_start=5)

    folium.Marker([usr_latt, usr_long], popup='you are here!',
                  icon=folium.Icon(color='yellow')).add_to(map)

    mov_density = folium.FeatureGroup(name="movies density")

    for lt, ln, ch, key in zip(lat, lon, filtered, places):
        mov_density.add_child(folium.CircleMarker(location=[lt, ln],
                                                  radius=10,
                                                  popup=ch[0],
                                                  fill_color=color_creator(
                                                      places, key),
                                                  color='red',
                                                  fill_opacity=0.5))

    movies_loc = folium.FeatureGroup(name='all movies for %d year' % year)
    for lt, ln, mov in zip(lat, lon, filtered):
        movies_loc.add_child(folium.Marker(location=[lt, ln],
                                           popup=mov[0],
                                           icon=folium.Icon()))

    population = folium.FeatureGroup(name='population')
    population.add_child(folium.GeoJson(data=open('world.json', 'r',
                                                  encoding='utf-8-sig').read(),
                                        style_function=lambda x: {
                                            'fillColor': 'green'
                                            if x['properties'][
                                                   'POP2005'] < 10000000
                                            else 'orange' if 10000000 <=
                                                             x['properties'][
                                                                 'POP2005'] < 20000000
                                            else 'purple'}))

    legend_html = '''
<div style="position: fixed;
            bottom: 50px; left: 50px;
            border:2px solid grey; z-index:9999; font-size:14px; background:white;
            ">&nbsp; The Population Markers <br>
              &nbsp; < 10.000.000  &nbsp; <i class="fa fa-circle fa-2x" style="color:green"></i><br>
              &nbsp; < 20.000.000  &nbsp; <i class="fa fa-circle fa-2x" style="color:purple"></i><br>
              &nbsp; > 10.000.000  &nbsp; <i class="fa fa-circle fa-2x" style="color:orange"></i>
</div>
'''

    map.add_child(mov_density)
    map.add_child(movies_loc)
    map.add_child(population)
    map.get_root().html.add_child(folium.Element(legend_html))

    map.add_child(folium.LayerControl())

    map.save('{}.html'.format(year))


if __name__ == "__main__":
    year = get_year()
    locations = parse_csv("locations.csv")
    places = to_dict(locations, year)
    usr_loc = get_user_location()
    mov_locations = to_dict(locations, year)
    filtered = to_sorted(locations, year)
    map_creator(usr_loc, mov_locations, filtered, year)
