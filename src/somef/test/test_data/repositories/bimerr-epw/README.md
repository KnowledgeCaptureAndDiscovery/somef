# BIMERR-EPW

- [Ontology](https://bimerr.iot.linkeddata.es/def/weather/)

## BIMERR EPW FILES

In the [epw folder](./Examples/epw) we can see an example of an epw file, which has been transformed into a json file compressed in a [zip file](./Examples/epw/ESP_PV_Bilbao-AP-080250_TMYx-2004-2018.zip) , with which the corresponding [RDF files](./RDF_Examples/epw/ESP_PV_Bilbao-AP-080250_TMYx-2004-2018.zip) have been obtained by means of declarative mappings. These files contain typical meteorological years in a given location and in all months belonging to a year, either in the same year or in different years.

This files come from [Energy Plus Weather](https://www.energyplus.net/weather) site, and [Climate OneBuilding](http://climate.onebuilding.org/).

## BIMERR OPEN-WEATHER-MAP FILES

In the [openweathermap folder](./Examples/openweathermap) we can see an example of a [json file](./Examples/openweathermap/Europe-Madrid(40.4196_-3.692).json), with which the corresponding [RDF files](./RDF_Examples/openweathermap/Europe-Madrid(40.4196_-3.692).ttl) have been obtained by means of declarative mappings.

This files come from [OpenWeatherMap](https://openweathermap.org/) site.

## CODE IMPLEMENTATION

The implementation of the code has been carried out using the [Python language](https://www.python.org/download/releases/3.0/) with the [Django library](https://www.djangoproject.com/), with which a rest service has been created with which all the tasks can be carried out in a simple way. Also, we have used [Helio](https://oeg-upm.github.io/helio/) and [RMLMapper](https://github.com/RMLio/rmlmapper-java) to achieve the transformation of the data by means of mappings to RDF format.

## Authors

- [Salvador González Gerpe (OEG-UPM)](https://github.com/Salva5297)
