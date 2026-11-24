from anthropic import Anthropic

# Everything below this line is ordinary Claude API code.
from dotenv import load_dotenv
from shopassist_lab import check

load_dotenv()
client = Anthropic()

# The model name lives in one constant, so a later update changes one line.
MODEL = "claude-sonnet-5-5"
SYSTEM = (
    "You are ShopAssist, an online store's support assistant. "
    "Returns are accepted within 30 days of delivery. "
    "Answer in one or two sentences."
)


def ask(messages):
    response = client.messages.create(
        model=MODEL,
        max_tokens=200,
        output_config={"effort": "low"},
        system=SYSTEM,
        messages=messages,
    )
    reply = None
    for block in response.content:
        if block.type == "text":
            reply = block.text
    return reply, response


second = [{"role": "user", "content": "Can I still return it?"}]  # provided
first_reply, _ = ask([{"role": "user", "content": "I bought a jacket 20 days ago."}])
second_reply, _ = ask(second)
print("1:", first_reply)
print("2:", second_reply)

check("no_state", first_reply=first_reply, second_reply=second_reply, sent=len(second))
