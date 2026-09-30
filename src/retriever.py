from build_graph import build_graph


# ---------- Helper ----------
def _find_node(G, node_type, name):
    """Naam (jaise 'Apple') se node ID (jaise 'Brand:Apple') dhundho."""
    for node, data in G.nodes(data=True):
        if data.get("type") == node_type and \
           str(data.get("name", "")).lower() == str(name).lower():
            return node
    return None


# ---------- Query 1: Brand + Vendor ----------
def products_by_brand_vendor(G, brand, vendor):
    b = _find_node(G, "Brand", brand)
    v = _find_node(G, "Vendor", vendor)
    if b is None or v is None:
        return []
    common = set(G.predecessors(b)) & set(G.successors(v))
    return sorted(G.nodes[p]["name"] for p in common)


# ---------- Query 2, 3, 4: Brand / Category / Vendor ke products ----------
def products_by_brand(G, brand):
    b = _find_node(G, "Brand", brand)
    if b is None:
        return []
    return sorted(G.nodes[p]["name"] for p in G.predecessors(b))


def products_by_category(G, category):
    c = _find_node(G, "Category", category)
    if c is None:
        return []
    return sorted(G.nodes[p]["name"] for p in G.predecessors(c))


def products_by_vendor(G, vendor):
    v = _find_node(G, "Vendor", vendor)
    if v is None:
        return []
    return sorted(G.nodes[p]["name"] for p in G.successors(v))


# ---------- Query 5: Customer ne kya kharida ----------
def customer_purchases(G, customer):
    c = _find_node(G, "Customer", customer)
    if c is None:
        return []
    result = []
    for order in G.successors(c):
        for product in G.successors(order):
            result.append({
                "order": G.nodes[order]["name"],
                "product": G.nodes[product]["name"],
                "quantity": G.edges[order, product]["quantity"],
            })
    return sorted(result, key=lambda r: r["order"])


# ---------- Query 6: Customer ne kaunse brands kharide ----------
def brands_bought_by_customer(G, customer):
    c = _find_node(G, "Customer", customer)
    if c is None:
        return []
    brands = set()
    for order in G.successors(c):
        for product in G.successors(order):
            for nxt in G.successors(product):
                if G.edges[product, nxt]["relation"] == "MADE_BY":
                    brands.add(G.nodes[nxt]["name"])
    return sorted(brands)


# ---------- Query 7: Product kisne kharida ----------
def customers_who_bought(G, product_name):
    p = _find_node(G, "Product", product_name)
    if p is None:
        return []
    buyers = set()
    for order in G.predecessors(p):
        if G.nodes[order]["type"] == "Order":
            for cust in G.predecessors(order):
                buyers.add(G.nodes[cust]["name"])
    return sorted(buyers)


# ---------- Query 8: Keyword search (banana ke liye) ----------
def search_keyword(G, keyword):
    return [
        {"type": data["type"], "name": data["name"]}
        for node, data in G.nodes(data=True)
        if keyword.lower() in str(data.get("name", "")).lower()
    ]


# ---------- Test ----------
if __name__ == "__main__":
    G = build_graph()
    print(products_by_brand_vendor(G, "Apple", "TechSupply"))
    print(products_by_brand_vendor(G, "Apple", "GadgetWorld"))
    print(products_by_brand_vendor(G, "Nokia", "TechSupply"))
    print(products_by_brand(G, "Samsung"))
    print(products_by_category(G, "Snacks"))
    print(products_by_vendor(G, "FreshFoods"))
    print(customer_purchases(G, "Rahul"))
    print(brands_bought_by_customer(G, "Rahul"))
    print(customers_who_bought(G, "Banana Chips"))
    print(search_keyword(G, "banana"))
