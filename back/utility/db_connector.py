import json
import copy

class DbConnector:
    def __init__(self, path: str):
        self.path = path
        self.content = []
        self._content_backup = []
        self._read_from_json()
    
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

    def get_many_by_attribute(self, attribute_name: str, attrbiute_value):
        result = []
        for item in self.content:
            if attribute_name not in item:
                continue
            if item[attribute_name] == attrbiute_value:
                result.append(item)
        return result

    # Create

    def insert_into_table(self, value) -> bool:
        self._begin_transaction()
        self.content.append(value.__dict__)
        return self._try_commit_else_rollback()
        
    # Update

    def update_one_by_attribute(self, value, attribute_name, attribute_value):
        for i in range(len(self.content)):
            item = self.content[i]
            if attribute_name not in item:
                continue
            if item[attribute_name] == attribute_value:
                self._begin_transaction()
                self.content[i] = value.__dict__
                return self._try_commit_else_rollback()
        return False

    # Stuff

    def _begin_transaction(self):
        self._content_backup = copy.deepcopy(self.content)
    
    def _try_commit_else_rollback(self) -> bool:
        try:
            self._write_to_json()
            self._content_backup = []
            return True
        except:
            self.content = self._content_backup
            self._content_backup = []
            self._write_to_json()
            return False
        
    def _rollback(self):
        self._content_backup = []

    def _read_from_json(self):
        with open(self.path, "r") as file:
            self.content = json.load(file)
    
    def _write_to_json(self):
        with open(self.path, "w") as file:
            json.dump(self.content, file, indent=4)