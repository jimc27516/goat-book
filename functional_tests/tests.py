import time
import unittest
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException


# https://www.obeythetestinggoat.com/book/chapter_05_post_and_database.html#_footnoteref_4


MAX_WAIT = 5

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Safari()
        return super().setUp()
    
    def tearDown(self):
        self.browser.quit()
        return super().tearDown()

    def wait_for_row_in_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element(By.ID, "id_list_table")
                rows = table.find_elements(By.TAG_NAME, "tr")
                self.assertIn(row_text, [row.text for row in rows])
                return
            except(AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

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

        # the page refreshes and now shows "1: Buy peacock feathers" as an item in a to-do list        
        self.wait_for_row_in_table("1: Buy peacock feathers")

        # the user types "use feathers to make a fly", hits enter
        inputbox = self.browser.find_element(By.ID, "id_new_element")
        inputbox.send_keys("use feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)

        # the page refreshes and now there should be two items,  a second item labeled "2: use feathers to make a fly" as an item
        self.wait_for_row_in_table("1: Buy peacock feathers")
        self.wait_for_row_in_table("2: use feathers to make a fly")        

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # user 1 starts a new list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element(By.ID, "id_new_element")
        inputbox.send_keys("Buy peacock feathers")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_table("1: Buy peacock feathers")

        # user 1 gets their own unique url
        user1_list_url = self.browser.current_url
        self.assertRegex(user1_list_url, "/lists/.+")

        # user 2 starts a new list

        # delete all the users cookies... might be rundandant
        self.browser.delete_all_cookies()

        self.browser.quit()
        self.browser = webdriver.Safari()

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertNotIn("make a fly", page_text)

        inputbox = self.browser.find_element(By.ID, "id_new_element")
        inputbox.send_keys("Buy milk")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_table("1: Buy milk")

        # user 2 gets their own unique url
        user2_list_url = self.browser.current_url
        self.assertRegex(user2_list_url, "/lists/.+")
        self.assertNotEqual(user1_list_url, user2_list_url)

        # there is no trace of user 1's list
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertIn("Buy milk", page_text)

        # the user is satisfied and goes back to sleep

