import streamlit as st
import streamlit.components.v1 as components

# 1. ตั้งค่าหน้าจอ (ชิดขอบซ้ายสุด)
st.set_page_config(page_title="Snake Game", layout="wide")

if 'start' not in st.session_state:
    st.title("🐍 สนามงูยัก-65หมูกระทะ 🇹🇭")
    team = st.radio("เลือกทีม:", ["แดง notty", "น้ำเงิน taty"], horizontal=True)
    if st.button("เริ่มเล่น"):
        st.session_state.start = True
        st.session_state.color = "#FF4B4B" if team == "แดง" else "#1C83E1"
        st.rerun()
else:
    # ตรงนี้แหละครับคุณพ่อ ห้ามมีช่องว่างข้างหน้าคำว่า game_code เยอะเกินไป
    game_code = """
    <div style="display: flex; flex-direction: column; align-items: center; background: #333; padding: 20px; border-radius: 20px;">
        <div style="color: white; font-size: 24px; margin-bottom: 10px;">Score: <span id="score">0</span></div>
        <canvas id="snakeCanvas" width="600" height="600" style="border: 5px solid white; background: #000;"></canvas>
        <div style="margin-top: 20px; display: grid; grid-template-columns: repeat(3, 80px); gap: 15px;">
            <div></div><button onclick="changeDir('UP')" style="width:80px; height:80px; font-size: 30px;">⬆️</button><div></div>
            <button onclick="changeDir('LEFT')" style="width:80px; height:80px; font-size: 30px;">⬅️</button>
            <button onclick="changeDir('DOWN')" style="width:80px; height:80px; font-size: 30px;">⬇️</button>
            <button onclick="changeDir('RIGHT')" style="width:80px; height:80px; font-size: 30px;">➡️</button>
        </div>
    </div>
    <script>
        const canvas = document.getElementById("snakeCanvas");
        const ctx = canvas.getContext("2d");
        let box = 15; let score = 0;
        let snake = [{x: 20 * box, y: 20 * box}];
        let food = {x: Math.floor(Math.random()*39)*box, y: Math.floor(Math.random()*39)*box};
        let dir = "RIGHT";
        function changeDir(d) { dir = d; }
        function draw() {
            ctx.fillStyle = "black"; ctx.fillRect(0, 0, 600, 600);
            for(let i=0; i<snake.length; i++) {
                ctx.fillStyle = (i==0) ? '""" + st.session_state.color + """' : "#AAA";
                ctx.fillRect(snake[i].x, snake[i].y, box, box);
            }
            ctx.fillStyle = "gold"; ctx.fillRect(food.x, food.y, box, box);
            let headX = snake[0].x; let headY = snake[0].y;
            if(dir=="LEFT") headX -= box; if(dir=="UP") headY -= box;
            if(dir=="RIGHT") headX += box; if(dir=="DOWN") headY += box;
            if(headX == food.x && headY == food.y) {
                score += 10; document.getElementById("score").innerHTML = score;
                food = {x: Math.floor(Math.random()*39)*box, y: Math.floor(Math.random()*39)*box};
            } else { snake.pop(); }
            let newHead = {x: headX, y: headY};
            if(headX<0 || headY<0 || headX>=600 || headY>=600) location.reload();
            snake.unshift(newHead);
        }
        setInterval(draw, 100);
    </script>
    """
    components.html(game_code, height=900)
