import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Big Field Small Snake", layout="wide")

st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🐍 🇹🇭 สนามงู 65หมูกระทะ 🇹🇭 ()</h1>", unsafe_allow_html=True)

if 'start' not in st.session_state:
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    team = st.radio("เลือกฝ่ายของหนูๆ:", ["🔴 แดง notty", "🔵 สีน้ำเงิน taty"], horizontal=True)
    if st.button("🚀 เริ่มเล่นเลย!"):
        st.session_state.start = True
        st.session_state.color = "#FF4B4B" if "แดง" in team else "#1C83E1"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
else:
    # ขนาดจอ 600 และขนาดงู (box) แค่ 15
    game_code = f"""
    <div style="display: flex; flex-direction: column; align-items: center; background: #333; padding: 10px; border-radius: 20px;">
        <div style="color: white; font-size: 24px; margin-bottom: 10px;">คะแนน: <span id="score">0</span></div>
        
        <canvas id="snakeCanvas" width="600" height="600" style="border: 5px solid white; background: #000; box-shadow: 0 0 20px rgba(0,0,0,0.5);"></canvas>
        
        <div style="margin-top: 20px; display: grid; grid-template-columns: repeat(3, 80px); gap: 15px;">
            <div></div><button onclick="changeDir('UP')" style="width:80px; height:80px; font-size: 30px; border-radius: 50%;">⬆️</button><div></div>
            <button onclick="changeDir('LEFT')" style="width:80px; height:80px; font-size: 30px; border-radius: 50%;">⬅️</button>
            <button onclick="changeDir('DOWN')" style="width:80px; height:80px; font-size: 30px; border-radius: 50%;">⬇️</button>
            <button onclick="changeDir('RIGHT')" style="width:80px; height:80px; font-size: 30px; border-radius: 50%;">➡️</button>
        </div>
    </div>

    <script>
        const canvas = document.getElementById("snakeCanvas");
        const ctx = canvas.getContext("2d");
        let box = 15; // ขนาดงูตัวจิ๋ว
        let score = 0;
        let snake = [{{x: 20 * box, y: 20 * box}}, {{x: 19 * box, y: 20 * box}}];
        let food = {{x: Math.floor(Math.random()*39)*box, y: Math.floor(Math.random()*39)*box}};
        let dir = "RIGHT";

        function changeDir(d) {{ 
            if(d=="UP" && dir!="DOWN") dir="UP";
            if(d=="DOWN" && dir!="UP") dir="DOWN";
            if(d=="LEFT" && dir!="RIGHT") dir="LEFT";
            if(d=="RIGHT" && dir!="LEFT") dir="RIGHT";
        }}

        document.addEventListener("keydown", (e) => {{
            if(e.keyCode==37 && dir!="RIGHT") dir="LEFT";
            if(e.keyCode==38 && dir!="DOWN") dir="UP";
            if(e.keyCode==39 && dir!="LEFT") dir="RIGHT";
            if(e.keyCode==40 && dir!="UP") dir="DOWN";
        }});

        function draw() {{
            ctx.fillStyle = "black";
            ctx.fillRect(0, 0, 600, 600);
            
            // วาดงูจิ๋ว
            for(let i=0; i<snake.length; i++) {{
                ctx.fillStyle = (i==0) ? "{st.session_state.color}" : "#AAA";
                ctx.strokeStyle = "black";
                ctx.fillRect(snake[i].x, snake[i].y, box, box);
                ctx.strokeRect(snake[i].x, snake[i].y, box, box);
            }}
            
            // วาดอาหาร
            ctx.fillStyle = "#FFD700";
            ctx.beginPath();
            ctx.arc(food.x+box/2, food.y+box/2, box/2 - 2, 0, Math.PI*2);
            ctx.fill();

            let headX = snake[0].x;
            let headY = snake[0].y;

            if(dir=="LEFT") headX -= box;
            if(dir=="UP") headY -= box;
            if(dir=="RIGHT") headX += box;
            if(dir=="DOWN") headY += box;

            // กินอาหาร
            if(headX == food.x && headY == food.y) {{
                score += 10;
                document.getElementById("score").innerHTML = score;
                food = {{x: Math.floor(Math.random()*39)*box, y: Math.floor(Math.random()*39)*box}};
            }} else {{
                snake.pop();
            }}

            let newHead = {{x: headX, y: headY}};

            // ชนขอบหรือชนตัวเองตาย
            if(headX<0 || headY<0 || headX>=600 || headY>=600 || collision(newHead, snake)) {{
                alert("เกมจบแล้ว! หนูทำได้ " + score + " คะแนน");
                location.reload();
            }}
            
            snake.unshift(newHead);
        }

        function collision(head, array) {{
            for(let i=0; i<array.length; i++) {{
                if(head.x == array[i].x && head.y == array[i].y) return true;
            }}
            return false;
        }}

        setInterval(draw, 100); // ความเร็วระดับกำลังดีสำหรับเด็กๆ
    </script>
    """
    components.html(game_code, height=850)
    
    if st.button("⬅️ กลับไปหน้าเลือกทีม"):
        del st.session_state.start
        st.rerun()
