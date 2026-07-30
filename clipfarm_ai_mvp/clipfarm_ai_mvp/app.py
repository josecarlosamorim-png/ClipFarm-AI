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

        if resultado.metadata and "language" in resultado.metadata:
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

                    st.write(segment.get("text", ""))

        # ======================
        # Melhores Clips
        # ======================

        if resultado.best_clips:

            st.header("🏆 Melhores Clips")

            for clip in resultado.best_clips[:5]:

                score = clip.get("score", "N/A")
                start = clip.get("start", 0)
                end = clip.get("end", 0)

                with st.expander(
                    f"⭐ {score} pontos | {start:.1f}s → {end:.1f}s"
                ):

                    st.write(f"**Título:** {clip.get('title', 'Sem título')}")
                    st.write(f"**Categoria:** {clip.get('category', 'N/A')}")

                    confidence = clip.get("confidence")

                    if confidence is not None:
                        st.write(
                            f"**Confiança:** {confidence:.2f}"
                        )

                    st.write(
                        f"**Heurística:** {clip.get('heuristic_score', 'N/A')}"
                    )

                    st.write(
                        f"**LLM:** {clip.get('llm_score', 'N/A')}"
                    )

                    reason = clip.get("reason")

                    if reason:
                        st.write("")
                        st.write("### Justificação")
                        st.write(reason)

                    st.write("")
                    st.write("### Transcrição")
                    st.write(clip.get("text", ""))

        # ======================
        # Clips exportados
        # ======================

        if resultado.generated_clips:

            st.header("🎥 Clips Gerados")

            for i, clip in enumerate(resultado.generated_clips):

                path = clip.get("path")

                if path is None:
                    continue

                title = clip.get("title") or Path(path).stem
                score = clip.get("score", "N/A")
                duration = clip.get("duration")

                st.subheader(title)

                st.write(f"Score: {score}")

                if duration is not None:
                    st.write(f"Duração: {duration:.1f}s")

                st.video(str(path))

                with open(path, "rb") as f:

                    st.download_button(
                        label="📥 Download",
                        data=f,
                        file_name=Path(path).name,
                        mime="video/mp4",
                        key=f"download_{i}"
                    )