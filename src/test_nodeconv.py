import unittest
from main import *
from leafnode import LeafNode
from textnode import TextNode, TextType
 
class TestNodeConversion(unittest.TestCase):
    def test_imgconv(self):
        text_node = TextNode("This is an image of a dog", TextType.IMAGES, "https://google.com/image")
        leafnode = text_node_to_html_node(text_node=text_node)
        final_html = leafnode.to_html()
        self.assertEqual(final_html, '<img src="https://google.com/image" alt="This is an image of a dog"></img>')


if __name__ == "__main__":
    unittest.main()
