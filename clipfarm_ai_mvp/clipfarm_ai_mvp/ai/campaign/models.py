from dataclasses import dataclass, field


@dataclass
class Campaign:

    # -----------------------------
    # Informação geral
    # -----------------------------

    name: str = ""

    description: str = ""

    # -----------------------------
    # Plataformas
    # -----------------------------

    platforms: list[str] = field(default_factory=list)

    # -----------------------------
    # Branding
    # -----------------------------

    requires_logo: bool = False

    logo_first_seconds: int | None = None

    # -----------------------------
    # Conteúdo
    # -----------------------------

    preferred: list[str] = field(default_factory=list)

    forbidden: list[str] = field(default_factory=list)

    # -----------------------------
    # Keywords
    # -----------------------------

    required_keywords: list[str] = field(default_factory=list)

    forbidden_keywords: list[str] = field(default_factory=list)

    # -----------------------------
    # Duração
    # -----------------------------

    min_duration: float | None = None

    max_duration: float | None = None

    # -----------------------------
    # Idioma
    # -----------------------------

    language: str | None = None

    # -----------------------------
    # Fontes
    # -----------------------------

    source_urls: list[str] = field(default_factory=list)