from pathlib import Path
import tempfile

import streamlit as st

from core.orchestrator import Orchestrator

st.set_page_config(
    page_title="ClipFinder AI V3",
    layout="wide"
)

st.title("🎬 ClipFinder AI V3")

st.write("Analisa vídeos e gera automaticamente os melhores clips.")

video = st.file_uploader(
    "Importar vídeo",
    type=["mp4", "mov", "mkv"]
)

if video:

    st.success(video.name)

    if st.button("🚀 Analisar"):

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=Path(video.name).suffix
        ) as tmp:

            tmp.write(video.read())
            video_path = tmp.name

        with st.spinner("A processar vídeo..."):

            orchestrator = Orchestrator()

            resultado = orchestrator.process_video(video_path)

        st.success("✅ Pipeline concluída!")

        # ======================
        # Metadados
        # ======================

        st.header("📹 Informações do vídeo")

        c1, c2, c3 = st.columns(3)

        c1.metric("Duração", f"{resultado.duration:.2f}s")
        c2.metric("FPS", resultado.fps)
        c3.metric(
            "Resolução",
            f"{resultado.width}×{resultado.height}"
        )

        st.write(f"Frames: {resultado.total_frames}")
        st.write(f"Cenas: {len(resultado.scenes)}")

        if "language" in resultado.metadata:
            st.write(f"Idioma: {resultado.metadata['language']}")

        # ======================
        # Transcrição
        # ======================

        if resultado.transcript:

            st.header("📝 Transcrição")

            for sentence in resultado.transcript[:10]:

                st.write(
                    f"[{sentence['start']:.2f}s] {sentence['text']}"
                )

        # ======================
        # Segmentos
        # ======================

        if resultado.segments:

            st.header("📚 Segmentos")

            for i, segment in enumerate(resultado.segments, start=1):

                with st.expander(
                    f"Segmento {i} ({segment['start']:.2f}s → {segment['end']:.2f}s)"
                ):

                    st.write(segment["text"])

        # ======================
        # Melhores clips
        # ======================

        if resultado.best_clips:

            st.header("🏆 Melhores Clips")

            for clip in resultado.best_clips[:5]:

                with st.expander(
                    f"⭐ {clip['score']} pontos | "
                    f"{clip['start']:.1f}s → {clip['end']:.1f}s"
                ):

                    st.write(f"**Título:** {clip['title']}")
                    st.write(f"**Categoria:** {clip['category']}")

                    if clip["confidence"] is not None:
                        st.write(
                            f"**Confiança:** {clip['confidence']:.2f}"
                        )

                    st.write(
                        f"**Heurística:** {clip['heuristic_score']}"
                    )

                    st.write(
                        f"**LLM:** {clip['llm_score']}"
                    )

                    if clip["reason"]:
                        st.write("")
                        st.write("### Justificação")
                        st.write(clip["reason"])

                    st.write("")
                    st.write("### Transcrição")
                    st.write(clip["text"])

        # ======================
        # Clips exportados
        # ======================

        if resultado.generated_clips:

            st.header("🎥 Clips Gerados")

            for clip in resultado.generated_clips:

                st.subheader(
                    clip["title"] if clip["title"] else clip["path"].stem
                )

                st.write(f"Score: {clip['score']}")
                st.write(f"Duração: {clip['duration']:.1f}s")

                st.video(str(clip["path"]))

                with open(clip["path"], "rb") as f:

                    st.download_button(
                        "📥 Download",
                        f,
                        file_name=clip["path"].name,
                        mime="video/mp4"
                    )
