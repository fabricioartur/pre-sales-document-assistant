# Security Policy

## Supported Versions

This project is currently in its initial public release.

| Version | Supported |
| ------- | --------- |
| v0.1.x  | Yes       |

## Reporting a Vulnerability

If you find a security issue, please do not open a public GitHub issue with sensitive details.

Report it privately to the project maintainer:

- GitHub: [fabricioartur](https://github.com/fabricioartur)

Please include:

- A clear description of the issue
- Steps to reproduce it
- Potential impact
- Any relevant logs or screenshots, with secrets and customer data removed

## Sensitive Data Guidelines

This project is designed to analyze procurement documents such as RFPs, RFIs, and public bids. These files may contain confidential customer, vendor, legal, commercial, or security information.

Before using this tool:

- Do not commit real procurement documents to the repository.
- Do not commit generated outputs that contain customer-sensitive content.
- Do not include API keys, passwords, tokens, or credentials in issues, pull requests, screenshots, or logs.
- Use `.env` for local secrets. The `.env` file is intentionally ignored by Git.
- Review generated outputs before sharing them publicly.

## API Key Handling

Milestone 1 runs with `MockAnalysisProvider` by default and does not require OpenAI credentials.

If you enable a future API-backed provider:

- Store API keys only in `.env` or a secure secret manager.
- Never hardcode API keys in source code.
- Rotate any key that may have been exposed.

## Dependency Security

Install dependencies from trusted package indexes and keep them updated.

For local development:

```bash
pip install -r requirements.txt
```

Optional README preview tooling uses:

```bash
pip install -r requirements-dev.txt
```

## Scope

This policy covers the source code and project documentation in this repository. It does not cover third-party services, APIs, models, or external documents processed by users.
