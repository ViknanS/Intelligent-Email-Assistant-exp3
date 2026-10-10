"""Part H - Complete Intelligent Email Assistant (Q10).

Menu driven application that keeps running until the user exits.
"""

import input_module
import intent_module
import reply_module
import retrieval_module
import summary_module
import tone_module
import utils

MENU = """  1. Enter Customer Email
  2. Detect Intent
  3. Retrieve Similar Email
  4. Generate AI Reply
  5. Improve Tone
  6. Summarize Conversation
  7. Save Reply
  8. Exit"""


def home_screen():
    print(utils.LINE)
    print("            INTELLIGENT EMAIL ASSISTANT")
    print("      Powered by {} running locally on Ollama".format(utils.OLLAMA_MODEL))
    print(utils.LINE)
    print(MENU)
    print(utils.LINE)


def handle(choice):
    if choice == "1":
        input_module.display_email(input_module.collect_email())
        return

    if choice == "2":
        email = utils.require("email", "Please enter a customer email first (option 1).")
        if email:
            intent_module.detect_intent(email)

    elif choice == "3":
        email = utils.require("email", "Please enter a customer email first (option 1).")
        if email:
            retrieval_module.retrieve_similar(email)

    elif choice == "4":
        email = utils.require("email", "Please enter a customer email first (option 1).")
        if not email:
            return
        state = utils.load_state()
        if not state.get("intent"):
            intent_module.detect_intent(email, verbose=False)
        if not state.get("previous_reply"):
            retrieval_module.retrieve_similar(email, verbose=False)
        reply_module.generate_reply()

    elif choice == "5":
        reply = utils.require("reply", "Please generate a reply first (option 4).")
        if reply:
            tone_module.improve_all(reply)

    elif choice == "6":
        if utils.require("reply", "Please generate a reply first (option 4)."):
            summary_module.summarize()

    elif choice == "7":
        if utils.require("reply", "Please generate a reply first (option 4)."):
            utils.save_reply(utils.load_state())

    else:
        print("Invalid choice. Please enter a number between 1 and 8.")


def main():
    try:
        utils.check_model()
    except utils.ModelError as exc:
        print(utils.LINE)
        print("  INTELLIGENT EMAIL ASSISTANT")
        print(utils.LINE)
        print(exc)
        return

    home_screen()

    while True:
        try:
            choice = input("Enter your choice : ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not choice:
            continue
        if choice == "8" or choice.lower() == "exit":
            print("\nThank you for using the Intelligent Email Assistant. Goodbye!")
            break

        print()
        try:
            handle(choice)
        except utils.ModelError as exc:
            print("Error: {}".format(exc))
        print(utils.LINE)


if __name__ == "__main__":
    main()
