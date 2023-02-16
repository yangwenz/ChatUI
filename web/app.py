import os
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output
from web.layout import create_banner, create_textbox, \
    create_conversation_box, create_controls

import web.callbacks
from web.callbacks import PLAYER_A

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title="Chatbot",
)
app.config["suppress_callback_exceptions"] = True
server = app.server

app.layout = dbc.Container(
    fluid=False,
    children=[
        create_banner(app),
        html.Br(),
        create_conversation_box(),
        create_controls(),
        html.Br(),
        dbc.Spinner(html.Div(id="loading-component")),
        dcc.Store(id="chat-history", data=""),
        dcc.Store(id="all-chats", data=""),
    ],
)


def _process_bot_responses(responses):
    children = []
    colors = ["green", "grey"]
    for i, text in enumerate(responses):
        text = text.replace("Robot:", "").replace("You:", "")
        if i == 0:
            children.append(html.Label(text, style={"font-weight": "bold"}))
            children.append(html.Br())
        else:
            children.append(html.Label(text, style={"color": colors[i % len(colors)]}))
            if i != len(responses) - 1:
                children.append(html.Br())
    return html.Div(children=children)


@app.callback(
    Output("display-conversation", "children"),
    Input("all-chats", "data")
)
def update_display(chats):
    boxes = []
    bot_responses = []
    for i, text in enumerate(chats.split("<split>")[:-1]):
        if text.startswith(PLAYER_A):
            if len(bot_responses) > 0:
                boxes.append(create_textbox(
                    app, _process_bot_responses(bot_responses), box="AI", inverse=False))
                bot_responses = []
            boxes.append(create_textbox(app, text, box="user"))
        else:
            bot_responses.append(text)
    if len(bot_responses) > 0:
        boxes.append(create_textbox(
            app, _process_bot_responses(bot_responses), box="AI", inverse=False))
    return boxes


@app.server.route("/ping")
def ping():
    return "{status: ok}"


if __name__ == "__main__":
    host = os.getenv("HOST", "localhost")
    port = os.getenv("PORT", "8080")
    app.run_server(host=host, port=port, debug=False)
