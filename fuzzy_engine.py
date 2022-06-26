import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def setup_fuzzy_engine():
    """
    Only have to call this once to setup the Fuzzy Control System, to which we feed the input later.
    :return: estimator - ControlSystemSimulation
    """
    global estimator, db_labels, perceived_db_level, db_level_dict, db_universe
    db_labels = ['silent', 'quiet', 'normal', 'loud', 'very loud']
    db_universe = np.arange(0, 180, 0.5)
    db_level = ctrl.Antecedent(db_universe, 'db')
    frequency = ctrl.Antecedent(np.arange(0, 20001, 10), 'frequency')
    perceived_db_level = ctrl.Consequent(np.arange(0, 180, 1), 'perceived')

    anger = ctrl.Antecedent(np.arange(0, 1, 0.1), 'anger')
    sadness = ctrl.Antecedent(np.arange(0, 1, 0.1), 'sadness')
    fear = ctrl.Antecedent(np.arange(0, 1, 0.1), 'fear')
    surprise = ctrl.Antecedent(np.arange(0, 1, 0.1), 'surprise')
    joy = ctrl.Antecedent(np.arange(0, 1, 0.1), 'joy')

    db_level_dict = {}
    db_level[db_labels[0]] = fuzz.trimf(db_universe, [0, 0, 50])
    db_level_dict[db_labels[0]] = fuzz.trimf(db_universe, [0, 0, 50])
    db_level[db_labels[1]] = fuzz.trimf(db_universe, [30, 40, 60])
    db_level_dict[db_labels[1]] = fuzz.trimf(db_universe, [30, 40, 60])
    db_level[db_labels[2]] = fuzz.trimf(db_universe, [50, 60, 80])
    db_level_dict[db_labels[2]] = fuzz.trimf(db_universe, [50, 60, 80])
    db_level[db_labels[3]] = fuzz.trimf(db_universe, [70, 90, 110])
    db_level_dict[db_labels[3]] = fuzz.trimf(db_universe, [70, 90, 110])
    db_level[db_labels[4]] = fuzz.trimf(db_universe, [90, 115, 115])
    db_level_dict[db_labels[4]] = fuzz.trimf(db_universe, [90, 115, 180])

    frequency['bass'] = fuzz.trimf(frequency.universe, [0, 120, 300])
    frequency['midrange'] = fuzz.trimf(frequency.universe, [250, 1000, 5000])
    frequency['highs'] = fuzz.trimf(frequency.universe, [4000, 8000, 15000])

    perceived_db_level['silent'] = fuzz.trimf(perceived_db_level.universe, [0, 0, 40])
    perceived_db_level['quiet'] = fuzz.trimf(perceived_db_level.universe, [30, 40, 70])
    perceived_db_level['normal'] = fuzz.trimf(perceived_db_level.universe, [40, 60, 75])
    perceived_db_level['loud'] = fuzz.trimf(perceived_db_level.universe, [70, 75, 90])
    perceived_db_level['very loud'] = fuzz.trimf(perceived_db_level.universe, [80, 100, 180])

    labels = ['low', 'medium', 'high']
    anger.automf(names=labels)
    sadness.automf(names=labels)
    fear.automf(names=labels)
    surprise.automf(names=labels)
    joy.automf(names=labels)

    rule1 = ctrl.Rule(db_level['silent'] & frequency['midrange'], perceived_db_level['silent'])
    rule2 = ctrl.Rule(db_level['quiet'] & frequency['midrange'], perceived_db_level['quiet'])
    rule3 = ctrl.Rule(db_level['normal'] & frequency['midrange'], perceived_db_level['normal'])
    rule4 = ctrl.Rule(db_level['loud'] & frequency['midrange'], perceived_db_level['loud'])
    rule5 = ctrl.Rule(db_level['very loud'] & frequency['midrange'], perceived_db_level['very loud'])

    rule6 = ctrl.Rule(db_level['silent'] & frequency['bass'], perceived_db_level['silent'])
    rule7 = ctrl.Rule(db_level['quiet'] & frequency['bass'], perceived_db_level['silent'])
    rule8 = ctrl.Rule(db_level['normal'] & frequency['bass'], perceived_db_level['quiet'])
    rule9 = ctrl.Rule(db_level['loud'] & frequency['bass'], perceived_db_level['normal'])
    rule10 = ctrl.Rule(db_level['very loud'] & frequency['bass'], perceived_db_level['normal'])

    rule11 = ctrl.Rule(db_level['silent'] & frequency['highs'], perceived_db_level['silent'])
    rule12 = ctrl.Rule(db_level['quiet'] & frequency['highs'], perceived_db_level['silent'])
    rule13 = ctrl.Rule(db_level['normal'] & frequency['highs'], perceived_db_level['normal'])
    rule14 = ctrl.Rule(db_level['loud'] & frequency['highs'], perceived_db_level['loud'])
    rule15 = ctrl.Rule(db_level['very loud'] & frequency['highs'], perceived_db_level['loud'])
    rule16 = ctrl.Rule(db_level['silent'], perceived_db_level['silent'])

    rule17 = ctrl.Rule(anger['high'], perceived_db_level['very loud'])
    rule18 = ctrl.Rule(sadness['high'], perceived_db_level['loud'])
    rule19 = ctrl.Rule(fear['high'], perceived_db_level['loud'])

    rule20 = ctrl.Rule(anger['medium'], perceived_db_level['loud'])
    rule21 = ctrl.Rule(sadness['medium'], perceived_db_level['loud'])
    rule22 = ctrl.Rule(fear['medium'], perceived_db_level['loud'])

    ctrlSystem = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9,
                                     rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17,
                                     rule18, rule19, rule20, rule21, rule22])

    estimator = ctrl.ControlSystemSimulation(ctrlSystem)
    return estimator


