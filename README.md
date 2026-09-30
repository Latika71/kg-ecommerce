# E-commerce Knowledge Graph with LLM-powered Retrieval

A Python project that builds a knowledge graph (NetworkX) from an e-commerce
dataset and answers natural-language questions using an LLM.
Answers are generated **only from data retrieved from the graph**.

## Flow

User Question -> LLM (question to JSON query plan) -> Graph function
-> Retrieved data -> LLM (answer from data only) -> Final answer

## Knowledge Graph

**Entities:** Product, Brand, Category, Vendor, Customer, Order

| Relationship | Direction |
|---|---|
| MADE_BY | Product -> Brand |
| BELONGS_TO | Product -> Category |
| SUPPLIES | Vendor -> Product |
| PLACED | Customer -> Order |
| CONTAINS | Order -> Product (has `quantity`) |

## Project structure

```
kg-ecommerce/
├── data/            products.csv, customers.csv, orders.csv
├── src/
│   ├── build_graph.py   builds the graph from CSVs
│   ├── retriever.py     graph query functions
│   ├── llm.py           LLM calls (query planning + answer)
│   └── main.py          entry point
├── results/sample_results.md
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

1. Clone the repo:
```
   git clone <your-repo-url>
   cd kg-ecommerce
```
2. Create and activate a virtual environment:
```
   python -m venv venv
   venv\Scripts\activate          # Windows
   source venv/bin/activate       # Mac/Linux
```
3. Install dependencies:
```
   pip install -r requirements.txt
```
4. Copy `.env.example` to `.env` and add your Gemini API key
   (free key: https://aistudio.google.com):
```
   LLM_PROVIDER=gemini
   GEMINI_API_KEY=your_key_here
   GEMINI_MODEL=gemini-3.1-flash-lite
```

## Run

```
python src/build_graph.py         # build graph, print counts, verify banana count
python src/retriever.py           # test graph queries without the LLM
python src/main.py                # interactive Q&A
python src/main.py --samples      # run 7 sample questions, save results
```

## How answers stay grounded in graph data

- The LLM never writes code or database queries. It only picks one function
  from a fixed whitelist and returns arguments as JSON.
- Python runs that function on the graph and returns the data.
- The second LLM call is told to answer only from that data, and to reply
  "No data found in the graph for this question." if the data is empty.
- Unknown function names or wrong arguments return empty data, never a guess.

## The "banana" requirement

The word "banana" appears exactly 5 times in the graph, as the name of 5 Product
nodes: Banana Chips, Banana Powder, Banana Bread Mix, Banana Shake Mix,
Banana Protein Bar. Running `python src/build_graph.py` prints the count and
checks that it equals 5. It is retrievable through the system, for example:
"Show all items related to banana."

## Sample questions and results

See `results/sample_results.md` (7 questions with query plan, retrieved data
and final answer).

## Notes

- The dataset is synthetic and was created for this assignment.
- The free Gemini tier has daily request limits. If you get a 429 error,
  change `GEMINI_MODEL` in `.env` or retry later.
- To use a different dataset, only the column mapping in `build_graph.py`
  needs to change.