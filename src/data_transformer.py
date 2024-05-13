import json
from numpy import mean
from classes.final_data_store import FinalDataStore

def transform_data(event_data_store):
    final_data_store = FinalDataStore()

    # Data relating to unique game sessions and users
    final_data_store.add_data("Users", event_data_store.unique_users)
    final_data_store.add_data("Sessions", event_data_store.game_sessions)
    final_data_store.add_data("Session Count", len(final_data_store.get_data("Sessions")))
    final_data_store.add_data("User Count", len(final_data_store.get_data("Users")))

    # Data relating to the length of runs (aka, game sessions)
    final_data_store.add_data("Run Times", filter_run_times(event_data_store.get_event_data('Amount Of Time Per Run')))
    final_data_store.add_data("Average Run Time", mean(final_data_store.get_data("Run Times")))

    # Assistant Selection statistics
    final_data_store.add_data("Total Assistant Hires", len(event_data_store.get_event_data("Assistant Chosen")))
    final_data_store.add_data("Assistant Selection Distribution", summarize_assistants(event_data_store.get_event_data("Assistant Chosen")))

    # Main Menu Selections statistics
    final_data_store.add_data("Total Runs Started", len(event_data_store.get_event_data("Main Menu Selections")))
    final_data_store.add_data("Menu Selection Distribution", summarize_main_menu_selections(event_data_store.get_event_data("Main Menu Selections")))

    # Wave Reveal / Run Length statistics
    final_data_store.add_data("Waves Revealed", parse_int_list(event_data_store.get_event_data('Number Of Waves Revealed')))
    final_data_store.add_data("Average Waves Revealed", mean(final_data_store.get_data('Waves Revealed')))
    final_data_store.add_data("Total Waves Revealed", sum(final_data_store.get_data("Waves Revealed")))
    
    # Hiring Booth statistics
    final_data_store.add_data("Hiring Booth Raw Data", summarize_hiring_booth(event_data_store.get_event_data("Hiring Booth")))
    final_data_store.add_data("Total Number of Assistants Fired", sum(final_data_store.get_data("Hiring Booth Raw Data")["Number of Assistants Fired"]))
    final_data_store.add_data("Total Number of Assistant Rerolls", sum(final_data_store.get_data("Hiring Booth Raw Data")["Number of Times Assistants Rerolled"]))
    final_data_store.add_data("Average Assistants Fired", mean(final_data_store.get_data("Hiring Booth Raw Data")["Number of Assistants Fired"]))
    final_data_store.add_data("Average Assistant Rerolls", mean(final_data_store.get_data("Hiring Booth Raw Data")["Number of Times Assistants Rerolled"]))
    
    # Player death statistics
    # {"Enemy That Killed Player": "Straw Berry", "Wave That Player Died On": "7", "Wave Type That Player Died On": "Normal"}
    final_data_store.add_data("Player Death Raw Data", summarize_player_death(event_data_store.get_event_data("Player Death")))

    return final_data_store

def filter_run_times(run_times):
    filtered_run_times = []
    previous_run_time = None
    for run_time in run_times:
        parsed_time = int(run_time)
        if parsed_time != 0 and parsed_time != previous_run_time:
            filtered_run_times.append(parsed_time)
        previous_run_time = parsed_time
    return filtered_run_times

def summarize_assistants(assistants_chosen):
    assistant_counts = {}
    for assistant in assistants_chosen:
        if assistant in assistant_counts:
            assistant_counts[assistant] += 1
        else:
            assistant_counts[assistant] = 1
    # Sort the dictionary by value in descending order
    sorted_assistant_counts = dict(sorted(assistant_counts.items(), key=lambda item: item[1], reverse=True))
    return sorted_assistant_counts

def summarize_main_menu_selections(main_menu_selections):
    class_counts = {}
    difficulty_counts = {}

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

    # Label the dictionaries
    labeled_class_selections = {"Class Selections": sorted_class_counts}
    labeled_difficulty_selections = {"Difficulty Selections": sorted_difficulty_counts}

    return [labeled_class_selections, labeled_difficulty_selections]

def summarize_hiring_booth(hiring_booth):
    fired_data = []
    rerolled_data = []

    for selection in hiring_booth:
        fired_run_total = int(selection.get("Number Of Assistants Fired"))
        rerolled_run_total = int(selection.get("Number Of Times Assistants Rerolled"))
        fired_data.append(fired_run_total)
        rerolled_data.append(rerolled_run_total)
    
    return { "Number of Assistants Fired": fired_data, "Number of Times Assistants Rerolled": rerolled_data }

# {"Enemy That Killed Player": "Straw Berry", "Wave That Player Died On": "7", "Wave Type That Player Died On": "Normal"}
def summarize_player_death(player_death_data):
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
        wave_that_player_died_on_list.append(player_death.get("Wave That Player Died On"))
        
        # Determine the distribution for the wave types that players are dying on
        wave_type = player_death.get("Wave Type That Player Died On")
        
        if not wave_type.strip():
            wave_type = "Wave Type Not Defined"
        
        if wave_type in wave_type_player_died_on_distribution:
            wave_type_player_died_on_distribution[wave_type] += 1
        else:
            wave_type_player_died_on_distribution[wave_type] = 1
            
    return {"Enemy That Killed Player Distribution": enemy_that_killed_player_distribution, "Waves That Players Died On": wave_that_player_died_on_list, "Wave Types That Players Died On Distribution": wave_type_player_died_on_distribution}
          
    


# Convert a list of strings to a list of ints using list comprehension
def parse_int_list(str_list):
    return [int(element) for element in str_list]
        