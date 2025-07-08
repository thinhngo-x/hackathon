import json
import logging
import os

from groq import Groq

from ticket_assistant.core.models import ClassificationResponse
from ticket_assistant.core.models import Department
from ticket_assistant.core.models import ErrorSeverity

logger = logging.getLogger(__name__)


class GroqClassifier:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY must be provided or set as environment variable")

        self.client = Groq(api_key=self.api_key)

    async def classify_error(
        self,
        error_description: str,
        error_message: str | None = None,
        context: str | None = None,
    ) -> ClassificationResponse:
        """Classify error and route to appropriate department using Groq API."""
        try:
            # Construct the prompt for classification
            prompt = self._build_classification_prompt(error_description, error_message, context)

            # Call Groq API
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert technical support classifier. "
                            "Analyze errors and route them to the appropriate department."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.1,
                max_tokens=1000,
            )

            response_text = chat_completion.choices[0].message.content

            # Parse the response
            classification = self._parse_classification_response(response_text)

            return classification

        except Exception as e:
            logger.error(f"Error in Groq classification: {e!s}")
            # Return a default classification
            return ClassificationResponse(
                department=Department.GENERAL,
                severity=ErrorSeverity.MEDIUM,
                confidence=0.5,
                reasoning="Classification failed due to API error",
                suggested_actions=["Manual review required"],
            )

    def _build_classification_prompt(
        self,
        error_description: str,
        error_message: str | None = None,
        context: str | None = None,
    ) -> str:
        """Build the prompt for error classification."""
        prompt = f"""
Please analyze the following error and classify it for routing to the appropriate department.

Error Description: {error_description}
"""

        if error_message:
            prompt += f"\nError Message: {error_message}"

        if context:
            prompt += f"\nContext: {context}"

        prompt += """

Based on this information, please provide a JSON response with the following structure:
{
    "department": "one of: backend, frontend, database, devops, security, api, integration, general",
    "severity": "one of: low, medium, high, critical",
    "confidence": "float between 0.0 and 1.0",
    "reasoning": "explanation of your classification decision",
    "suggested_actions": ["list", "of", "suggested", "actions"]
}

Consider these classification guidelines:
- Backend: Server-side logic, business logic errors, internal API issues
- Frontend: UI/UX issues, client-side JavaScript errors, rendering problems
- Database: Data storage, query issues, connection problems
- DevOps: Deployment, infrastructure, CI/CD, environment issues
- Security: Authentication, authorization, data privacy, vulnerability issues
- API: External API integration, endpoint errors, data format issues
- Integration: Third-party service integration, workflow automation issues
- General: Unclear issues or those spanning multiple departments

Severity levels:
- Critical: System down, data loss, security breach
- High: Major functionality broken, affecting many users
- Medium: Moderate impact, workarounds available
- Low: Minor issues, cosmetic problems
"""

        return prompt

    def _parse_classification_response(self, response_text: str) -> ClassificationResponse:
        """Parse the Groq API response into a ClassificationResponse object."""
        try:
            # Try to extract JSON from the response
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}") + 1

            if start_idx != -1 and end_idx != 0:
                json_str = response_text[start_idx:end_idx]
                parsed = json.loads(json_str)

                return ClassificationResponse(
                    department=Department(parsed.get("department", "general")),
                    severity=ErrorSeverity(parsed.get("severity", "medium")),
                    confidence=float(parsed.get("confidence", 0.7)),
                    reasoning=parsed.get("reasoning", "Automated classification"),
                    suggested_actions=parsed.get("suggested_actions", ["Review required"]),
                )
            else:
                raise ValueError("No valid JSON found in response")

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logger.error(f"Failed to parse classification response: {e!s}")
            # Return a default response
            return ClassificationResponse(
                department=Department.GENERAL,
                severity=ErrorSeverity.MEDIUM,
                confidence=0.5,
                reasoning="Failed to parse classification response",
                suggested_actions=["Manual review required"],
            )
