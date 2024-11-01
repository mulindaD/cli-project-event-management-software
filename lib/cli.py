#!/usr/bin/env python3

from rich.console import Console
from helpers import (
    initialize_database,
    display_main_menu,
    handle_events,
    handle_attendees,
    handle_vendors,
    handle_reports
)

console = Console()

def main():
    console.clear()
    console.print("[bold green]Welcome to Event Planner CLI![/bold green]")
    
    # Initialize database
    initialize_database()
    
    while True:
        choice = display_main_menu()
        
        if choice == '1':
            handle_events()
        elif choice == '2':
            handle_attendees()
        elif choice == '3':
            handle_vendors()
        elif choice == '4':
            handle_reports()
        elif choice.lower() == 'q':
            break
    
    console.print("\n[bold green]Thanks for using Event Planner CLI![/bold green]")

if __name__ == '__main__':
    main()