import json
from numpy import mean
from classes.final_data_store import FinalDataStore

def transform_data(event_data_store):
    final_data_store = FinalDataStore()

    # Data relating to unique game sessions and users
    final_data_store.add_data("General Analytics Data", process_general_analytics_data(event_data_store))

    # Data relating to the runs (one run = one play through that was at least started)
    final_data_store.add_data("Run Data", process_run_data(event_data_store))

    # Assistant Selection statistics
    final_data_store.add_data("Assistant Data", process_assistant_data(event_data_store.get_event_data("Assistant Chosen")))

    # Main Menu Selections statistics
    final_data_store.add_data("Menu Selection Distribution", process_main_menu_selections_data(event_data_store.get_event_data("Main Menu Selections")))

    # Wave Reveal Data
    final_data_store.add_data("Wave Reveal Data", process_wave_reveal_data(event_data_store.get_event_data('Number Of Waves Revealed')))
    
    # Hiring Booth statistics
    final_data_store.add_data("Hiring Booth Data", process_hiring_booth_data(event_data_store.get_event_data("Hiring Booth")))

    # Player death statistics
    # {"Enemy That Killed Player": "Straw Berry", "Wave That Player Died On": "7", "Wave Type That Player Died On": "Normal"}
    final_data_store.add_data("Player Death Data", process_player_death_data(event_data_store.get_event_data("Player Death")))

    return final_data_store

## DATA PROCESSING FUNCTIONS - Designs the final data schema
def process_general_analytics_data(event_data_store):
    users = event_data_store.unique_users
    sessions = event_data_store.game_sessions
    user_count = event_data_store.get_user_count()
    session_count = event_data_store.get_session_count()
    
    return {"User IDs": users, "Session IDs": sessions, "User Count": user_count, "Session Count": session_count}

def process_run_data(event_data_store):
    # Filter 0 values and obvious duplicates from run times
    filtered_run_times = filter_run_times(event_data_store.get_event_data("Amount Of Time Per Run"))
    average_run_time = mean(filtered_run_times)
    total_runs_started = len(event_data_store.get_event_data("Main Menu Selections"))
    
    return { "Run Times": filtered_run_times, "Average Run Time": average_run_time, "Total Runs": total_runs_started}

def process_assistant_data(assistants_chosen):
    assistant_counts = {}
    
    # Create Assistant selection distribution
    for assistant in assistants_chosen:
        if assistant in assistant_counts:
            assistant_counts[assistant] += 1
        else:
            assistant_counts[assistant] = 1
            
    # Sort the dictionary by value in descending order
    sorted_assistant_counts = dict(sorted(assistant_counts.items(), key=lambda item: item[1], reverse=True))
    
    # Additional statistics relating to distribution
    total_assistants_hired = len(assistants_chosen)
    
    return {"Raw Assistant Data": assistants_chosen, "Assistant Selection Distribution": sorted_assistant_counts, "Total Assistants Hired": total_assistants_hired }

def process_main_menu_selections_data(main_menu_selections):
    class_counts = {}
    difficulty_counts = {}

    # Main Menu Selection Distribution
    for selection_data in main_menu_selections:
        # Count "Class Selected"
        class_selected = selection_data.get("Class Selected")
        if class_selected in class_counts:
            class_counts[class_selected] += 1
        else:
            class_counts[class_selected] = 1

        # Count "Difficulty Selected"
        difficulty_selected = selection_data.get("Difficulty Selected")
        if difficulty_selected in difficulty_counts:
            difficulty_counts[difficulty_selected] += 1
        else:
            difficulty_counts[difficulty_selected] = 1

    # Sort both dictionaries by value in descending order
    sorted_class_counts = dict(sorted(class_counts.items(), key=lambda item: item[1], reverse=True))
    sorted_difficulty_counts = dict(sorted(difficulty_counts.items(), key=lambda item: item[1], reverse=True))


    return { "Class Selections": sorted_class_counts, "Difficulty Selections": sorted_difficulty_counts }

def process_wave_reveal_data(waves_revealed):
    parsed_waves_revealed = parse_int_list(waves_revealed)
    average_waves_revealed = mean(parsed_waves_revealed)
    total_waves_revealed = sum(parsed_waves_revealed)
    
    return { "Waves Revealed Raw Data": parsed_waves_revealed, "Average Waves Revealed": average_waves_revealed, "Total Waves Revealed": total_waves_revealed}

def process_hiring_booth_data(hiring_booth):
    fired_data = []
    rerolled_data = []

    for selection in hiring_booth:
        fired_run_total = int(selection.get("Number Of Assistants Fired"))
        rerolled_run_total = int(selection.get("Number Of Times Assistants Rerolled"))
        fired_data.append(fired_run_total)
        rerolled_data.append(rerolled_run_total)
   
    total_fired = sum(fired_data)
    total_rerolls = sum(rerolled_data)
    average_fired = mean(fired_data)
    average_reroll = mean(rerolled_data)
    
    return { "Assistants Fired Raw Data": fired_data, "Assistants Rerolled Raw Data": rerolled_data, "Total Number of Assistants Fired": total_fired, "Total Number of Assistant Rerolls": total_rerolls, "Average Assistants Fired": average_fired, "Average Assistant Rerolls": average_reroll }

def process_player_death_data(player_death_data):
    enemy_that_killed_player_distribution = {}
    wave_that_player_died_on_list = []
    wave_type_player_died_on_distribution = {}
    
    for player_death in player_death_data:
        enemy_type = player_death.get("Enemy That Killed Player")
        
        # Use "Enemy Not Defined" as the key if the enemy name is not provided/valid
        if not enemy_type.strip():
            enemy_type = "Enemy Not Defined"
        
        # Record the enemy that killed the player
        if enemy_type in enemy_that_killed_player_distribution:
            enemy_that_killed_player_distribution[enemy_type] += 1
        else:
            enemy_that_killed_player_distribution[enemy_type] = 1
        
        # Add wave numbers to the overall list for average, sum, and other calculations later
        wave_that_player_died_on_list.append(int(player_death.get("Wave That Player Died On")))
        
        # Determine the distribution for the wave types that players are dying on
        wave_type = player_death.get("Wave Type That Player Died On")
        
        if not wave_type.strip():
            wave_type = "Wave Type Not Defined"
        
        if wave_type in wave_type_player_died_on_distribution:
            wave_type_player_died_on_distribution[wave_type] += 1
        else:
            wave_type_player_died_on_distribution[wave_type] = 1
            
        average_wave_reached = mean(wave_that_player_died_on_list)
        highest_wave_reached = max(wave_that_player_died_on_list)
            
    return { "Enemy That Killed Player Distribution": enemy_that_killed_player_distribution, "Waves That Players Died On": wave_that_player_died_on_list, "Wave Types That Players Died On Distribution": wave_type_player_died_on_distribution,  "Average Wave Reached Before Death": average_wave_reached, "Highest Wave Reached": highest_wave_reached }

## HELPER FUNCTIONS
# Hopefully temporary helper function to remove duplicate and 0 value run times
def filter_run_times(run_times):
    filtered_run_times = []
    previous_run_time = None
    for run_time in run_times:
        parsed_time = int(run_time)
        if parsed_time != 0 and parsed_time != previous_run_time:
            filtered_run_times.append(parsed_time)
        previous_run_time = parsed_time
    return filtered_run_times

# Convert a list of strings to a list of ints using list comprehension
def parse_int_list(str_list):
    return [int(element) for element in str_list]
        