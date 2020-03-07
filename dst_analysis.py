import unittest
from datetime import datetime, timedelta
from skyfield import api, almanac
from pytz import timezone
import numpy as np
from geopy.distance import distance
from pprint import pprint


ts = api.load.timescale()
e = api.load('de421.bsp')  # load JPL ephemeris
eastern = timezone('US/Eastern')
rdu = api.Topos('35.8801 N', '78.7880 W')  # use RDU Airport coordinates for calculations
rdu.target = 'RDU'

manteo = api.Topos('35.9082 N', '75.6757 W')  # western NC
manteo.target = 'Dare'

murphy = api.Topos('35.0876 N', '84.0346 W')  # eastern NC
murphy.target = 'Cherokee'



def nearest_minute(dt):
    ''' rounds supplied datetime to the nearest minute '''
    return (dt + timedelta(seconds=30)).replace(second=0, microsecond=0)

def calculate_twilight_times(obs, dt):
    '''
    calcualtes the starting point of each twilight
    :param obs: Skyfield Topos object, coordinates of observer
    :param dt: datetime object to centerl sun almanac data on
    :return:
    '''
    t0 = ts.utc(dt.year, dt.month, dt.day-1)
    t1 = ts.utc(dt.year, dt.month, dt.day+2)
    t, y = almanac.find_discrete(t0, t1, almanac.dark_twilight_day(e, obs))

    data = {}
    for ti, yi in zip(t, y):
        dt = ti.utc_datetime().astimezone(eastern)
        data[nearest_minute(dt)]=almanac.TWILIGHTS[yi]
    return data

def calc_distance(p1, p2):
    '''
    :param p1: Skyfield topographic point
    :param p2: Skyfield topographic point
    :return: distance in miles
    '''
    p1_coords = p1.latitude._degrees, p1.longitude._degrees
    p2_coords = p2.latitude._degrees, p2.longitude._degrees
    d = distance(p1_coords, p2_coords).mi
    return (d)

def get_twilight(twilight_dict, dt1):
    v = np.array(sorted(list(twilight_dict.keys()) + [dt1]))
    index = np.where(v == dt1)[0][0] - 1
    dt0 = v[index]
    dt2 = v[index+2]
    delta_until = dt2 - dt1
    delta_since = dt1 - dt0
    result = twilight_dict[dt0]
    return result, delta_until, delta_since, v[index+2:index+5]


def report():
    first_seen = {}
    d = calc_distance(manteo, murphy)
    print(f"{d:.2f} miles between Murphy and Manteo")

    for d in range(8, 60):
        wakeup = ts.utc(2020, 3, d, 11).utc_datetime().astimezone(eastern)
        if wakeup.hour < 7:
            wakeup = ts.utc(2020, 3, d, 12).utc_datetime().astimezone(eastern)
        if d <= 9:
            print(f"\n{wakeup.strftime('%c')}")
        for loc in [manteo, rdu, murphy]:
            twilight_data = calculate_twilight_times(loc, wakeup)
            tw_str, delta_until, delta_since, next4 = get_twilight(twilight_data, wakeup)
            if d <= 9:
                msg = f"{loc.target:20} {tw_str} since {int(delta_since.seconds / 60)} mins ago,"
                msg += f"for another {int(delta_until.seconds / 60)} mins"
                for i in next4:
                    if twilight_data[i] == 'Day':
                        msg += f", sunrise: {i.strftime('%H:%M')}"
                print(msg)
            if tw_str == 'Day':
                if loc.target not in first_seen.keys():
                    first_seen[loc.target] = wakeup

def report():
    first_seen = {}
    d = calc_distance(manteo, murphy)
    print(f"{d:.2f} miles between Murphy and Manteo")

    for d in range(8, 60):
        wakeup = ts.utc(2020, 3, d, 11).utc_datetime().astimezone(eastern)
        if wakeup.hour < 7:
            wakeup = ts.utc(2020, 3, d, 12).utc_datetime().astimezone(eastern)
        if d <= 9:
            print(f"\n{wakeup.strftime('%c')}")
        for loc in [manteo, rdu, murphy]:
            twilight_data = calculate_twilight_times(loc, wakeup)
            tw_str, delta_until, delta_since, next4 = get_twilight(twilight_data, wakeup)
            if d <= 9:
                msg = f"{loc.target:20} {tw_str} since {int(delta_since.seconds / 60)} mins ago,"
                msg += f"for another {int(delta_until.seconds / 60)} mins"
                for i in next4:
                    if twilight_data[i] == 'Day':
                        msg += f", sunrise: {i.strftime('%H:%M')}"
                print(msg)
            if tw_str == 'Day':
                if loc.target not in first_seen.keys():
                    first_seen[loc.target] = wakeup
    print()
    print("First 7 am sunrise")
    print(f" Dare     {first_seen['Dare']}")
    print(f" RDU      {first_seen['RDU']}")
    print(f" Cherokee {first_seen['Cherokee']}")

class MyTestCase(unittest.TestCase):
    def test_report(self):
        report()

    def test_distance(self):
        pass

if __name__ == '__main__':
    report()
