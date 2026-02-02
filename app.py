import streamlit as st
import streamlit.components.v1 as components

# ตั้งค่าหน้าจอแบบกว้างสะใจ
st.set_page_config(page_title="Space Adventure", layout="centered")

st.markdown("<h1 style='text-align: center; color: #f1c40f;'>🚀 -notty-ผจญภัยเก็บอัญมณีอวกาศผจญภัยเก็บอัญมณีอวกาศ</h1>", unsafe_allow_html=True)

# ส่วนของ Logic เกมที่เขียนขึ้นใหม่ทั้งหมด
game_js = """
<div style="display: flex; flex-direction: column; align-items: center; background: #1a1a2e; padding: 20px; border-radius: 20px; border: 4px solid #16213e;">
    <div style="color: #e94560; font-size: 24px; margin-bottom: 10px; font-family: 'Courier New', Courier, monospace;">
        Gems: <span id="score">0</span> | HP: <span id="hp">❤️❤️❤️</span>
    </div>
    <canvas id="gameCanvas" width="500" height="500" style="background: #0f3460; border: 2px solid #533483;"></canvas>
    
    <div style="margin-top: 20px; display: grid; grid-template-columns: repeat(3, 80px); gap: 10px;">
        <div></div><button onclick="move('UP')" style="width:80px; height:80px; font-size: 30px; cursor: pointer; border-radius: 15px;">🔼</button><div></div>
        <button onclick="move('LEFT')" style="width:80px; height:80px; font-size: 30px; cursor: pointer; border-radius: 15px;">◀️</button>
        <button onclick="move('DOWN')" style="width:80px; height:80px; font-size: 30px; cursor: pointer; border-radius: 15px;">🔽</button>
        <button onclick="move('RIGHT')" style="width:80px; height:80px; font-size: 30px; cursor: pointer; border-radius: 15px;">▶️</button>
    </div>
</div>

<script>
    const canvas = document.getElementById("gameCanvas");
    const ctx = canvas.getContext("2d");
    let score = 0;
    let hp = 3;
    let player = { x: 250, y: 400, size: 30 };
    let gems = [];
    let enemies = [];

    // สร้างอัญมณีใหม่
    function createGem() {
        return { x: Math.random() * 470, y: 0, size: 20, speed: 2 + Math.random() * 3 };
    }

    // สร้างอุกกาบาต (สิ่งกีดขวาง)
    function createEnemy() {
        return { x: Math.random() * 470, y: 0, size: 25, speed: 4 + Math.random() * 2 };
    }

    function move(dir) {
        if(dir === 'UP' && player.y > 0) player.y -= 30;
        if(dir === 'DOWN' && player.y < 470) player.y += 30;
        if(dir === 'LEFT' && player.x > 0) player.x -= 30;
        if(dir === 'RIGHT' && player.x < 470) player.x += 30;
    }

    function update() {
        ctx.clearRect(0, 0, 500, 500);

        // วาดผู้เล่น (ยานอวกาศ)
        ctx.font = "30px Arial";
        ctx.fillText("🚀", player.x, player.y + 25);

        // จัดการอัญมณี
        if(Math.random() < 0.02) gems.push(createGem());
        gems.forEach((gem, index) => {
            gem.y += gem.speed;
            ctx.fillText("💎", gem.x, gem.y);
            
            // เช็คเก็บของได้
            if(Math.abs(player.x - gem.x) < 30 && Math.abs(player.y - gem.y) < 30) {
                score += 1;
                document.getElementById("score").innerText = score;
                gems.splice(index, 1);
            }
        });

        // จัดการอุกกาบาต
        if(Math.random() < 0.01) enemies.push(createEnemy());
        enemies.forEach((enemy, index) => {
            enemy.y += enemy.speed;
            ctx.fillText("☄️", enemy.x, enemy.y);
            
            // เช็คชนอุกกาบาต
            if(Math.abs(player.x - enemy.x) < 25 && Math.abs(player.y - enemy.y) < 25) {
                hp -= 1;
                document.getElementById("hp").innerText = "❤️".repeat(hp);
                enemies.splice(index, 1);
                if(hp <= 0) {
                    alert("Game Over! คุณเก็บอัญมณีได้: " + score);
                    location.reload();
                }
            }
        });

        requestAnimationFrame(update);
    }
    update();
</script>
"""

components.html(game_js, height=800)
