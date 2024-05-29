class ReportSection:
    def __init__(self, title, description):
        self.title = title
        self.description = description
        self.figures = []
        self.statistics = {}

    def add_figure(self, figure, width, height):
        self.figures.append((figure, width, height))

    def add_statistic(self, key, value):
        self.statistics[key] = value

class Report:
    def __init__(self):
        self.sections = []

    def add_section(self, section):
        self.sections.append(section)