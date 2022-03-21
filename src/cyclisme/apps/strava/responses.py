from dataclasses import dataclass


@dataclass
class AthleteResponse:
    id: str
    username: str
    weight: float
    profile_medium: str
    profile: str

    def __str__(self):
        return self.username


@dataclass()
class AuthenticationResponse:
    token_type: str
    expires_at: int
    expires_in: int
    refresh_token: str
    access_token: str
    athlete: AthleteResponse
