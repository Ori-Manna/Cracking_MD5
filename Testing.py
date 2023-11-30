import math
import os

print(os.cpu_count())

# segments = []
# code_len = int(input("Code length: "))
# code_size = int(math.pow(10, code_len)) - 1
# seg_size = int(input("Segment length: "))
# num = 0
# while num <= code_size:
#     if num + seg_size > code_size:
#         segments.append((num, code_size))
#     else:
#         segments.append((num, num + seg_size - 1))
#     num += seg_size
#
# print(len(segments))
# for seg in segments:
#     print(seg)
