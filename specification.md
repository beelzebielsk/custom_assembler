# Purpose

This is an assembler. It will take human readable instructions, then
encode them into machine code.  It will output these encoded
instructions in a Quartus MIF file, so that they can be loaded onto a
memory.

# Future

I may need assemblers for other chips or languages too. My hope is to
make the encoding and instruction formats completely separate from the
actual encoding logic itself. The logic would just take directions
from the encoding and instructions formats, then use those
instructions to turn assembly instructions into machine code.

---
vim:tw=70
---
