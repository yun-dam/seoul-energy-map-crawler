# seoul-energy-map-crawler


### Web-crawling energy consumption data and greenhouse gas emissions data of each energy source (electricity, natural gas, and district heating) by the administrative districts in Seoul from https://energyinfo.seoul.go.kr/


#### *class* seoulEnergyMap(outcomeType='energy', sourceType='electricity', guList = ['Gangnam'], howManyPreviousYears = 3, howManyMonths = 12)

#### **Parameters**:

outcomeType : 'energy' or 'greenhouse_gas'

sourceType : 'electricity', 'natural_gas', or 'district_heat'

guList : List of the districts ('Gu') where you want to check the data down to the neighborhood ('Dong') level 

(at this moment, it works only for 'Gangnam-Gu')

howManyPreviousYears : the range of years, starting from this year, for which I want to check the data.

#### **Methods**: 
dataCrawling() : Return district-level data and neighborhood-level data separately in the json format

#### **Examples**:

```python

from seoulEnergyMap import seoulEnergyMap
energyMap = seoulEnergyMap(outcomeType = 'energy', sourceType = 'electricity', guList = ['Gangnam'] , howManyPreviousYears = 3, howManyMonths = 12)
energyMap.dataCrawling()

```

