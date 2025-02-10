from django.test import TestCase
from lists.models import Item, List
import unittest
# Create your tests here.
class HomePageTest(TestCase):

    def test_home_page_returns_correct_html(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, 'home.html')

class NewListTest(TestCase):
    def test_can_save_a_POST_request(self):
        response = self.client.post("/lists/new", data={"item_text": "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirects_after_POST(self):
        response = self.client.post("/lists/new", data={"item_text": "A new list item"})
        list_ = List.objects.first()
        self.assertRedirects(response, f"/lists/{list_.id}/")

class ListViewTest(TestCase):
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f"/lists/{list_.id}/")
        self.assertTemplateUsed(response, "list.html")

    def test_displays_all_items(self):
        list_ = List.objects.create()
        Item.objects.create(text="Item1", list=list_)
        Item.objects.create(text="Item2", list=list_)
        response = self.client.get(f"/lists/{list_.id}/")
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

class ListModelTest(TestCase):
    def test_get_items_for_specific_list(self):
        list_ = List.objects.create()
        Item.objects.create(text="itemey 1", list=list_)
        Item.objects.create(text="itemey 2", list=list_)
        self.assertEqual(list_.get_items().count(), 2)
        self.assertEqual(list_.get_items()[0].text, "itemey 1")
        self.assertEqual(list_.get_items()[1].text, "itemey 2")
        
    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f"/lists/{correct_list.id}/")
        self.assertEqual(response.context["list"], correct_list)
        

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
        
# @unittest.skip("Temporarily skipping new item test")
class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        # make a new List 
        list_ = List.objects.create()

        # send a POST request to the list view
        self.client.post(
            f"/lists/{list_.id}/add_item",
            data={"item_text": "A new item for an existing list"}
        )

        self.assertEqual(list_.get_items().count(), 1)
        self.assertEqual(list_.get_items()[0].text, "A new item for an existing list")

        # now add a second item to the same list    
        self.client.post(
            f"/lists/{list_.id}/add_item",
            data={"item_text": "A second item for an existing list"}
        )

        self.assertEqual(list_.get_items().count(), 2)
        self.assertEqual(list_.get_items()[1].text, "A second item for an existing list")

    # def test_redirects_to_list_view(self):
        