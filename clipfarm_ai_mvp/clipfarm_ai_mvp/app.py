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

            for segment in resultado.transcript[:10]:

                st.write(
                    f"[{segment['start']:.2f}s] {segment['text']}"
                )
