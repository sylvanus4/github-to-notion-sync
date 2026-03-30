"""Tests for DeepEarLiteTools signal fetching and parsing.

Run from the skill directory:
    cd .cursor/skills/alphaear-deepear-lite && python -m pytest tests/ -v
"""

import importlib.util
import os
import sys
from unittest.mock import MagicMock, patch

import pytest

_MODULE_PATH = os.path.join(os.path.dirname(__file__), "..", "scripts", "deepear_lite.py")
_spec = importlib.util.spec_from_file_location("deepear_lite", _MODULE_PATH)
deepear_lite = importlib.util.module_from_spec(_spec)
sys.modules["deepear_lite"] = deepear_lite
_spec.loader.exec_module(deepear_lite)

DeepEarLiteTools = deepear_lite.DeepEarLiteTools

SAMPLE_SIGNALS = {
    "generated_at": "2026-03-27T09:00:00Z",
    "signals": [
        {
            "title": "Fed Rate Decision Impact",
            "summary": "Federal Reserve holds rates steady, signaling caution.",
            "sentiment_score": -0.2,
            "confidence": 0.85,
            "intensity": 0.6,
            "reasoning": "Hawkish hold with no forward guidance change.",
            "sources": [
                {"name": "Reuters", "url": "https://reuters.com/fed-decision"},
                {"name": "Bloomberg", "url": "https://bloomberg.com/fed"},
            ],
        },
        {
            "title": "NVIDIA Earnings Beat",
            "summary": "NVIDIA reports Q4 revenue above consensus.",
            "sentiment_score": 0.9,
            "confidence": 0.92,
            "intensity": 0.8,
            "reasoning": "Data-center segment grew 40% YoY.",
            "sources": [],
        },
    ],
}

EMPTY_SIGNALS = {
    "generated_at": "2026-03-27T09:00:00Z",
    "signals": [],
}


def _mock_response(json_data, status=200):
    resp = MagicMock()
    resp.status_code = status
    resp.json.return_value = json_data
    resp.raise_for_status = MagicMock()
    return resp


@pytest.fixture
def tools():
    return DeepEarLiteTools()


class TestFetchLatestSignals:
    """Verify signal parsing from mocked HTTP responses."""

    @patch("deepear_lite.requests.get")
    def test_parses_multiple_signals(self, mock_get, tools):
        mock_get.return_value = _mock_response(SAMPLE_SIGNALS)

        result = tools.fetch_latest_signals()

        assert "DeepEar Lite Signal Report" in result
        assert "Fed Rate Decision Impact" in result
        assert "NVIDIA Earnings Beat" in result

    @patch("deepear_lite.requests.get")
    def test_includes_sentiment_confidence_intensity(self, mock_get, tools):
        mock_get.return_value = _mock_response(SAMPLE_SIGNALS)

        result = tools.fetch_latest_signals()

        assert "Confidence" in result
        assert "Intensity" in result
        assert "-0.2" in result
        assert "0.9" in result
        assert "0.85" in result
        assert "0.92" in result

    @patch("deepear_lite.requests.get")
    def test_includes_source_links(self, mock_get, tools):
        mock_get.return_value = _mock_response(SAMPLE_SIGNALS)

        result = tools.fetch_latest_signals()

        assert "Reuters" in result
        assert "https://reuters.com/fed-decision" in result
        assert "Bloomberg" in result

    @patch("deepear_lite.requests.get")
    def test_includes_reasoning(self, mock_get, tools):
        mock_get.return_value = _mock_response(SAMPLE_SIGNALS)

        result = tools.fetch_latest_signals()

        assert "Hawkish hold with no forward guidance change" in result
        assert "Data-center segment grew 40% YoY" in result

    @patch("deepear_lite.requests.get")
    def test_signal_without_sources_still_rendered(self, mock_get, tools):
        mock_get.return_value = _mock_response(SAMPLE_SIGNALS)

        result = tools.fetch_latest_signals()

        assert "NVIDIA Earnings Beat" in result
        assert "NVIDIA reports Q4 revenue above consensus" in result

    @patch("deepear_lite.requests.get")
    def test_handles_empty_signals(self, mock_get, tools):
        mock_get.return_value = _mock_response(EMPTY_SIGNALS)

        result = tools.fetch_latest_signals()

        assert "No signals found" in result

    @patch("deepear_lite.requests.get")
    def test_handles_http_error(self, mock_get, tools):
        mock_get.side_effect = Exception("Connection refused")

        result = tools.fetch_latest_signals()

        assert "Error fetching DeepEar Lite data" in result
        assert "Connection refused" in result

    @patch("deepear_lite.requests.get")
    def test_generated_at_timestamp_shown(self, mock_get, tools):
        mock_get.return_value = _mock_response(SAMPLE_SIGNALS)

        result = tools.fetch_latest_signals()

        assert "2026-03-27T09:00:00Z" in result


class TestTelemetry:
    """Verify telemetry gating behavior."""

    @patch.dict(os.environ, {}, clear=True)
    @patch("deepear_lite.requests.post")
    @patch("deepear_lite.requests.get")
    def test_telemetry_disabled_by_default(self, mock_get, mock_post, tools):
        tools._record_telemetry()

        mock_get.assert_not_called()
        mock_post.assert_not_called()

    @patch.dict(os.environ, {"ALPHAEAR_TELEMETRY": "1"})
    @patch("deepear_lite.requests.post")
    @patch("deepear_lite.requests.get")
    def test_telemetry_enabled_when_env_set(self, mock_get, mock_post, tools):
        mock_get.return_value = MagicMock(status_code=200)
        mock_post.return_value = MagicMock(status_code=200)

        tools._record_telemetry()

        mock_get.assert_called_once()
        mock_post.assert_called_once()

    @patch.dict(os.environ, {"ALPHAEAR_TELEMETRY": "1"})
    @patch("deepear_lite.requests.post")
    @patch("deepear_lite.requests.get", side_effect=Exception("timeout"))
    def test_telemetry_failure_does_not_raise(self, mock_get, mock_post, tools):
        tools._record_telemetry()
