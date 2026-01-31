from datetime import datetime
import json
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

class NoteTaker:
    def __init__(self, filename='data.txt'):
        self.filename = filename

    # Process data from file
    def open_file(self) -> list:
        try:
            with open(self.filename, 'r') as file:
                results = json.load(file)
            return results
        except FileNotFoundError:
            print("File doesn't exist, creating ...")
            with open(self.filename,'w') as file:
                json.dump([],file,indent=2)
            return []

    # Write to file
    def write_file(self,list:list):
        with open(self.filename, 'w') as file:
            json.dump(list,file,indent=2)

    # Assign note id to notes
    def assign_id(self) -> int:
        expenses = self.open_file()
        if len(expenses) == 0:
            return 1
        else:
            max_id = max(expense['id'] for expense in expenses)
            return max_id + 1
        
    # Edit notes
    def edit_notes(self) -> str:
        notes = self.open_file()
        if not notes:
            return "[bold red]No notes found[/bold red]."
        id = int(questionary.text("Enter the id of the note you want to edit:\n> ").ask())
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
                    new_title = str(questionary.text("Enter the new title:\n> ").ask())
                    if not new_title.strip():
                        return "[bold yellow]Cannot leave title parameter blank[/bold yellow]."
                    item['title'] = new_title
                    item['edit_date'] = f'{datetime.now().strftime("%Y-%m-%d")}'
                elif choice == 'Content':
                    new_content = str(questionary.text("Enter the new content:\n> ").ask())
                    if not new_content.strip():
                        return "[bold yellow]Cannot leave content parameter blank[/bold yellow]."
                    item['content'] = new_content
                    item['edit_date'] = f'{datetime.now().strftime("%Y-%m-%d")}'
                elif choice == 'Tags':
                    new_tags = questionary.text("Enter the new tags (e.g. python learning lecture; default is 'general'):\n> ").ask()
                    if not new_tags:
                        item['tags'] = 'general'
                    else:
                        item['tags'] = new_tags
                    item['edit_date'] = f'{datetime.now().strftime("%Y-%m-%d")}'
        self.write_file(notes)
        return "[bold green]Note edited successfully[/bold green]."
    
    # Delete notes
    def delete_notes(self)-> str:
        notes = self.open_file()
        note_id = int(questionary.text("Enter the id of the note you want to delete:\n> ").ask())
        count = 0
        for item in notes:
            if item['id'] == note_id:
                notes.remove(item)
                count += 1
        if count < 1:
            return "[bold red]Note not found[/bold red]."
        self.write_file(notes)
        return "[bold green]Note deleted successfully[/bold green]."

    # Add notes
    def take_notes(self,date=f'{datetime.now().strftime("%Y-%m-%d")}') -> str:
        title = str(questionary.text("What is the title of the note?\n> ").ask())
        if not title.strip():
            return "[bold red]Cannot leave title parameter empty[/bold red]."
        content = str(questionary.text("What is the content of the note?\n> ").ask())
        if not content.strip():
            return "[bold red]Cannot leave content parameter empty[/bold red]."
        tags = str(questionary.text("What tags should be linked to this note (e.g. python learning lecture; default is 'general') ?\n> ").ask()).strip()
        if not tags.strip():
            tags = 'general'
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
        return "[bold green]Note added successfully[/bold green]."

    # View notes
    def view_notes(self):
        notes = self.open_file()
        table = Table()
        table.add_column("ID",justify="right",style="blue")
        table.add_column("Title",style="white")
        table.add_column("Content",style="red")
        table.add_column("Tags",style="magenta")
        table.add_column("Last Edited",style="green")
        for item in notes:
            table.add_row(str(item['id']),item['title'],item['content'],item['tags'],item['created'])
        console.print(table)

    # Search through all the notes
    def search_notes(self):
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
        table = Table()
        table.add_column("ID",justify="right",style="blue")
        table.add_column("Title",style="white")
        table.add_column("Content",style="red")
        table.add_column("Tags",style="magenta")
        table.add_column("Last Edited",style="green")
        if choice == 'Id':
            id = int(questionary.text("Enter the id of the note you want to find:\n> ").ask())
            for item in notes:
                if item['id'] == id:
                    table.add_row(str(item['id']),item['title'],item['content'],item['tags'],item['created'])
        elif choice == 'Title':
            title = str(questionary.text("Enter the title of the note you want to find:\n> ").ask())
            for item in notes:
                if item['title'] == title:
                    table.add_row(str(item['id']),item['title'],item['content'],item['tags'],item['created'])
        elif choice == 'Tags':
            tag = str(questionary.text("Enter the tag of the note you want to find:\n> ").ask())
            for item in notes:
                if tag in item['tags']:
                    table.add_row(str(item['id']),item['title'],item['content'],item['tags'],item['created'])
        elif choice == 'Creation date':
            date = str(questionary.text("Enter the creation date (yyyy-mm-dd) of the note you want to find:\n> ").ask())
            for item in notes:
                    if item['created'] == date:
                        table.add_row(str(item['id']),item['title'],item['content'],item['tags'],item['created'])
        console.print(table)

notes = NoteTaker()
console = Console()
running = True
while running:
    console.print(Panel("This is a fairly cool note taking app.",title="--- Note Manager ---",style='cyan'))
    choice = questionary.select(
        "What should be filtered?\nUse arrow keys to navigate",
        choices=[
            'Add a note',
            'Edit notes',
            'Delete notes',
            'View all notes',
            'Filter all notes',
            'Exit',
        ],
        pointer='>'
    ).ask()
    if choice == 'Add a note':
        console.print(notes.take_notes())
    elif choice == 'Edit notes':
        console.print(notes.edit_notes())
    elif choice == 'Delete notes':
        console.print(notes.delete_notes())
    elif choice == 'Filter all notes':
        notes.search_notes()
    elif choice == 'View all notes':
        notes.view_notes()
    elif choice == 'Exit':
        console.print("Exiting ...")
        running = False
    elif choice == None:
        console.print("Farewell.")
        running = False