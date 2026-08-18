import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="벽돌깨기",
    page_icon="🧱",
    layout="centered"
)

st.title("🧱 벽돌깨기")
st.caption("← → 또는 A / D 키로 이동 · Space로 시작")

game_html = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    body {
        margin: 0;
        background: #0f172a;
        display: flex;
        justify-content: center;
        align-items: center;
        font-family: Arial, sans-serif;
        overflow: hidden;
    }

    .game-container {
        width: 100%;
        max-width: 720px;
        text-align: center;
    }

    canvas {
        width: 100%;
        max-width: 700px;
        border-radius: 14px;
        background: #111827;
        box-shadow: 0 10px 30px rgba(0,0,0,0.35);
        display: block;
        margin: auto;
    }

    .info {
        color: white;
        font-size: 14px;
        margin-top: 10px;
    }

    button {
        margin-top: 10px;
        padding: 10px 20px;
        border: none;
        border-radius: 8px;
        background: #2563eb;
        color: white;
        font-size: 15px;
        cursor: pointer;
    }

    button:hover {
        background: #1d4ed8;
    }
</style>
</head>

<body>

<div class="game-container">
    <canvas id="gameCanvas" width="700" height="500"></canvas>
    <div class="info">
        ← → / A D : 이동 &nbsp;&nbsp; Space : 시작/일시정지
    </div>
    <button onclick="restartGame()">다시 시작</button>
</div>

<script>
const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

const WIDTH = canvas.width;
const HEIGHT = canvas.height;

// -------------------------
// 게임 변수
// -------------------------

let score = 0;
let lives = 3;
let gameStarted = false;
let gamePaused = false;
let gameOver = false;
let level = 1;

const paddle = {
    width: 110,
    height: 14,
    x: WIDTH / 2 - 55,
    y: HEIGHT - 35,
    speed: 8,
    dx: 0
};

const ball = {
    x: WIDTH / 2,
    y: HEIGHT - 55,
    radius: 8,
    speed: 5,
    dx: 4,
    dy: -5
};

const brickRows = 5;
const brickCols = 10;
const brickWidth = 60;
const brickHeight = 22;
const brickPadding = 8;

let bricks = [];

function createBricks() {
    bricks = [];

    const totalWidth =
        brickCols * brickWidth +
        (brickCols - 1) * brickPadding;

    const startX = (WIDTH - totalWidth) / 2;

    for (let r = 0; r < brickRows; r++) {
        for (let c = 0; c < brickCols; c++) {
            bricks.push({
                x: startX + c * (brickWidth + brickPadding),
                y: 60 + r * (brickHeight + brickPadding),
                width: brickWidth,
                height: brickHeight,
                alive: true,
                color: `hsl(${r * 35 + 10}, 80%, 60%)`
            });
        }
    }
}

function resetBall() {
    ball.x = WIDTH / 2;
    ball.y = HEIGHT - 55;

    ball.dx = (Math.random() > 0.5 ? 1 : -1) * 4;
    ball.dy = -5;

    gameStarted = false;
}

// -------------------------
// 그리기
// -------------------------

function drawBackground() {
    const gradient = ctx.createLinearGradient(0, 0, 0, HEIGHT);
    gradient.addColorStop(0, "#111827");
    gradient.addColorStop(1, "#020617");

    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, WIDTH, HEIGHT);
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
        if (!brick.alive) return;

        ctx.fillStyle = brick.color;

        ctx.fillRect(
            brick.x,
            brick.y,
            brick.width,
            brick.height
        );

        ctx.strokeStyle = "rgba(255,255,255,0.25)";
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

    ctx.fillText(`점수: ${score}`, 20, 30);
    ctx.fillText(`목숨: ${lives}`, 300, 30);
    ctx.fillText(`레벨: ${level}`, 590, 30);
}

