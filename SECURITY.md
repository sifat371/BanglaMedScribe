# Security and privacy

BanglaMedScribe is pre-release research software and is not approved for uncontrolled clinical use.

## Sensitive audio

Do not place patient audio, transcripts, credentials, access tokens, or identifiable clinical data
in issues, pull requests, repository fixtures, committed benchmark files, or public logs.

Use synthetic, scripted, public, de-identified, or appropriately consented data during development.

## Credentials

Keep Hugging Face and other service credentials in local environment variables. Never commit real
tokens to `.env`, fixtures, logs, or documentation.

## Reporting a security issue

Do not open a public issue containing sensitive details. Contact the repository owner privately with
a minimal reproduction and avoid including real patient data.

## Deployment boundary

Authentication, authorization, encrypted storage, retention policy, audit logging, consent
management, and institutional governance are outside the current public prototype and must be
addressed before any real-patient deployment.
