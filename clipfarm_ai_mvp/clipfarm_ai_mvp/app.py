        # ======================
        # Clips exportados
        # ======================

        if resultado.generated_clips:

            st.header("🎥 Clips Gerados")

            for clip in resultado.generated_clips:

                title = clip.get("title") or clip["path"].stem
                score = clip.get("score", "N/A")
                duration = clip.get("duration")

                st.subheader(title)

                st.write(f"Score: {score}")

                if duration is not None:
                    st.write(f"Duração: {duration:.1f}s")

                st.video(str(clip["path"]))

                with open(clip["path"], "rb") as f:

                    st.download_button(
                        "📥 Download",
                        data=f,
                        file_name=clip["path"].name,
                        mime="video/mp4",
                        key=f"download_{clip['path'].name}"
                    )