#!/usr/bin/python2

##################################################
## Starting Notes : {{{
##################################################

# First, create a set of common tokens:
# - Instructions: first word of a line
# - Registers
# - Character literal
# - Number literal

# Then, use an associative map to map instruction names to opcodes to
# place in the instruction.

# Then, use opcode/instruction to map to a way to parse the
# instruction. I can create the parsing out of parsable pieces, which
# I think are called tokens. For example, I could register/register
# functions take the following form:
#   {register}, {register}
# I can have the move/add immediate instructions take the following
# form:
#   {register}, {literal}

# Then, use the opcode/instruction name to map that to a list of
# steps to take for encoding the instruction.
# Example: Register-to-Register
#   0x0 {instruction: XXXX XXXi iixx xyyy }
# Example: Immediate-to-register
#   0x0 {instruction: XXXX XXXi iixx xyyy }
#   0x1 {immediate}

# DONE: Create instruction map
# DONE: Create parse map
# DONE: Create encoding map
# TODO: Create parsing error detection.

##################################################
## }}}
##################################################

import re;

####################################################
## Assembler Controls: {{{
####################################################

# Sets the highest register index, so that I can't
# try to access registers that don't exist.
NUM_REGISTERS = 8;

# The difference in location between each encoded piece of 
# information. In a normal processor, it would be 1 for each
# byte. Here, it's 1 for each half-word (2 bytes).
ADDRESS_SEPARATOR = 1;
MEMORY_DEPTH = 256; # 256 separate addresses.
MEMORY_WIDTH = 16 # 16 bit memory locations.
MAX_LITERAL_VALUE = 2**MEMORY_WIDTH - 1;

memory = [];

####################################################
## }}}
####################################################

####################################################
## Tokens : {{{
####################################################

# For condensing all whitespace into a single space, which
# will make parsing directions for instructions easier to
# create.
whitespace = re.compile('\s+');

# Regular expression for extracting an instruction
extractInstruction = re.compile('^\s*(\w+)', re.IGNORECASE);

####################################################
## }}}
####################################################

####################################################
## Tables : {{{
####################################################

instructions = {
    'mv'     : '000',
    'mvi'    : '001',
    'add'    : '010',
    'sub'    : '011',
};

# Contains a capture which specifies the information
# that a parsing function would need to return a value.
tokens = {
    'register' : re.compile('\$(\d+)'),
    'literal_hex' : re.compile('0[xX]([\da-fA-F]+)'),
    'literal_char' : re.compile("'(\w)'"),
    'literal_decimal' : re.compile('\d+'),
    'literal_binary' : re.compile('[bB]([01]+)'),
};

def parseNumericLiteral(match_string):
    returnValue = 0;
    if tokens['literal_hex'].match(match_string):
        returnValue =  tokenParse['literal_hex'](match_string);
    elif tokens['literal_binary'].match(match_string):
        returnValue =  tokenParse['literal_binary'](match_string);
    elif tokens['literal_decimal'].match(match_string):
        returnValue =  tokenParse['literal_decimal'](match_string);
    elif tokens['literal_char'].match(match_string):
        returnValue =  tokenParse['literal_char'](match_string);
    if returnValue > MAX_LITERAL_VALUE:
        raise SyntaxError("Literal " + match_string + " is larger than " + str(MAX_LITERAL_VALUE) );
    else:
        return returnValue;

def parseRegister( match_string):
    reg_num = int( tokens['register'].match(match_string).group(1), 10);
    if reg_num > NUM_REGISTERS:
        raise SyntaxError("Register " + match_string + " does not exist. " \
                "Largest regsiter index is " + str(NUM_REGISTERS - 1) + ".");
    else:
        return reg_num;

tokenParse = {
    'register' : 
        parseRegister,
    'literal_hex' :
        lambda match_string: int( tokens['literal_hex'].match(match_string).group(1), 16),
    'literal_decimal' :
        lambda match_string: int( tokens['literal_decimal'].match(match_string).group(0), 10),
    'literal_binary'  :
        lambda match_string: int( tokens['literal_binary'].match(match_string).group(1), 2),
    'literal_char'    :
        lambda match_string: int( tokens['literal_char'].match(match_string).group(1), 2),
    'numeric_literal' :
        parseNumericLiteral,
};

