    # ลบอันเก่าทิ้ง แล้ววางอันนี้แทนครับคุณพ่อ
    game_code = """
    <div style="display: flex; flex-direction: column; align-items: center; background: #333; padding: 15px; border-radius: 20px;">
        <div style="color: white; font-size: 28px; margin-bottom: 10px; font-weight: bold;">Score: <span id="score">0</span></div>
        <canvas id="snakeCanvas" width="600" height="600" style="border: 5px solid white; background: #000;"></canvas>
        
        <div style="margin-top: 25px; display: grid; grid-template-columns: repeat(3, 90px); gap: 15px;">
            <div></div><button onclick="changeDir('UP')" style="width:90px; height:90px; font-size: 35px; border-radius: 20px; background: #eee;">⬆️</button><div></div>
            <button onclick="changeDir('LEFT')" style="width:90px; height:90px; font-size: 35px; border-radius: 20px; background: #eee;">⬅️</button>
            <button onclick="changeDir('DOWN')" style="width:90px; height:90px; font-size: 35px; border-radius: 20px; background: #eee;">⬇️</button>
            <button onclick="changeDir('RIGHT')" style="width:90px; height:90px; font-size: 35px; border-radius: 20px; background: #eee;">➡️</button>
        </div>
    </div>

    <script>
        const canvas = document.getElementById("snakeCanvas");
        const ctx = canvas.getContext("2d");
        let box = 15; 
        let score = 0;
        let snake = [{x: 20 * box, y: 20 * box}, {x: 19 * box, y: 20 * box}];
        let food = {x: Math.floor(Math.random()*39)*box, y: Math.floor(Math.random()*39)*box};
        let dir = "RIGHT";

        function changeDir(d) { 
            if(d=="UP" && dir!="DOWN") dir="UP";
            if(d=="DOWN" && dir!="UP") dir="DOWN";
            if(d=="LEFT" && dir!="RIGHT") dir="LEFT";
            if(d=="RIGHT" && dir!="LEFT") dir="RIGHT";
        }

        function draw() {
            ctx.fillStyle = "black";
            ctx.fillRect(0, 0, 600, 600);
            
            for(let i=0; i<snake.length; i++) {
                ctx.fillStyle = (i==0) ? '""" + st.session_state.color + """' : "#AAA";
                ctx.fillRect(snake[i].x, snake[i].y, box-1, box-1);
            }
            
            ctx.fillStyle = "#FFD700"; // สีอาหาร (ทอง)
            ctx.beginPath();
            ctx.arc(food.x+box/2, food.y+box/2, box/2 - 2, 0, Math.PI*2);
            ctx.fill();

            let headX = snake[0].x;
            let headY = snake[0].y;

            if(dir=="LEFT") headX -= box;
            if(dir=="UP") headY -= box;
            if(dir=="RIGHT") headX += box;
            if(dir=="DOWN") headY += box;

            if(headX == food.x && headY == food.y) {
                score += 10;
                document.getElementById("score").innerHTML = score;
                food = {x: Math.floor(Math.random()*39)*box, y: Math.floor(Math.random()*39)*box};
            } else {
                snake.pop();
            }

            let newHead = {x: headX, y: headY};

            if(headX<0 || headY<0 || headX>=600 || headY>=600 || collision(newHead, snake)) {
                alert("Game Over! Score: " + score);
                location.reload();
            }
            
            snake.unshift(newHead);
        }

        function collision(head, array) {
            for(let i=0; i<array.length; i++) {
                if(head.x == array[i].x && head.y == array[i].y) return true;
            }
            return false;
        }

        setInterval(draw, 100);
    </script>
    """
