import json
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from ticket_assistant.core.models import ClassificationRequest
from ticket_assistant.core.models import Department
from ticket_assistant.core.models import ErrorSeverity
from ticket_assistant.services.groq_classifier import GroqClassifier


class TestGroqClassifier:
    @pytest.fixture
    def mock_groq_response(self):
        """Fixture for mock Groq API response"""
        return {
            "choices": [
                {
                    "message": {
                        "content": """
                        {
                            "department": "database",
                            "severity": "high",
                            "confidence": 0.95,
                            "reasoning": (
                                "The error indicates a database connection timeout, which is a database "
                                "infrastructure issue requiring immediate attention."
                            ),
                            "suggested_actions": [
                                "Check database server status",
                                "Verify network connectivity",
                                "Review connection pool settings",
                            ],
                        }
                        """
                    }
                }
            ]
        }

    @pytest.fixture
    def sample_classification_request(self):
        """Fixture for sample classification request"""
        return ClassificationRequest(
            error_description="Database connection timeout after 30 seconds",
            error_message="psycopg2.OperationalError: could not connect to server",
            context="User trying to load dashboard data",
        )

    def test_groq_classifier_initialization_with_api_key(self):
        """Test GroqClassifier initialization with API key"""
        classifier = GroqClassifier(api_key="test-api-key")  # pragma: allowlist secret
        assert classifier.api_key == "test-api-key"
        assert classifier.client is not None

    def test_groq_classifier_initialization_without_api_key(self):
        """Test GroqClassifier initialization without API key should raise error"""
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError, match="GROQ_API_KEY must be provided"):
                GroqClassifier()

    def test_groq_classifier_initialization_with_env_var(self):
        """Test GroqClassifier initialization with environment variable"""
        # pragma: allowlist secret
        with patch.dict("os.environ", {"GROQ_API_KEY": "env-api-key"}):
            classifier = GroqClassifier()
            assert classifier.api_key == "env-api-key"

    @pytest.mark.asyncio
    async def test_classify_error_success(self, mock_groq_response, sample_classification_request):
        """Test successful error classification"""
        with patch("ticket_assistant.services.groq_classifier.Groq") as mock_groq:
            # Setup mock
            mock_client = MagicMock()
            mock_groq.return_value = mock_client

            # Create a proper mock response object
            mock_response = MagicMock()
            mock_response.choices = [
                MagicMock(
                    message=MagicMock(
                        content=json.dumps(
                            {
                                "department": "database",
                                "severity": "high",
                                "confidence": 0.95,
                                "reasoning": (
                                    "The error indicates a database connection timeout, which is a database "
                                    "infrastructure issue requiring immediate attention."
                                ),
                                "suggested_actions": [
                                    "Check database server status",
                                    "Verify network connectivity",
                                    "Review connection pool settings",
                                ],
                            }
                        )
                    )
                )
            ]
            mock_client.chat.completions.create.return_value = mock_response

            classifier = GroqClassifier(api_key="test-key")

            result = await classifier.classify_error(
                error_description=sample_classification_request.error_description,
                error_message=sample_classification_request.error_message,
                context=sample_classification_request.context,
            )

            assert result.department == Department.DATABASE
            assert result.severity == ErrorSeverity.HIGH
            assert result.confidence == 0.95
            assert "database connection timeout" in result.reasoning.lower()
            assert len(result.suggested_actions) == 3

    @pytest.mark.asyncio
    async def test_classify_error_api_failure(self, sample_classification_request):
        """Test error classification when Groq API fails"""
        with patch("ticket_assistant.services.groq_classifier.Groq") as mock_groq:
            # Setup mock to raise exception
            mock_client = MagicMock()
            mock_groq.return_value = mock_client
            mock_client.chat.completions.create.side_effect = Exception("API Error")

            classifier = GroqClassifier(api_key="test-key")

            result = await classifier.classify_error(error_description=sample_classification_request.error_description)

            # Should return default classification
            assert result.department == Department.GENERAL
            assert result.severity == ErrorSeverity.MEDIUM
            assert result.confidence == 0.5
            assert "Classification failed due to API error" in result.reasoning

    def test_build_classification_prompt(self):
        """Test prompt building for classification"""
        classifier = GroqClassifier(api_key="test-key")

        prompt = classifier._build_classification_prompt(
            error_description="Test error",
            error_message="Error message",
            context="Test context",
        )

        assert "Test error" in prompt
        assert "Error message" in prompt
        assert "Test context" in prompt
        assert "department" in prompt
        assert "severity" in prompt
        assert "confidence" in prompt
        assert "JSON response" in prompt

    def test_build_classification_prompt_minimal(self):
        """Test prompt building with minimal information"""
        classifier = GroqClassifier(api_key="test-key")

        prompt = classifier._build_classification_prompt(error_description="Test error only")

        assert "Test error only" in prompt
        assert "department" in prompt
        assert "severity" in prompt

    def test_parse_classification_response_valid_json(self):
        """Test parsing valid JSON response"""
        classifier = GroqClassifier(api_key="test-key")

        response_text = """
        Here is the classification:
        {
            "department": "frontend",
            "severity": "low",
            "confidence": 0.8,
            "reasoning": "UI rendering issue",
            "suggested_actions": ["Check CSS", "Validate HTML"]
        }
        Additional text here.
        """

        result = classifier._parse_classification_response(response_text)

        assert result.department == Department.FRONTEND
        assert result.severity == ErrorSeverity.LOW
        assert result.confidence == 0.8
        assert result.reasoning == "UI rendering issue"
        assert len(result.suggested_actions) == 2

    def test_parse_classification_response_invalid_json(self):
        """Test parsing invalid JSON response"""
        classifier = GroqClassifier(api_key="test-key")

        response_text = "This is not a valid JSON response"

        result = classifier._parse_classification_response(response_text)

        # Should return default values
        assert result.department == Department.GENERAL
        assert result.severity == ErrorSeverity.MEDIUM
        assert result.confidence == 0.5
        assert "Failed to parse classification response" in result.reasoning

    def test_parse_classification_response_malformed_json(self):
        """Test parsing malformed JSON response"""
        classifier = GroqClassifier(api_key="test-key")

        response_text = """
        {
            "department": "invalid_department",
            "severity": "invalid_severity",
            "confidence": "not_a_number"
        }
        """

        result = classifier._parse_classification_response(response_text)

        # Should return default values due to invalid enum values
        assert result.department == Department.GENERAL
        assert result.severity == ErrorSeverity.MEDIUM
        assert result.confidence == 0.5

    @pytest.mark.asyncio
    async def test_classify_error_different_departments(self):
        """Test classification for different types of errors"""
        test_cases = [
            {
                "description": "React component not rendering properly",
                "expected_dept": "frontend",
            },
            {
                "description": "API endpoint returning 500 error",
                "expected_dept": "backend",
            },
            {"description": "SQL query timeout", "expected_dept": "database"},
            {"description": "Docker container won't start", "expected_dept": "devops"},
            {"description": "Unauthorized access attempt", "expected_dept": "security"},
        ]

        for case in test_cases:
            with patch("ticket_assistant.services.groq_classifier.Groq") as mock_groq:
                mock_client = MagicMock()
                mock_groq.return_value = mock_client

                # Create a proper mock response object
                mock_response = MagicMock()
                mock_response.choices = [
                    MagicMock(
                        message=MagicMock(
                            content=json.dumps(
                                {
                                    "department": case["expected_dept"],
                                    "severity": "medium",
                                    "confidence": 0.9,
                                    "reasoning": f"This is a {case['expected_dept']} issue",
                                    "suggested_actions": ["Action 1", "Action 2"],
                                }
                            )
                        )
                    )
                ]
                mock_client.chat.completions.create.return_value = mock_response

                classifier = GroqClassifier(api_key="test-key")

                result = await classifier.classify_error(error_description=case["description"])

                assert result.department.value == case["expected_dept"]
                assert result.confidence == 0.9


if __name__ == "__main__":
    pytest.main([__file__])
