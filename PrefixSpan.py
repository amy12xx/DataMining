'''
Algorithm for PrefixSpan
---------------------------------------------------------------------------
1. Get count of each item by counting the # of sequences it has occurred in.
2. Build prefix tree for each frequent item: remove first occurrence of frequent item, along with all preceding items from sequence.
3. Find freq of item and each item of prefix tree, and select only those more frequent than min. support
      
'''

from collections import OrderedDict, Counter, deque

class PrefixSpan:
  def __init__(self, data, support):
    self.data = data
    self.support = support
    self.total_items = len(self.data)
    self.freq_items = []
    self.seq_patterns = {}
    print 'about data: ', self.support, self.total_items
    
  def get_frequent_items(self, data, seq_item):
    
    items_list = Counter()

    all_items_arr = []

    for row in data:
      items_arr2 = []
      for items in row:
        if type(items) is tuple:
          for i in items:
            items_arr2.append(i)
        else:
          items_arr2.append(items)

      for items in set(items_arr2):
        items_list[items] += 1
      
      all_items_arr.append(items_arr2)


    freq_items = dict(filter(lambda (k,v): float(v)/float(self.total_items) > self.support, items_list.iteritems()))
    # print len(freq_items)

    new_dict = dict()
    for k,v in freq_items.iteritems():
      patt = seq_item
      if patt:
        patt = list(patt)
        patt.append(str(k))
        patt = tuple(patt)
        new_dict[patt] = v
      else:
        new_dict[k] = v

    self.seq_patterns.update(new_dict)
    return freq_items, all_items_arr

  def get_projected_db(self, item, data):
    # print
    # print 'Get projected db for : ', item
    proj_db = []

    for row in data:
      que = deque(row)
      for val in row:
        if item != val:
          _ = que.popleft()
        else:
          _ = que.popleft()
          break
      
      if list(que):
        proj_db.append(list(que))
    
    return proj_db


  def get_seq_patterns(self, data, items):
    frequent_items, all_items_arr = self.get_frequent_items(data, items)
    if frequent_items:
      self.freq_items.append(frequent_items)

    for item, _ in frequent_items.iteritems():
      proj_db = self.get_projected_db(item, all_items_arr)
      if proj_db:
        self.get_seq_patterns(proj_db, items + [item])

# Main program
def main():
  # toy datasets to test on
  # data = [[('bread','milk'),'one','two', 'one'],['three','four', 'one'],['five','dog','two'],['three','five','two'],['milk',('two','one')]]
  data = [['C', 'D'], ['A', 'B', 'C'], ['A', 'B', 'F'],['A', 'C', 'D', 'F'], ['A', 'B', 'F'], ['E'],['A','B','F'],['D','G','H'],['B','F'],['A','G','H']]

  p = PrefixSpan(data, 0.2)
  p.get_seq_patterns(data, [])

  print p.seq_patterns

if __name__ == '__main__':
  main()