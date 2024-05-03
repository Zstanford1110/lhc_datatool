import pandas as pd
from event_handlers import *
from event_data_store import EventDataStore

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

def process_data(data):
    event_data_store = EventDataStore()
    unique_user_ids = set()
    unique_session_ids = set()
    if 'event_name' in data.columns and 'string_props' in data.columns:
        # Process each row based on the event_name
        for index, row in data.iterrows():
            user_id = row['user_id']
            session_id = row['session_id']
            
            # Record the number of unique users and sessions
            if user_id not in unique_user_ids:
                event_data_store.add_user(user_id)
                unique_user_ids.add(user_id)
                
            if session_id not in unique_session_ids:
                event_data_store.add_session(session_id)
                unique_session_ids.add(session_id)
            
            event_name = row['event_name']
            string_props = row['string_props']
            
            if event_name in event_function_map:
                # Remove the event_name from the data and only push the value to the data store. The data store's property vars will track the event_name.
                # If the data is an object with several properties, store as full object.
                extracted_data = event_function_map[event_name](string_props)
                event_data_store.add_event(event_name, extracted_data)
            else:
                print(f"Unhandled event type: {event_name}")
                
    else:
        print("Required columns 'event_name' or 'string_props' are missing in the data.")
    return event_data_store
