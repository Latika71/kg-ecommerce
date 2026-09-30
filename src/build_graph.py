from pathlib import Path
import pandas as pd
import networkx as nx

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def build_graph():
    products = pd.read_csv(DATA_DIR / "products.csv")
    customers = pd.read_csv(DATA_DIR / "customers.csv")
    orders = pd.read_csv(DATA_DIR / "orders.csv")

    G = nx.DiGraph()

    # 1) Products, Brands, Categories, Vendors
    for _, row in products.iterrows():
        pid = f"Product:{row['product_id']}"
        brand = f"Brand:{row['brand']}"
        category = f"Category:{row['category']}"
        vendor = f"Vendor:{row['vendor']}"

        G.add_node(pid, type="Product", name=row["product_name"])
        G.add_node(brand, type="Brand", name=row["brand"])
        G.add_node(category, type="Category", name=row["category"])
        G.add_node(vendor, type="Vendor", name=row["vendor"])

        G.add_edge(pid, brand, relation="MADE_BY")
        G.add_edge(pid, category, relation="BELONGS_TO")
        G.add_edge(vendor, pid, relation="SUPPLIES")

    # 2) Customers
    for _, row in customers.iterrows():
        G.add_node(f"Customer:{row['customer_id']}", type="Customer",
                   name=row["customer_name"], city=row["city"])

    # 3) Orders
    for _, row in orders.iterrows():
        oid = f"Order:{row['order_id']}"
        G.add_node(oid, type="Order", name=row["order_id"])
        G.add_edge(f"Customer:{row['customer_id']}", oid, relation="PLACED")
        G.add_edge(oid, f"Product:{row['product_id']}", relation="CONTAINS",
                   quantity=int(row["quantity"]))

    return G


def find_banana(G):
    """Graph ke saare nodes ke name mein 'banana' dhundho."""
    return [
        (node, data["name"])
        for node, data in G.nodes(data=True)
        if "banana" in str(data.get("name", "")).lower()
    ]


if __name__ == "__main__":
    G = build_graph()
    print("Total nodes:", G.number_of_nodes())
    print("Total edges:", G.number_of_edges())

    # Type ke hisaab se count
    counts = {}
    for _, data in G.nodes(data=True):
        counts[data["type"]] = counts.get(data["type"], 0) + 1
    print("Node types:", counts)

    banana = find_banana(G)
    print("\nBanana count:", len(banana))
    for node, name in banana:
        print(" -", node, "->", name)
    print("Banana requirement OK?", len(banana) == 5)