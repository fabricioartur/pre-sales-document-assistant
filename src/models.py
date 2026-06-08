from __future__ import annotations

from typing import Any, TypedDict


class Requirement(TypedDict, total=False):
    requirement_id: str
    category: str
    requirement_description: str
    mandatory_or_optional: str
    fit_assessment: str
    notes: str


class Risk(TypedDict, total=False):
    risk_id: str
    description: str
    impact: str
    probability: str
    mitigation: str
    owner: str


class Question(TypedDict, total=False):
    question: str
    reason: str
    owner: str


class ComplianceItem(TypedDict, total=False):
    requirement: str
    response: str
    notes: str
    status: str


class AnalysisResult(TypedDict, total=False):
    executive_summary: dict[str, Any]
    document_type: str
    detected_language: str
    response_language: str
    customer_context: dict[str, Any]
    key_dates: list[dict[str, Any]]
    requirements: list[Requirement]
    risks: list[Risk]
    clarification_questions: list[Question]
    go_no_go: dict[str, Any]
    solution_outline: dict[str, Any]
    recommended_next_steps: list[str]
