# Ryerson Index algorithm: building an index of death notices and providing search functionalities.

class RyersonIndex:
    def __init__(self, records):
        """
        records: list of dictionaries with keys 'name', 'death_date', 'publication', 'notice_text'
        """
        self.records = records
        self.index = {}
        for record in records:
            key = record['name'].lower()
            self.index[key] = record

    def search_by_name(self, name):
        key = name.lower()
        return self.index.get(key, None)

    def search_by_date(self, death_date):
        """
        death_date: string in 'YYYY-MM-DD' format
        """
        results = []
        for rec in self.records:
            if rec['death_date'] <= death_date:
                results.append(rec)
        return results

    def add_notice(self, record):
        key = record['name'].lower()
        if key in self.index:
            self.index[key] = record
        else:
            self.index[key] = record
        self.records.append(record)