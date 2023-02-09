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


@app.callback(
    Output("display-conversation", "children"),
    Input("all-chats", "data")
)
def update_display(chats):
    boxes = []
    for i, text in enumerate(chats.split("<split>")[:-1]):
        if text.startswith(PLAYER_A):
            boxes.append(create_textbox(app, text, box="user"))
        else:
            color = "secondary" if i % 4 == 1 else "info"
            boxes.append(create_textbox(app, text, box="AI", color=color))
    return boxes


@app.server.route("/ping")
def ping():
    return "{status: ok}"


if __name__ == "__main__":
    host = os.getenv("HOST", "localhost")
    port = os.getenv("PORT", "8080")
    app.run_server(host=host, port=port, debug=False)
