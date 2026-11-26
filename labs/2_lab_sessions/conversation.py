from anthropic import Anthropic

# Everything below this line is ordinary Claude API code.
from dotenv import load_dotenv

from shared.shopassist_lab import check

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


def task1():
    second = [{"role": "user", "content": "Can I still return it?"}]  # provided
    first_reply, _ = ask(
        [{"role": "user", "content": "I bought a jacket 20 days ago."}]
    )
    second_reply, _ = ask(second)
    print("1:", first_reply)
    print("2:", second_reply)

    check(
        "no_state", first_reply=first_reply, second_reply=second_reply, sent=len(second)
    )


def task23():
    SESSIONS = {}  # provided: session id -> that customer's history
    TOKENS = {}  # provided: session id -> input tokens of each turn

    def say(session_id, text):
        history = SESSIONS.setdefault(session_id, [])  # session_id
        history.append({"role": "user", "content": text})
        reply, response = ask(history)  # history - the whole list
        history.append({"role": "assistant", "content": reply})  # "assistant"
        TOKENS.setdefault(session_id, []).append(response.usage.input_tokens)
        print(f"[{session_id} - user] {text}")
        print(f"[{session_id} - assistant] {reply}")

    SESSIONS.clear()
    TOKENS.clear()  # provided: re-running this cell starts fresh
    try:
        say("alex", "I bought a jacket 20 days ago.")
        say("alex", "Can I still return it?")
        say("alex", "And if I lost the receipt?")
    except (
        TypeError,
        KeyError,
        AttributeError,
    ) as exc:  # provided: a blank left above, said plainly
        if "llipsis" in str(exc):
            raise ValueError(
                "You still have ... above. Replace each one with the value named beside it."
            ) from None
        raise

    check("session_history", sessions=SESSIONS, say=say)

    try:
        say("sam", "Can I still return it?")  # "sam", "Can I still return it?"
        for session_id, counts in TOKENS.items():  # TOKENS
            print(session_id, "input tokens per turn:", counts)
    except (
        TypeError,
        KeyError,
        AttributeError,
    ) as exc:  # provided: a blank left above, said plainly
        if "llipsis" in str(exc):
            raise ValueError(
                "You still have ... above. Replace each one with the value "
                "named beside it."
            ) from None
        raise

    check("session_isolation", sessions=SESSIONS, tokens=TOKENS)


if __name__ == "__main__":
    # task1()
    task23()
