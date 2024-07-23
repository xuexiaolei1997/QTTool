class DataController:
    def __init__(self, model, view) -> None:
        self.model = model
        self.view = view
    
    def process_data(self):
        self.model.