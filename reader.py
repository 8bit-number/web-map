from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import folium


geolocator = Nominatim(user_agent="specify_your_app_name_here")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)


def get_year():
    """
    gets year from the user
    :(None)
    :return: year - (int)
    """
    print("please, enter the year from 1890-2024.")
    prompt = input()
    while 1:
        if int(prompt) not in range(1890, 2025):
            print("enter valid year.")
            prompt = input()
        else:
            prompt = int(prompt)
            break


    return prompt


def parse_csv(path):
    """
    processes data form .csv file to a python object list()
    :param path: the path to the csv file - (str)
    :param year: entered year - (int)
    :return: processed data - (list)
    """
    with open(path, encoding='utf-8', errors='ignore') as f:
        final = []

        for line in f.readlines()[1:]:
            tempo = []
            line = line.replace("\"", "")
            line = line.split(',')
            line = [i.strip() for i in line]
            tempo.append(line[0])
            try:
                tempo.append(int(line[1][0:4]))
            except ValueError:
                pass

            tempo.append(line[-1])
            final.append(tempo)
    return final

path = "locations1.csv"

def to_dict(final, year):
    d = {}
    filtered = []
    for each in final:
        if year == each[1] and each[2] != 'NO DATA':
                filtered.append(each)
                location = geolocator.geocode(each[2], timeout=10)
                if location:
                    d[each[2]] = (location.latitude, location.longitude)
                    each.append((location.latitude, location.longitude))

    return d

final = parse_csv(path)
year = get_year()



def to_sorted(final, year):
    filtered = []
    for w in final:
        if year == w[1] and w[2] != 'NO DATA':
            filtered.append(w)
    return filtered
# print(to_dict(parse_csv("locations1.csv"), get_year()))


def get_user_location():

    usr_loc = input("enter your city: ")
    location = geolocator.geocode(usr_loc, timeout=10)
    while 1:
        if location:
            break
        else:
            print("enter a valid city name: ")
            usr_loc = input("enter your city: ")
            location = geolocator.geocode(usr_loc, timeout=10)

    # return location
    # locations = to_dict(parse_csv("locations1.csv"), get_year())[0]


    return locations

locations = parse_csv(path)

# print(get_user_location(to_dict(parse_csv("locations1.csv"), get_year()))[1])


def color_creator(dictionary):
    for k in dictionary:
        if len(dictionary[k]) < 1000:
            return "green"
        elif 2000 <= len(dictionary[k]) <= 3500:
            return "yellow"
        else:
            return "red"
# usr_loc = get_user_location(locations)[0]


def map_creator(usr_loc, mov_locations, filtered, year):


    lat = [i[0] for i in list(mov_locations.values())]
    lon = [i[1] for i in list(mov_locations.values())]

    usr_latt = usr_loc.latitude
    usr_long = usr_loc.longitude

    map = folium.Map(location=[usr_latt, usr_long],
                     zoom_start=5)

    folium.Marker([usr_latt, usr_long], popup='you are here!',
                  icon=folium.Icon(color='yellow')).add_to(map)

    mov_density = folium.FeatureGroup(name="movies density")

    for lt, ln, ch in zip(lat, lon, filtered):
        mov_density.add_child(folium.CircleMarker(location=[lt, ln],
                                            radius=10,
                                            popup=ch[0],
                                            fill_color=color_creator(to_dict(parse_csv("locations1.csv"), get_year())[0]),
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
                                 style_function=lambda x: {'fillColor':'green'
        if x['properties']['POP2005'] < 10000000
        else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
        else 'purple'}))

    legend_html =   '''
                    <div style="position: fixed;
                                bottom: 50px; left: 50px; width: 100px; height: 90px;
                                border:2px solid grey; z-index:9999; font-size:14px; background:white;
                                ">&nbsp; Cool Legend <br>
                                  &nbsp; East &nbsp; <i class="fa fa-circle fa-2x" style="color:green"></i><br>
                                  &nbsp; West &nbsp; <i class="fa fa-circle fa-2x" style="color:red"></i>
                    </div>
                    '''

    map.add_child(mov_density)
    map.add_child(movies_loc)
    map.add_child(population)
    map.get_root().html.add_child(folium.Element(legend_html))

    map.add_child(folium.LayerControl())

    map.save('First.html')

#
# map_creator(get_user_location(to_dict(parse_csv("locations1.csv"), get_year()))[0],
#                  get_user_location(to_dict(parse_csv("locations1.csv"), get_year()))[1],
#                   get_user_location(to_dict(parse_csv("locations1.csv"), get_year()))[2],
#                   to_sorted(parse_csv("locations1.csv"), get_year()),
#                   get_year())

