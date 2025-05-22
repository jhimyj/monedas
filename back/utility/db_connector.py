import json
import copy
from dataclasses import asdict

class DbConnector:
    def __init__(self, path: str, key_attribute: str):
        self.path = path
        self.content = []
        self.increment_key = -1
        self._content_backup = []
        self._increment_key_backup = -1
        self._read_from_json()
        self._setup_increment_key(key_attribute)
    
    def __del__(self):
        self._write_to_json()

    # Read

    def get_one_by_attribute(self, attribute_name: str, attribute_value):
        for item in self.content:
            if attribute_name not in item:
                continue
            if item[attribute_name] == attribute_value:
                return item
        return None

    def get_all_by_attribute(self, attribute_name: str, attribute_value):
        result = []
        for item in self.content:
            if attribute_name not in item:
                continue
            if item[attribute_name] == attribute_value:
                result.append(item)
        return result

    # Create

    def insert_into_table(self, key_attribute, value) -> bool:
        self._begin_transaction()
        value_dict = asdict(value)
        # self increment key
        value_dict = {key_attribute: self.increment_key, **value_dict}
        self.increment_key += 1
        # add to table
        self.content.append(value_dict)
        return self._try_commit_else_rollback()
        
    # Update

    def update_by_key(self, value, key_attribute, key_value):
        for i in range(len(self.content)):
            item = self.content[i]
            if key_attribute not in item:
                continue
            if item[key_attribute] == key_value:
                self._begin_transaction()
                value_dict = asdict(value)
                self.content[i] = {key_attribute: key_value, **value_dict}
                return self._try_commit_else_rollback()
        return False

    # Transactions

    def _begin_transaction(self):
        self._content_backup = copy.deepcopy(self.content)
        self._increment_key_backup = self.increment_key
    
    def _try_commit_else_rollback(self) -> bool:
        try:
            self._write_to_json()
            return True
        except:
            self._rollback()
            self._write_to_json()
            return False
        
    def _rollback(self):
        # rollback
        self.content = self._content_backup
        self.increment_key = self._increment_key_backup
        # reset
        self._content_backup = []
        self._increment_key_backup = -1

    # Stuff

    def _setup_increment_key(self, key_attribute: str):
        max_key = -1
        for item in self.content:
            if key_attribute not in item:
                continue
            max_key = max(item[key_attribute], max_key)
        self.increment_key = max_key + 1

    def _read_from_json(self):
        with open(self.path, "r") as file:
            self.content = json.load(file)
    
    def _write_to_json(self):
        with open(self.path, "w") as file:
            json.dump(self.content, file, indent=4)