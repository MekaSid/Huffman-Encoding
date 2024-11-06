from huffman_bit_reader import *
from huffman_bit_writer import *
from ordered_list import *


class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char   # stored as an integer - the ASCII character code value
        self.freq = freq   # the freqency associated with the node
        self.left = None   # Huffman tree (node) to the left
        self.right = None  # Huffman tree (node) to the right
        
    def __eq__(self, other):
        '''Needed in order to be inserted into OrderedList'''
        if type(other) != HuffmanNode:
            return False
        return self.freq == other.freq and self.char == other.char and self.right == other.right and self.left == other.left

    def __lt__(self, other):
        '''Needed in order to be inserted into OrderedList'''
        if self.freq == other.freq and self.char < other.char:
            return True
        if self.freq < other.freq:
            return True
        if self.freq > other.freq:
            return False
        return False


def cnt_freq(filename):
    '''Opens a text file with a given file name (passed as a string) and counts the 
    frequency of occurrences of all the characters within that file'''

    lst = [0]*256
    with open(filename) as f:
        for line in f:
            for c in line:
                num = ord(c)
                lst[num] += 1

    return lst


def create_huff_tree(char_freq):
    '''Create a Huffman tree for characters with non-zero frequency
    Returns the root node of the Huffman tree'''
    if char_freq == []:
        return None
    lst = make_ordered_list(char_freq)
    while lst.size() > 1:

        a = lst.pop(0)
        b = lst.pop(0)

        newfreq = a.freq + b.freq
        newchar = None

        if a.char < b.char:
            newchar = a.char
        else:
            newchar = b.char
        # print(newchar)
        # print(chr(newchar))
        current = HuffmanNode(newchar, newfreq)
        current.left = a
        current.right = b

        lst.add(current)

    return lst.head.next.item


def make_ordered_list(char_freq):
    lst = OrderedList()
    index = 0
    for item in char_freq:
        if item != 0:

            lst.add(HuffmanNode(index, item))
        index+=1

    return lst

# def printOrdered(lst):
#     lst = lst.head.next
#     while lst.item != None:
#         print(str(lst.item.freq) + " " + str(lst.item.char) + " " + str(chr(lst.item.char)))
#         lst = lst.next


def create_code(node):
    '''Returns an array (Python list) of Huffman codes. For each character, use the integer ASCII representation 
    as the index into the arrary, with the resulting Huffman code for that character stored at that location'''
    if node is None:
        return None
    lst = 256*[""]
    str = ""
    create_code_helper(node, lst, str)
    return lst

def create_code_helper(node, lst, str):

    if not node.left and not node.right:
        lst[node.char] = str
    if node.left:
        create_code_helper(node.left, lst, str + "0")
    if node.right:
        create_code_helper(node.right, lst, str + "1")


def create_header(freqs):
    '''Input is the list of frequencies. Creates and returns a header for the output file
    Example: For the frequency list asscoaied with "aaabbbbcc, would return “97 3 98 4 99 2” '''
    string = ""
    index = 0
    for item in freqs:
        if item != 0:
            string = string + str(index) + " " + str(item) + " "
        index+=1

    return string.strip()

def huffman_encode(in_file, out_file):
    '''Takes inout file name and output file name as parameters - both files will have .txt extensions
    Uses the Huffman coding process on the text from the input file and writes encoded text to output file
    Also creates a second output file which adds _compressed before the .txt extension to the name of the file.
    This second file is actually compressed by writing individual 0 and 1 bits to the file using the utility methods 
    provided in the huffman_bits_io module to write both the header and bits.
    Take note of special cases - empty file and file with only one unique character'''

    freqlist = cnt_freq(in_file)

    Tree = create_huff_tree(freqlist)

    codes = create_code(Tree)
    header = create_header(freqlist)
    str = ""
    with open(in_file) as f:
        for line in f:
            for c in line:
                temp = codes[ord(c)]
                str = str + temp

    with open(out_file, 'w') as f:
        f.write(header + "\n" + str)

    compressed = out_file[0:len(out_file) - 4] + "_compressed" + ".txt"
    a = HuffmanBitWriter(compressed)
    a.write_str(header + "\n")
    a.write_code(str)
    a.close()

    isempty = True

    with open(in_file) as f:
        for line in f:
            if line != "":
                isempty = False

    if isempty:
        with open(in_file) as f:
            if (f.readline()) == "":
                with open(out_file, 'w') as f:
                    pass
                with open(compressed, 'w') as f:
                    pass


def huffman_decode(encoded_file, decode_file):


    file = HuffmanBitReader(encoded_file)

    str = file.read_str()

    listfreq = parse_header(str)

    tree = create_huff_tree(listfreq)
    numchars = num_characters(listfreq)

    string = ""
    i = 0
    while i < numchars:
        currentnode = tree
        temp = 0
        while(currentnode.left is not None and currentnode.right is not None):
            a = file.read_bit()
            if a:
                currentnode = currentnode.right
            else:
                currentnode = currentnode.left
            if currentnode.left is None and currentnode.right is None:
                temp = (currentnode.char)
        char = chr(temp)
        string = string + char
        i+=1

    file.close()
    with open(decode_file, 'w') as f:
        f.write(string)

    temp = ""
    if len(str.split()) == 2:
        with open(decode_file, 'w') as f:
            i = 0
            a = str.split()
            char = (chr(int(a[0])))
            while i < int(a[1]):

                temp = temp + char
                i+=1

            f.write(temp)

            #f.write(string)

    if str == "":
        with open(decode_file, 'w') as f:
            pass




def num_characters(listfreq):
    count = 0
    for item in listfreq:
        count+=item

    return count

def parse_header(header_string):
    input = header_string.split()
    lst = [0]*256
    i = 0
    while i < len(input):

        index = int(input[i])
        freq = int(input[i+1])

        lst[index] = freq

        i+=2

    return lst

