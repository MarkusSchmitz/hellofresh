import streamlit as st
import streamlit.components.v1 as components
import base64

def get_emoji_rain_html():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            .container {{
                height: 500px;
                width: 100%;
                position: relative;
                background: linear-gradient(135deg, #FF9A8B 0%, #FF6B6B 100%);
                overflow: hidden;
                border-radius: 10px;
            }}

            #startButton {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                padding: 15px 30px;
                font-size: 20px;
                cursor: pointer;
                background: white;
                border: none;
                border-radius: 25px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                z-index: 100;
            }}

            .falling-emoji {{
                position: absolute;
                font-size: 2.5rem;
                pointer-events: none;
                animation: fall linear forwards;
                z-index: 1;
            }}

            @keyframes fall {{
                from {{ transform: translateY(-20px) rotate(0deg); }}
                to {{ transform: translateY(500px) rotate(360deg); }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <button id="startButton">
                Start Food Rain! 🍔
            </button>
        </div>

        <script>
            const foodEmojis = ['🍕', '🍔', '🍟', '🌭', '🍿', '🧂', '🥨', '🥯', '🥖', '🥐'];
            let isActive = false;
            let interval;

            function spawnEmoji() {{
                const container = document.querySelector('.container');
                const emoji = document.createElement('div');
                emoji.className = 'falling-emoji';
                emoji.textContent = foodEmojis[Math.floor(Math.random() * foodEmojis.length)];
                emoji.style.left = Math.random() * container.offsetWidth + 'px';
                const duration = 2 + Math.random() * 3;
                emoji.style.animationDuration = duration + 's';
                container.appendChild(emoji);
                setTimeout(() => emoji.remove(), duration * 1000);
            }}

            document.getElementById('startButton').addEventListener('click', function() {{
                if (!isActive) {{
                    isActive = true;
                    this.textContent = 'Stop Food Rain! 🛑';
                    window.parent.postMessage('startAudio', '*');
                    interval = setInterval(spawnEmoji, 50);
                    for (let i = 0; i < 20; i++) {{
                        setTimeout(spawnEmoji, i * 50);
                    }}
                }} else {{
                    isActive = false;
                    this.textContent = 'Start Food Rain! 🍔';
                    clearInterval(interval);
                    window.parent.postMessage('stopAudio', '*');
                    document.querySelectorAll('.falling-emoji').forEach(e => e.remove());
                }}
            }});
        </script>
    </body>
    </html>
    """

def main():
    st.set_page_config(page_title="Food Emoji Rain", page_icon="🍔", layout="wide")

    # Load and encode the audio file in Base64
    audio_file = open('song.mp3', 'rb')
    audio_bytes = audio_file.read()
    base64_audio = base64.b64encode(audio_bytes).decode('utf-8')

    # Embed the audio playback with JavaScript
    st.write(f"""
    <script>
        const audio = new Audio('data:audio/mp3;base64,{base64_audio}');
        audio.loop = true;

        window.addEventListener('message', (event) => {{
            if (event.data === 'startAudio') {{
                audio.play();
            }} else if (event.data === 'stopAudio') {{
                audio.pause();
            }}
        }});
    </script>
    """, unsafe_allow_html=True)

    # Add the emoji rain component
    components.html(
        get_emoji_rain_html(),
        height=600,
        scrolling=False
    )

if __name__ == "__main__":
    main()
