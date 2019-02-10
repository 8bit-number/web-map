from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from tqdm import tqdm

geolocator = Nominatim(user_agent="specify_your_app_name_here")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)


def parse_csv(path):
    """
    processes data form .csv file to a python object list()
    :param path: the path to the csv file - (str)
    :param year: entered year - (int)
    :return: processed data - (list)
    """
    with open(path, encoding='utf-8', errors='ignore') as f:
        final = []
        lst = f.readlines()[1:]
        for line in lst:
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


def to_dict(final, year):
    d = {}
    filtered = []
    for each in tqdm(final):
        if year == each[1] and each[2] != 'NO DATA':
            filtered.append(each)
            location = geolocator.geocode(each[2], timeout=10)
            if location:
                d[each[2]] = (location.latitude, location.longitude)
                each.append((location.latitude, location.longitude))

    return d


def to_sorted(final, year):
    filtered = []
    for w in final:
        if year == w[1] and w[2] != 'NO DATA':
            filtered.append(w)
    return filtered
