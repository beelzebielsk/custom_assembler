##################################################
## PREAMBLE: {{{
##################################################

import custom_assembler

##################################################
## }}}
##################################################

#print "original examples:"
#for example in examples:
#    print '\t|', example
#
#print "With whitespace condensed:"
#for example in examples:
#    print '\t|', whitespace.sub(' ', example);
#
##print "examples are unchanged after strip:"
##for example in examples:
##    print '\t|', example
#
#print "Instructions on each line:"
#for example in examples:
#    print '\t|', extractInstruction.match(example).group(1).lower();
#
#print "Parsing instructions:"
#for example in examples:
#    print '\t|' ,example;
#    print '\t|', parseInstruction(example);
#
## instruction: 0000 0 {opcode} {register_x_bin_string, 3} {register_y_bin_string, 3}
#
