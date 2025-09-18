#!/usr/bin/env python3
encode_map = str.maketrans({
    'A':'4','a':'4','E':'3','e':'3','I':'1','i':'1','L':'1','l':'1',
    'O':'0','o':'0','T':'7','t':'7','S':'5','s':'5','G':'6','g':'6',
    'B':'8','b':'8','Z':'2','z':'2'
})
decode_map = str.maketrans({
    '0':'O','3':'E','1':'L','7':'T','5':'S',
    '4':'A','6':'G','8':'B','2':'Z'
})

import sys
mode = 'encode'
if len(sys.argv) > 1 and sys.argv[1] in ('encode','decode'):
    mode = sys.argv.pop(1)

text = ' '.join(sys.argv[1:]) or sys.stdin.read().strip()
if mode == 'encode':
    print(text.translate(encode_map))
else:
    print(text.translate(decode_map))
