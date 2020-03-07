import unittest
from skyfield.api import load
from scipy.signal import argrelextrema
import numpy as np

planets = load('de430t.bsp')
earth, sun  = planets['earth'], planets['sun']
ts = load.timescale()

def solar_conjunctions(years=100, start_year=1920, body='mercury'):
    days = round(years*365+(years/4)) # ignoring divisible by 100 rule, close enough

    t = ts.utc(start_year, 1, range(1, days), 12)

    # find the sun's right ascension, daily over the time period
    apparant = earth.at(t).observe(sun).apparent()
    ra_sun, dec, distance_sun = apparant.radec()

    # find mercury's right ascension, daily over the time period
    apparant = earth.at(t).observe(planets[body]).apparent()
    ra_body, dec, distance = apparant.radec()

    # angular separation (in hours), Skyfield is magic
    diff = ra_sun.hours - ra_body.hours

    # find minimums along that curve, each of those is a solar conjunction
    mins = argrelextrema(np.absolute(diff), np.less)[0]

    print (f"{len(mins)} inferior solar conjunctions between {start_year} and {start_year + years}")
    print (f"for an average of {len(mins)/years:.2f} yearly")
    return(len(mins))


class MyTestCase(unittest.TestCase):
    def test_something(self):
        result = solar_conjunctions(years=100, start_year=1920)
        self.assertEqual(result, 732)


if __name__ == '__main__':
    result = solar_conjunctions(years=100, start_year=1920)
