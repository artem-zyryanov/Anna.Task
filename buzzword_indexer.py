import json
import copy


class BuzzwordIndexer:
    STATE_FILE = 'state.json'

    def __init__(self):
        self._state = None

    def load(self):
        with open(self.STATE_FILE) as infile:
            self._state = json.load(infile)

    def persist(self):
        with open(self.STATE_FILE, 'w') as outfile:
            json.dump(self._state, outfile, sort_keys=True, indent=4, separators=(',', ': '))

    def process_item(self, item):
        if not item:
            return
        words_count = self._state['words_count']
        full_text = ''
        if 'text' in item:
            full_text += item['text']
        if 'title' in item:
            full_text += ' ' + item['title']
        for word in words_count:
            words_count[word] += full_text.lower().count(word.lower())
        self._state['total_processed'] += 1
        if not self._state['max_item'] or item['id'] > self._state['max_item']:
            self._state['max_item'] = item['id']
        if not self._state['min_item'] or item['id'] < self._state['min_item']:
            self._state['min_item'] = item['id']

    @property
    def max_item(self):
        return self._state['max_item']

    @property
    def min_item(self):
        return self._state['min_item']

    @property
    def state(self):
        return copy.deepcopy(self._state)
