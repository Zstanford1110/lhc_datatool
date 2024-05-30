import json
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
from classes.report import Report, ReportSection

def draw_figure(canvas, fig, x, y, width, height):
    fig_bytes = BytesIO()
    fig.savefig(fig_bytes, format='png')
    fig_bytes.seek(0)
    canvas.drawImage(fig_bytes, x, y, width, height)
    fig_bytes.close()

def generate_report(data):
    with open('../resources/data_schema.json', 'r') as schema_file:
        data_schema = json.load(schema_file)
    
    # Generate and organize the report data using ReportSection and Report classes
    report = Report()

    section_handlers = {
        "General Analytics Data": general_analytics,
        "Run Data": run_analytics,
        "Assistant Data": assistant_analytics,
        "Menu Selection Data": menu_analytics,
        "Wave Reveal Data": wave_reveal_analytics,
        "Hiring Booth Data": hiring_booth_analytics,
        "Player Death Data": death_analytics,
        "Wave Breakdown Data": wave_breakdown_analytics,
        "Weapon Data": weapon_analytics,
    }


    # Generate report sections to order, adding them to the Report as completed, send Report to export_pdf to draw file
    for section_name in data_schema:
        section_data = data.get_data(section_name)

        # Validate if valid section
        if section_data is None:
            print(section_name + " is not a valid section in the data schema.")
        
        handler = section_handlers.get(section_name)

        # Validate if valid handler
        if handler:
            handler(report, section_data)

    export_pdf(report)
    

# ReportSection generator functions
def general_analytics(report, analytics_data):
    # Generate charts, statistics, and store them
    section = ReportSection("General Analytics Data", "Data for Users and Session")

    # General Analytics Statistics
    section.add_statistic("Unique Users", analytics_data['User Count'])
    section.add_statistic("Unique Sessions", analytics_data['Session Count'])

    report.add_section(section)

def run_analytics(report, run_data):
    section = ReportSection("Run Data", "Data for runs")

    run_boxplot = create_boxplot("Run Duration Overview", "Run Duration (seconds)", run_data['Run Times'], 10, 2)
    section.add_figure(run_boxplot, 500, 100)
    
    boss_names = list(run_data['Bosses Killed Distribution'].keys())
    kill_frequency = list(run_data['Bosses Killed Distribution'].values())
    
    bosses_killed_distribution = create_barchart("Bosses Killed Distribution", "Boss", "Times Killed", boss_names, kill_frequency, 8, 6)
    section.add_figure(bosses_killed_distribution, 400, 300)

    section.add_statistic("Total Runs Started", run_data['Total Runs'])
    section.add_statistic("Average Run Duration", run_data['Average Run Time'])

    report.add_section(section)

def assistant_analytics(report, assistant_data):
    section = ReportSection("Assistant Data", "Data for Assistant Selection")

    # Extract Assistant Data
    assistant_names = list(assistant_data['Assistant Selection Distribution'].keys())
    frequencies = list(assistant_data['Assistant Selection Distribution'].values())


    assistant_distribution = create_barchart("Assistant Hiring Distribution", "Assistant Type", "Frequency", assistant_names, frequencies, 10, 6)
    section.add_figure(assistant_distribution, 500, 300)

    section.add_statistic("Total Assistants Hired", assistant_data['Total Assistants Hired'])

    report.add_section(section)

def menu_analytics(report, menu_data):
    section = ReportSection("Main Menu Data", "Data relating to menu selections when starting a run")

    class_names = list(menu_data['Class Selections'].keys())
    class_selections = list(menu_data['Class Selections'].values())

    class_distribution = create_barchart("Class Selection Distribution", "Class", "Frequency", class_names, class_selections, 8, 6)

    difficulty_names = list(menu_data['Difficulty Selections'].keys())
    difficulty_selections = list(menu_data['Difficulty Selections'].values())

    difficulty_distribution = create_barchart("Difficulty Selection Distribution", "Difficulty", "Frequency", difficulty_names, difficulty_selections, 8, 6)
    
    section.add_figure(class_distribution, 400, 300)
    section.add_figure(difficulty_distribution, 400, 300)

    report.add_section(section)
    
def wave_reveal_analytics(report, reveal_data):
    section = ReportSection("Wave Reveal Data", "Data relating to the player choosing to reveal upcoming wave information")
    
    reveal_boxplot = create_boxplot("Wave Reveal Overview", "Number of Waves Revealed (Per Run)", reveal_data['Waves Revealed Raw Data'], 10, 2)
    section.add_figure(reveal_boxplot, 500, 100)
    
    section.add_statistic("Average Waves Revealed", reveal_data['Average Waves Revealed'])
    section.add_statistic("Total Waves Revealed", reveal_data['Total Waves Revealed'])

    report.add_section(section)
    
