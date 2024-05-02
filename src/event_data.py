class EventDataStore:
    def __init__(self):
        self.data = {}
    
    def add_event(self, event_name, event_data):
        if event_name not in self.data:
            self.data[event_name] = []
        self.data[event_name].append(event_data)
    
    def get_event_data(self, event_name):
        return self.data.get(event_name, [])
    
    def get_all_data(self):
        return self.data

