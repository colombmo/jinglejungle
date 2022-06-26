from flickrapi import FlickrAPI
import pandas as pd
import sys
import json
import datetime as date
key='4a685580226691fc65b83525ddf3370d'
secret='e0dede9873b678e7'

'''
LONDON:
    lat = 51.5072466571743, 
    lon = -0.12824806049256623,
BERN:
    lat= 46.947640,
    lon = 7.447160,

ZURICH:
    lat = 47.376048, 
    lon = 8.542035,
'''
def get_urls(image_tag,MAX_COUNT):
    flickr = FlickrAPI(key, secret)
    try:
        photos = flickr.walk(text=image_tag,
                                tag_mode='all',
                                tags=image_tag,
                                is_public = 1,
                                has_geo = 1,
                                geo_context = 0, 
                                lat = 47.376048, 
                                lon = 8.542035,
                                radius= 5,
                                extras='description, owner_name, url_o, views',
                                per_page=500,
                                sort='relevance'
                                )
        count=0
        ids=[]
        detInfo = []
        for photo in photos:
            if count< MAX_COUNT:
                count=count+1
                print("Fetching url for image number {}".format(count))
                try:
                    _id=photo.get('id')
                    # ids.append(_id)
                    # info = flickr.photos.getInfo(photo_id = _id,format = 'json')
                    # detInfo.append(info)
                    # print(_id)
                    ids.append(_id)
                except:
                    print("Url for image number {} could not be fetched".format(count))
            else:
                print("Done fetching urls, fetched {} urls out of {}".format(len(ids),MAX_COUNT))
                break
        ids=pd.Series(ids)
        # detInfo = pd.Series(detInfo)
        print("Writing out the ids in the current directory")
        ids.to_csv(".//ids//zurich//"+ image_tag[0:-1] +"_ids.csv",index=False)
        # print("writing json objects")
        # try:
        #     i = 0
        #     with open(image_tag + '.json', 'w') as f:
        #         print >> f, '{ "photos": ['
        #         for item in detInfo:
        #             if i == 1:
        #                 print >> f, ','
        #             print >> f, item
                    
        #             if i == 0:
        #                 i += 1
        #         print >> f, ']}'
                
        # except:
        #     print('failed to save as json')
        # print("Done!!!")
    except Exception as e:
        print("couldn't load some ids")

def main():
    tag = []
    with open ('sound_dictionary.txt') as f:
        for line in f:
            tag.append(line.split(None,1)[0])
        print(tag)
    MAX_COUNT=int(sys.argv[1])
    if MAX_COUNT < 10:
        MAX_COUNT = 10
    elif MAX_COUNT > 10000:
        MAX_COUNT = 10000
    start = False
    for t in tag:
        print(t)
        get_urls(t,MAX_COUNT)

if __name__=='__main__':
    main()
