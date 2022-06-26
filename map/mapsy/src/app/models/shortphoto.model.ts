
export interface ShortPhoto {
    photo_id: string,
    description: string,
    tags: string,
    latitude: string,
    longitude: number
    properties: {
        sounds: [{
            sound: string,
            category: string,
            db: number
        }],
        dominant: {
            sound: string,
            category: string,
            db: number
        },
        emotions: {
            anger: number,
            surprise: number,
            sadness: number,
            fear: number,
            joy: number
        },
        categories: {
            music: number,
            mechanical: number,
            traffic: number,
            human: number,
            nature: number
        },
        sentence: string
    },
    url: [{
        type: string,
        _content: string
    }]
    
}