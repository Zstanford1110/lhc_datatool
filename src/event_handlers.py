# Event Handler functions that extract the raw data from each individual event
# The raw data is meant to be stored in one of the arrays in the data store based on event_name

import json

def process_time_per_run_event(string_props):
    # Ex: '{"Runtime":"18"}'
   return json.loads(string_props)['Runtime']
    #         filtered_run_times = [];
    # previous_run_time = None
    # for run_time in run_times:
    #     if run_time != 0 and run_time != previous_run_time:
    #         filtered_run_times.append(run_time)
    #     previous_run_time = run_time
    # return filtered_run_times
    
def process_assistant_chosen_event(string_props):
    # Ex: '{"Assistant Chosen":"Banker Assistant"}'
    return json.loads(string_props)['Assistant Chosen']

def process_hiring_booth_event(string_props):
    # Ex: '{"Number Of Assistants Fired":"0","Number Of Times Assistants Rerolled":"0"}'
    return json.loads(string_props)

def process_main_menu_selections_event(string_props):
    # Ex: '{"Class Selected":"Executive Chef","Difficulty Selected":"Easy"}'
    return json.loads(string_props)

def process_number_of_waves_revealed_event(string_props):
    # Ex: '{"Reveal Amount":"7"}'
    return json.loads(string_props)['Reveal Amount']

def process_player_death_event(string_props):
    # Ex: '{"Enemy That Killed Player":"Straw Berry","Wave That Player Died On":"7","Wave Type That Player Died On":"Normal"}'
    return json.loads(string_props)

def process_wave_breakdown_event(string_props):
    # Ex: '{"Wave Breakdown":"Wave Number: 1 - Wave Type: Normal - Money Earned: 79 - Enemy Groups:  Key Wi - Regular,"}'
    # May not have the same shape every time, enemy groups will vary in length
    return json.loads(string_props)

def process_weapon_chosen_event(string_props):
    # Ex: '{"Weapon Chosen":"Chef\'s Knife"}'
    return json.loads(string_props)['Weapon Chosen']

def process_weapons_shop_event(string_props):
    # Ex: '{"Number Of Times Weapons Rerolled":"0","Number Of Weapons Combined And Sold":"0"}'
    return json.loads(string_props)