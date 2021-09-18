def dictionary(file, dic):
  for line in file:
    key, value = line.rstrip('\n').split('=')

    dic[key] = value
  
  return dic
