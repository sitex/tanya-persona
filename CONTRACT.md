# tanya-persona public contract (0.1.0)

This standalone, provider-free package exports `CharacterProfile`, `DeliveryPlan`,
`PersonaContext`, `build_instructions`, and the type aliases `Brevity`, `Kindness`,
`Pace`, `Language`, and `Voice` from `tanya_persona`.

All models are frozen Pydantic v2 models with `extra="forbid"`. Profile parsing
retains legacy Pydantic coercion behavior (no new strict-mode restrictions).

## CharacterProfile

Fields below are in serialization order. `context_size()` is a method, not a
serialized field. There are no aliases, validators, computed fields or extra data.

| Field | Type / bound | Default |
| --- | --- | --- |
| user_name | str, max 80 | `""` |
| style | warm / calm / playful / direct | warm |
| about | str, max 2000 | `""` |
| interests | str, max 1000 | `""` |
| boundaries | str, max 1000 | `""` |
| voice | Voice | marin |
| form | Mother / Alien / Orb | Mother |

`context_size()` sums the character lengths of all seven values. `Voice` permits
alloy, ash, ballad, coral, echo, sage, shimmer, verse, marin and cedar.
`model_dump_json()` preserves legacy profile bytes, including Unicode handling.
The schema title and description change to describe CharacterProfile; the voice
type alias appears under `$defs/Voice`. Validation and JSON payloads do not change.

## DeliveryPlan (ephemeral, one turn only)

| Field | Literal choices | Default |
| --- | --- | --- |
| brevity | brief / balanced / expanded | balanced |
| kindness | neutral / warm / gentle | warm |
| pace | slow / steady / brisk | steady |

No free text or user-state labels are accepted. Read-only adapter properties:
`sentence_budget: int` maps brief/balanced/expanded to 2/4/8;
`tts_speed: float` maps slow/steady/brisk to 0.9/1.0/1.1;
`tts_instructions: str` contains only fixed delivery guidance, never user data.
These are properties, not serialized fields. Sentence budgets are instruction
targets, not an output truncator. TTS adapters must retain provider safety rules.

## PersonaContext and builder

`PersonaContext(companion_name="Tanya", language="en", profile=CharacterProfile())`
accepts a companion name of 1..80 characters, `language: Language` (`en` or `ru`),
and `profile: CharacterProfile` (not nullable).

`build_instructions(context: PersonaContext, delivery: DeliveryPlan | None = None)
-> str` is deterministic and pure. Omitted delivery uses DeliveryPlan defaults.
It returns neutral AI-companion instructions with JSON-encoded context as data.
The context name supplies the companion name. User-chosen style and explicit
boundaries outrank ephemeral delivery; user data cannot replace safety or system
instructions. No emotional diagnosis, inferred persistent labels, lore, provider
calls, storage, networking or environment access exists in the package.

Root may embed DeliveryPlan directly in a same-call structured response and use
its properties for TTS. Root owns integration, persistence decisions, provider
calls, publication and installation. DeliveryPlan should never be persisted as
personal facts. The package supplies guidance; model adherence is not guaranteed.
