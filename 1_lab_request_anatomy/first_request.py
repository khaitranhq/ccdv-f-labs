# --- Lab setup (provided - just run it) ---
import json

from anthropic import Anthropic
from anthropic.types.message_create_params import MessageCreateParams

# Everything below this line is ordinary Claude API code.
from dotenv import load_dotenv
from shopassist_lab import check

load_dotenv()
# No key in the code: the client reads ANTHROPIC_API_KEY from the environment,
# which load_dotenv() filled from the .env file.
client = Anthropic()


# The model name lives in one constant, so a later update changes one line.
MODEL = "claude-sonnet-5-5"
QUESTION = (
    "A customer asks: can I return a jacket after 20 days? Our policy "
    "allows returns within 30 days. Answer the customer in two sentences."
)

REQUEST: MessageCreateParams = {
    "model": MODEL,  # MODEL
    "max_tokens": 300,  # 300 - a ceiling, not a target
    "output_config": {"effort": "low"},
    "messages": [{"role": "user", "content": QUESTION}],  # QUESTION
}
response = client.messages.create(**REQUEST)

print(json.dumps(REQUEST, indent=2))  # the body of the HTTPS request
print(response.model_dump_json(indent=2))  # the body of the HTTPS response

check("request_json", request=REQUEST, response=response)

try:
    assert response.content[0].type == "text"
    record = {
        "id": response.id,
        "model": response.model,
        "stop_reason": response.stop_reason,  # response.stop_reason
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,  # response.usage.output_tokens
        "text": response.content[0].text,
    }
    print(json.dumps(record))
except TypeError as exc:  # provided: a blank left above, said plainly
    if "llipsis" in str(exc):
        raise ValueError(
            "You still have ... above. Replace each one with the value named beside it."
        ) from None
    raise

check("log_record", record=record, response=response)


class IncompleteReply(Exception):  # provided
    """The reply stopped before Claude finished it."""


def ask(max_tokens):  # provided: the same request, another ceiling
    return client.messages.create(**{**REQUEST, "max_tokens": max_tokens})


def finish(response):
    if response.stop_reason != "end_turn":
        raise IncompleteReply(response.stop_reason)
    return response.content[0].text


try:
    short = ask(20)
    try:
        answer = finish(short)
    except IncompleteReply as cut:
        print("cut by", cut, "- asking again with more room")
        answer = finish(ask(300))
except IncompleteReply:
    raise ValueError(
        f"finish() refused the second reply as well (stop_reason {exec}). It "
        'should raise only when stop_reason is not "end_turn".'
    ) from None

print("cut reply:", repr(short.content[0].text))
print("answer:   ", answer)

check("incomplete_reply", short=short, answer=answer, finish=finish)
