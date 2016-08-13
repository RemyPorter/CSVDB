from .structures.trie import Item
class Bucket:
    def __init__(self, name):
        self.name = name
        self._data = Item(name)

    def create(self, row):
        self._data.append(row)

    def read(self, query_row):
        return self._data.search(query_row)

    def update(self, query_row, new_data):
        self._data.remove(query_row)
        self._data.append(new_data)

    def delete(self, query_row):
        self._data.remove(query_row)
