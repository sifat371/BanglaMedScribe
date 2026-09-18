# BanglaMedScribe

> Working codename for a showcaseable Bangla/Banglish clinical documentation assistant.

BanglaMedScribe V1 turns a recorded or uploaded doctor–patient consultation into a timestamped transcript and, in later milestones, structured clinical facts, an editable clinical note, and claim-level transcript evidence.

## V1 product boundary

The V1 is a **clinical documentation assistant**. It is not an autonomous diagnostic or prescribing system.

Initial workflow:

```text
Audio
  ↓
ASR
  ↓
Timestamped transcript
  ↓
Speaker roles
  ↓
Structured clinical facts
  ↓
Evidence-linked clinical note
  ↓
Clinician review
```

Development is currently beginning with Sprint 1: repository foundation, audio preprocessing, pluggable ASR, transcript schema, tests, and a command-line pipeline.
