"""User-provided profile contract with stable legacy JSON serialization."""

from typing import Annotated, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

type Voice = Literal[
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
]


class CharacterProfile(BaseModel):
    """Editable preferences; values describe user choices, not inferred traits."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    user_name: Annotated[str, Field(max_length=80)] = ""
    style: Literal["warm", "calm", "playful", "direct"] = "warm"
    about: Annotated[str, Field(max_length=2_000)] = ""
    interests: Annotated[str, Field(max_length=1_000)] = ""
    boundaries: Annotated[str, Field(max_length=1_000)] = ""
    voice: Voice = "marin"
    form: Literal["Mother", "Alien", "Orb"] = "Mother"

    def context_size(self) -> int:
        """Count all seven profile values in a caller's shared context budget."""
        return sum(
            map(
                len,
                (
                    self.user_name,
                    self.style,
                    self.about,
                    self.interests,
                    self.boundaries,
                    self.voice,
                    self.form,
                ),
            )
        )
