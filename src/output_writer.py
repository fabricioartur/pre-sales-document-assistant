from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from src.models import AnalysisResult


def write_outputs(
    *,
    output_dir: Path,
    analysis: AnalysisResult,
    metadata: dict[str, Any],
) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)

    paths = {
        "executive_summary": output_dir / "01_executive_summary.md",
        "requirements_matrix": output_dir / "02_requirements_matrix.xlsx",
        "risk_register": output_dir / "03_risk_register.xlsx",
        "clarification_questions": output_dir / "04_clarification_questions.md",
        "go_no_go": output_dir / "05_go_no_go.md",
        "solution_outline": output_dir / "06_solution_outline.md",
        "structured_analysis": output_dir / "07_analysis.json",
    }

    structured_analysis = {**analysis, "run_metadata": metadata}
    paths["structured_analysis"].write_text(
        json.dumps(structured_analysis, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    paths["executive_summary"].write_text(
        _build_executive_summary(analysis, metadata), encoding="utf-8"
    )
    paths["clarification_questions"].write_text(
        _build_clarification_questions(analysis), encoding="utf-8"
    )
    paths["go_no_go"].write_text(_build_go_no_go(analysis), encoding="utf-8")
    paths["solution_outline"].write_text(
        _build_solution_outline(analysis), encoding="utf-8"
    )

    _write_excel(
        paths["requirements_matrix"],
        analysis.get("requirements", []),
        [
            "Requirement ID",
            "Category",
            "Requirement Description",
            "Mandatory or Optional",
            "Fit Assessment",
            "Notes",
        ],
        {
            "requirement_id": "Requirement ID",
            "category": "Category",
            "requirement_description": "Requirement Description",
            "mandatory_or_optional": "Mandatory or Optional",
            "fit_assessment": "Fit Assessment",
            "notes": "Notes",
        },
    )
    _write_excel(
        paths["risk_register"],
        analysis.get("risks", []),
        ["Risk ID", "Description", "Impact", "Probability", "Mitigation", "Owner"],
        {
            "risk_id": "Risk ID",
            "description": "Description",
            "impact": "Impact",
            "probability": "Probability",
            "mitigation": "Mitigation",
            "owner": "Owner",
        },
    )

    return paths


def _write_excel(
    path: Path,
    rows: list[dict[str, Any]],
    columns: list[str],
    column_map: dict[str, str],
) -> None:
    dataframe = pd.DataFrame(rows).rename(columns=column_map)
    if dataframe.empty:
        dataframe = pd.DataFrame(columns=columns)
    dataframe = dataframe.reindex(columns=columns)
    dataframe.to_excel(path, index=False)


def _build_executive_summary(
    analysis: AnalysisResult,
    metadata: dict[str, Any],
) -> str:
    summary = analysis.get("executive_summary", {})
    if isinstance(summary, str):
        summary = {"opportunity_overview": summary}

    lines = [
        "# Executive Summary",
        "",
        "## Metadata",
        "",
        f"- Source file: {metadata.get('source_file', '')}",
        f"- Document type: {analysis.get('document_type') or metadata.get('document_type', '')}",
        f"- Detected language: {analysis.get('detected_language') or metadata.get('detected_language', '')}",
        f"- Response language: {analysis.get('response_language') or metadata.get('response_language', '')}",
        f"- Model: {metadata.get('model', '')}",
        "",
        "## Customer Overview",
        "",
        str(summary.get("customer_overview", "Not identified.")),
        "",
        "## Opportunity Overview",
        "",
        str(summary.get("opportunity_overview", "Not identified.")),
        "",
        "## Key Objectives",
        "",
    ]

    lines.extend(_bullet_list(summary.get("key_objectives", []), "No key objectives found."))
    lines.extend(["", "## Major Requirements", ""])
    lines.extend(_bullet_list(summary.get("major_requirements", []), "No major requirements found."))
    lines.extend(["", "## Risks", ""])
    lines.extend(_bullet_list(summary.get("risks", []), "No risks found."))
    lines.extend(["", "## Recommendations", ""])
    lines.extend(_bullet_list(summary.get("recommendations", []), "No recommendations provided."))

    return "\n".join(lines) + "\n"


def _build_clarification_questions(analysis: AnalysisResult) -> str:
    lines = ["# Clarification Questions", ""]
    questions = analysis.get("clarification_questions", [])
    if not questions:
        lines.append("- No clarification questions generated.")
        return "\n".join(lines) + "\n"

    for index, item in enumerate(questions, start=1):
        lines.append(f"## Question {index}")
        lines.append("")
        lines.append(str(item.get("question", "")))
        lines.append("")
        lines.append(f"- Reason: {item.get('reason', '')}")
        lines.append(f"- Owner: {item.get('owner', '')}")
        lines.append("")
    return "\n".join(lines)


def _build_go_no_go(analysis: AnalysisResult) -> str:
    go_no_go = analysis.get("go_no_go", {})
    lines = [
        "# Go-No-Go Recommendation",
        "",
        f"## Recommendation: {go_no_go.get('recommendation', 'Needs review')}",
        "",
        "## Executive Recommendation",
        "",
        str(go_no_go.get("executive_recommendation", "No recommendation provided.")),
        "",
        "## Key Strengths",
        "",
    ]
    lines.extend(_bullet_list(go_no_go.get("key_strengths", []), "No key strengths identified."))
    lines.extend(["", "## Key Concerns", ""])
    lines.extend(_bullet_list(go_no_go.get("key_concerns", []), "No key concerns identified."))
    lines.extend(["", "## Recommended Next Actions", ""])
    lines.extend(_bullet_list(go_no_go.get("recommended_next_actions", []), "No next actions provided."))
    return "\n".join(lines) + "\n"


def _build_solution_outline(analysis: AnalysisResult) -> str:
    outline = analysis.get("solution_outline", {})
    lines = [
        "# Solution Outline",
        "",
        "## Overview",
        "",
        str(outline.get("overview", "No solution overview provided.")),
        "",
        "## Approach",
        "",
    ]
    lines.extend(_bullet_list(outline.get("approach", []), "No approach provided."))
    lines.extend(["", "## Architecture Components", ""])
    lines.extend(_bullet_list(outline.get("architecture_components", []), "No architecture components provided."))
    lines.extend(["", "## Delivery Considerations", ""])
    lines.extend(_bullet_list(outline.get("delivery_considerations", []), "No delivery considerations provided."))
    lines.extend(["", "## Assumptions", ""])
    lines.extend(_bullet_list(outline.get("assumptions", []), "No assumptions provided."))
    return "\n".join(lines) + "\n"


def _bullet_list(items: Any, empty_message: str) -> list[str]:
    if not items:
        return [f"- {empty_message}"]
    if isinstance(items, str):
        return [f"- {items}"]
    return [f"- {item}" for item in items]
