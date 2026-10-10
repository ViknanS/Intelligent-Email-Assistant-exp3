"""Part F - Conversation summary (Q8)."""

import utils

TARGET = 50

SYSTEM = ("You summarise customer support conversations. Write ONE paragraph of "
          "about 50 words describing the customer issue and how it was handled. "
          "No headings, no bullet points.")


def summarize(verbose=True):
    """Q8 - generate a summary of the customer issue in about 50 words."""
    state = utils.load_state()
    prompt = ("Customer Email:\n{}\n\nDetected Intent: {}\n\nReply sent:\n{}\n\n"
              "Summarise this conversation in about 50 words."
              ).format(state.get("email", ""), state.get("intent", ""),
                       state.get("reply", ""))

    summary = utils.ask(SYSTEM, prompt, temperature=0.3)
    utils.update_state(summary=summary)

    if verbose:
        print("Conversation Summary")
        print(utils.DASH)
        print(summary)
        print(utils.DASH)
        print("Summary length : {} words (target ~{})".format(
            len(summary.split()), TARGET))
    return summary


if __name__ == "__main__":
    utils.banner("CONVERSATION SUMMARY")
    if utils.require("reply", "No generated reply found. Generate a reply first."):
        summarize()
