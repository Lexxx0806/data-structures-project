// script.js
// v5: FINAL INTEGRATION - Connected to Python Server

// --- Settings ---
const CANVAS_WIDTH = 800;
const CANVAS_HEIGHT = 600;
const POINT_COLOR = "black";
const FOUND_COLOR = "lime";
const SELECTED_COLOR = "aqua";
const BOX_COLOR = "blue";
const SERVER_URL = "http://127.0.0.1:5000/search"; // The Python "Phone Number"

// --- Setup ---
const canvas = document.getElementById("search-canvas");
const ctx = canvas.getContext("2d");
canvas.width = CANVAS_WIDTH;
canvas.height = CANVAS_HEIGHT;

const sidebar = document.getElementById("sidebar");
const sidebarTitle = document.getElementById("sidebar-title");
const listingContainer = document.getElementById("listing-container");

// --- Modal Elements ---
const modalBackdrop = document.getElementById("modal-backdrop");
const modalContent = document.getElementById("modal-content");
const modalCloseBtn = document.getElementById("modal-close-btn");
const modalMainImage = document.getElementById("modal-main-image");
const modalThumbnails = document.getElementById("modal-thumbnails");

const mapImage = new Image();

let isDragging = false;
let dragStart = { x: 0, y: 0 };
let searchRect = { x: 0, y: 0, width: 0, height: 0 };

let allPoints = []; // Stores ALL points from server (for black dots)
let foundPoints = []; // Stores SEARCH results from server (for green dots)
let selectedPoint = null;

// --- Main Draw Function ---
function draw() {
  // 1. Draw Map
  if (!mapImage.complete || mapImage.naturalWidth === 0) {
    ctx.fillStyle = "#333";
    ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
  } else {
    ctx.drawImage(mapImage, 0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
  }

  // 2. Draw ALL points (black)
  ctx.fillStyle = POINT_COLOR;
  for (const point of allPoints) {
    ctx.beginPath();
    ctx.arc(point.x, point.y, 3, 0, 2 * Math.PI);
    ctx.fill();
  }

  // 3. Draw FOUND points (green)
  ctx.fillStyle = FOUND_COLOR;
  for (const point of foundPoints) {
    ctx.beginPath();
    ctx.arc(point.x, point.y, 4, 0, 2 * Math.PI);
    ctx.fill();
  }

  // 4. Draw SELECTED point (aqua)
  if (selectedPoint) {
    ctx.fillStyle = SELECTED_COLOR;
    ctx.strokeStyle = "white";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(selectedPoint.x, selectedPoint.y, 6, 0, 2 * Math.PI);
    ctx.fill();
    ctx.stroke();
  }

  // 5. Draw Search Box
  if (isDragging) {
    ctx.strokeStyle = BOX_COLOR;
    ctx.lineWidth = 3;
    ctx.fillStyle = "rgba(0, 150, 255, 0.2)";
    ctx.fillRect(
      searchRect.x,
      searchRect.y,
      searchRect.width,
      searchRect.height
    );
    ctx.strokeRect(
      searchRect.x,
      searchRect.y,
      searchRect.width,
      searchRect.height
    );
  }
}

// --- Sidebar Builder ---
function updateSidebar() {
  listingContainer.innerHTML = "";
  sidebarTitle.textContent = `Found ${foundPoints.length} Listings`;

  if (foundPoints.length > 0) {
    sidebar.classList.add("visible");

    for (const point of foundPoints) {
      const card = document.createElement("div");
      card.className = "listing-card";
      card.id = point.id;

      // Handle potential image errors with a fallback
      const imgSrc =
        point.photos && point.photos.length > 0
          ? point.photos[0]
          : "https://placehold.co/120x120?text=No+Img";

      card.innerHTML = `
                <img src="${imgSrc}" alt="${
        point.title
      }" onerror="this.src='https://placehold.co/120x120/505050/f5f5f5?text=Img+Err';">
                <div class="listing-card-info">
                    <h3>${point.title}</h3>
                    <p>${point.type} • ${point.address}</p>
                    <p class="price">NT$${point.price.toLocaleString()}/month</p>
                </div>
            `;

      card.addEventListener("click", () => {
        openImageGallery(point);
      });

      listingContainer.appendChild(card);
    }
  } else {
    sidebar.classList.remove("visible");
  }
}

// --- Click Helper ---
function findClickedPoint(clickX, clickY) {
  let closestPoint = null;
  let minDistance = 10;

  // Check found points first (priority)
  const pointsToCheck = foundPoints.length > 0 ? foundPoints : allPoints;

  for (const point of pointsToCheck) {
    const distance = Math.sqrt(
      (clickX - point.x) ** 2 + (clickY - point.y) ** 2
    );
    if (distance < minDistance) {
      minDistance = distance;
      closestPoint = point;
    }
  }
  return closestPoint;
}

// --- Image Gallery Modal ---
function openImageGallery(point) {
  modalThumbnails.innerHTML = "";

  if (!point.photos || point.photos.length === 0) return;

  modalMainImage.src = point.photos[0];

  point.photos.forEach((photoSrc, index) => {
    const thumb = document.createElement("img");
    thumb.src = photoSrc;
    thumb.className = "thumbnail-img";
    if (index === 0) thumb.classList.add("active");

    thumb.addEventListener("click", () => {
      modalMainImage.src = photoSrc;
      document
        .querySelectorAll("#modal-thumbnails .thumbnail-img")
        .forEach((t) => t.classList.remove("active"));
      thumb.classList.add("active");
    });

    modalThumbnails.appendChild(thumb);
  });

  modalBackdrop.classList.add("visible");
}

function closeImageGallery() {
  modalBackdrop.classList.remove("visible");
}

modalCloseBtn.addEventListener("click", closeImageGallery);
modalBackdrop.addEventListener("click", (e) => {
  if (e.target === modalBackdrop) closeImageGallery();
});

// --- HELPER: Fetch from Server ---
// This function handles the "phone call" to Python
async function fetchPointsFromServer(rect) {
  try {
    const response = await fetch(SERVER_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(rect),
    });

    if (!response.ok) throw new Error("Server error");
    return await response.json();
  } catch (error) {
    console.error("Connection failed:", error);
    return null;
  }
}

