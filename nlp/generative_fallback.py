def get_answer(query: str, department: str, context_snippet: str | None = None) -> str:
    """Generate an answer using OpenAI GPT‑4.
    Raises RuntimeError if OpenAI key not set or library unavailable.
    """
    try:
        import openai
    except ImportError as e:
        raise RuntimeError("openai package is not installed") from e
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set in environment")
    openai.api_key = api_key
    prompt = f"You are an internal corporate assistant for the {department} department. Answer the employee's question concisely and professionally."
    if context_snippet:
        prompt += f"\nRelevant policy excerpt:\n{context_snippet}"
    prompt += f"\nQuestion: {query}\nAnswer:"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=500,
    )
    return response.choices[0].message.content.strip()
