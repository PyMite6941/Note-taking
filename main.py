from datetime import datetime
import json

class NoteTaker:
    def __init__(self, filename='data.txt'):
        self.filename = filename

    def open_file(self) -> list:
        try:
            with open(self.filename, 'r') as file:
                results = json.load(file)
            return results
        except FileNotFoundError:
            print("File doesn't exist, creating ...")
            json.dump([],self.filename,indent=2)
            return []

    def write_file(self,list:list):
        with open(self.filename, 'w') as file:
            json.dump(list,file,indent=2)

    def assign_id(self) -> int:
        expenses = self.open_file()
        if len(expenses) == 0:
            return 1
        else:
            max_id = max(expense['id'] for expense in expenses)
            return max_id + 1
        
    def edit_notes(self):
        notes = self.open_file()
        id = int(input("Enter the id of the note you want to edit:\n> "))
        choice = int(input("What do you want to edit?\n1. Title\n2. Content\n3. Tags\n> "))
        for item in notes:
            if item['id'] == id:
                if choice == 1:
                    new_title = str(input("Enter the new title:\n> "))
                    item['title'] = new_title
                    item['edit_date'] = f'{datetime.now().strftime("%Y-%m-%d")}'
                elif choice == 2:
                    new_content = str(input("Enter the new content:\n> "))
                    item['content'] = new_content
                    item['edit_date'] = f'{datetime.now().strftime("%Y-%m-%d")}'
                elif choice == 3:
                    new_tags = input("Enter the new tags (e.g. python learning lecture):\n> ").split()
                    item['tags'] = new_tags
                    item['edit_date'] = f'{datetime.now().strftime("%Y-%m-%d")}'
        self.write_file(notes)
        return "Note edited successfully."
    
    def delete_notes(self):
        notes = self.open_file()
        id = int(input("Enter the id of the note you want to delete:\n> "))
        for item in notes:
            if item['id'] == id:
                notes.pop(item)
        self.write_file(notes)
        return "Note deleted successfully."

    def take_notes(self,id:int,title:str,content:str,tags:list,date=f'{datetime.now().strftime('%Y-%m-%d')}'):
        notes = {
            'id': self.assign_id(),
            'title': title,
            'content': content,
            'tags': tags,
            'created': date,
        }
        results = list(self.open_file())
        results.append(notes)
        self.write_file(results)

    def view_notes(self) -> list:
        notes = self.open_file()
        for item in notes:
            print(f"\nId: {item['id']}\nTitle: {item['title']}\nContent: {item['content']}\nTags: {' '.join(item['tags'])}\nCreated: {item['created']}\n")

    def search_notes(self) -> list:
        notes = self.open_file()
        choice = int(input("--- Filter Menu ---\n\n1. Id\n2. Title\n3. Tags\n4. Creation Date"))
        if choice == 1:
            id = int(input("Enter the id of the note you want to find:\n> "))
            count = 1
            for item in notes:
                if item['id'] == id:
                    print(f"Note {count}:\nId: {item['id']}\nTitle: {item['title']}\nContent: {item['content']}\nTags: {' '.join(item['tags'])}\nCreated: {item['created']}\n")
                    count += 1
        elif choice == 2:
            title = str(input("Enter the title of the note you want to find:\n> "))
            count = 1
            for item in notes:
                if item['title'] == title:
                    print(f"Note {count}:\nId: {item['id']}\nTitle: {item['title']}\nContent: {item['content']}\nTags: {' '.join(item['tags'])}\nCreated: {item['created']}\n")
                    count += 1
        elif choice == 3:
            tag = str(input("Enter the tag of the note you want to find:\n> "))
            count = 1
            for item in notes:
                if tag in item['tags']:
                    print(f"Note {count}:\nId: {item['id']}\nTitle: {item['title']}\nContent: {item['content']}\nTags: {' '.join(item['tags'])}\nCreated: {item['created']}\n")
                    count += 1
        elif choice == 4:
            date = str(input("Enter the creation date (yyyy-mm-dd) of the note you want to find:\n> "))
            count = 1
            for item in notes:
                if item['created'] == date:
                    print(f"Note {count}:\nId: {item['id']}\nTitle: {item['title']}\nContent: {item['content']}\nTags: {' '.join(item['tags'])}\nCreated: {item['created']}\n")
                    count += 1

notes = NoteTaker()
running = True
while running:
    choice = int(input("--- Menu ---\n\n1. Add a note\n\n2. Edit Notes\n3. Delete Notes\n4. Filter all notes\n5. View all notes\n0. Exit\n> "))
    if choice == 1:
        id = notes.assign_id()
        title = str(input("What is the title of the note?\n> "))
        content = str(input("What is the content of the note?\n> "))
        tags = input("What tags should be linked to this note (e.g. python learning lecture) ?\n> ").split()
        date = f'{datetime.now().strftime("%Y-%m-%d")}'
        notes.take_notes(id,title,content,tags,date)
    elif choice == 2:
        print(notes.edit_notes())
    elif choice == 3:
        print(notes.delete_notes())
    elif choice == 4:
        notes.search_notes()
    elif choice == 5:
        notes.view_notes()
    elif choice == 0:
        print("Exiting ...")
        running = False
    else:
        print("Choose a valid number from the menu above")