// script.js
// This is Team 2's main file. It runs the UI in "Slow Mode".

// --- Settings ---
const CANVAS_WIDTH = 800;
const CANVAS_HEIGHT = 600;
const POINT_COUNT = 2000;
const POINT_COLOR = "white";
const FOUND_COLOR = "lime";
const BOX_COLOR = "aqua";

// --- Setup ---
const canvas = document.getElementById('search-canvas');
const ctx = canvas.getContext('2d');
canvas.width = CANVAS_WIDTH;
canvas.height = CANVAS_HEIGHT;

const resultsLabel = document.getElementById('results-label');

let isDragging = false;
let dragStart = { x: 0, y: 0 };
let searchRect = { x: 0, y: 0, width: 0, height: 0 };

let allPoints = [];
let foundPoints = [];

// --- Data Generation ---
// Generate random points (IN JAVASCRIPT)
function generateRandomPoints(count, width, height) {
    let points = [];
    for (let i = 0; i < count; i++) {
        points.push({
            x: Math.floor(Math.random() * width),
            y: Math.floor(Math.random() * height)
        });
    }
    return points;
}

// --- Main Draw Function ---
function draw() {
    // 1. Clear the canvas
    ctx.fillStyle = "#333"; // Background color
    ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

    // 2. Draw all points (as small white dots)
    ctx.fillStyle = POINT_COLOR;
    for (const point of allPoints) {
        ctx.beginPath();
        ctx.arc(point.x, point.y, 2, 0, 2 * Math.PI);
        ctx.fill();
    }

    // 3. Draw the found points (as larger green dots)
    ctx.fillStyle = FOUND_COLOR;
    for (const point of foundPoints) {
        ctx.beginPath();
        ctx.arc(point.x, point.y, 3, 0, 2 * Math.PI);
        ctx.fill();
    }
    
    // 4. Draw the search box
    if (isDragging) {
        ctx.strokeStyle = BOX_COLOR;
        ctx.lineWidth = 2;
        ctx.strokeRect(searchRect.x, searchRect.y, searchRect.width, searchRect.height);
    }
}

// --- Mouse Event Handlers ---
canvas.addEventListener('mousedown', (e) => {
    isDragging = true;
    dragStart.x = e.offsetX;
    dragStart.y = e.offsetY;
    foundPoints = []; // Clear old results
    searchRect = { x: 0, y: 0, width: 0, height: 0 };
});

canvas.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    
    // Calculate the search rectangle
    searchRect.x = Math.min(e.offsetX, dragStart.x);
    searchRect.y = Math.min(e.offsetY, dragStart.y);
    searchRect.width = Math.abs(e.offsetX - dragStart.x);
    searchRect.height = Math.abs(e.offsetY - dragStart.y);
    
    // Redraw the screen to show the box
    draw();
});

canvas.addEventListener('mouseup', (e) => {
    isDragging = false;
    
    // --- THIS IS THE "SLOW" SEARCH ---
    // Team 2: When Team 1 is done, you will replace this
    // "for" loop with a call to the Python server.
    console.log("Running slow search...");
    foundPoints = [];
    for (const point of allPoints) {
        const isInside = (
            point.x >= searchRect.x &&
            point.x <= searchRect.x + searchRect.width &&
            point.y >= searchRect.y &&
            point.y <= searchRect.y + searchRect.height
        );
        if (isInside) {
            foundPoints.push(point);
        }
    }
    console.log(`Found ${foundPoints.length} points.`);
    resultsLabel.textContent = `Found: ${foundPoints.length} points`;
    // --- END OF SLOW SEARCH ---
    
    // Redraw one last time to show final results
    draw();
});

// --- Initialization ---
function init() {
    allPoints = generateRandomPoints(POINT_COUNT, CANVAS_WIDTH, CANVAS_HEIGHT);
    draw();
}

init();