from selenium import webdriver

# browser = webdriver.Safari()
# browser.get("http://localhost:8000")

# assert "Congratulations!" in browser.title
# print("OK")

browser = webdriver.Safari()

# the user navigates to the url
browser.get("http://localhost:8000")

# the welcome page has "To-Do" in the title
assert "To-Do" in browser.title

# the page invites the user to enter a todo item straight away, they just start typing

# the user types "buy peacock feathers" and hits enter

# the page refreshes and now shows "1: Buy peacock feathers" as an item in a to-do list

# the user types "use feathers to make a fly", hits enter

# the page refreshes and now shows a second item labeled "2: use feathers to make a fly" as an item

browser.quit()