// --- Mouse Events ---
canvas.addEventListener("mousedown", (e) => {
  if (e.detail === 1) {
    selectedPoint = findClickedPoint(e.offsetX, e.offsetY);

    document
      .querySelectorAll(".listing-card")
      .forEach((c) => c.classList.remove("selected"));

    if (selectedPoint) {
      console.log("Clicked:", selectedPoint.title);
      const selectedCard = document.getElementById(selectedPoint.id);
      if (selectedCard) {
        selectedCard.classList.add("selected");
        selectedCard.scrollIntoView({ behavior: "smooth", block: "nearest" });
      } else {
        // If clicked a black dot (not in sidebar), show gallery directly?
        // Optional: openImageGallery(selectedPoint);
      }
    }
    draw();
    isDragging = false;
  }
});

canvas.addEventListener("dragstart", (e) => e.preventDefault());

canvas.addEventListener("mousemove", (e) => {
  if (e.buttons === 1 && !isDragging) {
    isDragging = true;
    dragStart.x = e.offsetX;
    dragStart.y = e.offsetY;
    foundPoints = [];
    selectedPoint = null;
    searchRect = { x: 0, y: 0, width: 0, height: 0 };
  }

  if (!isDragging) return;

  searchRect.x = Math.min(e.offsetX, dragStart.x);
  searchRect.y = Math.min(e.offsetY, dragStart.y);
  searchRect.width = Math.abs(e.offsetX - dragStart.x);
  searchRect.height = Math.abs(e.offsetY - dragStart.y);

  draw();
});

// --- FINAL INTEGRATION: Fast Search ---
canvas.addEventListener("mouseup", async (e) => {
  if (!isDragging) return;
  isDragging = false;

  // Only search if box is big enough
  if (searchRect.width < 5 || searchRect.height < 5) {
    draw();
    return;
  }

  // 1. Ask Server for points inside the box
  console.log("Searching server...");
  const results = await fetchPointsFromServer(searchRect);

  if (results) {
    foundPoints = results;
    console.log(`Server found ${foundPoints.length} points.`);
  } else {
    alert("Cannot connect to server. Is 'py server.py' running?");
  }

  updateSidebar();
  draw();
});

// --- Initialization ---
async function init() {
  mapImage.onload = () => {
    draw(); // Draw map immediately
  };
  mapImage.src = "map.jpg";

  // 1. On startup, ask server for ALL points (to draw black dots)
  // We send a rectangle covering the whole world
  const allWorld = { x: 0, y: 0, width: CANVAS_WIDTH, height: CANVAS_HEIGHT };

  console.log("Connecting to server to get initial points...");
  const results = await fetchPointsFromServer(allWorld);

  if (results) {
    allPoints = results;
    draw();
    console.log(
      "Connected! Loaded " + allPoints.length + " points from server."
    );
  } else {
    console.log("Server offline. Waiting for user to start server...");
    // Retry logic could go here, or just show a message
    ctx.font = "20px Arial";
    ctx.fillStyle = "red";
    ctx.fillText("Error: Python Server Not Running", 10, 30);
  }
}

init();
