from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()

MODEL = "claude-sonnet-5-5"

TEST_SET = [
    (
        "I bought a jacket, delivered 20 days ago. Can I return it?",
        "YES",
    ),
    (
        "The shoes I ordered arrived yesterday, but they don't fit. Can I return them?",
        "YES",
    ),
    (
        "I received a watch as a gift few hours ago, but I don't like it. Can I return it?",
        "NO",
    ),
    (
        "My order was delivered 40 days ago, and I want to return it. Is that possible?",
        "NO",
    ),
    (
        "The underwear I ordered arrived 10 days ago, but I changed my mind. Can I return it?",
        "NO",
    ),
]

PROMPT_V1 = (
    "You are ShopAssist, an online store's support assistant. "
    "Returns are accepted within 30 days of delivery. "
    "Begin your answer with 'YES' or 'NO', then one sentence. "
)

PROMPT_V2 = (
    "You are ShopAssist, an online store's support assistant. "
    "Returns are accepted within 30 days of delivery. "
    "Begin your answer with 'YES' or 'NO', then one sentence. "
    "Gift and underwear items cannot be returned."
)


def answer(system, text):
    response = client.messages.create(
        model=MODEL,
        max_tokens=200,
        output_config={"effort": "low"},
        system=system,
        messages=[{"role": "user", "content": text}],
    )
    for block in response.content:
        if block.type == "text":
            return block.text


def evaluate(name, system):
    score = 0
    for text, expected in TEST_SET:
        reply = answer(system, text)
        ok = expected in reply.strip().upper()
        score += ok
        print("PASS" if ok else "FAIL", f"({expected})", text, "->", reply)
    print(f"{name} score: {score}/{len(TEST_SET)}")


evaluate("v1", PROMPT_V1)
evaluate("v2", PROMPT_V2)
