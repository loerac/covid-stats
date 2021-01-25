# COVID-19 Stats
Display COVID-19 cases from United States. This is a simple and dirty COVID-19 call to get the current COVID-19 cases in a state.

## covid-tracking
It creates a table under the database name "covid", with values from the [covidtracking](https://covidtracking.com/data/api) website. At the start, it'll add the historical COVID-19 data to the table. Afterwords, it'll daily get and update the table with COVID-19 cases.

## covid-graph
Command line tool to get the data from the database. It'l show the state's COVID-19 case:
* Positive cases
* Negative cases
* Deaths
* and more

### Commands for covid-graph
* `-r` or `--region`:
  * Region from United States of America. The regions are located in [regions.py](regions.py) file.
* `-s` or `--save`:
  * Save the graph image. The image will be saved under the states name i.e. California.png.
* `-g` or `--graph`:
  * Display the graph image but not save it.
* `-stat` or `--statistics`:
  * Display daily increase on COVID-19 cases.
