import os

from dotenv import load_dotenv
import openai

from utils.constants import OPENAI_MODEL, PERSONAS


# Load environment variables
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def accept_persona_input(messages):
    user_choice_valid = False

    while not user_choice_valid:
        print("Who do you want to talk to?")
        for index, persona in enumerate(PERSONAS.keys()):
            print(f"{index + 1}: {persona}")

        user_choice = input("Persona choice: ")

        if user_choice.isdigit() and 1 <= int(user_choice) <= len(PERSONAS):
            chosen_persona = list(PERSONAS.keys())[int(user_choice) - 1]
            messages.append({"role": "system", "content": PERSONAS[chosen_persona]})
            user_choice_valid = True
            return chosen_persona
        else:
            print("Invalid choie. Please try again.")


def accept_user_input(messages):
    user_input = input("User: ")
    messages.append({"role": "user", "content": user_input})


def perform_query(messages, model=OPENAI_MODEL):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.2,
    )

    return response


def main() -> None:
    messages = []
    chosen_persona = accept_persona_input(messages)
    while True:
        accept_user_input(messages)
        response = perform_query(messages)
        messages.append(
            {"role": "system", "content": response["choices"][0]["message"]["content"]}
        )

        print(f"{chosen_persona}: {response['choices'][0]['message']['content']} \n")


# Entrypoint
if __name__ == "__main__":
    main()
