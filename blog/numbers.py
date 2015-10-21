import sys

def number_generator_maker():
  n = -1
  while True:
    n += 1
    yield n

#numbers = number_generator_maker()

class Numbers(object):
  def __init__(self):
    self.gen = number_generator_maker()
  
  def next(self):
    if sys.version_info[0] <= 2:
      return self.gen.next()
    else:
      return self.gen.__next__()


if __name__ == "__main__":
  up_to = int(sys.argv[1])
  while True:
    if sys.version_info[0] <= 2:
      n = numbers.next()
    else:
      n = numbers.__next__()
    if n > up_to:
      break
    else:
      print (n)
