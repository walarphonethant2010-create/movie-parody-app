voice_audio = None
            if audio_option == "Auto AI Voice Generator" and ai_script:
                tts = gTTS(text=ai_script, lang=selected_lang, slow=False)
                tts_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
                tts.save(tts_path)
                voice_audio = mp.AudioFileClip(tts_path)
            elif audio_option == "Upload Custom Audio" and custom_audio_file:
                ca_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                ca_file.write(custom_audio_file.read())
                voice_audio = mp.AudioFileClip(ca_file.name)

            if bgm_file:
                bgm_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                bgm_path.write(bgm_file.read())
                bgm_audio = mp.AudioFileClip(bgm_path.name).volumex(0.18)
                
                if voice_audio:
                    final_audio = mp.CompositeAudioClip([voice_audio, bgm_audio.set_duration(final_video.duration)])
                else:
                    final_audio = mp.CompositeAudioClip([raw_clip.audio.volumex(0.8), bgm_audio.set_duration(final_video.duration)])
            else:
                final_audio = voice_audio if voice_audio else raw_clip.audio

            if final_audio:
                final_video = final_video.set_audio(final_audio)

            final_video = final_video.speedx(speed_factor)
            output_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
            final_video.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=24)
            
            st.success("🎉 Render Complete! Master Video Asset Ready.")
            st.video(output_path)
            
            with open(output_path, "rb") as file:
                st.download_button("📥 Download Final Video", file, file_name="MMVL_Master_v6.mp4")
                
            st.subheader("🔥 Auto SEO Title & Hashtags Matrix")
            st.code(f"""
[VIRAL TITLE]: {sub_text} - Best Scenes Breakdown! 😱 #Shorts
[SEO DESCRIPTION]: Watch this scene reaction & story recap! Subscribe for daily content.
[HASHTAGS]: #MovieRecap #MovieReaction #Shorts #Reels #TikTokViral
            """, language="markdown")
else:
    st.info("👈 Upload media files in the sidebar to start execution.")