# The {} enclosed names refer to tokens in the tokens dictionary.
# This allows me to quickly specify the format of an instruction
# and it's arguments.
# These are going to be lists of tuples. They will exactly specify how to build
# the instruction.
# Provided information:
#   - A list of lists.
#        - Each sublist specifies how to build
#           one half-word of the instruction.
#        - There is one sublist per half-word.
#   - How to build each half-word: a tuple
#       - Argument Type to Parse
#       - Width in bits of parsed result.
# Example: '001' (mvi) : [2, [ (opcode, 10), (register, 3), "000" ], [ (numeric_literal, 16) ] ]
# The order that these tokens appear in these tuples
# is the order that these tokens are expected to appear in the
# argument list.

instructionParseMap = {
    '000' : [ [ ("opcode", 10), ("register", 3), ("register", 3) ] ],
    '001' : [ 
                [ ("opcode", 10), ("register", 3), "000" ], 
                [ ("numeric_literal", 16) ] 
            ],
    '010' : [ [ ("opcode", 10), ("register", 3), ("register", 3) ] ],
    '011' : [ [ ("opcode", 10), ("register", 3), ("register", 3) ] ],
};

    # '010' : ["register" , "register"]        ,
    # '011' : ["register" , "register"]        ,

# Returns an encoded instruction to place into memory.
# Not all instructions are of the same length, so some
# instructions will take more than one data word
# (these are currently half-words (two bytes).
# To return potentially more than one, this
# function will return arrays of strings, where
# each string is a data word, in bits.
def parseInstruction( line ):
    match = extractInstruction.match(line);

    # Get instruction information.
    instructionName = match.group(1).lower();
    opcode = instructions[instructionName];

    # Create argument list.
    argumentListStart = match.end(1);
    argumentList = map( lambda s: s.strip(), example[argumentListStart:].split(',') )

    # Keep track of current argument to examine.
    currentArgument = 0;

    # Create list of data words to output.
    words = [];

    for data_word_specification in instructionParseMap[opcode]:
        data_word = "";
        for field_tuple in data_word_specification:

            # If the encoding directions contain a string
            # directly, then just concatenate the string.
            if isinstance( field_tuple, str ):
                data_word += field_tuple;
                continue;

            # Else, get the token type and width of the bits to use.
            tokenType = field_tuple[0];
            width = field_tuple[1];

            if (tokenType == "opcode"):
                data_word += opcode.zfill(width);
            else:
                # Parse the literal according to tokenType.
                try:
                    parsed_literal = tokenParse[tokenType]( argumentList[ currentArgument ] );
                except AttributeError as err:
                    raise SyntaxError("Could not parse '" + argumentList[currentArgument] + \
                            "' as " + tokenType + ".");


                # Truncate the 0b off of the binary literal,
                # then left-pad with zeroes as necessary.
                data_word += bin( parsed_literal )[2:].zfill(width);
                currentArgument += 1;

        words.append(data_word);
    return words;

####################################################
## }}}
####################################################

examples = [ 
    '    mv $0, $1', 'mv       $2,   $3', # Can we strip the whitespace?
    ' mvI $4, 0x1', 
    #'mvi $0, 0x12345', # Can we detect literals that are too large?
    'add $0, $1',
    #'add        $7, $9', # Can we detect out of range register names?
    #'sub $0, $10',
    'sub $5, $2',
    'mvi $0, 0x000F',
    'mvi $0, 15',
    'mvi $0, b1111',
    'mvi $2, 0x0002',
    'add $1, $0',
    'sub $1, $2',
    #'add $d, $2',
];

print "original examples:"
for example in examples:
    print example

print "With whitespace condensed:"
for example in examples:
    print whitespace.sub(' ', example);

print "examples are unchanged after strip:"
for example in examples:
    print example

print "Instructions on each line:"
for example in examples:
    print extractInstruction.match(example).group(1).lower();

print "Parsing instructions:"
for example in examples:
    print example;
    print parseInstruction(example);

# instruction: 0000 0 {opcode} {register_x_bin_string, 3} {register_y_bin_string, 3}
