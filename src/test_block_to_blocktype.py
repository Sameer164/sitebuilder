import unittest
from main import block_to_block_type

class TestBlockToBlockType(unittest.TestCase):
    def test_code_block(self):
        block = "```\nThis is a code\n```"
        self.assertEqual("code", block_to_block_type(block))
    
    def test_no_code_block(self):
        block = "```\nThis is a code\n``"
        self.assertEqual("paragraph", block_to_block_type(block))
    
    def test_one_heading_block(self):
        block = "# \nThis is a heading\n```"
        self.assertEqual("heading", block_to_block_type(block))
    
    def test_two_heading_block(self):
        block = "## \nThis is a heading\n```"
        self.assertEqual("heading", block_to_block_type(block))

    def test_three_heading_block(self):
        block = "### \nThis is a heading\n```"
        self.assertEqual("heading", block_to_block_type(block))

    def test_four_heading_block(self):
        block = "#### \nThis is a heading\n```"
        self.assertEqual("heading", block_to_block_type(block))

    def test_five_heading_block(self):
        block = "##### \nThis is a heading\n```"
        self.assertEqual("heading", block_to_block_type(block))

    def test_six_heading_block(self):
        block = "###### \nThis is a heading\n```"
        self.assertEqual("heading", block_to_block_type(block))

    def test_no_heading_block(self):
        block = "####### \nThis is a heading\n```"
        self.assertEqual("paragraph", block_to_block_type(block))

        block = "#####\nThis is a heading\n```"
        self.assertEqual("paragraph", block_to_block_type(block))
    
    def test_quote(self):
        block = ">\nThis is a quote\n```"
        self.assertEqual("quote", block_to_block_type(block))


        block = ">Also a quote"
        self.assertEqual("quote", block_to_block_type(block))
    
    def test_unordered_list(self):
        block = "* A line\n* A list item"
        self.assertEqual("unordered_list", block_to_block_type(block))

    def test_not_unordered_list(self):
        block = "*\nA line\n* A list item"
        self.assertEqual("paragraph", block_to_block_type(block))

    def test_ordered_list(self):
        block = "1. Hello\n2. Hey"
        self.assertEqual("ordered_list", block_to_block_type(block))

    def test_not_ordered_list(self):
        block = "1. Hello\n0. Hey"
        self.assertEqual("paragraph", block_to_block_type(block))




