import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


'''
Frequency: measures in Hz in range 0 Hz - 20kHz
Loudness: relationship between frequency and pressure, measured in phon, 60 phon = 60dB at 1kHz frequency 
= perceived loudness, https://www.onosokki.co.jp/English/hp_e/whats_new/SV_rpt/SV_7/sv7_13.htm
Pressure: volume, measured in dB. Human hearing covers between 10-140dB 
distance: from sound source, impacts sound propagation, the further you are away from the source, the worse the sound pressure
http://noisetools.net/noisecalculator2?receiver=[1.5,7500]&barrier=[0]&display=2
'''


def fuzzy_set(distance_input, frequency_input, pressure_input):
    distance = ctrl.Antecedent(np.arange(0, 10000, 10), 'distance')
    sound_frequency = ctrl.Antecedent(np.arange(0, 20001, 50), 'sound frequency (Hz)')  # use 250 steps instead
    sound_pressure = ctrl.Antecedent(np.arange(0, 140, 1), 'sound pressure (db)')

    loudness = ctrl.Consequent(np.arange(0, 140, 1), 'perceived loudness (phon)')
    annoyance = ctrl.Consequent(np.arange(0, 100, 1), 'annoyance')

    # auto-membership function to populate fuzzy variables with terms

    distance['very close'] = fuzz.trapmf(distance.universe, [0, 0, 20, 30])
    distance['close'] = fuzz.trapmf(distance.universe, [20, 100, 200, 300])
    distance['midrange'] = fuzz.trapmf(distance.universe, [250, 500, 700, 1500])
    distance['far'] = fuzz.trapmf(distance.universe, [1000, 2000, 3000, 5000])
    distance['very far'] = fuzz.trapmf(distance.universe, [3000, 7500, 10000, 10000])

    sound_frequency['sub-bass'] = fuzz.trapmf(sound_frequency.universe, [0, 0, 40, 80])
    sound_frequency['bass'] = fuzz.trapmf(sound_frequency.universe, [60, 80, 120, 300])
    sound_frequency['low-midrange'] = fuzz.trapmf(sound_frequency.universe, [250, 300, 400, 600])
    sound_frequency['midrange'] = fuzz.trapmf(sound_frequency.universe, [500, 1000, 1500, 2000])
    sound_frequency['upper-midrange'] = fuzz.trapmf(sound_frequency.universe, [1500, 3000, 4000, 5000])
    sound_frequency['lower treble'] = fuzz.trapmf(sound_frequency.universe, [4000, 6000, 8000, 15000])
    sound_frequency['highs'] = fuzz.trapmf(sound_frequency.universe, [5000, 15000, 20000, 20000])

    sound_pressure['silent'] = fuzz.trimf(sound_pressure.universe, [0, 0, 30])
    sound_pressure['very quiet'] = fuzz.trimf(sound_pressure.universe, [10, 30, 50])
    sound_pressure['quiet'] = fuzz.trimf(sound_pressure.universe, [30, 40, 55])
    sound_pressure['normal'] = fuzz.trimf(sound_pressure.universe, [50, 60, 75])
    sound_pressure['loud'] = fuzz.trimf(sound_pressure.universe, [70, 75, 85])
    sound_pressure['very loud'] = fuzz.trimf(sound_pressure.universe, [80, 95, 115])
    sound_pressure['extremely loud'] = fuzz.trimf(sound_pressure.universe, [110, 140, 140])

    loudness['silent'] = fuzz.trimf(loudness.universe, [0, 0, 30])
    loudness['very quiet'] = fuzz.trimf(loudness.universe, [10, 30, 50])
    loudness['quiet'] = fuzz.trimf(loudness.universe, [40, 55, 70])
    loudness['normal'] = fuzz.trimf(loudness.universe, [50, 60, 75])
    loudness['loud'] = fuzz.trimf(loudness.universe, [70, 75, 85])
    loudness['very loud'] = fuzz.trimf(loudness.universe, [80, 95, 115])
    loudness['extremely loud'] = fuzz.trimf(loudness.universe, [110, 140, 140])

    #sound_pressure.view()
    #distance.view()
    #sound_frequency.view()
    #loudness.view()


    rule1 = ctrl.Rule(sound_frequency['sub-bass'] & sound_pressure['silent'], loudness['silent'])
    rule2 = ctrl.Rule(sound_frequency['sub-bass'] & sound_pressure['very quiet'], loudness['silent'])
    rule3 = ctrl.Rule(sound_frequency['sub-bass'] & sound_pressure['quiet'], loudness['very quiet'])
    rule4 = ctrl.Rule(sound_frequency['sub-bass'] & sound_pressure['normal'], loudness['very quiet'])
    rule5 = ctrl.Rule(sound_frequency['sub-bass'] & sound_pressure['loud'], loudness['quiet'])
    rule6 = ctrl.Rule(sound_frequency['sub-bass'] & sound_pressure['very loud'], loudness['normal'])
    rule7 = ctrl.Rule(sound_frequency['sub-bass'] & sound_pressure['extremely loud'], loudness['very loud'])

    rule8 = ctrl.Rule(sound_frequency['bass'] & sound_pressure['silent'], loudness['silent'])
    rule9 = ctrl.Rule(sound_frequency['bass'] & sound_pressure['very quiet'], loudness['very quiet'])
    rule10 = ctrl.Rule(sound_frequency['bass'] & sound_pressure['quiet'], loudness['quiet'])
    rule11 = ctrl.Rule(sound_frequency['bass'] & sound_pressure['normal'], loudness['normal'])
    rule12 = ctrl.Rule(sound_frequency['bass'] & sound_pressure['loud'], loudness['loud'])
    rule13 = ctrl.Rule(sound_frequency['bass'] & sound_pressure['very loud'], loudness['very loud'])
    rule14 = ctrl.Rule(sound_frequency['bass'] & sound_pressure['extremely loud'], loudness['very loud'])

    rule15 = ctrl.Rule(sound_frequency['low-midrange'] & sound_pressure['silent'], loudness['silent'])
    rule16 = ctrl.Rule(sound_frequency['low-midrange'] & sound_pressure['very quiet'], loudness['quiet'])
    rule17 = ctrl.Rule(sound_frequency['low-midrange'] & sound_pressure['quiet'], loudness['quiet'])
    rule18 = ctrl.Rule(sound_frequency['low-midrange'] & sound_pressure['normal'], loudness['normal'])
    rule19 = ctrl.Rule(sound_frequency['low-midrange'] & sound_pressure['loud'], loudness['loud'])
    rule20 = ctrl.Rule(sound_frequency['low-midrange'] & sound_pressure['very loud'], loudness['very loud'])
    rule21 = ctrl.Rule(sound_frequency['low-midrange'] & sound_pressure['extremely loud'], loudness['very loud'])

    rule22 = ctrl.Rule(sound_frequency['midrange'] & sound_pressure['silent'], loudness['very quiet'])
    rule23 = ctrl.Rule(sound_frequency['midrange'] & sound_pressure['very quiet'], loudness['quiet'])
    rule24 = ctrl.Rule(sound_frequency['midrange'] & sound_pressure['quiet'], loudness['normal'])
    rule25 = ctrl.Rule(sound_frequency['midrange'] & sound_pressure['normal'], loudness['normal'])
    rule26 = ctrl.Rule(sound_frequency['midrange'] & sound_pressure['loud'], loudness['loud'])
    rule27 = ctrl.Rule(sound_frequency['midrange'] & sound_pressure['very loud'], loudness['very loud'])
    rule28 = ctrl.Rule(sound_frequency['midrange'] & sound_pressure['extremely loud'], loudness['very loud'])

    rule29 = ctrl.Rule(sound_frequency['upper-midrange'] & sound_pressure['silent'], loudness['very quiet'])
    rule30 = ctrl.Rule(sound_frequency['upper-midrange'] & sound_pressure['very quiet'], loudness['quiet'])
    rule31 = ctrl.Rule(sound_frequency['upper-midrange'] & sound_pressure['quiet'], loudness['normal'])
    rule32 = ctrl.Rule(sound_frequency['upper-midrange'] & sound_pressure['normal'], loudness['normal'])
    rule33 = ctrl.Rule(sound_frequency['upper-midrange'] & sound_pressure['loud'], loudness['loud'])
    rule34 = ctrl.Rule(sound_frequency['upper-midrange'] & sound_pressure['very loud'], loudness['very loud'])
    rule35 = ctrl.Rule(sound_frequency['upper-midrange'] & sound_pressure['extremely loud'], loudness['very loud'])

    rule36 = ctrl.Rule(sound_frequency['lower treble'] & sound_pressure['silent'], loudness['quiet'])
    rule37 = ctrl.Rule(sound_frequency['lower treble'] & sound_pressure['very quiet'], loudness['quiet'])
    rule38 = ctrl.Rule(sound_frequency['lower treble'] & sound_pressure['quiet'], loudness['normal'])
    rule39 = ctrl.Rule(sound_frequency['lower treble'] & sound_pressure['normal'], loudness['loud'])
    rule40 = ctrl.Rule(sound_frequency['lower treble'] & sound_pressure['loud'], loudness['loud'])
    rule41 = ctrl.Rule(sound_frequency['lower treble'] & sound_pressure['very loud'], loudness['very loud'])
    rule42 = ctrl.Rule(sound_frequency['lower treble'] & sound_pressure['extremely loud'], loudness['very loud'])

    rule43 = ctrl.Rule(sound_frequency['highs'] & sound_pressure['silent'], loudness['very quiet'])
    rule44 = ctrl.Rule(sound_frequency['highs'] & sound_pressure['very quiet'], loudness['quiet'])
    rule45 = ctrl.Rule(sound_frequency['highs'] & sound_pressure['quiet'], loudness['normal'])
    rule46 = ctrl.Rule(sound_frequency['highs'] & sound_pressure['normal'], loudness['normal'])
    rule47 = ctrl.Rule(sound_frequency['highs'] & sound_pressure['loud'], loudness['loud'])
    rule48 = ctrl.Rule(sound_frequency['highs'] & sound_pressure['very loud'], loudness['very loud'])
    rule49 = ctrl.Rule(sound_frequency['highs'] & sound_pressure['extremely loud'], loudness['very loud'])

    rule50 = ctrl.Rule(distance['very close'] & sound_pressure['silent'], loudness['silent'])
    rule51 = ctrl.Rule(distance['very close'] & sound_pressure['quiet'], loudness['silent'])
    rule52 = ctrl.Rule(distance['very close'] & sound_pressure['very quiet'], loudness['very quiet'])
    rule53 = ctrl.Rule(distance['very close'] & sound_pressure['normal'], loudness['quiet'])
    rule54 = ctrl.Rule(distance['very close'] & sound_pressure['loud'], loudness['normal'])
    rule55 = ctrl.Rule(distance['very close'] & sound_pressure['very loud'], loudness['loud'])
    rule56 = ctrl.Rule(distance['very close'] & sound_pressure['extremely loud'], loudness['very loud'])

    rule57 = ctrl.Rule(distance['close'] & sound_pressure['silent'], loudness['silent'])
    rule58 = ctrl.Rule(distance['close'] & sound_pressure['quiet'], loudness['silent'])
    rule59 = ctrl.Rule(distance['close'] & sound_pressure['very quiet'], loudness['silent'])
    rule60 = ctrl.Rule(distance['close'] & sound_pressure['normal'], loudness['silent'])
    rule61 = ctrl.Rule(distance['close'] & sound_pressure['loud'], loudness['very quiet'])
    rule62 = ctrl.Rule(distance['close'] & sound_pressure['very loud'], loudness['quiet'])
    rule63 = ctrl.Rule(distance['close'] & sound_pressure['extremely loud'], loudness['normal'])

    rule64 = ctrl.Rule(distance['midrange'] & sound_pressure['silent'], loudness['silent'])
    rule65 = ctrl.Rule(distance['midrange'] & sound_pressure['quiet'], loudness['silent'])
    rule66 = ctrl.Rule(distance['midrange'] & sound_pressure['very quiet'], loudness['silent'])
    rule67 = ctrl.Rule(distance['midrange'] & sound_pressure['normal'], loudness['silent'])
    rule68 = ctrl.Rule(distance['midrange'] & sound_pressure['loud'], loudness['very quiet'])
    rule69 = ctrl.Rule(distance['midrange'] & sound_pressure['very loud'], loudness['quiet'])
    rule70 = ctrl.Rule(distance['midrange'] & sound_pressure['extremely loud'], loudness['normal'])

    rule71 = ctrl.Rule(distance['far'] & sound_pressure['silent'], loudness['silent'])
    rule72 = ctrl.Rule(distance['far'] & sound_pressure['quiet'], loudness['silent'])
    rule73 = ctrl.Rule(distance['far'] & sound_pressure['very quiet'], loudness['silent'])
    rule74 = ctrl.Rule(distance['far'] & sound_pressure['normal'], loudness['silent'])
    rule75 = ctrl.Rule(distance['far'] & sound_pressure['loud'], loudness['silent'])
    rule76 = ctrl.Rule(distance['far'] & sound_pressure['very loud'], loudness['very quiet'])
    rule77 = ctrl.Rule(distance['far'] & sound_pressure['extremely loud'], loudness['quiet'])

    rule78 = ctrl.Rule(distance['very far'] & sound_pressure['silent'], loudness['silent'])
    rule79 = ctrl.Rule(distance['very far'] & sound_pressure['quiet'], loudness['silent'])
    rule80 = ctrl.Rule(distance['very far'] & sound_pressure['very quiet'], loudness['silent'])
    rule81 = ctrl.Rule(distance['very far'] & sound_pressure['normal'], loudness['silent'])
    rule82 = ctrl.Rule(distance['very far'] & sound_pressure['loud'], loudness['silent'])
    rule83 = ctrl.Rule(distance['very far'] & sound_pressure['very loud'], loudness['silent'])
    rule84 = ctrl.Rule(distance['very far'] & sound_pressure['extremely loud'], loudness['silent'])

    sound_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11,
                                     rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20, rule21,
                                     rule22, rule23, rule24, rule25, rule26, rule27, rule28, rule29, rule30, rule31,
                                     rule32, rule33, rule34, rule35, rule36, rule37, rule38, rule39, rule40, rule41,
                                     rule42, rule43, rule44, rule45, rule46, rule47, rule48, rule49, rule50, rule51,
                                     rule52, rule53, rule54, rule55, rule56, rule57, rule58, rule59, rule60, rule61,
                                     rule62, rule63, rule64, rule65, rule66, rule67, rule68, rule69, rule70, rule71,
                                     rule72, rule73, rule74, rule75, rule76, rule77, rule78, rule79, rule80, rule81,
                                     rule82, rule83, rule84])

    sound_level = ctrl.ControlSystemSimulation(sound_ctrl)

    sound_level.input['distance'] = distance_input
    sound_level.input['sound frequency (Hz)'] = frequency_input
    sound_level.input['sound pressure (db)'] = pressure_input

    sound_level.compute()
    #print(sound_level.output['perceived loudness (phon)'])
    loudness.view(sim=sound_level)

if __name__ == '__main__':
    fuzzy_set(0, 1300, 80)