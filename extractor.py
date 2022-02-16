import typing
import re

wordWild = r"[~～～]"

def loadRawCSV(path : str):
  ret = []
  with open(path,encoding='utf-8',mode='r') as raw_file:
    for line in raw_file.readlines():
      ret.append(line.strip().split(","))
  return ret

def containWordWild(input : str):
  return re.search(wordWild,input) is not None
def locateWordLine(lines: typing.List[str]):
  ret = []
  for line in lines:
    dsc = line[2]
    if containWordWild(dsc):
      ret.append(line)
  return ret
  
def posWordInLine(line:str):
  return list(res.start() for res in re.finditer(wordWild,line))

# 先 define 啲 helper，然後寫一個提詞方法
def isCJK(char : str):
  utfcode = ord(char.encode("utf-8").decode())
  cpr = []
  # regular
  cpr.append((0x4E00,0x9FFF))
  # ExtA
  cpr.append((0x3400,0x4DBF))
  # ExtB
  cpr.append((0x20000,0x2A6DF))
  # ExtC
  cpr.append((0x2A700,0x2B73F))
  # ExtD
  cpr.append((0x2B740,0x2B81F))
  # ExtE
  cpr.append((0x2B820,0x2CEAF))
  # ExtF
  cpr.append((0x2CEB0,0x2EBEF))
  # ExtG
  cpr.append((0x30000,0x3134F))
  return any(cmp[0] <= utfcode <= cmp[1] for cmp in cpr)

# 寫切詞方法
def splitWord(line:str):
  def traverseUntilNotCJK(line:str,start_pos :int,direction : int, len_limit = 3):
    cur_pos = start_pos
    should_skip = lambda char : not containWordWild(char) and not isCJK(char)
    for i in (range(start_pos,len(line),1) if direction > 0 else range(start_pos,0,-1)):
      char = line[i] 
      cur_pos = i
      if should_skip(char):
        break
      if(len_limit == 0):
        break
      len_limit -= 1
    if should_skip(line[cur_pos]) and direction < 0:
      cur_pos += 1
    if cur_pos == len(line) - 1 and not should_skip(line[cur_pos]):
      cur_pos += 1  # definetly would out of bound
    return cur_pos
  
  ret = []
  if(type(line) != str):
    return ret
  pos = posWordInLine(line)
  for eachPos in pos:
    left_bound = right_bound = eachPos
    left_bound = traverseUntilNotCJK(line,left_bound,-1)
    right_bound = traverseUntilNotCJK(line,right_bound,1)
    word = line[left_bound:right_bound]
    ret.append(word)
  return ret

def demo():
  raw_data = loadRawCSV("faanjyutExport.csv")
  ele_with_words = locateWordLine(raw_data)


  for ele in ele_with_words:
    line = ele[2]
    single_char = ele[0]
    pron = ele[1]
    words_in_line = splitWord(line)
    if(len(words_in_line) == 0):
      continue
    print(single_char,words_in_line)

demo()