def predict_sound_level(word, distance, emotions):
    """
    Predicts sound level based on word, it's boundaries for frequency and decibel, distance and emotions.

    :param word: sound bearing word from the sound_dictionary.txt
    :param distance: distance word ['close', 'far']
    :param emotions: set of 5 basic emotions and their score
    :return: predicted perceived sound level in db and as fuzzy variable (loud, silent, etc.)
    """
    if len(distance) > 1:
        distance = 'normal'
    elif 'close' in distance:
        distance = 'close'
    else:
        distance = 'far'
    estimated_db, estimated_freq = fuzzify_sound_word(word, distance)
    print('Estimated DB: ', estimated_db)
    print('Estimated Freq: ', estimated_freq)
    estimator.input['db'] = estimated_db
    estimator.input['frequency'] = estimated_freq
    estimator.input['anger'] = emotions['anger']
    estimator.input['sadness'] = emotions['sadness']
    estimator.input['fear'] = emotions['fear']

    estimator.compute()

    perceived_val = estimator.output['perceived']
    max = 0
    max_db_label = ''
    for label in db_labels:
        mfx = db_level_dict[label]
        membership = fuzz.interp_membership(db_universe, mfx, perceived_val)
        if membership > max:
            max = membership
            max_db_label = label
    # perceived_db_level.view(sim=estimator)
    print('Emotions: ', emotions)
    print('Perceived Sound level: ', round(perceived_val), 'db')
    print('Perceived Sound level: ', max_db_label)

    return perceived_val, max_db_label, sound_dictionary[word]['category']

