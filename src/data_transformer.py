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
    final_data_store.add_data("Run Times", filter_runtimes(event_data_store.get_event_data('Amount Of Time Per Run')))
    final_data_store.add_data("Average Run Time", mean(final_data_store.get_data("Run Times")))

    # Assistant Selection statistics
    final_data_store.add_data("Total Assistant Hires", len(event_data_store.get_event_data("Assistant Chosen")))
    final_data_store.add_data("Assistant Selection Distribution", summarize_assistants(event_data_store.get_event_data("Assistant Chosen")))

    # Main Menu Selectrions statistics
    final_data_store.add_data("Total Runs Started", len(event_data_store.get_event_data("Main Menu Selections")))
    final_data_store.add_data("Menu Selection Distribution", summarize_main_menu_selections(event_data_store.get_event_data("Main Menu Selections")))

    # Wave Reveal / Run Length statistics
    final_data_store.add_data("Waves Revealed", filter_waves_revealed(event_data_store.get_event_data('Number Of Waves Revealed')))
    final_data_store.add_data("Average Waves Revealed", mean(final_data_store.get_data('Waves Revealed')))

    return final_data_store

def filter_runtimes(run_times):
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

def filter_waves_revealed(waves_revealed):
    filtered_reveals = []
    for revealed in waves_revealed:
        parsed_revealed = int(revealed)
        if parsed_revealed != 0:
            filtered_reveals.append(parsed_revealed)
    return filtered_reveals