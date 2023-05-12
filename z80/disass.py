#!/usr/bin/env python

import os, sys, re

def main(file):
  for line in open(file):
    line = re.sub('#.*', '', line.strip())
    if not line: continue
    parsed = line.split(' ', 2)
    if ' ' not in line:
      print(f'case {line}:')
      continue
    number, opcode = parsed[:2]
    args = ""
    if len(parsed) >= 3: args = parsed[2]
    if opcode == 'shift':
      print(f'case {number}: return disassemble_{args}(address);')
      continue
    print(f'case {number}: res="<span class=opcode>{opcode}</span>";')
    args = re.sub(r'(REGISTER[HL]?)', r'<span class=register>" + \1 + "</span>', args);
    args = re.sub(r'(AF|BC|DE|HL|SP|PC|IX|IY|(\b[AFBCDEHL]\b))', r'<span class=register>\1</span>', args)
    if 'nnnn' in args:
      pre = args[:args.find('nnnn')]
      post = args[args.find('nnnn') + 4:]
      print(
          f'res += " {pre}" + addressHtml((readbyte(address + 1) << 8) | readbyte(address)) + "{post}"; address += 2;'
      )
    elif 'nn' in args:
      pre = args[:args.find('nn')]
      post = args[args.find('nn') + 2:]
      print(
          f'res += " {pre}0x" + hexbyte(readbyte(address)) + "{post}"; address += 1;'
      )
    elif 'offset' in args:
      pre = args[:args.find('offset')]
      post = args[args.find('offset') + 6:]
      print('var reladdr = address + 1 + sign_extend(readbyte(address));')
      print(f'res += " {pre}" + addressHtml(reladdr) + "{post}"; address += 1;')
    elif 'dd' in args:
      pre = args[:args.find('+dd')]
      post = args[args.find('+dd') + 3:]
      print('var offset = sign_extend(readbyte(address));')
      print('var sign = offset > 0 ? "+" : "-";')
      print(
          f'res += " {pre}" + sign + "0x" + hexbyte(offset) + "{post}"; address += 1;'
      )
    elif opcode == 'RST':
      print(f'res += " " + addressHtml(0x{args});')
    elif args:
      print(f'res += " {args}";')
    print("break;")

if __name__ == '__main__':
  main(sys.argv[1])

