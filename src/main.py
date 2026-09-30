import sys
import time
from pathlib import Path

from build_graph import build_graph, find_banana
import retriever
from llm import question_to_query, generate_answer

RESULTS_FILE = Path(__file__).resolve().parent.parent / "results" / "sample_results.md"

# Whitelist: the LLM can only pick from these pre-written functions
FUNCTIONS = {
    "products_by_brand_vendor": retriever.products_by_brand_vendor,
    "products_by_brand": retriever.products_by_brand,
    "products_by_category": retriever.products_by_category,
    "products_by_vendor": retriever.products_by_vendor,
    "customer_purchases": retriever.customer_purchases,
    "brands_bought_by_customer": retriever.brands_bought_by_customer,
    "customers_who_bought": retriever.customers_who_bought,
    "search_keyword": retriever.search_keyword,
}

SAMPLE_QUESTIONS = [
    "Which Apple products are supplied by TechSupply?",
    "What has Rahul purchased?",
    "Which brands has Rahul bought?",
    "Who bought Banana Chips?",
    "Show all items related to banana.",
    "What products are in the Snacks category?",
    "Which Nokia products does TechSupply supply?",
]


def answer_question(G, question):
    """Full pipeline: question -> plan -> graph data -> answer."""
    plan = question_to_query(question)
    name = plan.get("function", "none")
    args = plan.get("args", {})

    if name not in FUNCTIONS:
        data = []
    else:
        try:
            data = FUNCTIONS[name](G, **args)
        except TypeError:  # LLM gave wrong argument names
            data = []

    answer = generate_answer(question, data)
    return plan, data, answer


def run_samples(G):
    lines = ["# Sample Questions and Results\n"]
    for i, q in enumerate(SAMPLE_QUESTIONS, start=1):
        plan, data, answer = answer_question(G, q)
        print(f"Q{i}: {q}\n   -> {answer}\n")
        lines.append(f"## Q{i}: {q}\n")
        lines.append(f"- **Query plan:** `{plan}`")
        lines.append(f"- **Retrieved data:** `{data}`")
        lines.append(f"- **Answer:** {answer}\n")
        time.sleep(5)  # stay within free-tier rate limits
    RESULTS_FILE.write_text("\n".join(lines), encoding="utf-8")
    print("Saved to", RESULTS_FILE)


def chat(G):
    print("Ask a question (type 'exit' to quit).")
    while True:
        q = input("\nYou: ").strip()
        if q.lower() in ("exit", "quit", ""):
            break
        plan, data, answer = answer_question(G, q)
        print("Plan  :", plan)
        print("Data  :", data)
        print("Answer:", answer)


if __name__ == "__main__":
    G = build_graph()
    print(f"Graph loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    print(f"'banana' appears {len(find_banana(G))} times in the graph")

    if "--samples" in sys.argv:
        run_samples(G)
    else:
        chat(G)