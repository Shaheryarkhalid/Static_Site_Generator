import unittest

from main import extract_title


class TestMain(unittest.TestCase):

    test_cases = [
        {
            "input": "# Hello",
            "expected": "Hello",
            "exception": False,
            "print": "Testing extract_title in main.py",
        },
        {
            "input": """## Hellosss

```
Testing
```
# Hello
# Test 
# Test 

##Testing

####Testing

- Testing
            """,
            "expected": "Hello",
            "exception": False,
            "print": "Testing extract_title in main.py",
        },
        {
            "input": """## Hellosss

```
Testing
```

##Testing

####Testing

- Testing
            """,
            "expected": "Markdown file does not contain any headers.",
            "exception": True,
            "print": "Testing extract_title in main.py. looking for an exception ",
        },
    ]

    def test_main_for_output(self):
        for test_case in TestMain.test_cases:
            if not test_case["exception"]:
                actual = extract_title(test_case["input"])
                if "print" in test_case:
                    print(test_case["print"])
                try:
                    self.assertEqual(actual, test_case["expected"])
                except Exception as _:
                    print("Testing failed while testing extract title in main")
                    print("Test Failed")
                    print("expected :")
                    print(test_case["expected"])
                    print("actual :")
                    print(actual)
                    self.fail("Test failed for text_node_to_parent_Html_node.")

    def test_main_for_exception(self):
        for test_case in TestMain.test_cases:
            if test_case["exception"]:
                try:
                    if "print" in test_case:
                        print(test_case["print"])
                    actual = extract_title(test_case["input"])
                except Exception as e:
                    try:
                        self.assertEqual(str(e), test_case["expected"])
                    except Exception as err:
                        self.print_exception(test_case, err)
                else:
                    self.print_exception(test_case, actual)

    def print_exception(self, test_case, actual):
        print("Testing failed while testing extract title in main")
        print("Test Failed")
        print("Exception expected :")
        print(test_case["expected"])
        print("actual :")
        print(actual)
        self.fail("Test failed for extract_title in main Exception.")
