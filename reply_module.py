"""Part D - AI reply generation (Q6)."""

import utils

SYSTEM = ("You are a professional customer support agent. Write a complete email "
          "reply. Start with 'Dear Customer,' and end with 'Regards,' on one line "
          "and 'Support Team' on the next. Keep it under 120 words. "
          "Return only the email, with no commentary.")


def generate_reply(verbose=True):
    """Q6 - generate a professional reply from the email and the previous reply."""
    state = utils.load_state()

    prompt = ("Customer Email:\n{}\n\n"
              "Detected Intent: {}\n\n"
              "A previous reply used for a similar case:\n{}\n\n"
              "Write a professional reply to this customer."
              ).format(state.get("email", ""), state.get("intent", ""),
                       state.get("previous_reply", ""))

    reply = utils.ask(SYSTEM, prompt)
    utils.update_state(reply=reply)

    if verbose:
        print("AI Generated Reply")
        print(utils.DASH)
        print(reply)
        print(utils.DASH)
        print("Words : {}".format(len(reply.split())))
    return reply


if __name__ == "__main__":
    utils.banner("AI REPLY GENERATION")
    if utils.require("email", "No customer email found. Enter one first."):
        state = utils.load_state()
        print("Customer Email : {}".format(state.get("email")))
        print("Intent         : {}".format(state.get("intent", "not detected")))
        print()
        generate_reply()
