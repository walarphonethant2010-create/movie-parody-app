import os
import cv2
import numpy as np
import streamlit as st
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip

st.set_page_config(page_title="Movie Parody Engine", layout="wide")
st.title(" Parody Video Processing & Anti-Copyright Engine")

# 1. FILE UPLOADERS
st.sidebar.header(" Media Uploads")
video_file = st.sidebar.file_uploader("1. Upload Movie Clip (MP4)", type=["mp4", "mov"])
audio_file = st.sidebar.file_uploader("2. Upload Myanmar Voiceover (MP3/WAV)", type=["mp3", "wav"])
logo_file = st.sidebar.file_uploader("3. Upload Brand Logo (PNG)", type=["png"])

# 2. EDITING CONTROLS
st.sidebar.header(" Editing Controls")
blur_y_pct = st.sidebar.slider("Subtitle Blur Y-Start (%)", 60, 95, 80)
blur_h_pct = st.sidebar.slider("Blur Height (%)", 5, 25, 12)
logo_pos = st.sidebar.selectbox("Logo Position", ["Top-Right", "Top-Left", "Bottom-Right", "Bottom-Left"])
logo_size_pct = st.sidebar.slider("Logo Size (%)", 5, 25, 10)

def process_video(v_path, a_path, l_path):
    cap = cv2.VideoCapture(v_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    y1 = int(height * (blur_y_pct / 100.0))
    y2 = int(y1 + (height * (blur_h_pct / 100.0)))

    blurred_temp = "temp_blur.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(blurred_temp, fourcc, fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        sub_roi = frame[y1:y2, 0:width]
        frame[y1:y2, 0:width] = cv2.GaussianBlur(sub_roi, (51, 51), 30)
        out.write(frame)

    cap.release()
    out.release()

    clip = VideoFileClip(blurred_temp)
    w, h = clip.size
    clip = clip.crop(x1=w*0.02, y1=h*0.02, x2=w*0.98, y2=h*0.98).resize((w, h))
    clip = clip.fx(VideoFileClip.speedx, 1.03)

    elements = [clip]

    if l_path:
        logo_w = int(w * (logo_size_pct / 100.0))
        logo = ImageClip(l_path).resize(width=logo_w).set_duration(clip.duration)
        pos_mapping = {
            "Top-Right": ("right", "top"),
            "Top-Left": ("left", "top"),
            "Bottom-Right": ("right", "bottom"),
            "Bottom-Left": ("left", "bottom")
        }
        logo = logo.set_position(pos_mapping[logo_pos])
        elements.append(logo)

    final_clip = CompositeVideoClip(elements)

    if a_path:
        new_audio = AudioFileClip(a_path)
        if new_audio.duration > final_clip.duration:
            new_audio = new_audio.subclip(0, final_clip.duration)
        final_clip = final_clip.set_audio(new_audio)
    else:
        final_clip = final_clip.without_audio()

    final_output = "final_output.mp4"
    final_clip.write_videofile(final_output, codec="libx264", audio_codec="aac")

    if os.path.exists(blurred_temp):
        os.remove(blurred_temp)

    return final_output

if video_file:
    with open("input.mp4", "wb") as f:
        f.write(video_file.getbuffer())
    if audio_file:
        with open("input.mp3", "wb") as f:
            f.write(audio_file.getbuffer())
    if logo_file:
        with open("logo.png", "wb") as f:
            f.write(logo_file.getbuffer())

    if st.button(" Render Parody Video"):
        with st.spinner("Processing Video, Blur & Audio Dubbing..."):
            a_in = "input.mp3" if audio_file else None
            l_in = "logo.png" if logo_file else None
            out_file = process_video("input.mp4", a_in, l_in)
            
            st.success("Processing Complete!")
            st.video(out_file)
            
            with open(out_file, "rb") as file:
                st.download_button(
                    label=" Download Copyright-Safe Video",
                    data=file,
                    file_name="parody_final.mp4",
                    mime="video/mp4"
                )
