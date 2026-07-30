from core.orchestrator import Orchestrator
import streamlit as st
st.set_page_config(page_title='ClipFinder AI V3')
st.title('ClipFinder AI V3')
st.write('Projeto inicial carregado.')
video=st.file_uploader('Importar vídeo',type=['mp4','mov','mkv'])
if video:
    st.success(video.name)
    if st.button("Analisar"):

        orchestrator = Orchestrator()

        resultado = orchestrator.process_video(video_path)

        st.success("Pipeline executada!")

        st.json(resultado)
