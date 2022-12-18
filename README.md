# Accelerating Energy Transition
Our submission to the Mercuria Hackathon 22. The main headline of this hackathon was to find solutions for reducing carbon emissions of vessels by optimising cargo-loading and routing logistics. We utilised AIS (Automatic Identification System) data to complete this task.

## Our Solution
Given the identifier of a vessel (IMO), our solution creates estimated automated reports on travelled distance, average velocity, consumed fuel and GHG emissions. This allows for comparison with manually created reports (Noon reports) and therefore potential correction of previous estimates.


```
=========================== Automated Report ===========================
Voyage dates:                   2022-08-01 to 2022-08-30
Total distance travelled (km):  13046.77
Avg velocity (km/h):            19.13
Avg fuel consump. (tonnes/day): 262.39
GHG emissions (kg/day):         817.08
```

Another output of our solution is an automatically created GeoJSON file which visualises the vessel route.

![](./geojson.png)

## Important Links
* Introduction Presentation - [here](./intro-presentation/Mercuria-Hackathon-on-the-day-presentation.pdf)
* API Service - https://api.hackathon.mercuria-apps.com/api/
* Dashboard Service - https://grafana.hackathon.mercuria-apps.com
