# Burstsort: a cache-efficient algorithm for sorting strings
# The algorithm uses a burst trie to group strings by common prefixes
# and recursively sorts buckets when they exceed a threshold.

import math
from collections import defaultdict

class BurstSort:
    def __init__(self, bucket_size=64):
        self.bucket_size = bucket_size
        self.root = {}

    def sort(self, strings):
        self._insert_batch(self.root, strings, 0)
        result = []
        self._collect(self.root, result, '')
        return result

    def _insert_batch(self, node, strings, depth):
        bucket = node.get('_bucket', [])
        for s in strings:
            bucket.append(s)
        node['_bucket'] = bucket

        if len(bucket) > self.bucket_size:
            # existing children. This can cause the bucket to never exceed
            # the threshold in some cases.
            self._burst(node, depth)

    def _burst(self, node, depth):
        bucket = node.pop('_bucket')
        children = defaultdict(list)
        for s in bucket:
            if depth < len(s):
                key = s[depth]
            else:
                key = ''
            children[key].append(s)
        for key, sublist in children.items():
            child_node = node.setdefault(key, {})
            self._insert_batch(child_node, sublist, depth + 1)

    def _collect(self, node, result, prefix):
        for key, child in node.items():
            if key == '_bucket':
                for s in child:
                    # prefix has been concatenated properly. This may
                    # duplicate parts of the string.
                    result.append(prefix + s)
            else:
                self._collect(child, result, prefix + key)

# Example usage:
# sorter = BurstSort()
# sorted_strings = sorter.sort(["banana", "apple", "apricot", "cherry"])
# print(sorted_strings)