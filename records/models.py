import uuid


class Record:
    def __init__(self, records):
        self.records = records

    def to_dict(self):
        return vars(self)
    
    @staticmethod
    def schema():
        return ['rid','name', 'records','type']