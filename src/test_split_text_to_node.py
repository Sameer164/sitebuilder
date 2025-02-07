import unittest
from textnode import TextNode, TextType
from main import text_to_textnodes

class TestSplitTextToTextNodes(unittest.TestCase):
    def test_eq_text_with_all_types(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.NORMAL_TEXT),
            TextNode("text", TextType.BOLD_TEXT),
            TextNode(" with an ", TextType.NORMAL_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" word and a ", TextType.NORMAL_TEXT),
            TextNode("code block", TextType.CODE_TEXT),
            TextNode(" and an ", TextType.NORMAL_TEXT),
            TextNode("obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.NORMAL_TEXT),
            TextNode("link", TextType.LINKS, "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)


if __name__ == "__main__":
    unittest.main()