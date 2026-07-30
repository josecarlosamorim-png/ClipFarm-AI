import json
import os

from openai import OpenAI

from ai.llm_interface import LLMInterface
from ai.prompts import SYSTEM_PROMPT


class OpenAIClient(LLMInterface):

    def __init__(self):

        self.api_key = os.getenv("OPENAI_API_KEY")

        self.enabled = bool(self.api_key)

        if self.enabled:

            self.client = OpenAI(
                api_key=self.api_key
            )

    def analyze_segment(self, segment: dict) -> dict:

        # -------------------------------
        # Modo Offline (fallback)
        # -------------------------------

        if not self.enabled:

            return self._fallback(segment)

        try:

            response = self.client.chat.completions.create(

                model="gpt-4.1-mini",

                temperature=0.3,

                response_format={"type": "json_object"},

                messages=[

                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },

                    {
                        "role": "user",
                        "content": segment["text"]
                    }

                ]

            )

            result = json.loads(

                response.choices[0].message.content

            )

            return {

                "score": int(

                    result.get(

                        "score",

                        50

                    )

                ),

                "title": result.get(

                    "title",

                    "Untitled"

                ),

                "category": result.get(

                    "category",

                    "General"

                ),

                "confidence": float(

                    result.get(

                        "confidence",

                        0.80

                    )

                ),

                "reason": result.get(

                    "reason",

                    ""

                )

            }

        except Exception:

            return self._fallback(segment)

    def _fallback(self, segment):

        text = segment["text"]

        words = len(text.split())

        duration = segment["duration"]

        score = 50

        if 20 <= duration <= 40:
            score += 10

        if words > 80:
            score += 15

        if "?" in text:
            score += 5

        if "!" in text:
            score += 5

        score = min(score, 95)

        preview = text.strip().split(".")[0][:60]

        return {

            "score": score,

            "title": preview,

            "category": "Unknown",

            "confidence": 0.60,

            "reason": "Fallback heuristic"

        }