# TODO: Make directives
#   - .data : Start data segment
#   - .text : Start text segment
#   - .here : Start of current instruction
#   - .next : Start of next instruction

# .here
# .here is the current length of the array of encoded
# instructions. So if it's empty, then it's 0x0.
# If there's a single half-word, then it's 0x1.

# .next
# .next is .here plus the length of the current instruction
# to be encoded. We can figure out the length through:
#   - instructionParseMap for normal instructions
#   - Figuring out the lengths of individual instructions
#       which compose a pseudoinstruction.

# .data
# Switches assembler into data mode.
# Data mode lines are label names, followed by values.
# They count down from the end of the memory. So the first
# defined thing has it's last byte at the end of the memory.
# The second defined thing has it's last byte right before
# the first byte of the first defined thing, and so on.
# They're written in reverse order, with things that are
# defined sooner coming before things that are defined
# later. However, all of those things still have their
# half-words written with earlier half-words having
# lower addresses than later half-words.

# .text
# Swtiches assembler to text mode.
# This mode expects instructions, or labels.

# Pass one:
# Define label values.
# Pass two:
# Replace label values with numeric literals.
# Pass three:
# Assemble file.

