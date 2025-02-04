import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Safari()
        return super().setUp()
    
    def tearDown(self):
        self.browser.quit()
        return super().tearDown()

    def test_can_start_a_todo_list(self):
        # the user navigates to the url
        self.browser.get("http://localhost:8000")

        # the welcome page has "To-Do" in the title
        self.assertIn("To-Do", self.browser.title)

        # also there is a header with "To-Do" in it
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        # the page invites the user to enter a todo item straight away, they just start typing
        inputbox = self.browser.find_element(By.ID, "id_new_element")

        # the user types "buy peacock feathers" and hits enter
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")
        inputbox.send_keys("Buy peakcock feathers")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # the page refreshes and now shows "1: Buy peacock feathers" as an item in a to-do list
        table = self.browser.find_element(By.ID, "id_list_table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        self.assertTrue(any(row.text == "1: Buy peacock feathers" for row in rows),
                        "New to-do item did not appear in table",
                        )

        # the user types "use feathers to make a fly", hits enter

        # the page refreshes and now shows a second item labeled "2: use feathers to make a fly" as an item
        self.fail("Finish the test!")

        
if __name__ == "__main__":
    unittest.main()