def hiring_booth_analytics(report, hiring_data):
    section = ReportSection("Hiring Booth Data", "Data relating to decisions made by the player in the hiring booth menu")
    
    section.add_statistic("Total Assistants Fired", hiring_data['Total Number of Assistants Fired'])
    section.add_statistic("Average Assistants Fired (All Runs)", hiring_data['Average Assistants Fired'])
    section.add_statistic("Total Assistant Rerolls", hiring_data['Total Number of Assistant Rerolls'])
    section.add_statistic("Average Assistant Rerolls (All Runs)", hiring_data['Average Assistant Rerolls'])
    
    report.add_section(section)
    
def death_analytics(report, death_data):
    section = ReportSection("Player Death Data", "Data relating to a player death and end of a run")
    
    enemy_type, death_frequency = extract_keys_values(death_data['Enemy That Killed Player Distribution']) 
    enemy_death_distribution = create_barchart("Enemy that Killed Player Distribution", "Enemy Type", "Player Deaths", enemy_type, death_frequency, 8, 6)
    section.add_figure(enemy_death_distribution, 400, 300)
    
    wave_type, wave_type_death_frequency = extract_keys_values(death_data['Wave Types That Players Died On Distribution'])
    wave_type_death_distribution = create_barchart("Wave Types Players Died On Distribution", "Wave Type", "Player Deaths", wave_type, wave_type_death_frequency, 8, 6)
    section.add_figure(wave_type_death_distribution, 400, 300)
    
    player_death_distribution = create_boxplot("Player Death Distribution (By Wave)", "Wave Number", death_data['Waves That Players Died On'], 10, 2)
    section.add_figure(player_death_distribution, 500, 100)
    
    section.add_statistic("Average Wave Reached Before Death", death_data['Average Wave Reached Before Death'])
    section.add_statistic("Highest Wave Reached", death_data['Highest Wave Reached'])
    
    report.add_section(section)

def wave_breakdown_analytics(report, breakdown_data):
    section = ReportSection("Wave Breakdown Data", "Data relating to different wave characteristics")

    wave_number_distribution = create_barchart(
        "Wave Number Distribution", 
        "Wave Number", 
        "Occurrences", 
        list(breakdown_data['Wave Number Distribution'].keys()), 
        list(breakdown_data['Wave Number Distribution'].values()), 
        8, 6,
        annotate=False  # Disable annotations
    )
    section.add_figure(wave_number_distribution, 400, 300)

    wave_type_distribution = create_barchart(
        "Wave Type Distribution", 
        "Wave Type", 
        "Occurrences", 
        list(breakdown_data['Wave Type Distribution'].keys()), 
        list(breakdown_data['Wave Type Distribution'].values()), 
        8, 6
    )
    section.add_figure(wave_type_distribution, 400, 300)

    enemy_group_distribution = create_horizontal_barchart(
        "Enemy Group Distribution", 
        "Occurrences", 
        "Enemy Group", 
        list(breakdown_data['Enemy Group Distribution'].keys()), 
        list(breakdown_data['Enemy Group Distribution'].values()), 
        8, 6
    )
    section.add_figure(enemy_group_distribution, 400, 300)

    report.add_section(section)

def weapon_analytics(report, weapon_data):
    section = ReportSection("Weapon Data", "Data relating to weapon choices and modifications")

    weapon_chosen_distribution = create_horizontal_barchart(
        "Weapon Chosen Distribution", 
        "Frequency", 
        "Weapon Name", 
        list(weapon_data['Weapon Chosen Distribution'].keys()), 
        list(weapon_data['Weapon Chosen Distribution'].values()), 
        10, 6
    )
    section.add_figure(weapon_chosen_distribution, 500, 300)

    section.add_statistic("Average Weapon Rerolls", weapon_data['Average Weapon Rerolls'])
    section.add_statistic("Average Weapon Combines or Sells", weapon_data['Average Weapon Combines or Sells'])

    report.add_section(section)
    
    
    
def export_pdf(report):
    c = canvas.Canvas("report.pdf", pagesize=letter)
    c.setTitle("Let Him Cook Data")
    
    # Set initial cursor position
    y_position = 750
    
    # Draw the title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, y_position, "Let Him Cook Data")
    y_position -= 50  # Move down for the first section
    
    # Iterate through sections in the report
    for section in report.sections:
        c.setFont("Helvetica-Bold", 14)
        c.drawString(72, y_position, section.title)
        y_position -= 20
        
        c.setFont("Helvetica", 12)
        for stat_title, stat_value in section.statistics.items():
            c.drawString(72, y_position, f"{stat_title}: {stat_value}")
            y_position -= 15

        for figure in section.figures:
            figure_obj, fig_width, fig_height = figure
            # Check if there's enough space for the figure on the current page
            if y_position - fig_height < 50:
                c.showPage()
                y_position = 750  # Reset y_position for new page
            
            # Draw the figure on the canvas
            c.drawImage(ImageReader(figure_obj), 72, y_position - fig_height, fig_width, fig_height)
            draw_figure(c, figure_obj, 72, y_position - fig_height, fig_width, fig_height)  # Adjust width and height as needed
            y_position -= fig_height # Adjust space after figure

        # Check if there's enough space to continue on this page
        if y_position < 200:
            c.showPage()
            y_position = 750  # Reset y_position for new page
        else:
            y_position -= 30
    
    c.save()
    

