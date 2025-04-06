# streamlit_app.py
import streamlit as st
from controller.game_controller import GameController
from controller.mapping import players


def run():
    # UI controls
    st.title("Thor Vs Loki Bot Playground ")
    players_list = players.keys()

    env = st.selectbox("Environment", ["local", "mock", "sandbox", "live"])
    board_size = st.number_input('Board Size', value=6)
    player1_logic = st.selectbox("Player 1 Logic", players_list)
    player2_logic = st.selectbox("Player 2 Logic (Required for local)", players_list, index=None)
    player1_role = st.selectbox("Player 1 Role", ["Thor", "Loki"])
    display_board = st.checkbox("Display Board", value=True)


    # Run button
    if st.button("Start Game"):
        controller = GameController(
            env=env,
            p1_logic=player1_logic,
            p2_logic=player2_logic,
            player1_role=player1_role,
            board_size=board_size
        )
        controller.run()
