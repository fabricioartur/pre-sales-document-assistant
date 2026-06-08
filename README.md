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
- Runs by default with a local mock analysis provider for Milestone 1 validation
- Keeps an optional OpenAI provider as a future extension point
- Generates structured output in JSON, Markdown, and Excel
- Handles common errors such as missing files, non-PDF input, empty PDFs, missing API keys, unavailable dependencies, API failures, and invalid JSON returned by the model

## Setup

```bash
pip install -r requirements.txt
```

Milestone 1 does not require a `.env` file or OpenAI credentials.

To test the future OpenAI provider, copy `.env.example` to `.env` and set:

```text
OPENAI_API_KEY=your_api_key_here
ANALYSIS_PROVIDER=openai
```

## Usage

```bash
python main.py input/rfp.pdf
```

Optional arguments:

```bash
python main.py input/rfp.pdf --output-dir output
python main.py input/rfp.pdf --provider openai --model gpt-4.1-mini
```

## Outputs

Each run creates:

- `output/01_executive_summary.md`
- `output/02_requirements_matrix.xlsx`
- `output/03_risk_register.xlsx`
- `output/04_clarification_questions.md`
- `output/05_go_no_go.md`
- `output/06_solution_outline.md`
- `output/07_analysis.json`

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