def draw_figure(canvas, fig_buffer, x, y, width, height):
    canvas.drawImage(ImageReader(fig_buffer), x, y, width, height)

def create_boxplot(title, xlabel, data, w, h):
    # Scale up the figure size for better visibility
    plt.figure(figsize=(w, h))
    # Create a boxplot with a custom color palette
    box = plt.boxplot(data, vert=False, patch_artist=True, boxprops=dict(facecolor='lightblue', color='darkblue'), showfliers=True)

    # Annotate the median
    for median_line in box['medians']:
        median = median_line.get_ydata()[0]
        median_value = median_line.get_xdata()[0]
        plt.text(median_value, median + 0.3, f'Median: {median_value}', verticalalignment='center', fontsize=10, color='red')

    # Annotate the whiskers
    for whisker in box['whiskers']:
        whisker_top = whisker.get_ydata()[0]
        whisker_value = whisker.get_xdata()[1]
        plt.text(whisker_value, whisker_top + 0.1, f'{whisker_value}', verticalalignment='center', fontsize=10, color='blue')

    # Annotate the outliers
    if 'fliers' in box and len(box['fliers'][0].get_data()[1]) > 0:
        for flier in box['fliers']:
            outliers = flier.get_data()
            for j in range(len(outliers[0])):
                plt.text(outliers[0][j], outliers[1][j] + 0.2, f'{outliers[0][j]}', verticalalignment='center', fontsize=10, color='green')

    plt.title(title, fontsize=14)
    plt.xlabel(xlabel, fontsize=12)
    plt.gca().yaxis.set_visible(False)
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(10))
    # Set the background color of the plot for better contrast
    plt.gca().set_facecolor('lightgrey')
    plt.grid(True, linestyle='--', linewidth=0.5, color='black')  # Add grid lines for better readability

    plt.tight_layout(pad=2.0)
    plt.subplots_adjust(bottom=0.4)

    # Save the current figure and clear it so that plt does not render the same figure everytime
    fig = plt.gcf()
    buf = BytesIO()
    fig.savefig(buf, format='png')
    plt.clf()
    buf.seek(0)
    return buf

def create_barchart(title, x_label, y_label, x_data, y_data, w, h, annotate=True):
    plt.figure(figsize=(w, h))
    bars = plt.bar(x_data, y_data, color='skyblue')

    if annotate:
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.2f}', verticalalignment='bottom', fontsize=10, color='darkblue')

    plt.title(title, fontsize=14)
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.xticks(rotation=45, ha='right')

    plt.gca().set_facecolor('lightgrey')
    plt.grid(True, linestyle='--', linewidth=0.5, color='black')

    plt.tight_layout(pad=2.0)
    plt.subplots_adjust(bottom=0.4)

    fig = plt.gcf()
    buf = BytesIO()
    fig.savefig(buf, format='png')
    plt.clf()
    buf.seek(0)
    return buf

def create_horizontal_barchart(title, x_label, y_label, x_data, y_data, w, h, annotate=True):
    plt.figure(figsize=(w, h))
    bars = plt.barh(x_data, y_data, color='skyblue', height=0.5)  # Adjust bar height for spacing

    if annotate:
        for bar in bars:
            yval = bar.get_width()
            plt.text(yval, bar.get_y() + bar.get_height()/2, f'{yval:.2f}', horizontalalignment='left', fontsize=10, color='darkblue')


    plt.title(title, fontsize=14)
    plt.xlabel(x_label, fontsize=12)
    plt.ylabel(y_label, fontsize=12)
    plt.gca().set_facecolor('lightgrey')
    plt.grid(True, linestyle='--', linewidth=0.5, color='black')

    plt.tight_layout(pad=2.0)
    plt.subplots_adjust(left=0.3)  # Adjust the left margin to make room for labels

    fig = plt.gcf()
    buf = BytesIO()
    fig.savefig(buf, format='png')
    plt.clf()
    buf.seek(0)
    return buf

def extract_keys_values(data):
    keys = list(data.keys())
    values = list(data.values())
    return keys, values    
