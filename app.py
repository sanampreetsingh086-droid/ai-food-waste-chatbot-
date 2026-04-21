import os
from typing import List, Dict

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


SYSTEM_PROMPT = """
You are a professional chef and food sustainability expert.
Your task is to reduce food waste by suggesting recipes using leftover ingredients provided by the user.

You must stay strictly within the cooking and food waste reduction domain.
Only answer questions related to recipes, ingredients, cooking methods, substitutions, portion adjustments, storage, and food waste reduction.
If the user asks something outside this domain, politely refuse and redirect them back to recipe or ingredient-related questions.

Always:
- Use the given ingredients as the core of the recipe
- Suggest a creative but realistic recipe
- Provide:
  1. Recipe Name
  2. Ingredients List
  3. Step-by-step Instructions
- Suggest substitutions if needed
- Keep instructions clear, practical, and beginner-friendly
- Mention optional additions separately when useful
- Support follow-up questions based on earlier conversation context
- Prioritize reducing food waste and using what the user already has

Preferred response format:
Recipe Name: <name>

Ingredients:
- <ingredient 1>
- <ingredient 2>

Optional Additions:
- <optional item 1>
- <optional item 2>

Steps:
1. <step one>
2. <step two>

Substitutions / Tips:
- <tip or substitution>
""".strip()


SUGGESTED_INGREDIENTS = [
    "rice, carrots, peas, soy sauce",
    "chicken, mushrooms, cream",
    "bread, tomatoes, cheese",
    "potatoes, onions, eggs",
    "spinach, paneer, garlic",
]


def initialize_session_state() -> None:
    """Create persistent chat history for the current browser session."""
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]


def get_api_key() -> str | None:
    """Read the OpenAI API key from environment variables loaded via .env."""
    return os.getenv("OPENAI_API_KEY")


def get_client(api_key: str) -> OpenAI:
    """Create a reusable OpenAI client."""
    return OpenAI(api_key=api_key)


def build_messages(user_input: str) -> List[Dict[str, str]]:
    """Append the current user message to the existing session history."""
    conversation = st.session_state.messages.copy()
    conversation.append({"role": "user", "content": user_input})
    return conversation


def generate_recipe_response(client: OpenAI, messages: List[Dict[str, str]]) -> str:
    """
    Send the full conversation to the OpenAI Responses API so the chatbot
    can answer with memory of previous turns.
    """
    response = client.responses.create(
        model="gpt-4o",
        input=messages,
        # Low temperature keeps recipe output stable, factual, and well-structured.
        temperature=0.2,
        # Slightly broad sampling allows some creativity without drifting off-domain.
        top_p=0.9,
        # Enough room for recipe title, ingredients, instructions, and substitutions.
        max_output_tokens=650,
    )
    return response.output_text.strip()


def render_chat_history() -> None:
    """Display chat messages except the hidden system prompt."""
    for message in st.session_state.messages:
        if message["role"] == "system":
            continue
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def main() -> None:
    st.set_page_config(
        page_title="AI Food Waste Reduction Chatbot",
        page_icon="AI",
        layout="centered",
    )

    st.title("AI-Based Food Waste Reduction Platform")
    st.caption(
        "A domain-specific generative AI chef assistant that turns leftover ingredients into practical recipes."
    )

    st.info(
        "Ask for recipes, substitutions, cooking steps, storage tips, or follow-up improvements using your leftover ingredients."
    )

    initialize_session_state()
    api_key = get_api_key()

    with st.sidebar:
        st.subheader("Quick Start")
        st.write("Try one of these leftover ingredient ideas:")
        for sample in SUGGESTED_INGREDIENTS:
            st.code(sample, language="text")

        if st.button("Clear Chat", use_container_width=True):
            st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            st.rerun()

        st.divider()
        st.write("Architecture Flow")
        st.write("User Input -> Backend -> Prompt Construction -> OpenAI API -> Response -> Chat UI")

    if not api_key:
        st.error(
            "Missing OPENAI_API_KEY. Add it to your .env file before running the app."
        )
        st.stop()

    render_chat_history()

    user_input = st.chat_input(
        "Enter leftover ingredients or ask a cooking follow-up question..."
    )

    if not user_input:
        return

    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        client = get_client(api_key)
        messages = build_messages(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("assistant"):
            with st.spinner("Cooking up a food-waste-friendly recipe..."):
                assistant_reply = generate_recipe_response(client, messages)
                st.markdown(assistant_reply)

        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_reply}
        )

    except Exception as exc:
        error_message = (
            "I couldn't reach the recipe model right now. Please check your API key, "
            f"internet connection, and billing setup.\n\nTechnical details: `{exc}`"
        )
        with st.chat_message("assistant"):
            st.error(error_message)
        st.session_state.messages.append(
            {"role": "assistant", "content": error_message}
        )


if __name__ == "__main__":
    main()
