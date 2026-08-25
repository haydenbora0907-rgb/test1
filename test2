import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="벽돌깨기",
    page_icon="🧱",
    layout="centered"
)

st.title("🧱 벽돌깨기")
st.caption("📱 화면의 버튼으로 패들을 움직이세요!")

game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport"
      content="width=device-width, initial-scale=1.0,
      maximum-scale=1.0, user-scalable=no">

<style>
* {
    box-sizing: border-box;
    -webkit-tap-highlight-color: transparent;
}

body {
    margin: 0;
    padding: 0;
    background: #020617;
    font-family: Arial, sans-serif;
    color: white;
    user-select: none;
    -webkit-user-select: none;
}

.game {
    width: 100%;
    max-width: 700px;
    margin: auto;
}

canvas {
    display: block;
    width: 100%;
    height: auto;
    background: #020617;
    border-radius: 14px;
    touch-action: none;
}

.controls {
    display: flex;
    gap: 12px;
    justify-content: center;
    align-items: center;
    margin-top: 15px;
}

.control-btn {
    width: 120px;
    height: 60px;
    border: none;
    border-radius: 14px;
    background: #2563eb;
    color: white;
    font-size: 25px;
    font-weight: bold;
    touch-action: manipulation;
}

.control-btn:active {
    background: #1d4ed8;
    transform: scale(0.95);
}

.start-btn {
    width: 160px;
    height: 52px;
    margin-top: 14px;
    border: none;
    border-radius: 12px;
    background: #16a34a;
    color: white;
    font-size: 18px;
    font-weight: bold;
}

.pause-btn {
    width: 100px;
    height: 52px;
    margin-top: 14px;
    border: none;
    border-radius: 12px;
    background: #475569;
    color: white;
    font-size: 17px;
}

.buttons {
    display: flex;
    justify-content: center;
    gap: 10px;
}

.info {
    text-align: center;
    margin-top: 10px;
    color: #cbd5e1;
    font-size: 14px;
}
</style>
</head>

<body>

<div class="game">

<canvas id="gameCanvas"
        width="700"
        height="500">
</canvas>

<div class="controls">

<button class="control-btn"
        id="leftBtn">◀</button>

<button class="control-btn"
        id="rightBtn">▶</button>

</div>

<div class="buttons">

<button class="start-btn"
        id="startBtn">
▶ 게임 시작
</button>

<button class="pause-btn"
        id="pauseBtn">
Ⅱ 일시정지
</button>

</div>

<div class="info">
📱 버튼을 누르고 있는 동안 패들이 이동합니다.
</div>

</div>

<script>

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const WIDTH = 700;
const HEIGHT = 500;

let score = 0;
let lives = 3;
let level = 1;

let gameStarted = false;
let gamePaused = false;
let gameOver = false;

const paddle = {
    width: 115,
    height: 14,
    x: WIDTH / 2 - 57,
    y: HEIGHT - 35,
    speed: 9,
    dx: 0
};

const ball = {
    x: WIDTH / 2,
    y: HEIGHT - 55,
    radius: 8,
    dx: 4,
    dy: -5
};

const rows = 5;
const cols = 10;

const brickWidth = 60;
const brickHeight = 22;
const brickPadding = 8;

let bricks = [];


function createBricks() {

    bricks = [];

    const totalWidth =
        cols * brickWidth +
        (cols - 1) * brickPadding;

    const startX =
        (WIDTH - totalWidth) / 2;

    for (let r = 0; r < rows; r++) {

        for (let c = 0; c < cols; c++) {

            bricks.push({
                x: startX +
                   c * (brickWidth + brickPadding),

                y: 60 +
                   r * (brickHeight + brickPadding),

                width: brickWidth,
                height: brickHeight,

                alive: true,

                color:
                    `hsl(${r * 35 + 10},
                    80%, 60%)`
            });

        }
    }
}


function resetBall() {

    ball.x = WIDTH / 2;
    ball.y = HEIGHT - 55;

    ball.dx =
        Math.random() > 0.5 ? 4 : -4;

    ball.dy = -5;

    gameStarted = false;
}


function drawBackground() {

    const gradient =
        ctx.createLinearGradient(
            0, 0, 0, HEIGHT
        );

    gradient.addColorStop(
        0, "#111827"
    );

    gradient.addColorStop(
        1, "#020617"
    );

    ctx.fillStyle = gradient;

    ctx.fillRect(
        0, 0, WIDTH, HEIGHT
    );
}


