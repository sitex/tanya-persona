from pathlib import Path

import pytest
from pydantic import ValidationError

from tanya_persona import CharacterProfile


@pytest.mark.parametrize(
    ("raw", "expected", "size"),
    [
        (
            "{}",
            "default.json",
            15,
        ),
        (
            """{"form":"Orb","voice":"cedar","boundaries":"No advice",
"interests":"Music","about":"Hello\\nworld",
"style":"direct","user_name":"Гость"}""",
            "custom.json",
            44,
        ),
    ],
)
def test_legacy_json_bytes_and_context_budget(
    raw: str,
    expected: str,
    size: int,
) -> None:
    profile = CharacterProfile.model_validate_json(raw)

    fixture = Path(__file__).parent / "fixtures" / expected
    assert profile.model_dump_json().encode() == fixture.read_bytes().rstrip(b"\n")
    assert profile.context_size() == size


@pytest.mark.parametrize(
    ("field", "limit"),
    [("user_name", 80), ("about", 2000), ("interests", 1000), ("boundaries", 1000)],
)
def test_text_fields_accept_exact_legacy_limit(field: str, limit: int) -> None:
    profile = CharacterProfile.model_validate({field: "x" * limit})

    assert getattr(profile, field) == "x" * limit


@pytest.mark.parametrize(
    ("field", "limit"),
    [("user_name", 80), ("about", 2000), ("interests", 1000), ("boundaries", 1000)],
)
def test_text_fields_reject_over_legacy_limit(field: str, limit: int) -> None:
    with pytest.raises(ValidationError, match="string_too_long"):
        _ = CharacterProfile.model_validate({field: "x" * (limit + 1)})


@pytest.mark.parametrize(
    "raw",
    [
        '{"voice":"unknown"}',
        '{"style":"intimate"}',
        '{"form":"Human"}',
        '{"user_name":null}',
        '{"about":1}',
        '{"context_size":1}',
        '{"diagnosis":"anxious"}',
    ],
)
def test_profile_rejects_invalid_legacy_inputs(raw: str) -> None:
    with pytest.raises(ValidationError):
        _ = CharacterProfile.model_validate_json(raw)


@pytest.mark.parametrize("style", ["warm", "calm", "playful", "direct"])
def test_legacy_styles_are_accepted(style: str) -> None:
    profile = CharacterProfile.model_validate({"style": style})

    assert profile.style == style


@pytest.mark.parametrize("form", ["Mother", "Alien", "Orb"])
def test_legacy_forms_are_accepted(form: str) -> None:
    profile = CharacterProfile.model_validate({"form": form})

    assert profile.form == form


@pytest.mark.parametrize(
    "voice",
    [
        "alloy",
        "ash",
        "ballad",
        "coral",
        "echo",
        "sage",
        "shimmer",
        "verse",
        "marin",
        "cedar",
    ],
)
def test_existing_voice_allowlist_is_accepted(voice: str) -> None:
    profile = CharacterProfile.model_validate({"voice": voice})

    assert profile.voice == voice


def test_profile_retains_legacy_utf8_bytes_coercion() -> None:
    profile = CharacterProfile.model_validate({"user_name": b"Guest"})

    assert profile.user_name == "Guest"
