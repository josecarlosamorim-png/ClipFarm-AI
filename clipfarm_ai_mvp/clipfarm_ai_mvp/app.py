from pathlib import Path

import streamlit as st

from core.orchestrator import Orchestrator
from ai.campaign.manager.manager import CampaignManager

st.set_page_config(
    page_title="ClipFinder AI V3",
    layout="wide",
)

st.title("🎬 ClipFinder AI V3")
st.write("Analisa vídeos e gera automaticamente os melhores clips.")

# ======================================================
# Pastas
# ======================================================

# CORRIGIDO:
# Antes era .parent.parent
# Agora é apenas .parent
ROOT = Path(__file__).resolve().parent

INPUT_DIR = ROOT / "input"

VIDEO_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".mkv",
    ".avi",
    ".webm",
}

campaign_manager = CampaignManager()

# ======================================================
# Vídeos
# ======================================================

videos = []

if INPUT_DIR.exists():

    videos = sorted(

        [

            f

            for f in INPUT_DIR.iterdir()

            if f.is_file()

            and f.suffix.lower() in VIDEO_EXTENSIONS

        ]

    )

if not videos:

    st.warning("Nenhum vídeo encontrado na pasta input.")

    st.stop()

selected_video = st.selectbox(

    "📂 Escolhe um vídeo",

    videos,

    format_func=lambda p: p.name,

)

st.success(

    f"Vídeo selecionado: {selected_video.name}"

)

# ======================================================
# Campanhas
# ======================================================

campaigns = campaign_manager.list()

if not campaigns:

    st.error(

        "Nenhuma campanha encontrada."

    )

    st.stop()

selected_campaign = st.selectbox(

    "🎯 Escolhe uma campanha",

    campaigns,

)

st.success(

    f"Campanha selecionada: {selected_campaign}"

)

# ======================================================
# Processamento
# ======================================================

