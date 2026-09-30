import os
import json
import time 
from dotenv import load_dotenv

load_dotenv()

PROVIDER = os.getenv("LLM_PROVIDER", "gemini")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

FUNCTIONS_INFO = """
1. products_by_brand_vendor(brand, vendor) - products of a brand supplied by a vendor
2. products_by_brand(brand)                - all products of a brand
3. products_by_category(category)          - all products in a category
4. products_by_vendor(vendor)              - all products supplied by a vendor
5. customer_purchases(customer)            - a customer's orders (order, product, quantity)
6. brands_bought_by_customer(customer)     - brands a customer has bought
7. customers_who_bought(product_name)      - customers who bought a product
8. search_keyword(keyword)                 - all nodes containing a word (e.g. banana)
"""




def call_llm(prompt):
    """Single place where the LLM is called. Retries if the server is busy."""
    for attempt in range(6):
        try:
            if PROVIDER == "claude":
                import anthropic
                client = anthropic.Anthropic()
                msg = client.messages.create(
                    model="claude-sonnet-5-5",
                    max_tokens=500,
                    messages=[{"role": "user", "content": prompt}],
                )
                return msg.content[0].text

            from google import genai
            client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
            resp = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
            return resp.text
        except Exception as e:
            if attempt == 5:
                raise
            wait = 10 * (attempt + 1)
            print(f"LLM busy, retrying in {wait}s... ({type(e).__name__})")
            time.sleep(5 * (attempt + 1))




def question_to_query(question):
    """Step 1: convert a natural-language question into a structured query (JSON)."""
    prompt = f"""You are a query planner for an e-commerce knowledge graph.
Choose exactly ONE function from the list below that can answer the user's question.

Functions:
{FUNCTIONS_INFO}

Return ONLY this JSON and nothing else:
{{"function": "<function name>", "args": {{"<arg name>": "<value>"}}}}

Use the exact argument names from the function signatures
(brand, vendor, category, customer, product_name, keyword).
If no function fits, return:
{{"function": "none", "args": {{}}}}

Question: {question}"""

    text = call_llm(prompt).strip()
    text = text.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"function": "none", "args": {}}


def generate_answer(question, data):
    """Step 2: write the final answer using ONLY the retrieved graph data."""
    prompt = f"""You are an assistant. Below are a question and DATA retrieved from a knowledge graph.

    Rules:
1. Answer ONLY from the DATA. Do not add any outside knowledge.
2. If the DATA is empty, reply exactly: "No data found in the graph for this question."
3. Include every relevant detail present in the DATA (for example order ID and quantity). Do not omit or invent any.
4. Keep the answer short and clear.


Question: {question}
DATA: {json.dumps(data, ensure_ascii=False)}"""

    return call_llm(prompt).strip()


if __name__ == "__main__":
    print(question_to_query("Which Apple products does TechSupply supply?"))
    print(generate_answer("What are Apple's products?", ["iPhone 14", "iPhone 15"]))
    print(generate_answer("What are Nokia's products?", []))