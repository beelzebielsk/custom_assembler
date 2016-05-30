import assembler;
from assembler.assembler import parseInstruction;
#import parseInstruction;

if __name__ == '__main__':
    print "I'm main.";
else:
    print "I'm not main, but I'm", __name__ + ".";

print "Testing import";
print '\t', dir(assembler);
print "Testing Function include";
print '\t', dir(parseInstruction);