function drawMessage() {
    if (!gameStarted && !gameOver) {
        ctx.fillStyle = "rgba(0,0,0,0.45)";
        ctx.fillRect(0, 0, WIDTH, HEIGHT);

        ctx.fillStyle = "#ffffff";
        ctx.font = "30px Arial";
        ctx.textAlign = "center";

        ctx.fillText(
            "SPACE 키를 눌러 시작",
            WIDTH / 2,
            HEIGHT / 2
        );

        ctx.font = "16px Arial";

        ctx.fillText(
            "← → 또는 A / D 로 패들을 움직이세요",
            WIDTH / 2,
            HEIGHT / 2 + 35
        );

        ctx.textAlign = "left";
    }

    if (gamePaused && !gameOver) {
        ctx.fillStyle = "rgba(0,0,0,0.45)";
        ctx.fillRect(0, 0, WIDTH, HEIGHT);

        ctx.fillStyle = "#ffffff";
        ctx.font = "32px Arial";
        ctx.textAlign = "center";

        ctx.fillText(
            "일시정지",
            WIDTH / 2,
            HEIGHT / 2
        );

        ctx.textAlign = "left";
    }

    if (gameOver) {
        ctx.fillStyle = "rgba(0,0,0,0.6)";
        ctx.fillRect(0, 0, WIDTH, HEIGHT);

        ctx.fillStyle = "#ffffff";
        ctx.font = "42px Arial";
        ctx.textAlign = "center";

        ctx.fillText(
            lives <= 0 ? "GAME OVER" : "CLEAR!",
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

// -------------------------
// 충돌 판정
// -------------------------

function circleRectCollision(circle, rect) {
    const closestX = Math.max(
        rect.x,
        Math.min(circle.x, rect.x + rect.width)
    );

    const closestY = Math.max(
        rect.y,
        Math.min(circle.y, rect.y + rect.height)
    );

    const distanceX = circle.x - closestX;
    const distanceY = circle.y - closestY;

    return (
        distanceX * distanceX +
        distanceY * distanceY
    ) < circle.radius * circle.radius;
}

// -------------------------
// 게임 업데이트
// -------------------------

function update() {
    if (!gameStarted || gamePaused || gameOver) {
        return;
    }

    // 패들 이동
    paddle.x += paddle.dx;

    if (paddle.x < 0) {
        paddle.x = 0;
    }

    if (paddle.x + paddle.width > WIDTH) {
        paddle.x = WIDTH - paddle.width;
    }

    // 공 이동
    ball.x += ball.dx;
    ball.y += ball.dy;

    // 벽 충돌
    if (ball.x - ball.radius < 0) {
        ball.x = ball.radius;
        ball.dx *= -1;
    }

    if (ball.x + ball.radius > WIDTH) {
        ball.x = WIDTH - ball.radius;
        ball.dx *= -1;
    }

    if (ball.y - ball.radius < 42) {
        ball.y = 42 + ball.radius;
        ball.dy *= -1;
    }

    // 패들 충돌
    if (circleRectCollision(ball, paddle) && ball.dy > 0) {
        const paddleCenter = paddle.x + paddle.width / 2;

        const hitPosition =
            (ball.x - paddleCenter) / (paddle.width / 2);

        ball.dx = hitPosition * 6;

        if (Math.abs(ball.dx) < 1) {
            ball.dx = ball.dx < 0 ? -1 : 1;
        }

        ball.dy = -Math.abs(ball.dy);
    }

    // 벽돌 충돌
    for (let brick of bricks) {
        if (!brick.alive) continue;

        if (circleRectCollision(ball, brick)) {
            brick.alive = false;

            score += 10;

            // 충돌 방향 판단
            const centerX = brick.x + brick.width / 2;
            const centerY = brick.y + brick.height / 2;

            const diffX = ball.x - centerX;
            const diffY = ball.y - centerY;

            if (Math.abs(diffX) > Math.abs(diffY)) {
                ball.dx *= -1;
            } else {
                ball.dy *= -1;
            }

            break;
        }
    }

    // 모든 벽돌 제거
    const remainingBricks =
        bricks.filter(brick => brick.alive).length;

    if (remainingBricks === 0) {
        level++;

        if (level > 3) {
            gameOver = true;
            return;
        }

        createBricks();

        ball.speed += 1;

        ball.dx =
            (ball.dx > 0 ? 1 : -1) *
            (4 + level);

        ball.dy =
            (ball.dy > 0 ? 1 : -1) *
            (5 + level);
    }

    // 공이 바닥으로 떨어짐
    if (ball.y - ball.radius > HEIGHT) {
        lives--;

        if (lives <= 0) {
            gameOver = true;
        } else {
            resetBall();
        }
    }
}

// -------------------------
// 게임 루프
// -------------------------

function gameLoop() {
    update();

    drawBackground();
    drawBricks();
    drawPaddle();
    drawBall();
    drawHUD();
    drawMessage();

    requestAnimationFrame(gameLoop);
}

// -------------------------
// 키 입력
// -------------------------

document.addEventListener("keydown", e => {

    if (
        e.key === "ArrowLeft" ||
        e.key.toLowerCase() === "a"
    ) {
        paddle.dx = -paddle.speed;
    }

    if (
        e.key === "ArrowRight" ||
        e.key.toLowerCase() === "d"
    ) {
        paddle.dx = paddle.speed;
    }

    if (e.code === "Space") {
        e.preventDefault();

        if (gameOver) {
            restartGame();
            return;
        }

        if (!gameStarted) {
            gameStarted = true;
        } else {
            gamePaused = !gamePaused;
        }
    }
});

document.addEventListener("keyup", e => {
    if (
        e.key === "ArrowLeft" ||
        e.key.toLowerCase() === "a"
    ) {
        if (paddle.dx < 0) {
            paddle.dx = 0;
        }
    }

    if (
        e.key === "ArrowRight" ||
        e.key.toLowerCase() === "d"
    ) {
        if (paddle.dx > 0) {
            paddle.dx = 0;
        }
    }
});

// -------------------------
// 다시 시작
// -------------------------

function restartGame() {
    score = 0;
    lives = 3;
    level = 1;

    gameStarted = false;
    gamePaused = false;
    gameOver = false;

    paddle.x = WIDTH / 2 - paddle.width / 2;

    ball.speed = 5;

    createBricks();
    resetBall();
}

createBricks();
gameLoop();

</script>

</body>
</html>
"""

components.html(
    game_html,
    height=570,
    scrolling=False
)
