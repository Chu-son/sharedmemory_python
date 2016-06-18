import mmap
import struct

map = mmap.mmap(-1, 1000,"testmap")
map.seek(12)
print(struct.unpack("i",map.read(4)))

# close the map
map.close()