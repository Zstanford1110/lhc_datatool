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
        "Run Data": run_analytics
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

    # convert run times to HH:MM:SS for the box plot

    run_boxplot = create_boxplot("Run Duration Overview", "Run Duration (seconds)", run_data['Run Times'], 10, 2)
    section.add_figure(run_boxplot)

    section.add_statistic("Total Runs Started", run_data['Total Runs'])
    section.add_statistic("Average Run Duration", run_data['Average Run Time'])

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
            if y_position < 320:
                c.showPage()
                y_position = 750
            draw_figure(c, figure, 72, y_position - 300, 400, 300)  # Adjust width and height as needed
            y_position -= 310  # Adjust space after figure
        
        # Check if there's enough space to continue on this page
        if y_position < 50:
            c.showPage()
            y_position = 750  # Reset y_position for new page
        else:
            y_position -= 30
    
    c.save()
    
    

def draw_figure(canvas, fig, x, y, width, height):
    fig_bytes = BytesIO()
    fig.savefig(fig_bytes, format='png')
    fig_bytes.seek(0)
    canvas.drawImage(ImageReader(fig_bytes), x, y, width, height)
    fig_bytes.close()

def create_boxplot(title, xlabel, data, w, h):
    # Scale up the figure size for better visibility
    plt.figure(figsize=(w, h))
    # Create a boxplot with a custom color palette
    box = plt.boxplot(data, vert=False, patch_artist=True, boxprops=dict(facecolor='lightblue', color='darkblue'))
    plt.title(title, fontsize=14)
    plt.xlabel(xlabel, fontsize=12)
    plt.gca().yaxis.set_visible(False)
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(10))
    # Set the background color of the plot for better contrast
    plt.gca().set_facecolor('lightgrey')
    plt.grid(True, linestyle='--', linewidth=0.5, color='black')  # Add grid lines for better readability
    return plt
