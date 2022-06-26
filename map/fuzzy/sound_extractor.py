import indicoio
import json
from fuzzy_engine import read_sound_dictionary, setup_fuzzy_engine, predict_sound_level

indicoio.config.api_key = '' # Add you secret key here


sample_sentence = 'no words can help me'
sound_words = []


def read_sound_file(filename):
    """
    Converts the list of sound bearing words from the sound_dictionary.txt file to a list.
    :param filename: name of sound dictionary txt file
    :return: list of sound bearing words occurring in the sound dictionary
    """
    sound_file = open(filename, 'r')
    for line in sound_file:
        word = line.split(None, 1)[0]
        word = word[:-1]
        sound_words.append(word)


def analyse_text(text):
    """
    Analyses the input text by first extracting sound bearing words and distance annotations. Then it runs
    a sentiment analysis i.e. emotion detection on the sentence to get a score for each emotion. The sound
    bearing words and distance words are passed to the fuzzy logic system to predict the perceived sound
    level in decibel. Finally, we return a JSON object of the sentence containing all relevant information
    to be annotated on the map
    :param text: str - input sentence
    :return: JSON object with keys: sentence, sounds, categories, dominant (sound), emotions
    """
    sound_dictionary = read_sound_dictionary('sound_dictionary.txt')
    
    read_sound_file('sound_dictionary.txt')
    sentence_summary = {}
    text_information = split_sentence(text)  # keys: sentence: str, words: list, distances: list
    if len(text_information['words']) != 0:
        emotions = detect_emotion(text)
        sounds, categories, dominant_sound = analyse_sound_words(text_information['words'], text_information['distances'], emotions)

        sentence_summary['sentence'] = text
        sentence_summary['sounds'] = sounds
        sentence_summary['categories'] = [categories]
        sentence_summary['dominant'] = dominant_sound
        sentence_summary['emotions'] = [emotions]
    sentence_json = json.dumps(sentence_summary)
    #print(sentence_json)
    return sentence_summary


def analyse_sound_words(sound_words, distance_words, emotions):
    """
    Builds sound object by parsing through the list of sound bearing words, calling the fuzzy control system
    to predict the sound level in db based on sound pressure, frequency, distance and emotions. Furthermore,
    keeps track of the loudest sound occurring and the max db per sound category.
    :param sound_words: sound bearing words from the sound dictionary occurring in the sentence
    :param distance_words: distance annotations occuring in the sentence. either 'close' or 'far'
    :param emotions: dict of six basic emotions with their corresponding score
    :return: list of all the sounds with their estimated db level, their category, the list of categories with their max
    db level and the most dominant sound.
    """
    dominant_sound = {}
    categories = {'traffic': 0, 'human': 0, 'nature': 0, 'music': 0, 'mechanical': 0}
    sounds = []
    max_db = 0

    for word in sound_words:
        db_level, db_level_lable, category,  = predict_sound_level(word, distance_words, emotions)

        # create sound object
        sound_obj = {}
        sound_obj['sound'] = word
        sound_obj['db'] = db_level
        sound_obj['category'] = category
        sounds.append(sound_obj)

        if db_level > categories[category]:
            categories[category] = db_level

        # check if sound is dominant
        if max_db < db_level:
            max_db = db_level
            dominant_sound = sound_obj

    return sounds, categories, dominant_sound


def split_sentence(sentence):
    """
    Parse the input sentence to obtain the sound bearing words and distance annotations.
    :param sentence: input sentence
    :return: set of sound bearing words and distance annotations present in the sentence
    """
    global sound_words
    remove_chars = ['.', ',', '!', '?', ';', '(', ')', ':', '#']
    close_distances = ['close', 'near', 'short-distance', 'closely', 'short-range', 'here']
    far_distances = ['far', 'long-distances', 'further', 'away', 'long-range', 'there', 'distant']
    words = set()
    distances = set()
    word_details = {}
    for word in sentence.split(' '):
        word = word.lower()
        # check if sentence contains sound bearing words
        if word in sound_words:
            # parse words and clean from special characters
            for i in remove_chars:
                word = word.replace(i, ' ')
            words.add(word)

        # check if sentence contains distance annotations
        if word in close_distances:
            distances.add('close')
        elif word in far_distances:
            distances.add('far')

    # Set word details as dictionary
    word_details['sentence'] = sentence
    word_details['words'] = words
    word_details['distances'] = distances
    return word_details


def detect_emotion(sentence):
    """
    Returns a dictionary of emotions and their score in the format:
    {'joy': 0.6934858560562134, 'surprise': 0.11561262607574463, 'sadness': 0.0868280753493309, 'fear': 0.06403486430644989, 'anger': 0.04003848880529404}
    :param sentence: string input sentence to be analysed
    :return: emotion dictionary with scroes for each emotion between 0 and 1.
    """
    emotion_dict = indicoio.emotion(sentence)
    return emotion_dict


if __name__ == '__main__':
    sound_dictionary = read_sound_dictionary('sound_dictionary.txt')
    setup_fuzzy_engine()
    analyse_text('I love listening to birds during breakfast')
