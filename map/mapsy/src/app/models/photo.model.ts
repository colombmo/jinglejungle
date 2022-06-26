import { IGeoJson } from './city.model';
import { StringMap } from '@angular/compiler/src/compiler_facade_interface';

export interface Photo {
    id: string,
    secret: string,
    server: string,
    farm: number,
    dateuploaded: string,
    isfavorite: string,
    license: string,
    safety_level: number,
    rotation: number,
    originalsecret: string,
    originalformat: string,
    owner: {
        nsid: string,
        username: string,
        realname: string,
        location: string,
        iconserver: string,
        iconfarm: number,
        path_alias: string
    },
    title: {
        _content: string
    },
    description: {
        _content: string
    },
    location: {
        latitude: string,
        longitude: string
        accuracy: string,
        context: string,
        neighbourhood: {
            _content: string,
            place_id: string,
            woeid: string
        },
        locality: {
            _content: string,
            place_id: string,
            woeid: string
        },
        county: {
            _content: string,
            place_id: string,
            woeid: string
        },
        region: {
            _content: string,
            place_id: string,
            woeid: string
        },
        country: {
            _content: string,
            place_id: string,
            woeid: string
        },
        place_id: string,
        woeid: string
    },
    visibility: {
        ispublic: number,
        isfriend: number,
        isfamily: number
    },
    dates: {
        posted: string,
        taken: string,
        takengranularity: string,
        takenunknown: number,
        lastupdate: string
    },
    views: string,
    editability: {
        cancomment: number,
        canaddmeta: number
    },
    publiceditability: {
        cancomment: number,
        canaddmeta: number
    }
    usage: {
        candownload: number,
        canblog: number,
        canprint: number,
        canshare: number
    },
    comments: {
        _content: string
    },
    notes: { note: any[] },
    people: { haspeople: number }
    tags: { tag: any[] },
    geoperms: {
        ispublic: number,
        iscontact: number, 
        isfriend: number, 
        isfamily: number
    },
    urls: {
        url: any[]
    },
    media: string
}

export interface PhotoShort{
    id: string,
    geoJson: IGeoJson,
    description: Description

}
export interface SoundWords{
    word: string,
    dbLvl: number,

}
export interface Category{
    word: SoundWords[],
    category: string,
    isMax: boolean
}

export interface Emotions{
    emotion: string,
    score: number
}
export interface Description{
    content: string,
    categories: Category[],
    emotions: Emotions[],

}







