import numpy as np
import pandas as pd

class DataModel:
    def __init__(self) -> None:
        self.data = None
        self.data_stack = []

    def load_data(self, filepath):
        self.data = pd.read_csv(filepath)
    
    def process_data(self):
        self.processed_data = self.data
        return self.processed_data
