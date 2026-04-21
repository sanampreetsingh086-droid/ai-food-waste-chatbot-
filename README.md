# ai-food-waste-chatbot-
# AI-Based Food Waste Reduction Platform using Generative AI Chatbot

This project is a domain-specific generative AI chatbot built for food waste reduction. Users can enter leftover ingredients and receive realistic recipe suggestions, ingredient lists, optional additions, substitutions, and step-by-step cooking instructions through an interactive web chat interface.

## Features

- Domain-specific chef assistant for cooking and food waste reduction
- Interactive multi-turn chatbot with session-based memory
- OpenAI API integration using a real generative model
- Streamlit web app with chat-style interface
- Follow-up question support using conversation history
- Clear Chat button and loading spinner
- Beginner-friendly Python code and setup

## Project Structure

```text
project/
|-- app.py
|-- requirements.txt
|-- .env
|-- README.md
```

## Architecture

```text
User Input (UI)
-> Backend (Python / Streamlit)
-> Prompt Construction
-> OpenAI API Call
-> Response Parsing
-> Display to UI
```

## Model Configuration

The app uses these settings in the OpenAI API call:

- `temperature = 0.2` for more factual, stable, and structured recipe output
- `top_p = 0.9` to allow a small amount of creativity without making recipes unrealistic
- `max_output_tokens = 650` to give enough space for recipe name, ingredients, steps, and tips

## Setup Instructions

1. Create and activate a virtual environment if you want an isolated Python setup.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add your OpenAI API key to the `.env` file:

```env
OPENAI_API_KEY=your_key_here
```

4. Run the Streamlit app:

```bash
streamlit run app.py
```

5. Open the local URL shown by Streamlit in your browser.

## Example Input

```text
chicken, mushrooms, cream
```

## Example Output Format

```text
Recipe Name: Creamy Mushroom Chicken

Ingredients:
- chicken
- mushrooms
- cream
- garlic
- butter

Optional Additions:
- parsley
- black pepper

Steps:
1. Heat butter in a pan.
2. Add mushrooms and cook until softened.
3. Add chicken and cook through.
4. Stir in cream and simmer.

Substitutions / Tips:
- Use milk plus a little flour if cream is unavailable.
```

## Screenshots

- Add screenshot of the home screen here
- Add screenshot of chatbot conversation here

## Notes

- Do not hardcode your API key in the Python file.
- The chatbot is intentionally restricted to the cooking domain through the system prompt.
- The app stores conversation history in Streamlit `session_state` to support follow-up questions and memory.  
