from __future__ import annotations


def detect_language(text: str) -> str:
    lowered = text[:12000].lower()

    portuguese_hits = _count_hits(
        lowered,
        [
            "proposta",
            "licitação",
            "pregão",
            "edital",
            "fornecedor",
            "contrato",
            "prazo",
            "solução",
            "técnica",
        ],
    )
    spanish_hits = _count_hits(
        lowered,
        [
            "propuesta",
            "licitación",
            "pliego",
            "proveedor",
            "contrato",
            "plazo",
            "solución",
            "técnica",
        ],
    )
    english_hits = _count_hits(
        lowered,
        [
            "proposal",
            "request for",
            "vendor",
            "supplier",
            "contract",
            "deadline",
            "technical",
            "solution",
        ],
    )

    scores = {
        "Portuguese": portuguese_hits,
        "Spanish": spanish_hits,
        "English": english_hits,
    }
    language, score = max(scores.items(), key=lambda item: item[1])
    return language if score > 0 else "English"


def classify_document_type(text: str) -> str:
    lowered = text[:16000].lower()

    if any(term in lowered for term in ["request for proposal", "rfp", "solicitação de proposta"]):
        return "RFP"
    if any(term in lowered for term in ["request for information", "rfi", "solicitação de informação"]):
        return "RFI"
    if any(
        term in lowered
        for term in [
            "government tender",
            "public bid",
            "public procurement",
            "licitação",
            "pregão",
            "edital",
            "licitación pública",
        ]
    ):
        return "Government Tender"
    return "Unknown"


def detect_response_language(text: str, fallback_language: str) -> str:
    lowered = text[:16000].lower()
    if any(
        term in lowered
        for term in [
            "responses must be submitted in english",
            "proposal must be submitted in english",
            "language of response: english",
        ]
    ):
        return "English"
    if any(
        term in lowered
        for term in [
            "proposta deve ser apresentada em português",
            "resposta deve ser apresentada em português",
            "idioma da resposta: português",
        ]
    ):
        return "Portuguese"
    if any(
        term in lowered
        for term in [
            "propuesta debe presentarse en español",
            "respuesta debe presentarse en español",
            "idioma de respuesta: español",
        ]
    ):
        return "Spanish"
    return fallback_language


def _count_hits(text: str, terms: list[str]) -> int:
    return sum(1 for term in terms if term in text)
