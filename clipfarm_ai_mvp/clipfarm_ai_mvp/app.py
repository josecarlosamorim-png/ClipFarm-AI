from pathlib import Path
import tempfile

import streamlit as st

from core.orchestrator import Orchestrator

st.set_page_config(page_title="ClipFinder AI V3")

st.title("ClipFinder AI V3")

st.write("Projeto inicial carregado.")

video = st.file_uploader(
    "Importar vídeo",
    type=["mp4", "mov", "mkv"]
)

if video:

    st.success(video.name)

    if st.button("Analisar"):

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=Path(video.name).suffix
        ) as tmp:

            tmp.write(video.read())
            video_path = tmp.name

        orchestrator = Orchestrator()

        resultado = orchestrator.process_video(video_path)

        st.success("Pipeline executada!")

        st.subheader("Informações do vídeo")

        st.write(f"**Duração:** {resultado.duration:.2f} s")
        st.write(f"**FPS:** {resultado.fps}")
        st.write(f"**Resolução:** {resultado.width} × {resultado.height}")
        st.write(f"**Frames:** {resultado.total_frames}")
        st.write(f"**Cenas detetadas:** {len(resultado.scenes)}")

        if "language" in resultado.metadata:
            st.write(f"**Idioma:** {resultado.metadata['language']}")

        if resultado.transcript:

            st.subheader("Primeiras frases")

            for sentence in resultado.transcript[:10]:

                st.write(
                    f"[{sentence['start']:.2f}s] {sentence['text']}"
                )

        if resultado.segments:

            st.subheader("Segmentos")

            for i, segment in enumerate(resultado.segments, start=1):

                with st.expander(
                    f"Segmento {i} ({segment['start']:.2f}s → {segment['end']:.2f}s)"
                ):

                    st.write(segment["text"])

                if resultado.best_clips:

            st.subheader("🏆 Melhores Clips")

            for clip in resultado.best_clips[:5]:

                with st.expander(
                    f"⭐ {clip['score']} pontos | "
                    f"{clip['start']:.1f}s → {clip['end']:.1f}s"
                ):

                    st.write(f"**Título sugerido:** {clip['title']}")
                    st.write(f"**Categoria:** {clip['category']}")
                    st.write(
                        f"**Confiança:** {clip['confidence']:.2f}"
                        if clip["confidence"] is not None
                        else "**Confiança:** N/A"
                    )

                    st.write(
                        f"**Pontuação Total:** {clip['score']}"
                    )

                    st.write(
                        f"• Heurística: {clip['heuristic_score']}"
                    )

                    st.write(
                        f"• IA: {clip['llm_score']}"
                    )

                    st.write("")

                    st.write("### Motivos")

                    for reason in clip["reasons"]:

                        st.write(f"• {reason}")

                    if clip["reason"]:

                        st.write("")
                        st.write("### Justificação da IA")

                        st.write(clip["reason"])

                    st.write("")

                    st.write("### Transcrição")

                    st.write(clip["text"])
