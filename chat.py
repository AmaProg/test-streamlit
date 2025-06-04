import streamlit as st
import ollama


class ChatBot:
    def __init__(self):
        pass

    @classmethod
    def run(cls):

        st.title("John Snow Senior assistant of HVACR")

        if "message" not in st.session_state:
            st.session_state.message = []

        for message in st.session_state.message:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        prompt = st.chat_input("What is up?")

        if prompt:

            with st.chat_message("user"):
                st.markdown(prompt)

            st.session_state.message.append({"role": "user", "content": prompt})

            # Prépare la zone pour la réponse
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""

                # Itération sur la réponse en streaming
                for chunk in ollama.chat(
                    model="snow3",
                    messages=[{"role": "user", "content": prompt}],
                    stream=True,
                ):
                    # Ajoute le contenu progressivement
                    full_response += chunk["message"]["content"]
                    message_placeholder.markdown(
                        full_response + "▌"
                    )  # petit curseur pour l'effet "en cours"

                # Enlève le curseur à la fin
                message_placeholder.markdown(full_response)

            # Ajoute la réponse complète à l'historique
            st.session_state.message.append(
                {"role": "assistant", "content": full_response}
            )
