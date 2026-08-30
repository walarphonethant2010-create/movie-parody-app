import streamlit as st
import moviepy.editor as mp
from moviepy.video.fx.all import mirror_x, colorx
from gtts import gTTS
import tempfile
import os

st.set_page_config(page_title="Myat Mahar Video Lab v6.1", layout="wide", page_icon="🎬")

st.title("🎬 Myat Mahar Video Lab (MMVL v6.1 Master Engine)")
st.caption("World's #1 Automation Engine: Reaction, Parody, Recap, Meme Inserts, Anti-Copyright Shield & SEO Matrix")

# STEP 1: MEDIA UPLOADS
st.sidebar.header("📁 Step 1: Media Assets Upload")
video_file = st.sidebar.file_uploader("1. Upload Main Video Clip (MP4/MOV)", type=["mp4", "mov"])
insert_clip_files = st.sidebar.file_uploader("2. Upload Meme/Funny Inserts (Optional)", type=["mp4", "mov"], accept_multiple_files=True)
bgm_file = st.sidebar.file_uploader("3. Upload Background Music BGM (Optional)", type=["mp3", "wav"])
avatar_file = st.sidebar.file_uploader("4. Upload AI Avatar Photo (For Reaction Style)", type=["png", "jpg", "jpeg"])
logo_file = st.sidebar.file_uploader("5. Upload Brand Logo (PNG)", type=["png"])

# STEP 2: CONTENT STYLE & NARRATION STRATEGY
st.sidebar.header("🎙️ Step 2: Content Style & Voice Strategy")
narration_style = st.sidebar.selectbox(
    "Select Content Style:", 
    ["Movie Reaction (AI Avatar)", "Funny Parody", "Movie Recap", "Cinematic Documentary"]
)

audio_option = st.sidebar.radio("Audio Source Strategy:", ["Auto AI Voice Generator", "Upload Custom Audio", "Keep Original Audio"])

ai_script = ""
selected_lang = "my"

if audio_option == "Auto AI Voice Generator":
    doc_lang = st.sidebar.selectbox("Script Language:", ["Myanmar (မြန်မာ)", "English"])
    selected_lang = 'my' if doc_lang == "Myanmar (မြန်မာ)" else 'en'
    voice_gender = st.sidebar.selectbox("Narrator Voice Tone:", ["Male Tone (အမျိုးသား)", "Female Tone (အမျိုးသမီး)"])
    
    st.sidebar.caption("💡 Quick AI Script Generator Helper")
    movie_title_input = st.sidebar.text_input("Movie Title for Script Preset:", "Inception")
    
    if st.sidebar.button("Generate Auto Script Preset"):
        if "Movie Reaction" in narration_style:
            ai_script = f"ဝါး... ဒီ {movie_title_input} ဇာတ်ကားရဲ့ အခန်းကတော့ တကယ်ကို မိုက်လွန်းတယ်ဗျာ။ မင်းသားရဲ့ ရိုက်ချက်တွေက တကယ် ကြက်သန်းထစရာပဲ။"
        elif "Funny" in narration_style:
            ai_script = f"ဒီနေ့မှာတော့ {movie_title_input} ဇာတ်လမ်းရဲ့ ဟာသ ဖြစ်ရပ်ဆန်းလေးတွေကို ရယ်မောဖွယ် တင်ဆက်ပေးသွားပါမယ်။"
        elif "Movie Recap" in narration_style:
            ai_script = f"ဒီနေ့မှာတော့ စိတ်လှုပ်ရှားဖွယ်ရာ {movie_title_input} ရုပ်ရှင်ဇာတ်လမ်းအကျဉ်းကို အစမှ အဆုံး တင်ဆက်ပေးသွားပါမည်။"
        else:
            ai_script = f"ယခု တင်ဆက်ပေးမှာကတော့ {movie_title_input} ရုပ်ရှင်၏ သမိုင်းဝင် လေးနက်သော ရိုက်ချက်များအကြောင်းပဲ ဖြစ်ပါတယ်။"
    else:
        default_text = "ဝါး... ဒီအခန်းကတော့ တကယ်ကို မိုက်လွန်းတယ်ဗျာ။" if "Movie Reaction" in narration_style else "ဒီနေ့မှာတော့ စိတ်လှုပ်ရှားဖွယ် ဇာတ်လမ်းအကျဉ်းကို တင်ဆက်ပေးပါမယ်။"
        ai_script = st.sidebar.text_area("Enter Narration Script:", default_text)

elif audio_option == "Upload Custom Audio":
    custom_audio_file = st.sidebar.file_uploader("Upload Voice Audio (MP3/WAV)", type=["mp3", "wav"])

