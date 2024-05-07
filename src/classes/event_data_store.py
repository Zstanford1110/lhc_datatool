class EventDataStore:
    def __init__(self):
        self.data = {}
        self.game_sessions = []
        self.unique_users = []
    
    # Setter Methods
    def add_event(self, event_name, event_data):
        if event_name not in self.data:
            self.data[event_name] = []
        self.data[event_name].append(event_data)
    
    def add_user(self, user_id):
        self.unique_users.append(user_id)
    
    def add_session(self, session_id):
        self.game_sessions.append(session_id)
        
    # Getter Methods
    def get_user_count(self):
        return len(self.unique_users)
    
    def get_session_count(self):
        return len(self.game_sessions)
        
    def get_event_data(self, event_name):
        return self.data.get(event_name, [])
    
    def get_all_data(self):
        return self.data

