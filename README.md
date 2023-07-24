# pathy 🚲

Pathy is a small script that talks with an OTP[^1] instance running localy. With Pathy the user can provide a CSV file with start and end stops coordinates, that OTP will generate bicycle routes between. The goal of Pathy is to quickly and easily generate thousands of routes between equally thousands of start and end stops, and have them exported into a single GeoJSON file.

## CSV File

The CSV file should be in the following format: 

```
lat,lon,lat,lon
lat,lon,lat,lon
[...]
```

[^1]: OTP stands for [OpenTripPlanner](https://www.opentripplanner.org)
