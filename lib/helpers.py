from db.models import Event, Attendee, Vendor, Session, init_db
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich import print as rprint

console = Console()

def get_session():
    return Session()

def initialize_database():
    """Initialize the database if it doesn't exist"""
    try:
        init_db()
        console.print("[green]Database initialized successfully![/green]")
    except Exception as e:
        console.print(f"[red]Error initializing database: {str(e)}[/red]")

# Main menu functions
def display_main_menu():
    console.clear()
    console.print("[bold blue]Event Planner CLI[/bold blue]")
    console.print("\nMain Menu:")
    console.print("1. Event Management")
    console.print("2. Attendee Management")
    console.print("3. Vendor Management")
    console.print("4. Reports")
    console.print("Q. Quit")
    return input("\nSelect an option: ")

# Event Management Functions
def handle_events():
    while True:
        console.clear()
        console.print("[bold blue]Event Management[/bold blue]")
        console.print("\n1. Create New Event")
        console.print("2. List All Events")
        console.print("3. View Event Details")
        console.print("4. Update Event")
        console.print("5. Delete Event")
        console.print("B. Back to Main Menu")
        
        choice = input("\nSelect an option: ").lower()
        
        if choice == '1':
            create_event()
        elif choice == '2':
            list_events()
        elif choice == '3':
            view_event_details()
        elif choice == '4':
            update_event()
        elif choice == '5':
            delete_event()
        elif choice == 'b':
            break

def create_event():
    session = get_session()
    console.print("\n[bold]Create New Event[/bold]")
    
    try:
        name = input("Event Name: ")
        date_str = input("Date (YYYY-MM-DD): ")
        date = datetime.strptime(date_str, "%Y-%m-%d")
        location = input("Location: ")
        budget = float(input("Budget: "))
        status = input("Status (planning/ongoing/completed): ")
        description = input("Description: ")

        event = Event(
            name=name,
            date=date,
            location=location,
            budget=budget,
            status=status,
            description=description
        )
        
        session.add(event)
        session.commit()
        console.print("\n[green]Event created successfully![/green]")
    except ValueError as e:
        console.print("\n[red]Invalid input format. Please try again.[/red]")
        console.print(f"Error: {str(e)}")
    except Exception as e:
        console.print(f"\n[red]Error creating event: {str(e)}[/red]")
        session.rollback()
    finally:
        session.close()
        input("\nPress Enter to continue...")

def list_events():
    session = get_session()
    try:
        events = session.query(Event).all()
        
        if not events:
            console.print("\n[yellow]No events found.[/yellow]")
            return
            
        table = Table(title="Events List")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="magenta")
        table.add_column("Date", style="green")
        table.add_column("Location", style="blue")
        table.add_column("Status", style="yellow")
        table.add_column("Budget", style="red")
        
        for event in events:
            table.add_row(
                str(event.id),
                event.name,
                event.date.strftime("%Y-%m-%d"),
                event.location or "N/A",
                event.status or "N/A",
                f"${event.budget:,.2f}" if event.budget else "N/A"
            )
        
        console.clear()
        console.print(table)
        
    except Exception as e:
        console.print(f"\n[red]Error listing events: {str(e)}[/red]")
    finally:
        session.close()
        input("\nPress Enter to continue...")

def view_event_details():
    session = get_session()
    try:
        # First list all events
        events = session.query(Event).all()
        
        if not events:
            console.print("\n[yellow]No events found.[/yellow]")
            return
            
        # Show events list
        table = Table(title="Select an Event")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="magenta")
        table.add_column("Date", style="green")
        
        for event in events:
            table.add_row(
                str(event.id),
                event.name,
                event.date.strftime("%Y-%m-%d")
            )
            
        console.print(table)
        
        # Get event selection
        event_id = input("\nEnter event ID to view details (or press Enter to cancel): ")
        
        if not event_id:
            return
            
        event = session.query(Event).filter_by(id=int(event_id)).first()
        
        if event:
            console.clear()
            console.print(f"[bold blue]Event Details: {event.name}[/bold blue]\n")
            console.print(f"Date: {event.date.strftime('%Y-%m-%d')}")
            console.print(f"Location: {event.location or 'N/A'}")
            console.print(f"Status: {event.status or 'N/A'}")
            console.print(f"Budget: ${event.budget:,.2f}" if event.budget else "Budget: N/A")
            console.print(f"Description: {event.description or 'N/A'}\n")
            
            # Show attendees
            if event.attendees:
                console.print("[bold]Attendees:[/bold]")
                for attendee in event.attendees:
                    console.print(f"- {attendee.name} ({attendee.rsvp_status or 'No RSVP'})")
            else:
                console.print("[bold]No attendees registered[/bold]")
                
            # Show vendors
            if event.vendors:
                console.print("\n[bold]Vendors:[/bold]")
                for vendor in event.vendors:
                    console.print(f"- {vendor.name} ({vendor.service_type or 'Service not specified'})")
            else:
                console.print("\n[bold]No vendors assigned[/bold]")
        else:
            console.print("\n[red]Event not found![/red]")
            
    except ValueError:
        console.print("\n[red]Invalid input. Please enter a valid event ID.[/red]")
    except Exception as e:
        console.print(f"\n[red]Error viewing event details: {str(e)}[/red]")
    finally:
        session.close()
        input("\nPress Enter to continue...")

