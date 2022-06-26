# Intro
Zuzzy map is a seminar project. The whole idea behind zuzzy map is to gather data from various social media networs analyze them and try to annotate the map.
The anotation of the map is done by analyzing the description or the tags of a social media post/picture or tweet. 
The analysis is done based on sound baring words ,e.g. train, bird,river etc.
Depending from the word we encounter on the description or the tags of a post we try to assign a certain decibel level to the sound-baring word using fuzzy logic.

## Getting Started

We have seperated our project into three parts.

### Part 1: Fuzzy Engine & Sound analysis

We have `fuzzy_engine.py`, `fuzzy_logic_control.py` and `sound_extractor.py`.
In this scripts we have the following dependecies:
indicoio, skfuzzy, and numpy. You can install them by using the following commands:
```bash
pip install indicoio
pip install skfuzzy
pip install numpy
```
You can test if it works by executing `sound_extractor.py`:
```bash
python sound_extractor.py
```
### Part 2: Gathering the data
We use python and flickrapi to scrape data from flickr
#### flickrapi

The easiest to use, most complete, and most actively developed Python interface to the Flickr API.It includes support for authorized and non-authorized access, uploading and replacing photos, and all Flickr API functions.
To install execute the following command:
```bash
pip install flickrapi
```
#### How to use it?
We have the datascraper which is split into two files located on the `fuzzy` folder. 

The two files: `FlickrSearch.py` and `FlickrScarpper.py`

This two scripts have two different responsibilities and we have to execute them in order.

First we run `FlickrSearch.py` by simply executing the following command `python FlickrSearch.py <MAX_COUNT>`. We have to provide a runtime argument which is a number and we can provide a value starting from 10 to 10 000 if it is higher than 10 000 it will set the value back to 10 000 if it is lower than 10 it will set the value back to 10. The `<MAX_COUNT>` corresponds to number of ids we'll fetch per tag and stores them under the `ids` folder. We generate a file per tag eg. let assume we search for the tag `train` we will output it's ids on `ids/<city>/train.csv`. The tags are loaded from the `sound_dictionary.txt`. This scrapper only grabs the ids that have tags of sound-baring words.

Secondly we run `FlickrScrapper.py` to run this we execute the following command `python FlickrScrapper.py`. Here there are no run-time arguments we have to hard-wire the changes we want to do. This script first accesses the `ids/<city>/` folder grabs a `*.csv` loads it into a list and starts grabing the photo information corresponding to the id, formats them to a prefered dictonary and dumps the info to a json file on `json/<city>.json`. Worth noting that here we also call the fuzzy engine by providing it with the `description` and formated `tags` of a photo.

Finally after all of this has been done running you have manually put the generated json file to the angular project on the assets directory, you can locate that on `mapsy/src/assets`.

Note: The json file needs to be formatted properly you can either do that with your favourite text editor or by writting a small script. To do this you need to remove the empty lists, try finding `[]` and remove it. Next is the following find `][` replaace it with `,`


### Part 3: Rendering the map

Before I start explaining let me first mention resources we use here:
Angular
LeafletJS:        for handling the map
MapBox:           for providing a cool looking map
OpenStreetMap:    that MapBox uses to get the map data
CanvasJS :        for having some cool graphs
and more..

To run the application and install the necessary dependecies you can see the README.md inside `mapsy` directory.

Now that we have the dependencies installed and the project is up and running, you'd like to know how to load your own markers and see them rendered on the map.

You can go the `file.service.ts` that you can find in directory `mapsy/src/app/services`. Either create a new method if it is for a new city or modify the ones by changing the file name.
If you add a new method make sure to include that on `map.component.ts` located in `mapsy/src/app/map`.
