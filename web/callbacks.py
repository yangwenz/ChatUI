import pprint
from dash import Input, Output, State, callback

# TODO: Replace this naive model
from models.naive import NaiveBot

model = NaiveBot()

PLAYER_A = "You:"
PLAYER_B = "Robot:"
_DEBUG_ = False


def query(payload):
    if _DEBUG_:
        pprint.pprint(payload)
    answer = model.predict(payload)
    return {"generated_answer": answer}


@callback(
    Output("user-input", "value"),
    [
        Input("submit", "n_clicks"),
        Input("user-input", "n_submit")
    ],
)
def clear_input(n_clicks, n_submit):
    return ""


def _process_chat_history(chat_history):
    chats = chat_history.split("<split>")
    past_user_inputs = [s[len(PLAYER_A):].strip() for s in chats if s.startswith(PLAYER_A)]
    generated_responses = [s[len(PLAYER_B):].strip() for s in chats if s.startswith(PLAYER_B)]
    return past_user_inputs, generated_responses


@callback(
    [
        Output("chat-history", "data"),
        Output("all-chats", "data"),
        Output("loading-component", "children")
    ],
    [
        Input("submit", "n_clicks"),
        Input("user-input", "n_submit")
    ],
    [
        State("user-input", "value"),
        State("chat-history", "data"),
        State("all-chats", "data")
    ],
)
def run_chatbot(n_clicks, n_submit, user_input, chat_history, all_chats):
    if n_clicks == 0 and n_submit is None:
        return "", "", None
    if user_input is None or user_input == "":
        return chat_history, all_chats, None

    past_user_inputs, generated_responses = \
        _process_chat_history(chat_history)
    output = query({
        "inputs": {
            "past_user_inputs": past_user_inputs,
            "generated_responses": generated_responses,
            "text": user_input,
            "prompt": None
        }
    })
    model_output = output["generated_answer"]
    if isinstance(model_output, list):
        chat_history += f"{PLAYER_A} {user_input}<split>{PLAYER_B} {model_output[0]}<split>"
        all_chats += f"{PLAYER_A} {user_input}<split>" + \
                     "<split>".join([f"{PLAYER_B} {s}" for s in model_output]) + "<split>"
    else:
        chat_history += f"{PLAYER_A} {user_input}<split>{PLAYER_B} {model_output}<split>"
        all_chats += f"{PLAYER_A} {user_input}<split>{PLAYER_B} {model_output}<split>"

    return chat_history, all_chats, None
