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

        st.write(resultado)
