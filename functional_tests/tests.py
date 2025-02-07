import time
import unittest
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


# https://www.obeythetestinggoat.com/book/chapter_05_post_and_database.html#_footnoteref_4
class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Safari()
        return super().setUp()
    
    def tearDown(self):
        # TODO clean up after testcase runs
        self.browser.quit()
        return super().tearDown()

    def find_row_in_table(self, row_text):
        table = self.browser.find_element(By.ID, "id_list_table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        self.assertIn(row_text, [row.text for row in rows])       

    def test_can_start_a_todo_list(self):
        # the user navigates to the url
        self.browser.get(self.live_server_url)

        # the welcome page has "To-Do" in the title
        self.assertIn("To-Do", self.browser.title)

        # also there is a header with "To-Do" in it
        header_text = self.browser.find_element(By.TAG_NAME, "h1").text
        self.assertIn("To-Do", header_text)

        # the page invites the user to enter a todo item straight away, they just start typing
        inputbox = self.browser.find_element(By.ID, "id_new_element")

        # the user types "buy peacock feathers" and hits enter
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")
        inputbox.send_keys("Buy peacock feathers")
        inputbox.send_keys(Keys.ENTER)
        # TODO remove sleeps
        time.sleep(1)

        # the page refreshes and now shows "1: Buy peacock feathers" as an item in a to-do list        
        self.find_row_in_table("1: Buy peacock feathers")

        # the user types "use feathers to make a fly", hits enter
        inputbox = self.browser.find_element(By.ID, "id_new_element")
        inputbox.send_keys("use feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # the page refreshes and now there should be two items,  a second item labeled "2: use feathers to make a fly" as an item
        self.find_row_in_table("1: Buy peacock feathers")
        self.find_row_in_table("2: use feathers to make a fly")        


