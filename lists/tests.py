from django.test import TestCase
from lists.models import Item, List

# Create your tests here.
class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post("/", data={"item_text": "A new list item"})
        self.assertEqual(Item.objects.count(), 1, f"Item.objects.count: {Item.objects.count()}")
        new_Item = Item.objects.first()
        self.assertEqual(new_Item.text, "A new list item")

    def test_only_saves_items_when_necessary(self):
        self.client.get("/")
        self.assertEqual(Item.objects.count(), 0, f"Item.objects.count(): {Item.objects.count()}")

    def test_displays_all_list_items(self):
        list_ = List.objects.create()
        Item.objects.create(text="Item1", list=list_)
        Item.objects.create(text="Item2", list=list_)
        
        response = self.client.get("/")
        self.assertContains(response, "Item1")
        self.assertContains(response, "Item2")

    def test_redirects_after_POST(self):
        response = self.client.post("/", data={"item_text": "A new list item"})
        self.assertRedirects(response, "/lists/the-only-list-in-the-world/")

class ListViewTest(TestCase):
    def test_uses_list_template(self):
        response = self.client.get("/lists/the-only-list-in-the-world/")
        self.assertTemplateUsed(response, "home.html")

    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text="Item1", list=list_)
        Item.objects.create(text="Item2", list=list_)
        response = self.client.get("/lists/the-only-list-in-the-world/")
        self.assertContains(response, "Item1")
        self.assertContains(response, "Item2")

class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List.objects.create()
        
        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)

class ListAndItemModelsTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'Item the second')
        self.assertEqual(second_saved_item.list, list_)
        