function drawPaddle() {

    ctx.fillStyle = "#38bdf8";

    ctx.fillRect(
        paddle.x,
        paddle.y,
        paddle.width,
        paddle.height
    );
}


function drawBall() {

    ctx.beginPath();

    ctx.arc(
        ball.x,
        ball.y,
        ball.radius,
        0,
        Math.PI * 2
    );

    ctx.fillStyle = "#ffffff";
    ctx.fill();

    ctx.closePath();
}


function drawBricks() {

    bricks.forEach(brick => {

        if (!brick.alive)
            return;

        ctx.fillStyle = brick.color;

        ctx.fillRect(
            brick.x,
            brick.y,
            brick.width,
            brick.height
        );

        ctx.strokeStyle =
            "rgba(255,255,255,0.25)";

        ctx.strokeRect(
            brick.x,
            brick.y,
            brick.width,
            brick.height
        );
    });
}


function drawHUD() {

    ctx.fillStyle = "#ffffff";
    ctx.font = "18px Arial";

    ctx.fillText(
        `점수: ${score}`,
        20,
        30
    );

    ctx.fillText(
        `목숨: ${lives}`,
        300,
        30
    );

    ctx.fillText(
        `레벨: ${level}`,
        590,
        30
    );
}


function drawMessage() {

    if (!gameStarted && !gameOver) {

        ctx.fillStyle =
            "rgba(0,0,0,0.45)";

        ctx.fillRect(
            0, 0, WIDTH, HEIGHT
        );

        ctx.fillStyle = "#ffffff";
        ctx.textAlign = "center";

        ctx.font = "30px Arial";

        ctx.fillText(
            "게임 시작 버튼을 누르세요",
            WIDTH / 2,
            HEIGHT / 2
        );

        ctx.font = "17px Arial";

        ctx.fillText(
            "아래 ◀ ▶ 버튼으로 이동",
            WIDTH / 2,
            HEIGHT / 2 + 35
        );

        ctx.textAlign = "left";
    }


    if (gamePaused && !gameOver) {

        ctx.fillStyle =
            "rgba(0,0,0,0.55)";

        ctx.fillRect(
            0, 0, WIDTH, HEIGHT
        );

        ctx.fillStyle = "#ffffff";

        ctx.font = "35px Arial";

        ctx.textAlign = "center";

        ctx.fillText(
            "일시정지",
            WIDTH / 2,
            HEIGHT / 2
        );

        ctx.textAlign = "left";
    }


    if (gameOver) {

        ctx.fillStyle =
            "rgba(0,0,0,0.65)";

        ctx.fillRect(
            0, 0, WIDTH, HEIGHT
        );

        ctx.fillStyle = "#ffffff";

        ctx.textAlign = "center";

        ctx.font = "42px Arial";

        ctx.fillText(
            lives <= 0
                ? "GAME OVER"
                : "CLEAR!",
            WIDTH / 2,
            HEIGHT / 2 - 20
        );

        ctx.font = "20px Arial";

        ctx.fillText(
            `최종 점수: ${score}`,
            WIDTH / 2,
            HEIGHT / 2 + 25
        );

        ctx.textAlign = "left";
    }
}


function collision(circle, rect) {

    const closestX =
        Math.max(
            rect.x,
            Math.min(
                circle.x,
                rect.x + rect.width
            )
        );

    const closestY =
        Math.max(
            rect.y,
            Math.min(
                circle.y,
                rect.y + rect.height
            )
        );

    const dx =
        circle.x - closestX;

    const dy =
        circle.y - closestY;

    return (
        dx * dx +
        dy * dy
    ) < circle.radius * circle.radius;
}


