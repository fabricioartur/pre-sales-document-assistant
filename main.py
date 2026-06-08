from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

from src.config import AppConfig, ConfigError
from src.detectors import classify_document_type, detect_language, detect_response_language
from src.analysis_providers import AnalysisError, build_analysis_provider
from src.output_writer import write_outputs
from src.pdf_extractor import PdfExtractionError, extract_text_from_pdf


LOGGER = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analyze procurement PDFs for pre-sales teams."
    )
    parser.add_argument("pdf_path", help="Path to the RFP, RFI, or tender PDF.")
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory where the numbered PRD outputs will be written.",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="OpenAI model override. Used only by the openai provider.",
    )
    parser.add_argument(
        "--provider",
        choices=["mock", "openai"],
        default=None,
        help="Analysis provider to use. Defaults to ANALYSIS_PROVIDER or mock.",
    )
    return parser


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    parser = build_parser()
    args = parser.parse_args()

    try:
        LOGGER.info("Loading configuration.")
        config = AppConfig.from_env(
            provider_override=args.provider,
            model_override=args.model,
        )
        provider = build_analysis_provider(config)
        LOGGER.info("Extracting text from PDF.")
        text = extract_text_from_pdf(Path(args.pdf_path))

        detected_language = detect_language(text)
        document_type = classify_document_type(text)
        response_language = detect_response_language(text, detected_language)
        LOGGER.info(
            "Detected language=%s document_type=%s response_language=%s",
            detected_language,
            document_type,
            response_language,
        )

        LOGGER.info("Analyzing document with %s provider.", provider.name)
        analysis = provider.analyze(
            text=text,
            document_type=document_type,
            detected_language=detected_language,
            response_language=response_language,
        )

        LOGGER.info("Writing outputs.")
        output_paths = write_outputs(
            output_dir=Path(args.output_dir),
            analysis=analysis,
            metadata={
                "source_file": str(Path(args.pdf_path).resolve()),
                "detected_language": detected_language,
                "document_type": document_type,
                "response_language": response_language,
                "analysis_provider": provider.name,
                "model": config.model,
            },
        )

    except (ConfigError, PdfExtractionError, AnalysisError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Interrupted.", file=sys.stderr)
        return 130

    print("Analysis completed.")
    print(json.dumps({name: str(path) for name, path in output_paths.items()}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