def fuzzify_sound_word(word, distance):
    """
    fuzzify the word from sound dictionary depending on distance. only do that once, to predict the db and freq,
    that will later be fed to the fuzzy control system
    :param word: sound bearing word from dictionary
    :param distance: 'close' or 'far'
    :return: estimated db level and estimated freq level
    """
    global db_universe
    if len(distance) > 1:
        distance = 'normal'
    elif 'close' in distance:
        distance = 'close'
    else:
        distance = 'far'
    print('word: ', word, ' , distance: ', distance)
    frequency = ctrl.Antecedent(np.arange(0, 20000, 10), 'frequency')
    sound_level = ctrl.Antecedent(db_universe, 'db')

    sound = sound_dictionary[word]
    f_low = int(sound['freq_low'])
    f_peak = int(sound['freq_peak'])
    f_high = int(sound['freq_high'])
    freq_universe = np.arange(0, 20000, 10)
    print('Freq: low - peak -high: ', f_low, f_peak, f_high)

    frequency['low'] = fuzz.trimf(freq_universe, [f_low, f_low, f_peak])
    frequency['normal'] = fuzz.trimf(freq_universe, [f_low, f_peak, f_high])
    frequency['high'] = fuzz.trimf(freq_universe, [f_peak, f_high, f_high])

    low = int(sound['level_low'])
    peak = int(sound['level_peak'])
    high = int(sound['level_high'])
    print('DB level: low - peak -high: ', low, peak, high)
    sound_level['low'] = fuzz.trimf(db_universe, [low, low, peak])
    sound_level['normal'] = fuzz.trimf(db_universe, [low, peak, high])
    sound_level['high'] = fuzz.trimf(db_universe, [peak, high, high])

    estimate_db = ctrl.Consequent(db_universe, 'estimated_db')
    estimate_db['low'] = fuzz.trimf(db_universe, [low, low, peak])
    estimate_db['normal'] = fuzz.trimf(db_universe, [low, peak, high])
    estimate_db['high'] = fuzz.trimf(db_universe, [peak, high, high])

    estimate_freq = ctrl.Consequent(freq_universe, 'estimated_freq')
    estimate_freq['low'] = fuzz.trimf(freq_universe, [f_low, f_low, f_peak])
    estimate_freq['normal'] = fuzz.trimf(freq_universe, [f_low, f_peak, f_high])
    estimate_freq['high'] = fuzz.trimf(freq_universe, [f_peak, f_high, f_high])

    if distance == 'close':
        rule1 = ctrl.Rule(sound_level['low'], estimate_db['high'])
        rule2 = ctrl.Rule(sound_level['normal'], estimate_db['high'])
        rule3 = ctrl.Rule(sound_level['high'], estimate_db['high'])

        rule4 = ctrl.Rule(frequency['low'], estimate_db['high'])
        rule5 = ctrl.Rule(frequency['normal'], estimate_db['high'])
        rule6 = ctrl.Rule(frequency['high'], estimate_db['high'])

        rule7 = ctrl.Rule(frequency['low'], estimate_freq['low'])
        rule8 = ctrl.Rule(frequency['normal'], estimate_freq['normal'])
        rule9 = ctrl.Rule(frequency['high'], estimate_freq['high'])
    elif distance == 'far':
        rule1 = ctrl.Rule(sound_level['low'], estimate_db['low'])
        rule2 = ctrl.Rule(sound_level['normal'], estimate_db['low'])
        rule3 = ctrl.Rule(sound_level['high'], estimate_db['low'])

        rule4 = ctrl.Rule(frequency['low'], estimate_db['low'])
        rule5 = ctrl.Rule(frequency['normal'], estimate_db['low'])
        rule6 = ctrl.Rule(frequency['high'], estimate_db['low'])

        rule7 = ctrl.Rule(frequency['low'], estimate_freq['low'])
        rule8 = ctrl.Rule(frequency['normal'], estimate_freq['normal'])
        rule9 = ctrl.Rule(frequency['high'], estimate_freq['high'])
    else:
        rule1 = ctrl.Rule(sound_level['low'], estimate_db['normal'])
        rule2 = ctrl.Rule(sound_level['normal'], estimate_db['normal'])
        rule3 = ctrl.Rule(sound_level['high'], estimate_db['normal'])

        rule4 = ctrl.Rule(frequency['low'], estimate_db['normal'])
        rule5 = ctrl.Rule(frequency['normal'], estimate_db['normal'])
        rule6 = ctrl.Rule(frequency['high'], estimate_db['normal'])

        rule7 = ctrl.Rule(frequency['low'], estimate_freq['low'])
        rule8 = ctrl.Rule(frequency['normal'], estimate_freq['normal'])
        rule9 = ctrl.Rule(frequency['high'], estimate_freq['high'])

    ctrlSystem = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
    estimator = ctrl.ControlSystemSimulation(ctrlSystem)

    mfx = fuzz.trimf(db_universe, [low, peak, high])
    defuzz_db = fuzz.defuzz(db_universe, mfx, 'centroid')
    estimator.input['db'] = int(defuzz_db)

    mfx = fuzz.trimf(freq_universe, [f_low, f_peak, f_high])
    defuzz_freq = fuzz.defuzz(freq_universe, mfx, 'centroid')
    estimator.input['frequency'] = int(defuzz_freq)

    #estimate_db.view()
    estimator.compute()
    #estimate_db.view(sim=estimator)
    #estimate_freq.view(sim=estimator)
    estimated_db = round(estimator.output['estimated_db'])
    estimated_freq = round(estimator.output['estimated_freq'])
    return estimated_db, estimated_freq


def read_sound_dictionary(filename):
    """
    reads sound dictionary to dictionary. only has to be done once
    :param filename: name of sound_dictionary.txt
    :return: dict with sound-bearing word as key returning sound object with all details.
    """
    global sound_dictionary
    sound_file = open(filename, 'r')
    sound_dictionary = {}
    for line in sound_file:
        sound_details = [word.strip() for word in line.split(',')]
        sound = {}
        sound['sound'] = sound_details[0]
        sound['category'] = sound_details[1]
        sound['freq_low'] = sound_details[2]
        sound['freq_peak'] = sound_details[3]
        sound['freq_high'] = sound_details[4]
        sound['level_low'] = sound_details[5]
        sound['level_peak'] = sound_details[6]
        sound['level_high'] = sound_details[7]
        sound_dictionary[sound_details[0]] = sound
    return sound_dictionary


if __name__ == '__main__':
    sound_dictionary = read_sound_dictionary('sound_dictionary.txt')
    setup_fuzzy_engine()
    emotions = {'anger': 0.79, 'sadness': 0.11422713100910187, 'fear': 0.04237992689013481,
                'surprise': 0.024785879999399185, 'joy': 0.820769251510500908}
    predict_sound_level('airplane', ['close'], emotions)


