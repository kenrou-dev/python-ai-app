import google.generativeai as genai

_model = None


def get_model(api_key: str, model_name: str = "gemini-2.5-flash") -> genai.GenerativeModel:
    global _model
    genai.configure(api_key=api_key)
    _model = genai.GenerativeModel(model_name)
    return _model


def generate(api_key: str, prompt: str, model_name: str = "gemini-2.5-flash") -> str:
    model = get_model(api_key, model_name)
    response = model.generate_content(prompt)
    return response.text
