import unittest
from textnode import TextNode, TextType
from main import split_nodes_image, split_nodes_link

class TestSplitImagesLinks(unittest.TestCase):
    def test_eq_split_img(self):
        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL_TEXT,
        )
        expected = [
            TextNode("This is text with a link ", TextType.NORMAL_TEXT),
            TextNode("to boot dev", TextType.IMAGES, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL_TEXT),
            TextNode(
                "to youtube", TextType.IMAGES, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(split_nodes_image([node]), expected)


    def test_eq_split_img_two_same_img(self):
        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL_TEXT,
        )
        expected = [
            TextNode("This is text with a link ", TextType.NORMAL_TEXT),
            TextNode("to boot dev", TextType.IMAGES, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL_TEXT),
            TextNode(
                "to youtube", TextType.IMAGES, "https://www.youtube.com/@bootdotdev"
            ),
            TextNode(" and ", TextType.NORMAL_TEXT),
            TextNode(
                "to youtube", TextType.IMAGES, "https://www.youtube.com/@bootdotdev"
            ),

        ]
        self.assertEqual(split_nodes_image([node]), expected)
    
    def test_eq_split_img_no_img(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL_TEXT,
        )
        expected = node
        self.assertEqual(split_nodes_image([node]), [expected])
    
    def test_eq_split_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL_TEXT,
        )
        expected = [
            TextNode("This is text with a link ", TextType.NORMAL_TEXT),
            TextNode("to boot dev", TextType.LINKS, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL_TEXT),
            TextNode(
                "to youtube", TextType.LINKS, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(split_nodes_link([node]), expected)


    def test_eq_split_img_two_same_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL_TEXT,
        )
        expected = [
            TextNode("This is text with a link ", TextType.NORMAL_TEXT),
            TextNode("to boot dev", TextType.LINKS, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL_TEXT),
            TextNode(
                "to youtube", TextType.LINKS, "https://www.youtube.com/@bootdotdev"
            ),
            TextNode(" and ", TextType.NORMAL_TEXT),
            TextNode(
                "to youtube", TextType.LINKS, "https://www.youtube.com/@bootdotdev"
            ),

        ]
        self.assertEqual(split_nodes_link([node]), expected)
    
    def test_eq_split_img_no_link(self):
        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL_TEXT,
        )
        expected = node
        self.assertEqual(split_nodes_link([node]), [expected])

if __name__ == "__main__":
    unittest.main()

