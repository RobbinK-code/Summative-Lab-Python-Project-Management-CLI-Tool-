import argparse
from engine import BakeryEngine
import storage
from rich.console import Console
from rich.table import Table

console = Console()

def main():
    engine = BakeryEngine()
    storage.load_data(engine)

    # Seed an initial Manager account if file is completely fresh
    if not engine.users:
        engine.register("chef", "chef123", role="Manager")

    parser = argparse.ArgumentParser(description="Bakery Inventory & Order System CLI")
    subparsers = parser.add_subparsers(dest="command", help="Bakery Actions")

    # Command: register
    p_reg = subparsers.add_parser("register", help="Register a staff member")
    p_reg.add_argument("--name", required=True)
    p_reg.add_argument("--password", required=True)
    p_reg.add_argument("--role", choices=["Manager", "Staff"], default="Staff")

    # Command: add-item (Manager Only)
    p_item = subparsers.add_parser("add-item", help="Bake/Restock an inventory item (Manager Only)")
    p_item.add_argument("--mgr-name", required=True)
    p_item.add_argument("--mgr-pass", required=True)
    p_item.add_argument("--name", required=True, help="Item name (e.g., Croissant)")
    p_item.add_argument("--price", type=float, required=True)
    p_item.add_argument("--stock", type=int, required=True)

    # Command: order
    p_ord = subparsers.add_parser("order", help="Process a customer purchase")
    p_ord.add_argument("--user", required=True, help="Staff member processing order")
    p_ord.add_argument("--item", required=True)
    p_ord.add_argument("--qty", type=int, required=True)

    # Command: dashboard
    subparsers.add_parser("dashboard", help="Show current showcase items & sales")

    args = parser.parse_args()

    # --- CLI Routing Loop ---
    if args.command == "register":
        success, msg = engine.register(args.name, args.password, args.role)
        console.print(f"[green]{msg}[/green]" if success else f"[red]{msg}[/red]")
        storage.save_data(engine.users, engine.inventory)

    elif args.command == "add-item":
        mgr_obj, msg = engine.login(args.mgr_name, args.mgr_pass)
        if not mgr_obj:
            console.print(f"[red]{msg}[/red]")
            return
        
        success, action_msg = engine.add_inventory_item(mgr_obj, args.name, args.price, args.stock)
        console.print(f"[green]{action_msg}[/green]" if success else f"[red]{action_msg}[/red]")
        storage.save_data(engine.users, engine.inventory)

    elif args.command == "order":
        success, msg = engine.process_bakery_order(args.user, args.item, args.qty)
        console.print(f"[green]{msg}[/green]" if success else f"[red]{msg}[/red]")
        storage.save_data(engine.users, engine.inventory)

    elif args.command == "dashboard":
        # Table 1: Inventory showcase
        t_inv = Table(title="🧁 Bakery Menu & Stock Showcase 🧁")
        t_inv.add_column("Item Name", style="cyan")
        t_inv.add_column("Price Each", style="green")
        t_inv.add_column("Stock Available", style="yellow")

        for item in engine.inventory.values():
            stock_style = "green" if item.stock > 5 else "bold red"
            t_inv.add_row(item.name, f"${item.price:.2f}", f"[{stock_style}]{item.stock}[/{stock_style}]")
        
        console.print(t_inv)

if __name__ == "__main__":
    main()