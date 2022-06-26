from flickrapi import FlickrAPI
import json
from sound_extractor import analyse_text
import pandas as pd
from os import listdir
from os.path import isfile, join
from fuzzy_engine import read_sound_dictionary, setup_fuzzy_engine, predict_sound_level
key='4a685580226691fc65b83525ddf3370d'
secret='e0dede9873b678e7'
flickr = FlickrAPI(key,secret)



def readIds(max_count,filename):
    with open(filename) as f:
            if max_count == -1:
                photo_ids = f.read().splitlines()
            else:
                photo_ids = f.read().splitlines()[: max_count]
    return photo_ids
def getPhotoDet(ids):
    photos_det = []
    index = 0
    for id in ids:
        index += 1
        print(index )
        print(" out of ")
        print(len(ids))
        try:
            photos_det.append(flickr.photos.getInfo(photo_id = id,format = 'json'))
        except:
            print("Details for image number {} could not be fetched".format(id))

    return photos_det
def loadJson(photos_det):
    photos = []
    for photo in photos_det:
        photo = "[" + photo +"]"
        photos.append(json.loads(photo))
    return (photos)
def proccessJson(photos):
    desc = []
    for photo in photos:
        try:
            short_desc = {}
            tags = photo[0]['photo']['tags']['tag']
            tagToString = ""
            for t in tags:
                tagToString += " " + t['_content']
            short_desc.update({'photo_id': photo[0]['photo']['id']})
            short_desc.update({ 'description': photo[0]['photo']['description']['_content']})
            short_desc.update({'tags': tagToString})
            short_desc.update({'properties': analyse_text(photo[0]['photo']['description']['_content'] + tagToString)})
            short_desc.update({'longitude': photo[0]['photo']['location']['longitude']})
            short_desc.update({'latitude': photo[0]['photo']['location']['latitude']})
            short_desc.update({'url': photo[0]['photo']['urls']['url']})
            # print(short_desc)
            desc.append(short_desc)
        except:
            print("something went wrong while trying to fuzzy")
    return desc

def main():
    mypath = './ids/zurich'
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    setup_fuzzy_engine()
    index = 0
    with open('json/zurich4.json','w') as f:
        for filepath in onlyfiles:
            index +=1
            a = len(onlyfiles) - index
            print("reading from: " + filepath + ". Left ")
            print(a)
            photo_json = proccessJson(loadJson(getPhotoDet(readIds(-1,'ids/zurich/' + filepath)))) # -1 for reading all
            x = json.dumps(photo_json)
            f.write(x)
    
    # print(type(x))
    # print(x)
if __name__=='__main__':
    main()
