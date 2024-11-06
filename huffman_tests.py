import unittest
import filecmp
import subprocess
from ordered_list import *
from huffman import *


class TestList(unittest.TestCase):

    def test_empty4(self):
        freqlist = cnt_freq("empty_file.txt")
        newlst = 256*[0]
        self.assertEqual(freqlist, newlst)

    def test_cnt_freq(self):
        freqlist = cnt_freq("file2.txt")
        anslist = [2, 4, 8, 16, 0, 2, 0]
        self.assertListEqual(freqlist[97:104], anslist)

        a = create_header(freqlist)
        self.assertEqual(a, "97 2 98 4 99 8 100 16 102 2")

    def test_one(self):
        lst = []
        self.assertEqual(create_huff_tree(lst), None)
        lst2 = [1]
        self.assertEqual(create_huff_tree(lst2), HuffmanNode(0, 1))
        lst3 = ['']*256
        self.assertEqual(create_code(HuffmanNode(97, 1)), lst3)

    def test_lt_and_eq(self):
        anslist = [2, 4, 8, 16, 0, 2, 0]
        ascii = 97
        lst = OrderedList()
        for freq in anslist:
            node = HuffmanNode(ascii, freq)
            lst.add(node)
            ascii += 1

        self.assertEqual(lst.index(HuffmanNode(101, 0)), 0)
        self.assertEqual(lst.index(HuffmanNode(100, 16)), 6)
        self.assertEqual(lst.index(HuffmanNode(97, 2)), 2)
        self.assertFalse(HuffmanNode(97, 2) == None)
        a = HuffmanNode(97, 2)
        self.assertTrue(HuffmanNode(97, 2), a)

    def test_video(self):
        freqlist = cnt_freq("file1.txt")
        anslist = [4, 3, 2, 1]
        self.assertEqual(anslist, freqlist[97:101])
        ascii = 97
        lst = OrderedList()
        for freq in anslist:
            node = HuffmanNode(ascii, freq)
            lst.add(node)
            ascii += 1
        self.assertEqual(lst.index(HuffmanNode(97, 4)), 3)
        self.assertEqual(lst.index(HuffmanNode(100, 1)), 0)
        self.assertEqual(lst.index(HuffmanNode(99, 2)), 1)
        self.assertEqual(lst.index(HuffmanNode(98, 3)), 2)

    def test_create_huff_tree(self):
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        # a = make_ordered_list(freqlist)
        # printOrdered(a)

        self.assertEqual(hufftree.freq, 32)
        self.assertEqual(hufftree.char, 97)
        left = hufftree.right
        self.assertEqual(left.freq, 16)
        self.assertEqual(hufftree.left.char, 97)
        right = hufftree.right
        self.assertEqual(right.freq, 16)
        self.assertEqual(right.char, 100)

    def test_create_header(self):
        freqlist = cnt_freq("file1.txt")
        hufftree = create_huff_tree(freqlist)

        a = create_header(freqlist)
        self.assertEqual(a, "32 3 97 4 98 3 99 2 100 1")
        self.assertEqual(hufftree.freq, 13)
        self.assertEqual(hufftree.char, 32)
        self.assertEqual(hufftree.left.freq, 6)
        self.assertEqual(hufftree.left.char, 32)
        self.assertEqual(hufftree.left.left.char, 32)
        self.assertEqual(hufftree.left.left.freq, 3)
        self.assertEqual(hufftree.left.right.freq, 3)
        self.assertEqual(hufftree.left.right.char, 98)

        self.assertEqual(hufftree.right.freq, 7)
        self.assertEqual(hufftree.right.char, 97)
        self.assertEqual(hufftree.right.right.char, 97)
        self.assertEqual(hufftree.right.right.freq, 4)

        self.assertEqual(hufftree.right.left.char, 99)
        self.assertEqual(hufftree.right.left.freq, 3)
        self.assertEqual(hufftree.right.left.left.char, 100)
        self.assertEqual(hufftree.right.left.left.freq, 1)
        self.assertEqual(hufftree.right.left.right.freq, 2)
        self.assertEqual(hufftree.right.left.right.char, 99)

    #
    #
    def test_empty(self):
        huffman_encode("empty_file.txt", "empty_file_out.txt")
        err = subprocess.call("diff -wb empty_file_out.txt empty_file.txt", shell=True)
        self.assertEqual(err, 0)
        err2 = subprocess.call("diff -wb empty_file_out_compressed.txt empty_file.txt", shell=True)
        self.assertEqual(err2, 0)

    def test_create_code(self):
        freqlist = cnt_freq("file2.txt")
        hufftree = create_huff_tree(freqlist)
        codes = create_code(hufftree)

        self.assertEqual(codes[ord('d')], '1')
        self.assertEqual(codes[ord('a')], '0000')
        self.assertEqual(codes[ord('f')], '0001')
        self.assertEqual(codes[ord('b')], '001')
        self.assertEqual(codes[ord('c')], '01')

    def test_video_code(self):
        freqlist = cnt_freq("file1.txt")
        hufftree = create_huff_tree(freqlist)
        codes = create_code(hufftree)

        self.assertEqual(codes[ord('a')], '11')
        self.assertEqual(codes[ord('b')], '01')
        self.assertEqual(codes[ord('c')], '101')
        self.assertEqual(codes[ord('d')], '100')
        self.assertEqual(codes[ord(' ')], '00')
    #
    #

    def test_01_textfile(self):

        with self.assertRaises(FileNotFoundError):
            huffman_encode("test.txt", "test_out.txt")
        huffman_encode("file1.txt", "file1_out.txt")
        # capture errors by running 'diff' on your encoded file with a *known* solution file
        err = subprocess.call("diff -wb file1_out.txt file1_soln.txt", shell=True)
        self.assertEqual(err, 0)

        err01 = subprocess.call("diff -wb file1_out_compressed.txt file1_compressed_soln.txt", shell=True)
        self.assertEqual(err01, 0)

        huffman_encode("file2.txt", "file2_out.txt")
        err2 = subprocess.call("diff -wb file2_out.txt file2_soln.txt", shell=True)
        self.assertEqual(err2, 0)

        err22 = subprocess.call("diff -wb file2_out_compressed.txt file2_compressed_soln.txt", shell=True)
        self.assertEqual(err22, 0)

        huffman_encode("declaration.txt", "declaration_out.txt")
        err3 = subprocess.call("diff -wb declaration_out.txt declaration_soln.txt", shell=True)
        self.assertEqual(err3, 0)

        err33 = subprocess.call("diff -wb declaration_out_compressed.txt declaration_compressed_soln.txt", shell=True)
        self.assertEqual(err33, 0)

        huffman_encode("multiline.txt", "multiline_out.txt")
        err4 = subprocess.call("diff -wb multiline_out.txt multiline_soln.txt", shell=True)
        self.assertEqual(err4, 0)

        err44 = subprocess.call("diff -wb multiline_out_compressed.txt multiline_compressed_soln.txt", shell=True)
        self.assertEqual(err44, 0)

        # huffman_encode("file_WAP.txt", "file_WAP_out.txt")
        # err5 = subprocess.call("diff -wb file_WAP_out.txt file_WAP_soln.txt", shell=True)
        # self.assertEqual(err5, 0)
        err66 = subprocess.call("diff -wb file1_out_compressed.txt file1_compressed_soln.txt", shell=True)
        self.assertEqual(err66, 0)

    def test_hi(self):
        self.assertEqual(1, 1)
        huffman_encode("filecharacter.txt", "filecharacter_out.txt")
        err = subprocess.call("diff -wb filecharacter_out.txt filecharacter_soln.txt", shell=True)
        self.assertEqual(err, 0)

    def test_code(self):

        huffman_encode("filecharacter.txt", "filecharacter_out.txt")
        err = subprocess.call("diff -wb filecharacter_out.txt filecharacter_soln.txt", shell=True)
        self.assertEqual(err, 0)

        err2 = subprocess.call("diff -wb filecharacter_out_compressed.txt filecharacter_soln.txt", shell=True)
        self.assertEqual(err2, 0)

    def test_01_test_file1_decode(self):
        huffman_decode("file1_compressed_soln.txt", "file1_decoded.txt")
        err = subprocess.call("diff -wb file1.txt file1_decoded.txt", shell = True)
        self.assertEqual(err, 0)

        huffman_decode("file2_compressed_soln.txt", "file2_decoded.txt")
        err = subprocess.call("diff -wb file2.txt file2_decoded.txt", shell=True)
        self.assertEqual(err, 0)

        huffman_decode("declaration_compressed_soln.txt", "declaration_decoded.txt")
        err = subprocess.call("diff -wb declaration.txt declaration_decoded.txt", shell=True)
        self.assertEqual(err, 0)

        huffman_decode("multiline_compressed_soln.txt", "multiline_decoded.txt")
        err = subprocess.call("diff -wb multiline.txt multiline_decoded.txt", shell=True)
        self.assertEqual(err, 0)

        huffman_decode("filecharacter_out_compressed.txt", "filecharacter_decoded.txt")
        err = subprocess.call("diff -wb filecharacter.txt filecharacter_decoded.txt", shell=True)
        self.assertEqual(err, 0)

        huffman_decode("empty_file_out.txt", "empty_file_decoded.txt")
        err = subprocess.call("diff -wb empty_file.txt empty_file_decoded.txt", shell=True)
        self.assertEqual(err, 0)

        # huffman_decode("file_WAP_compressed_soln.txt", "file_WAP_decoded.txt")
        # err = subprocess.call("diff -wb file_WAP.txt file_WAP_decoded.txt", shell=True)
        # self.assertEqual(err, 0)

        with self.assertRaises(FileNotFoundError):
            huffman_decode("fempty.txt",  "fdfasdfa.txt")

        # 97 2 98 4 99 8 100 16 102 2

        lst = 256*[0]
        lst[97] = 2
        lst[98] = 4
        lst[99] = 8
        lst[100] = 16
        lst[102] = 2

        a = parse_header("97 2 98 4 99 8 100 16 102 2")
        self.assertEqual(a, lst)
        emlst = 256*[0]
        b = parse_header("")
        self.assertEqual(b, emlst)


if __name__ == '__main__': 
    unittest.main()
