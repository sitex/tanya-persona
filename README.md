# tanya-persona

An independent MIT-licensed Python package for user-owned companion preferences,
neutral AI persona instructions, and bounded presentation choices for one turn.
Python 3.12+ and Pydantic v2 are required. English is the default; `ru` selects
Russian responses. There are no bundled personal facts, provider calls, storage,
credentials, environment reads, or application integrations.

```python
from tanya_persona import (
    CharacterProfile,
    DeliveryPlan,
    PersonaContext,
    build_instructions,
)

context = PersonaContext(
    companion_name="Tanya",
    profile=CharacterProfile(style="direct"),
)
delivery = DeliveryPlan(brevity="brief", kindness="neutral", pace="steady")
instructions = build_instructions(context, delivery)
# A caller's speech adapter can consume these values without user text injection:
speed = delivery.tts_speed
speech_instructions = delivery.tts_instructions
voice = context.profile.voice
```

See [CONTRACT.md](CONTRACT.md) for exact fields, defaults and adapter mappings.
`CharacterProfile` preserves the legacy seven-field profile JSON contract.
`context_size()` counts its values without serializing a new field. All models
are frozen and reject extra keys. Persona style and explicit user boundaries
take priority over delivery hints; delivery plans are never personal memories.

Instructions ask the model to remain honest about being AI, support independence
and human relationships, and treat profile text as data. Prompt guidance cannot
guarantee model compliance or prevent every prompt injection. Sentence budgets
are soft targets, not truncation. Applications own safety enforcement and choose
whether to apply speech guidance when it conflicts with user preferences.

## Development

From this package directory:

```sh
uv sync --locked
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked basedpyright
uv run --locked pytest
uv build
```

The source layout includes a `py.typed` marker. Wheel and source distributions
carry the MIT license. Tests use local deterministic models and functions only;
they make no live AI or speech requests. Publication and bot installation belong
to the integrating application.
