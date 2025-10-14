# Session Logs

This directory contains JSON logs of all user interactions with the AutoMind expert system.

## Log Format

Each session is saved as `session_YYYYMMDD_HHMMSS.json` with the following structure:

```json
{
  "session_id": "20251014_153045",
  "interactions": [
    {
      "timestamp": "2025-10-14T15:30:50.123456",
      "question": "Preferred fuel or powertrain?",
      "answer": "Electric",
      "value": "electric"
    },
    ...
  ]
}
```

## Usage

These logs are useful for:
- Debugging logical inconsistencies in question flow
- Analyzing user interaction patterns
- Identifying which questions lead to successful guesses
- Validating constraint rules (e.g., electric cars shouldn't be asked about engine displacement)
- Improving the expert system's reasoning

## Privacy

Logs only contain question-answer pairs, no personal information is collected.
