import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(page_title="Classic Snake Multiplayer", layout="centered")

# ส่วนหัวข้อ
st.title("🐍 Classic Snake: Team Battle")

if 'game_started' not in st.session_state:
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.player_name = st.text_input("ชื่อผู้เล่น:", "Player1")
    with col2:
        st.session_state.player_team = st.radio("เลือกทีม:", ["Red notty", "Blue taty"], horizontal=True)
    
    if st.button("เริ่มเกมเลื้อย"):
        st.session_state.game_started = True
        st.rerun()
else:
    team_color = "#FF4B4B" if st.session_state.player_team == "Red" else "#1C83E1"
    
    # ส่วนแสดงคะแนน
    st.subheader(f"ผู้เล่น: {st.session_state.player_name} | ทีม: {st.session_state.player_team}")

    # โค้ด JavaScript สำหรับงูแบบมีหางและขยับเอง
    snake_js_code = f"""
    <div style="display: flex; justify-content: center; flex-direction: column; align-items: center;">
        <canvas id="snakeGame" width="400" height="400" style="background: #111; border: 4px solid {team_color};"></canvas>
        <h2 id="scoreDisplay" style="color: white; font-family: sans-serif;">Score: 0</h2>
    </div>

    <script>
    const canvas = document.getElementById("snakeGame");
    const ctx = canvas.getContext("2d");
    const scoreEl = document.getElementById("scoreDisplay");

    let box = 20;
    let score = 0;
    let snake = [{{x: 9 * box, y: 10 * box}}, {{x: 8 * box, y: 10 * box}}]; // ตัวงูเริ่มต้นมี 2 ข้อ
    let food = {{x: Math.floor(random(0,19)) * box, y: Math.floor(random(0,19)) * box}};
    let d = "RIGHT";

    document.addEventListener("keydown", direction);
    function direction(event) {{
        if(event.keyCode == 37 && d != "RIGHT") d = "LEFT";
        else if(event.keyCode == 38 && d != "DOWN") d = "UP";
        else if(event.keyCode == 39 && d != "LEFT") d = "RIGHT";
        else if(event.keyCode == 40 && d != "UP") d = "DOWN";
    }}

    function random(min, max) {{ return Math.random() * (max - min) + min; }}

    function draw() {{
        ctx.fillStyle = "#111";
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // วาดหางงู
        for(let i = 0; i < snake.length; i++) {{
            ctx.fillStyle = (i == 0) ? "{team_color}" : "#CCCCCC"; 
            ctx.fillRect(snake[i].x, snake[i].y, box-2, box-2);
        }}

        // วาดอาหาร
        ctx.fillStyle = "gold";
        ctx.fillRect(food.x, food.y, box-2, box-2);

        let snakeX = snake[0].x;
        let snakeY = snake[0].y;

        if( d == "LEFT") snakeX -= box;
        if( d == "UP") snakeY -= box;
        if( d == "RIGHT") snakeX += box;
        if( d == "DOWN") snakeY += box;

        // ถ้ากินอาหาร
        if(snakeX == food.x && snakeY == food.y) {{
            score += 10;
            scoreEl.innerHTML = "Score: " + score;
            food = {{
                x: Math.floor(random(0,19)) * box,
                y: Math.floor(random(0,19)) * box
            }};
        }} else {{
            snake.pop(); // ตัดหางออกเพื่อให้ตัวเท่าเดิมถ้าไม่ได้กิน
        }}

        let newHead = {{x: snakeX, y: snakeY}};

        // กฎการแพ้: ชนขอบ หรือ ชนตัวเอง
        if(snakeX < 0 || snakeY < 0 || snakeX >= canvas.width || snakeY >= canvas.height || collision(newHead, snake)) {{
            clearInterval(game);
            alert("Game Over! คะแนนรวมของคุณ: " + score);
            location.reload();
        }}

        snake.unshift(newHead);
    }}

    function collision(head, array) {{
        for(let i = 0; i < array.length; i++) {{
            if(head.x == array[i].x && head.y == array[i].y) return true;
        }}
        return false;
    }}

    let game = setInterval(draw, 120); // ปรับความเร็วตรงนี้ (120ms)
    </script>
    """
    
    components.html(snake_js_code, height=500)
    
    if st.button("กลับหน้าหลัก"):
        del st.session_state.game_started
        st.rerun()