if st.button("🚀 Analisar"):

    with st.spinner(

        "A processar vídeo..."

    ):

        campaign = campaign_manager.load(

            selected_campaign

        )

        orchestrator = Orchestrator()

        resultado = orchestrator.process_video(

            str(selected_video),

            campaign,

        )

    st.success(

        "✅ Pipeline concluída!"

    )

    # ======================================================
    # Metadados
    # ======================================================

    st.header("📹 Informações do vídeo")

    c1, c2, c3 = st.columns(3)

    c1.metric(

        "Duração",

        f"{resultado.duration:.2f}s",

    )

    c2.metric(

        "FPS",

        resultado.fps,

    )

    c3.metric(

        "Resolução",

        f"{resultado.width}×{resultado.height}",

    )

    st.write(

        f"Frames: {resultado.total_frames}"

    )

    st.write(

        f"Cenas: {len(resultado.scenes)}"

    )

    if (

        resultado.metadata

        and "language" in resultado.metadata

    ):

        st.write(

            f"Idioma: {resultado.metadata['language']}"

        )

    # ======================================================
    # Transcrição
    # ======================================================

    if resultado.transcript:

        st.header("📝 Transcrição")

        for sentence in resultado.transcript[:10]:

            st.write(

                f"[{sentence['start']:.2f}s] {sentence['text']}"

            )

    # ======================================================
    # Segmentos
    # ======================================================

    if resultado.segments:

        st.header("📚 Segmentos")

        for i, segment in enumerate(

            resultado.segments,

            start=1,

        ):

            with st.expander(

                f"Segmento {i} ({segment['start']:.2f}s → {segment['end']:.2f}s)"

            ):

                st.write(

                    segment.get(

                        "text",

                        "",

                    )

                )

    # ======================================================
    # Melhores Clips
    # ======================================================

    if resultado.best_clips:

        st.header("🏆 Melhores Clips")

        for clip in resultado.best_clips[:5]:

            with st.expander(

                f"⭐ {clip.score} pontos | {clip.start:.1f}s → {clip.end:.1f}s"

            ):
                st.write(

                    f"**Título:** {clip.title or 'Sem título'}"

                )

                st.write(

                    f"**Categoria:** {clip.category or 'N/A'}"

                )

                st.write(

                    f"**Subcategoria:** {clip.subcategory or 'N/A'}"

                )

                st.write(

                    f"**Emoção:** {clip.emotion or 'N/A'}"

                )

                st.write(

                    f"**Público-Alvo:** {clip.target_audience or 'N/A'}"

                )

                st.write(

                    f"**Confiança:** {clip.confidence:.2f}"

                )

                st.write(

                    f"**Score Final:** {clip.score}"

                )

                st.write(

                    f"**Score Heurístico:** {clip.heuristic_score}"

                )

                st.write(

                    f"**Score Hook:** {clip.hook_score}"

                )

                st.write(

                    f"**Score LLM:** {clip.llm_score}"

                )

                st.write(

                    f"**Retenção:** {clip.retention_score}"

                )

                st.write(

                    f"**Viralidade:** {clip.virality_score}"

                )

                if clip.keywords:

                    st.write(

                        "**Keywords:**"

                    )

                    st.write(

                        ", ".join(

                            clip.keywords

                        )

                    )

                if clip.reason:

                    st.write(

                        "### Justificação da IA"

                    )

                    st.write(

                        clip.reason

                    )

                campaign = clip.campaign

                st.write(

                    "### Validação da Campanha"

                )

                st.write(

                    f"Score: {campaign.score}"

                )

                st.write(

                    f"Passed: {campaign.passed}"

                )

                if campaign.passed_checks:

                    st.success(

                        "\n".join(

                            campaign.passed_checks

                        )

                    )

                if campaign.warnings:

                    st.warning(

                        "\n".join(

                            campaign.warnings

                        )

                    )

                if campaign.errors:

                    st.error(

                        "\n".join(

                            campaign.errors

                        )

                    )

                st.write(

                    "### Transcrição"

                )

                st.write(

                    clip.transcript

                )

    # ======================================================
    # Clips Gerados
    # ======================================================

    if resultado.generated_clips:

        st.header("🎥 Clips Gerados")

        for i, clip in enumerate(resultado.generated_clips):
            path = clip.get("path")

            if path is None:
                continue

            title = clip.get(
                "title",
                Path(path).stem,
            )

            score = clip.get(
                "score",
                "N/A",
            )

            duration = clip.get(
                "duration",
            )

            st.subheader(title)

            c1, c2 = st.columns(2)

            c1.metric(
                "Score",
                score,
            )

            if duration is not None:

                c2.metric(
                    "Duração",
                    f"{duration:.1f}s",
                )

            st.video(str(path))

            with open(path, "rb") as f:

                st.download_button(

                    label="📥 Download",

                    data=f,

                    file_name=Path(path).name,

                    mime="video/mp4",

                    key=f"download_{i}",

                )

    # ======================================================
    # Resumo do processamento
    # ======================================================

    with st.expander("📊 Resumo do Processamento"):

        st.write(
            f"Tempo total: {resultado.elapsed_time:.2f}s"
        )

        st.write(
            f"Estado: {resultado.status}"
        )

        st.write(
            f"Etapa atual: {resultado.current_stage}"
        )

        st.write(
            f"Progresso: {resultado.progress}%"
        )

        st.write(
            f"Segmentos encontrados: {len(resultado.segments)}"
        )

        st.write(
            f"Melhores clips: {len(resultado.best_clips)}"
        )

        st.write(
            f"Clips gerados: {len(resultado.generated_clips)}"
        )

        st.write(
            f"Campanha: {selected_campaign}"
        )

        st.write(
            f"Vídeo: {selected_video.name}"
        )

        if resultado.logs:

            st.subheader("Logs")

            for log in resultado.logs:

                st.text(log)
        if resultado.errors:

            st.subheader("Erros")

            for erro in resultado.errors:

                st.error(erro)

        else:

            st.success(
                "Nenhum erro encontrado durante o processamento."
            )

        # ======================================================
        # Logs completos
        # ======================================================

        if resultado.logs:

            with st.expander("📜 Logs completos"):

                for log in resultado.logs:

                    st.text(log)

    # ======================================================
    # Rodapé
    # ======================================================

    st.divider()

    st.caption(
        "ClipFinder AI V3 • Pipeline concluída com sucesso."
    )