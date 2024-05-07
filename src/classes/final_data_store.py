class FinalDataStore:
    def __init__(self):
        self.data = {}
        self.game_sessions = []
        self.unique_users = []
    
    def add_data(self, data_label, data):
        if data_label not in self.data:
            self.data[data_label] = data

    def update_data(self, data_label, data):
        if data_label in self.data:
            self.data[data_label] = data

    def get_data(self, data_label):
        return self.data.get(data_label, [])
    
    def get_all_data(self):
        return self.data