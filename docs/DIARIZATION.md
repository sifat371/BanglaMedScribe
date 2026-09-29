# Speaker diarization

BanglaMedScribe includes a concrete optional adapter for the current open-source
`pyannote/speaker-diarization-community-1` pipeline plus a model-agnostic provider boundary.

The repository still does **not** claim a Bengali clinical diarization accuracy or DER until a
reviewed multi-speaker evaluation set is run.

## Install

```bash
python -m pip install -e ".[diarization,dev]"
```

Before first use, accept the Community-1 model conditions on Hugging Face and provide an access
token locally:

```bash
export BMS_DIARIZATION_HF_TOKEN=...
```

Do not commit access tokens.

## Run

```bash
python scripts/run_diarization.py path/to/conversation.wav
```

or, after package installation:

```bash
bms-diarize path/to/conversation.wav
```

By default the adapter requests the Community-1 **exclusive speaker diarization** output when
available. Exclusive turns are useful for reconciling one active speaker label with ASR timestamps.

## Architecture

The project deliberately separates:

```text
audio
  |-- ASR -> timestamped words/segments
  |-- diarization -> anonymous speaker turns
                         |
                         v
                temporal alignment
                         |
                         v
              speaker-attributed ASR
                         |
                         v
             role identification
             (doctor/patient/etc.)
```

Diarization labels such as `SPEAKER_00` are not automatically doctor/patient identities. A
separate role-identification step and evaluation are required.

## What is tested without model downloads

CI tests:

- provider-independent diarization data structures;
- ASR/turn overlap alignment;
- conversion of pyannote-style annotations into stable `SpeakerTurn` objects.

CI intentionally does not download Community-1 weights.

## Before making a performance claim

Run a reviewed multi-speaker benchmark and report:

- audio source and consent/data-governance status;
- number of conversations and speakers;
- recording conditions;
- diarization model/configuration;
- DER (or another clearly defined speaker metric);
- role-attribution protocol if doctor/patient roles are reported.
