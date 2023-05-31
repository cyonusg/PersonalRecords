import csv
import json
import os
from records.models import Record

class RecordService:

    def __init__(self, table_name):
        self.table_name = table_name

    def create(self, record):
        with open(self.table_name, mode='w') as f:
            json.dump(record.to_dict()["records"], f)

    def lists(self):
        with open(self.table_name) as f:
            # Opening JSON file
            f = open(self.table_name)
            data = json.load(f)
            return data
        
    def delete_client(self, record_id):
        records = self.lists()
        updated_rows = [row for row in records if row['uid'] != record_id]
        self._save_to_disk(updated_rows)


        self._save_to_disk(updated_rows)

    def _save_to_disk(self,clients):
        tmp_table_name = self.table_name + '.tmp'
        with open(tmp_table_name, mode='w') as f:
             writer = csv.DictWriter (f, fieldnames=Record.schema())
             writer.writerows(clients)

        os.remove(self.table_name)
        os.rename(tmp_table_name, self.table_name)