def update_event():
    session = get_session()
    try:
        # First list all events
        events = session.query(Event).all()
        
        if not events:
            console.print("\n[yellow]No events found to update.[/yellow]")
            return
            
        # Show events list
        table = Table(title="Select an Event to Update")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="magenta")
        table.add_column("Date", style="green")
        table.add_column("Status", style="yellow")
        
        for event in events:
            table.add_row(
                str(event.id),
                event.name,
                event.date.strftime("%Y-%m-%d"),
                event.status or "N/A"
            )
            
        console.print(table)
        
        # Get event selection
        event_id = input("\nEnter event ID to update (or press Enter to cancel): ")
        
        if not event_id:
            return
            
        event = session.query(Event).filter_by(id=int(event_id)).first()
        
        if event:
            console.clear()
            console.print(f"[bold]Updating Event: {event.name}[/bold]")
            console.print("(Press Enter to keep current value)\n")
            
            name = input(f"Name [{event.name}]: ") or event.name
            date_str = input(f"Date [{event.date.strftime('%Y-%m-%d')}]: ")
            location = input(f"Location [{event.location or 'N/A'}]: ") or event.location
            budget_str = input(f"Budget [{event.budget or 'N/A'}]: ")
            status = input(f"Status [{event.status or 'N/A'}]: ") or event.status
            description = input(f"Description [{event.description or 'N/A'}]: ") or event.description
            
            # Update values
            event.name = name
            if date_str:
                event.date = datetime.strptime(date_str, "%Y-%m-%d")
            if budget_str:
                event.budget = float(budget_str)
            event.location = location
            event.status = status
            event.description = description
            
            session.commit()
            console.print("\n[green]Event updated successfully![/green]")
        else:
            console.print("\n[red]Event not found![/red]")
            
    except ValueError as e:
        console.print("\n[red]Invalid input format. Please try again.[/red]")
        console.print(f"Error: {str(e)}")
    except Exception as e:
        console.print(f"\n[red]Error updating event: {str(e)}[/red]")
        session.rollback()
    finally:
        session.close()
        input("\nPress Enter to continue...")

def delete_event():
    session = get_session()
    try:
        # First, list all events
        events = session.query(Event).all()
        
        if not events:
            console.print("\n[yellow]No events found to delete.[/yellow]")
            input("\nPress Enter to continue...")
            return
            
        console.print("\n[bold]Delete Event[/bold]")
        console.print("\nAvailable Events:")
        
        # Display events in a table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID")
        table.add_column("Name")
        table.add_column("Date")
        table.add_column("Location")
        
        for event in events:
            table.add_row(
                str(event.id),
                event.name,
                event.date.strftime("%Y-%m-%d"),
                event.location or "N/A"
            )
            
        console.print(table)
        
        # Get event ID to delete
        event_id = input("\nEnter the ID of the event to delete (or press Enter to cancel): ")
        
        if not event_id:
            console.print("\n[yellow]Deletion cancelled.[/yellow]")
            return
            
        event = session.query(Event).filter_by(id=int(event_id)).first()
        
        if event:
            # Confirm deletion
            confirm = input(f"\nAre you sure you want to delete '{event.name}'? (y/N): ").lower()
            
            if confirm == 'y':
                session.delete(event)
                session.commit()
                console.print(f"\n[green]Event '{event.name}' deleted successfully![/green]")
            else:
                console.print("\n[yellow]Deletion cancelled.[/yellow]")
        else:
            console.print("\n[red]Event not found![/red]")
            
    except ValueError:
        console.print("\n[red]Invalid input. Please enter a valid event ID.[/red]")
    except Exception as e:
        console.print(f"\n[red]Error deleting event: {str(e)}[/red]")
        session.rollback()
    finally:
        session.close()
        input("\nPress Enter to continue...")

# Attendee Management Functions
def handle_attendees():
    while True:
        console.clear()
        console.print("[bold blue]Attendee Management[/bold blue]")
        console.print("\n1. Add New Attendee")
        console.print("2. List All Attendees")
        console.print("3. Update Attendee")
        console.print("4. Delete Attendee")
        console.print("5. Manage RSVPs")
        console.print("B. Back to Main Menu")
        
        choice = input("\nSelect an option: ").lower()
        
        if choice == 'b':
            break

# Vendor Management Functions
def handle_vendors():
    while True:
        console.clear()
        console.print("[bold blue]Vendor Management[/bold blue]")
        console.print("\n1. Add New Vendor")
        console.print("2. List All Vendors")
        console.print("3. Update Vendor")
        console.print("4. Delete Vendor")
        console.print("5. Manage Ratings")
        console.print("B. Back to Main Menu")
        
        choice = input("\nSelect an option: ").lower()
        
        if choice == 'b':
            break

# Report Functions
def handle_reports():
    while True:
        console.clear()
        console.print("[bold blue]Reports[/bold blue]")
        console.print("\n1. Guest Lists")
        console.print("2. Budget Reports")
        console.print("3. Vendor Assignments")
        console.print("4. Event Summary")
        console.print("B. Back to Main Menu")
        
        choice = input("\nSelect an option: ").lower()
        
        if choice == 'b':
            break