# STEP 3: ADVANCED ANTI-COPYRIGHT SHIELD
st.sidebar.header("🛡️ Step 3: Anti-Copyright Shield Matrix")
enable_flip = st.sidebar.checkbox("Apply Horizontal Flip", value=True)
enable_zoom = st.sidebar.checkbox("Apply 105% Subtle Zoom", value=True)
color_intensity = st.sidebar.slider("Color Grade Filter", 0.8, 1.2, 1.05)
speed_factor = st.sidebar.slider("Playback Speed Modulation", 1.00, 1.20, 1.05)

# STEP 4: CANVAS & ASPECT RATIO
st.sidebar.header("📐 Step 4: Canvas & Layout Strategy")
aspect_ratio = st.sidebar.selectbox("Select Output Ratio:", ["9:16 (Shorts / Reels / TikTok)", "1:1 (Square Feed)"])
bg_blur_radius = st.sidebar.slider("Background Blur Intensity", 1, 31, 15, step=2)

# STEP 5: SUBTITLES & ON-SCREEN TITLES
st.sidebar.header("✍️ Step 5: Subtitle & On-Screen Title")
enable_subtitles = st.sidebar.checkbox("Add On-Screen Subtitles / Title", value=True)
sub_text = ""
if enable_subtitles:
    sub_text = st.sidebar.text_input("Title Overlay:", "MYAT MAHAR EXCLUSIVE")
    text_color = st.sidebar.color_picker("Text Color", "#FFFF00")

# MAIN PROCESSING ENGINE
if video_file:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(video_file.read())
    st.subheader("📺 Source Video Input Preview")
    st.video(tfile.name)
    
    if st.button("🚀 Render Master Empire Video Asset"):
        with st.spinner("Rendering Video with Anti-Copyright Shield & AI Stack..."):
            main_clip = mp.VideoFileClip(tfile.name)
            
            if enable_flip:
                main_clip = mirror_x(main_clip)
            if enable_zoom:
                main_clip = main_clip.crop(x1=int(main_clip.w * 0.025), y1=int(main_clip.h * 0.025),
                                          x2=int(main_clip.w * 0.975), y2=int(main_clip.h * 0.975))
            main_clip = colorx(main_clip, color_intensity)
            
            target_w, target_h = (1080, 1920) if aspect_ratio.startswith("9:16") else (1080, 1080)

            if insert_clip_files:
                final_video_sequence = []
                segment_duration = main_clip.duration / (len(insert_clip_files) + 1)
                
                for i, ins_file in enumerate(insert_clip_files):
                    seg = main_clip.subclip(i * segment_duration, (i + 1) * segment_duration)
                    final_video_sequence.append(seg)
                    
                    ins_temp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
                    ins_temp.write(ins_file.read())
                    ins_clip = mp.VideoFileClip(ins_temp.name).resize(width=main_clip.w)
                    final_video_sequence.append(ins_clip)
                
                final_video_sequence.append(main_clip.subclip(len(insert_clip_files) * segment_duration, main_clip.duration))
                raw_clip = mp.concatenate_videoclips(final_video_sequence, method="compose")
            else:
                raw_clip = main_clip

            bg_clip = raw_clip.resize(height=target_h) if (raw_clip.w / raw_clip.h) < (target_w / target_h) else raw_clip.resize(width=target_w)
            bg_clip = bg_clip.crop(x_center=bg_clip.w/2, y_center=bg_clip.h/2, width=target_w, height=target_h)
            bg_clip = bg_clip.fl_image(lambda image: mp.vfx.gaussian_blur(image, bg_blur_radius))
            
            fg_clip = raw_clip.resize(width=target_w) if (raw_clip.w / raw_clip.h) > (target_w / target_h) else raw_clip.resize(height=target_h)
            
            video_layers = [bg_clip, fg_clip.set_position("center")]
            
            if "Movie Reaction" in narration_style and avatar_file:
                av_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
                av_file.write(avatar_file.read())
                avatar_clip = mp.ImageClip(av_file.name).set_duration(raw_clip.duration)
                avatar_clip = avatar_clip.resize(width=int(target_w * 0.35))
                avatar_clip = avatar_clip.set_position((target_w - avatar_clip.w - 30, target_h - avatar_clip.h - 50))
                video_layers.append(avatar_clip)
                
            if enable_subtitles and sub_text:
                txt_clip = mp.TextClip(sub_text, fontsize=45, color=text_color, font='Arial-Bold', method='caption', size=(target_w - 100, None))
                txt_clip = txt_clip.set_position(('center', int(target_h * 0.15))).set_duration(raw_clip.duration)
                video_layers.append(txt_clip)

            final_video = mp.CompositeVideoClip(video_layers, size=(target_w, target_h))
            
            voice_audio = None
            if audio_option == "Auto AI Voice Generator" and ai_script:
                tts = gTTS(text=ai_script, lang=selected_lang, slow=False)
                tts_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
                tts.save(tts_path)
                voice_audio = mp.AudioFileClip(tts_path)
            elif audio_option == "Upload Custom Audio" and 'custom_audio_file' in locals() and custom_audio_file:
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
