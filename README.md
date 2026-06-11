# Pre-Sales Document Assistant

Command-line assistant for analyzing enterprise procurement documents.

It supports:

- RFP
- RFI
- Government tender documents / public bids

Target users:

- Sales Engineers
- Solutions Engineers
- Solution Architects
- Bid Managers
- Pre-Sales professionals

## Features

- Extracts text from PDF files with `pypdf`
- Detects document language: English, Portuguese, or Spanish
- Classifies document type: RFP, RFI, Government Tender, or Unknown
- Detects the required response language
- Runs by default with a local mock analysis provider (no API key required)
- OpenAI provider using the Responses API with retry and exponential backoff
- `--reasoning` flag with four effort levels matching the OpenAI Codex interface
- Generates structured output in JSON, Markdown, and Excel
- Handles common errors such as missing files, non-PDF input, empty PDFs, missing API keys, unavailable dependencies, API failures, and invalid JSON returned by the model

## Setup

```bash
pip install -r requirements.txt
```

The mock provider requires no `.env` file or OpenAI credentials.

To use the OpenAI provider, copy `.env.example` to `.env` and set:

```text
OPENAI_API_KEY=your_api_key_here
ANALYSIS_PROVIDER=openai
```

## Usage

```bash
# Demo mode — no API key required
python main.py input/rfp.pdf --provider mock

# Standard run with default model
python main.py input/rfp.pdf --provider openai

# High-quality analysis for a complex tender
python main.py input/rfp.pdf --provider openai --model gpt-5.4

# Strategic account — maximum depth
python main.py input/rfp.pdf --provider openai --model gpt-5.5 --reasoning extra_high
```

## Model Selection

| Model | Cost (input / output per MTok) | Use When |
|-------|-------------------------------|----------|
| `gpt-5.4-mini` *(default)* | $0.75 / $4.50 | Routine RFP analysis, daily use — fast and cost-efficient |
| `gpt-5.4` | $2.50 / $15.00 | Complex enterprise tenders and final deliverables |
| `gpt-5.5` | $5.00 / $30.00 | Strategic accounts, board-level reports, highest output quality |

### Reasoning Effort

GPT-5 models support a `--reasoning` flag that controls how deeply the model thinks before producing output.

| Level | Use When |
|-------|----------|
| `low` | Fast summaries and routine documents — lowest cost |
| `medium` | Balanced quality for standard enterprise tenders |
| `high` | Complex requirements, technical architecture, compliance-heavy scenarios |
| `extra_high` | Strategic accounts, final proposals, maximum output quality |

> **Note:** When `--reasoning` is set, `temperature` is disabled — reasoning models control their own sampling internally.

## Outputs

Each run creates:

- `output/01_executive_summary.md`
- `output/02_requirements_matrix.xlsx`
- `output/03_risk_register.xlsx`
- `output/04_clarification_questions.md`
- `output/05_go_no_go.md`
- `output/06_solution_outline.md`
- `output/07_analysis.json`

## Preview

### Executive Summary

![Executive Summary preview](docs/images/executive-summary.png)

### Requirements Matrix

![Requirements Matrix preview](docs/images/requirements-matrix.png)

### Risk Register

![Risk Register preview](docs/images/risk-register.png)

### Go-No-Go Recommendation

![Go-No-Go Recommendation preview](docs/images/go-no-go.png)

To refresh these preview images, install the optional development dependency and run:

```bash
pip install -r requirements-dev.txt
python tools/generate_readme_previews.py
```

## Project Structure

```text
pre-sales-document-assistant/
  README.md
  requirements.txt
  .env.example
  main.py
  src/
  input/
  output/
  sample_documents/
  sample_outputs/
```

## Sample Execution

1. Place a PDF at `input/rfp.pdf`.
2. Install dependencies with `pip install -r requirements.txt`.
3. Run `python main.py input/rfp.pdf`.

The default `mock` provider generates placeholder analysis outputs without external API calls. Select `--provider openai` only when OpenAI credentials are configured.

## Notes

This tool is designed to accelerate pre-sales review. It does not replace legal, compliance, procurement, or security review.

## Author

Created by Fabricio Puliafico Artur.

- GitHub: [fabricioartur](https://github.com/fabricioartur)

## License

Copyright (c) 2026 Fabricio Puliafico Artur.

This project is released under the MIT License. See [LICENSE](LICENSE) for details.
