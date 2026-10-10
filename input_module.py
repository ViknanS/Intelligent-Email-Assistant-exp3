"""Part A - User input (Q1, Q2)."""

import utils


def collect_email():
    """Q1 - read the customer name, email subject and customer email."""
    print("Enter Customer Email Details")
    print(utils.DASH)

    name = ""
    while not name:
        name = input("Customer Name  : ").strip()
        if not name:
            print("Customer name cannot be empty.")

    subject = input("Email Subject  : ").strip() or "General Inquiry"

    email = ""
    while not email:
        email = input("Customer Email : ").strip()
        if not email:
            print("The email body cannot be empty.")

    utils.update_state(name=name, subject=subject, email=email,
                       intent="", reply="", summary="")
    return {"name": name, "subject": subject, "email": email}


def display_email(details):
    """Q2 - display the entered details."""
    print()
    print(utils.DASH)
    print("CUSTOMER EMAIL")
    print(utils.DASH)
    print("Customer Name : {}".format(details["name"]))
    print("Subject       : {}".format(details["subject"]))
    print("Customer Email")
    print(details["email"])
    print(utils.DASH)


if __name__ == "__main__":
    utils.banner("CUSTOMER EMAIL INPUT")
    display_email(collect_email())
