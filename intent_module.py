"""Part B - Intent detection using Ollama (Q3)."""

import utils

INTENTS = ("Delivery Issue", "Refund Request", "Product Complaint",
           "Technical Support", "Order Cancellation", "Payment Issue",
           "Warranty", "Account Issue", "Exchange Request", "General Inquiry")

SYSTEM = (
    "You classify customer support emails. Reply with exactly one of these "
    "categories and nothing else:\n" + "\n".join(INTENTS) + "\n\n"
    "Examples:\n"
    "My order has not arrived yet. -> Delivery Issue\n"
    "I want my money back. -> Refund Request\n"
    "The app keeps crashing. -> Technical Support\n"
    "The item I received is damaged. -> Product Complaint\n"
    "Please cancel my order. -> Order Cancellation\n"
    "I was charged twice. -> Payment Issue\n"
    "Is this product still under warranty? -> Warranty\n"
    "I cannot log in to my account. -> Account Issue\n"
    "I would like a different size. -> Exchange Request\n"
    "What are your working hours? -> General Inquiry"
)


def detect_intent(email, verbose=True):
    """Q3 - identify the customer intent with the local model."""
    raw = utils.ask(SYSTEM, "Email: {}\nCategory:".format(email), temperature=0.0)
    text = raw.lower()

    intent = None
    for candidate in INTENTS:
        if candidate.lower() in text:
            intent = candidate
            break
    if intent is None:
        keywords = [("deliver", "Delivery Issue"), ("refund", "Refund Request"),
                    ("cancel", "Order Cancellation"), ("warrant", "Warranty"),
                    ("exchange", "Exchange Request"), ("payment", "Payment Issue"),
                    ("account", "Account Issue"), ("login", "Account Issue"),
                    ("technical", "Technical Support"), ("complaint", "Product Complaint")]
        for key, value in keywords:
            if key in text:
                intent = value
                break
    intent = intent or "General Inquiry"

    utils.update_state(intent=intent)

    if verbose:
        print("Detected Intent")
        print(utils.DASH)
        print(intent)
        print(utils.DASH)
    return intent


if __name__ == "__main__":
    utils.banner("INTENT DETECTION  (model: {})".format(utils.OLLAMA_MODEL))
    email = utils.require("email", "No customer email found. Enter one first.")
    if email:
        print("Customer Email : {}".format(email))
        print()
        detect_intent(email)
