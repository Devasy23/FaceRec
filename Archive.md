```python
# Mock simulation of MongoDB collection
class MockMongoCollection:
    def __init__(self):
        self.data = {}

    def insert_one(self, document):
        # Simulate insert operation
        self.data[document["EmployeeCode"]] = document

    def find(self):
        # Simulate find operation
        return self.data.values()

    def find_one(self, filter):
        # Simulate find_one operation
        return self.data.get(filter["EmployeeCode"])

    def find_one_and_delete(self, filter):
        # Simulate find_one_and_delete operation
        return self.data.pop(filter["EmployeeCode"], None)

    def update_one(self, filter, update):
        # Simulate update_one operation
        employee = self.data.get(filter["EmployeeCode"])
        if employee:
            employee.update(update["$set"])
            return MagicMock(modified_count=1)
        return MagicMock(modified_count=0)

```