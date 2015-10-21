
def number_generator_maker():
    n = -1
    while True:
        n += 1
        yield n

numbers = number_generator_maker()

if __name__ == "__main__":
  import sys
  up_to = int(sys.argv[1])
  while True:
    n = numbers.next()
    if n > up_to:
      break
    else:
      print n
