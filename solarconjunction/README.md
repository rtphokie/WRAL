Using Skyfield, creates a daily time series between the given starting year for the given number of years.  
Calculates the right ascention of the Sun and the given body (Mercury by default), compares those right assentions and returns
a count of the minimums (days when the Sun and the body are essentially at the same right ascension, or solar conjunction).

```
732 inferior solar conjunctions between 1920 and 2020
for an average of 7.32 yearly
```

This code was quickly put together to calculate numbers used in a WRAL.com article on the subject of the Nov 11, 2019 Transit of Mercury.  

Handling of leap days has been simplified here.
