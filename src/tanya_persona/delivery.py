"""Ephemeral delivery choices and provider-independent speech adapter values."""

from typing import ClassVar, Literal, assert_never

from pydantic import BaseModel, ConfigDict

type Brevity = Literal["brief", "balanced", "expanded"]
type Kindness = Literal["neutral", "warm", "gentle"]
type Pace = Literal["slow", "steady", "brisk"]


class DeliveryPlan(BaseModel):
    """One turn's presentation choices, never persistent user attributes."""

    model_config: ClassVar[ConfigDict] = ConfigDict(frozen=True, extra="forbid")

    brevity: Brevity = "balanced"
    kindness: Kindness = "warm"
    pace: Pace = "steady"

    @property
    def sentence_budget(self) -> int:
        """Return the suggested maximum sentences; never truncate safety content."""
        match self.brevity:
            case "brief":
                return 2
            case "balanced":
                return 4
            case "expanded":
                return 8
            case _:
                assert_never(self.brevity)

    @property
    def tts_speed(self) -> float:
        """Return a conservative speech speed multiplier for a caller's adapter."""
        match self.pace:
            case "slow":
                return 0.9
            case "steady":
                return 1.0
            case "brisk":
                return 1.1
            case _:
                assert_never(self.pace)

    @property
    def tts_instructions(self) -> str:
        """Return fixed speech guidance without interpolating user content."""
        match self.kindness:
            case "neutral":
                tone = "Use a courteous, neutral tone."
            case "warm":
                tone = "Use a friendly, warm tone without exaggerated intimacy."
            case "gentle":
                tone = "Use a gentle, respectful tone without pity or diagnosis."
            case _:
                assert_never(self.kindness)
        match self.pace:
            case "slow":
                rhythm = "Speak slowly with natural pauses."
            case "steady":
                rhythm = "Speak at a steady conversational pace."
            case "brisk":
                rhythm = "Speak a little briskly while keeping words clear."
            case _:
                assert_never(self.pace)
        return f"{tone} {rhythm} Read the supplied text faithfully."
