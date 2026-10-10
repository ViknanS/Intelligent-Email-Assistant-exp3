"""Part C - Similar email retrieval (Q4, Q5)."""

from sentence_transformers import SentenceTransformer, util

import utils

_model = None
_emails = None
_embeddings = None


def _build():
    """Q4 - load the previous customer interactions and embed them."""
    global _model, _emails, _embeddings
    if _embeddings is None:
        _emails = utils.load_emails()
        _model = SentenceTransformer(utils.EMBEDDING_MODEL)
        _embeddings = _model.encode(_emails["Customer_Email"].tolist(),
                                    normalize_embeddings=True)
    return _emails, _model, _embeddings


def retrieve_similar(email, verbose=True):
    """Q5 - retrieve the most similar previous email and its reply."""
    emails, model, embeddings = _build()
    query = model.encode(email, normalize_embeddings=True)
    scores = util.cos_sim(query, embeddings)[0]
    best = int(scores.argmax())
    row = emails.iloc[best]
    score = float(scores[best])

    utils.update_state(previous_email=row["Customer_Email"],
                       previous_reply=row["Previous_Reply"])

    if verbose:
        print("Similar Email Retrieval")
        print(utils.DASH)
        print("Dataset records   : {}".format(len(emails)))
        print("Matched Email ID  : {}".format(row["Email_ID"]))
        print("Category          : {}".format(row["Category"]))
        print("Similarity Score  : {}".format(round(score, 4)))
        print()
        print("Previous Email")
        print(row["Customer_Email"])
        print()
        print("Previous Reply")
        print(row["Previous_Reply"])
        print(utils.DASH)
    return {"email": row["Customer_Email"], "reply": row["Previous_Reply"],
            "score": score, "category": row["Category"]}


if __name__ == "__main__":
    utils.banner("SIMILAR EMAIL RETRIEVAL")
    email = utils.require("email", "No customer email found. Enter one first.")
    if email:
        print("Customer Email : {}".format(email))
        print()
        retrieve_similar(email)
