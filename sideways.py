def PrintSideWays(stringy):
  maxlen= 0
  tokens = stringy.split()

  #Find the longest word in the string (so we know how many times to iterate down)
  for h in tokens:
    if len(h) > maxlen:
      maxlen = len(h)

  #We never actually use the lines variable but it could be used to return the 2d array instead of just print the string
  lines = []


  for i in range(0,maxlen):
    line = []
    for j in range(0,len(tokens)):
      if ((i) >= len(tokens[j])):
        line.append(' ')
      else:
        line.append(tokens[j][i])
    print ' '.join(line)
    lines.append(line)

PrintSideWays("This string is all matrixy. I made this because I got really bored :(")
