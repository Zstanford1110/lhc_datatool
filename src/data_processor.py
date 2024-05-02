import pandas as pd
from event_handlers import *
from event_data import EventDataStore

event_data_store = EventDataStore()

def process_data(data):
    if 'event_name' in data.columns and 'string_props' in data.columns:
        # Process each row based on the event_name
        for index, row in data.iterrows():
            event_name = row['event_name']
            string_props = row['string_props']
            
            event_function_map = {
                'Amount Of Time Per Run': process_time_per_run_event,
                'Assistant Chosen': process_assistant_chosen_event,
                'Hiring Booth': process_hiring_booth_event,
                'Main Menu Selections': process_main_menu_selections_event,
                'Number Of Waves Revealed': process_number_of_waves_revealed_event,
                'Player Death': process_player_death_event,
                'Wave Breakdown': process_wave_breakdown_event,
                'Weapon Chosen': process_weapon_chosen_event,
                'Weapons Shop': process_weapons_shop_event
            }
            
            if event_name in event_function_map:
                event_function_map[event_name](string_props)
            else:
                print(f"Unhandled event type: {event_name}")
                
    else:
        print("Required columns 'event_name' or 'string_props' are missing in the data.")

    
    print("Data shape:", data.shape)