function update() {

    if (
        !gameStarted ||
        gamePaused ||
        gameOver
    ) {
        return;
    }


    paddle.x += paddle.dx;


    if (paddle.x < 0)
        paddle.x = 0;


    if (
        paddle.x +
        paddle.width >
        WIDTH
    ) {
        paddle.x =
            WIDTH - paddle.width;
    }


    ball.x += ball.dx;
    ball.y += ball.dy;


    // 좌우 벽

    if (
        ball.x -
        ball.radius < 0
    ) {

        ball.x = ball.radius;
        ball.dx *= -1;
    }


    if (
        ball.x +
        ball.radius > WIDTH
    ) {

        ball.x =
            WIDTH - ball.radius;

        ball.dx *= -1;
    }


    // 위쪽 벽

    if (
        ball.y -
        ball.radius < 42
    ) {

        ball.y =
            42 + ball.radius;

        ball.dy *= -1;
    }


    // 패들

    if (
        collision(ball, paddle) &&
        ball.dy > 0
    ) {

        const center =
            paddle.x +
            paddle.width / 2;

        const hit =
            (ball.x - center) /
            (paddle.width / 2);

        ball.dx = hit * 6;

        if (
            Math.abs(ball.dx) < 1
        ) {
            ball.dx =
                ball.dx < 0
                ? -1
                : 1;
        }

        ball.dy =
            -Math.abs(ball.dy);
    }


    // 벽돌

    for (
        let brick of bricks
    ) {

        if (!brick.alive)
            continue;


        if (
            collision(ball, brick)
        ) {

            brick.alive = false;

            score += 10;

            ball.dy *= -1;

            break;
        }
    }


    // 클리어

    const remaining =
        bricks.filter(
            b => b.alive
        ).length;


    if (remaining === 0) {

        level++;

        if (level > 3) {

            gameOver = true;
            return;
        }

        createBricks();

        ball.dx *= 1.15;
        ball.dy *= 1.15;
    }


    // 공이 떨어짐

    if (
        ball.y -
        ball.radius >
        HEIGHT
    ) {

        lives--;

        if (lives <= 0) {

            gameOver = true;

        } else {

            resetBall();
        }
    }
}


function draw() {

    drawBackground();
    drawBricks();
    drawPaddle();
    drawBall();
    drawHUD();
    drawMessage();
}


function loop() {

    update();
    draw();

    requestAnimationFrame(loop);
}


// ============================
// 모바일 버튼
// ============================

function startMoving(direction) {

    paddle.dx =
        direction *
        paddle.speed;
}


function stopMoving() {

    paddle.dx = 0;
}


const left =
    document.getElementById(
        "leftBtn"
    );

const right =
    document.getElementById(
        "rightBtn"
    );


// 왼쪽 버튼

left.addEventListener(
    "touchstart",
    e => {
        e.preventDefault();
        startMoving(-1);
    },
    {passive:false}
);

left.addEventListener(
    "touchend",
    e => {
        e.preventDefault();
        stopMoving();
    },
    {passive:false}
);

left.addEventListener(
    "mousedown",
    () => startMoving(-1)
);

left.addEventListener(
    "mouseup",
    stopMoving
);

left.addEventListener(
    "mouseleave",
    stopMoving
);


// 오른쪽 버튼

right.addEventListener(
    "touchstart",
    e => {
        e.preventDefault();
        startMoving(1);
    },
    {passive:false}
);

right.addEventListener(
    "touchend",
    e => {
        e.preventDefault();
        stopMoving();
    },
    {passive:false}
);

right.addEventListener(
    "mousedown",
    () => startMoving(1)
);

right.addEventListener(
    "mouseup",
    stopMoving
);

right.addEventListener(
    "mouseleave",
    stopMoving
);


// ============================
// 시작 버튼
// ============================

document
.getElementById("startBtn")
.addEventListener(
    "click",
    () => {

        if (gameOver) {
            restart();
            return;
        }

        gameStarted = true;
        gamePaused = false;
    }
);


// ============================
// 일시정지
// ============================

document
.getElementById("pauseBtn")
.addEventListener(
    "click",
    () => {

        if (!gameStarted ||
            gameOver) {
            return;
        }

        gamePaused =
            !gamePaused;
    }
);


// ============================
// 다시 시작
// ============================

function restart() {

    score = 0;
    lives = 3;
    level = 1;

    gameStarted = false;
    gamePaused = false;
    gameOver = false;

    paddle.x =
        WIDTH / 2 -
        paddle.width / 2;

    paddle.dx = 0;

    ball.dx = 4;
    ball.dy = -5;

    createBricks();
    resetBall();

    document
    .getElementById("startBtn")
    .innerText =
        "▶ 게임 시작";
}


// 초기화

createBricks();
draw();
loop();

</script>

</body>
</html>
"""

components.html(
    game_html,
    height=650,
    scrolling=False
)
