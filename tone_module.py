"""Part E - Tone improver (Q7)."""

import utils

TONES = ("Friendly", "Formal", "Empathetic")

SYSTEM = ("You rewrite customer support emails in a requested tone. "
          "Keep the same facts and keep it under 120 words. "
          "Return only the rewritten email, with no commentary.")


def rewrite(reply, tone, verbose=True):
    """Rewrite one reply in the requested tone."""
    text = utils.ask(SYSTEM, "Rewrite this reply in a {} tone:\n\n{}".format(tone, reply))
    if verbose:
        print("{} Tone".format(tone))
        print(utils.DASH)
        print(text)
        print(utils.DASH)
        print()
    return text


def improve_all(reply, verbose=True):
    """Q7 - rewrite the reply in friendly, formal and empathetic tones."""
    results = {}
    for tone in TONES:
        results[tone] = rewrite(reply, tone, verbose)
    utils.update_state(tones=results)
    return results


if __name__ == "__main__":
    utils.banner("TONE IMPROVEMENT")
    reply = utils.require("reply", "No generated reply found. Generate a reply first.")
    if reply:
        improve_all(reply)
