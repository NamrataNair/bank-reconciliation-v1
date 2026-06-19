import json
import requests
from django.conf import settings

class BaseAIService:
    def get_match_suggestion(self, bank_tx_data, source_tx_data):
        raise NotImplementedError("Subclasses must implement this method")

    def _build_prompt(self, bank_tx_data, source_tx_data):
        return f"""
        You are an expert accountant matching bank transactions.
        Bank Transaction: {json.dumps(bank_tx_data)}
        Source Transaction: {json.dumps(source_tx_data)}

        Do these transactions represent the same event?
        Return ONLY a JSON object with 'confidence_score' (0.0 to 1.0) and 'reasoning' (string).
        """

class OpenAIService(BaseAIService):
    def __init__(self):
        from openai import OpenAI
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-4o-mini"

    def get_match_suggestion(self, bank_tx_data, source_tx_data):
        prompt = self._build_prompt(bank_tx_data, source_tx_data)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        result = json.loads(response.choices[0].message.content)
        return {
            'confidence_score': result.get('confidence_score', 0.0),
            'model_version': self.model
        }

class GeminiService(BaseAIService):
    def __init__(self):
        import google.generativeai as genai
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def get_match_suggestion(self, bank_tx_data, source_tx_data):
        prompt = self._build_prompt(bank_tx_data, source_tx_data)
        response = self.model.generate_content(prompt)
        try:
            # Basic parsing, Gemini might wrap in markdown
            text = response.text.strip().replace('```json', '').replace('```', '')
            result = json.loads(text)
            return {
                'confidence_score': result.get('confidence_score', 0.0),
                'model_version': 'gemini-1.5-flash'
            }
        except:
            return {'confidence_score': 0.0, 'model_version': 'gemini-error'}

class OllamaService(BaseAIService):
    def __init__(self):
        self.endpoint = settings.OLLAMA_ENDPOINT
        self.model = settings.OLLAMA_MODEL

    def get_match_suggestion(self, bank_tx_data, source_tx_data):
        prompt = self._build_prompt(bank_tx_data, source_tx_data)
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }
        try:
            response = requests.post(self.endpoint, json=payload, timeout=10)
            response.raise_for_status()
            result = json.loads(response.json().get('response', '{}'))
            return {
                'confidence_score': result.get('confidence_score', 0.0),
                'model_version': self.model
            }
        except:
            return {'confidence_score': 0.0, 'model_version': f'ollama-{self.model}-error'}

class AIFactory:
    @staticmethod
    def get_service():
        provider = settings.AI_PROVIDER.lower()
        if provider == 'openai':
            return OpenAIService()
        elif provider == 'gemini':
            return GeminiService()
        elif provider == 'ollama':
            return OllamaService()
        else:
            raise ValueError(f"Unknown AI provider: {provider}")
