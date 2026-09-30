# Sample Questions and Results

## Q1: Which Apple products are supplied by TechSupply?

- **Query plan:** `{'function': 'products_by_brand_vendor', 'args': {'brand': 'Apple', 'vendor': 'TechSupply'}}`
- **Retrieved data:** `['iPhone 14', 'iPhone 15']`
- **Answer:** TechSupply supplies iPhone 14 and iPhone 15.

## Q2: What has Rahul purchased?

- **Query plan:** `{'function': 'customer_purchases', 'args': {'customer': 'Rahul'}}`
- **Retrieved data:** `[{'order': 'O001', 'product': 'iPhone 15', 'quantity': 1}, {'order': 'O002', 'product': 'Banana Chips', 'quantity': 2}, {'order': 'O009', 'product': 'iPhone 14', 'quantity': 1}]`
- **Answer:** Rahul has purchased iPhone 15, Banana Chips, and iPhone 14.

## Q3: Which brands has Rahul bought?

- **Query plan:** `{'function': 'brands_bought_by_customer', 'args': {'customer': 'Rahul'}}`
- **Retrieved data:** `['Apple', 'NatureBite']`
- **Answer:** Rahul has bought Apple and NatureBite.

## Q4: Who bought Banana Chips?

- **Query plan:** `{'function': 'customers_who_bought', 'args': {'product_name': 'Banana Chips'}}`
- **Retrieved data:** `['Rahul']`
- **Answer:** Rahul bought Banana Chips.

## Q5: Show all items related to banana.

- **Query plan:** `{'function': 'search_keyword', 'args': {'keyword': 'banana'}}`
- **Retrieved data:** `[{'type': 'Product', 'name': 'Banana Chips'}, {'type': 'Product', 'name': 'Banana Powder'}, {'type': 'Product', 'name': 'Banana Bread Mix'}, {'type': 'Product', 'name': 'Banana Shake Mix'}, {'type': 'Product', 'name': 'Banana Protein Bar'}]`
- **Answer:** The items related to banana are:
* Banana Chips
* Banana Powder
* Banana Bread Mix
* Banana Shake Mix
* Banana Protein Bar

## Q6: What products are in the Snacks category?

- **Query plan:** `{'function': 'products_by_category', 'args': {'category': 'Snacks'}}`
- **Retrieved data:** `['Banana Chips', 'Banana Protein Bar']`
- **Answer:** The products in the Snacks category are Banana Chips and Banana Protein Bar.

## Q7: Which Nokia products does TechSupply supply?

- **Query plan:** `{'function': 'products_by_brand_vendor', 'args': {'brand': 'Nokia', 'vendor': 'TechSupply'}}`
- **Retrieved data:** `[]`
- **Answer:** No data found in the graph for this question.
