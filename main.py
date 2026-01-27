from datetime import datetime
import json
import questionary
from rich import Console

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
        if not notes:
            return "[bold red]No notes found[/bold red]."
        id = int(input("Enter the id of the note you want to edit:\n> "))
        choice = questionary.select(
            "What should be edited?\nUse arrow keys to navigate",
            choices=[
                'Title',
                'Content',
                'Tags',
            ],
            pointer='>'
        ).ask()
        for item in notes:
            if item['id'] == id:
                if choice == 'Title':
                    new_title = str(input("Enter the new title:\n> "))
                    item['title'] = new_title
                    item['edit_date'] = f'{datetime.now().strftime("%Y-%m-%d")}'
                elif choice == 'Content':
                    new_content = str(input("Enter the new content:\n> "))
                    item['content'] = new_content
                    item['edit_date'] = f'{datetime.now().strftime("%Y-%m-%d")}'
                elif choice == 'Tags':
                    new_tags = input("Enter the new tags (e.g. python learning lecture):\n> ").split()
                    item['tags'] = new_tags
                    item['edit_date'] = f'{datetime.now().strftime("%Y-%m-%d")}'
        self.write_file(notes)
        return "[bold green]Note edited successfully[/bold green]."
    
    def delete_notes(self):
        notes = self.open_file()
        note_id = int(input("Enter the id of the note you want to delete:\n> "))
        for item in notes:
            if item['id'] == note_id:
                notes.pop(item)
        self.write_file(notes)
        return "Note deleted successfully."

    def take_notes(self,title:str,content:str,tags:list,date=f'{datetime.now().strftime('%Y-%m-%d')}'):
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
        if not notes:
            return "[bold red]No notes found[/bold red]."
        choice = questionary.select(
            "What should be filtered?\nUse arrow keys to navigate",
            choices=[
                'Id',
                'Title',
                'Tags',
                'Creation date',
            ],
            pointer='>'
        ).ask()
        if choice == 'Id':
            id = int(input("Enter the id of the note you want to find:\n> "))
            count = 1
            for item in notes:
                if item['id'] == id:
                    print(f"Note {count}:\nId: {item['id']}\nTitle: {item['title']}\nContent: {item['content']}\nTags: {' '.join(item['tags'])}\nCreated: {item['created']}\n")
                    count += 1
        elif choice == 'Title':
            title = str(input("Enter the title of the note you want to find:\n> "))
            count = 1
            for item in notes:
                if item['title'] == title:
                    print(f"Note {count}:\nId: {item['id']}\nTitle: {item['title']}\nContent: {item['content']}\nTags: {' '.join(item['tags'])}\nCreated: {item['created']}\n")
                    count += 1
        elif choice == 'Tags':
            tag = str(input("Enter the tag of the note you want to find:\n> "))
            count = 1
            for item in notes:
                if tag in item['tags']:
                    print(f"Note {count}:\nId: {item['id']}\nTitle: {item['title']}\nContent: {item['content']}\nTags: {' '.join(item['tags'])}\nCreated: {item['created']}\n")
                    count += 1
        elif choice == 'Creation date':
            date = str(input("Enter the creation date (yyyy-mm-dd) of the note you want to find:\n> "))
            count = 1
            for item in notes:
                if item['created'] == date:
                    print(f"Note {count}:\nId: {item['id']}\nTitle: {item['title']}\nContent: {item['content']}\nTags: {' '.join(item['tags'])}\nCreated: {item['created']}\n")
                    count += 1

notes = NoteTaker()
running = True
while running:
    choice = questionary.select(
        "What should be filtered?\nUse arrow keys to navigate",
        choices=[
            'Add a note',
            'Edit notes',
            'Delete notes',
            'Filter all notes',
            'View all notes'
            'Exit',
        ],
        pointer='>'
    ).ask()
    if choice == 'Add a note':
        id = notes.assign_id()
        title = str(input("What is the title of the note?\n> "))
        content = str(input("What is the content of the note?\n> "))
        tags = input("What tags should be linked to this note (e.g. python learning lecture) ?\n> ").split()
        date = f'{datetime.now().strftime("%Y-%m-%d")}'
        notes.take_notes(id,title,content,tags,date)
    elif choice == 'Edit notes':
        print(notes.edit_notes())
    elif choice == 'Delete notes':
        print(notes.delete_notes())
    elif choice == 'Filter all notes':
        notes.search_notes()
    elif choice == 'View all notes':
        notes.view_notes()
    elif choice == 'Exit':
        print("Exiting ...")
        running = False
    else:
        print("Choose a valid number from the menu above")