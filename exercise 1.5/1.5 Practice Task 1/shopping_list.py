class ShoppingList(object):
    def __init__(self, list_name):
        shopping_list = []
        self.list_name = list_name
        self.shopping_list = shopping_list

    def add_item(self, item):
        self.item = item
        if item not in self.shopping_list:
            self.shopping_list.append(item)
            print(item, ' added to your list')
        else:
            print('this item is already in your list') 

    def remove_item(self, item):
        if item in self.shopping_list:
            self.shopping_list.remove(item)
            print(item, ' has been removed from your list')
        else:
            print('this item is not in your list')

    def view_list(self):
        print('==========================================')
        print('Shopping list - ', self.list_name)
        print('==========================================')
        for item in self.shopping_list:
            print('Item - ', item)

# creating new list
pet_store_list = ShoppingList('Pet Store Shopping List')

# adding items to list
pet_store_list.add_item('dog food')
pet_store_list.add_item('frisbee')
pet_store_list.add_item('bowl')
pet_store_list.add_item('collars')
pet_store_list.add_item('flea collars')

# removing items from list
pet_store_list.remove_item('flea collars')

# adding item to list
pet_store_list.add_item('frisbee')

# viewing the list
pet_store_list.view_list()