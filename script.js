// script.js
const CANVAS_WIDTH = 800;
const CANVAS_HEIGHT = 600;
const SERVER_URL = "http://127.0.0.1:5000";
const COLORS = {
  POINT: "#9ca3af",
  FOUND: "#84cc16",
  SELECTED: "#06b6d4",
  BOX_STROKE: "#3b82f6",
  BOX_FILL: "rgba(59, 130, 246, 0.15)",
  GRID: "rgba(200, 200, 200, 0.3)", // Lighter grid for better looks
};

const canvas = document.getElementById("search-canvas");
const canvasWrapper = document.getElementById("canvas-wrapper");
const ctx = canvas.getContext("2d");
const sidebar = document.getElementById("sidebar");
const sidebarTitle = document.getElementById("sidebar-title");
const sidebarCloseBtn = document.getElementById("sidebar-close-btn");
const resultCount = document.getElementById("result-count");
const listingContainer = document.getElementById("listing-container");
const modalBackdrop = document.getElementById("modal-backdrop");
const modalMainImage = document.getElementById("modal-main-image");
const modalThumbnails = document.getElementById("modal-thumbnails");
const modalCloseBtn = document.getElementById("modal-close-btn");
const landingView = document.getElementById("landing-view");
const appView = document.getElementById("app-view");
const loginModal = document.getElementById("login-modal");
const loginPanel = document.getElementById("login-panel");
const loginFormContent = document.getElementById("login-form-content");
const loginLoading = document.getElementById("login-loading");
const navLoginBtn = document.getElementById("nav-login-btn");
const heroCtaBtn = document.getElementById("hero-cta-btn");
const loginCloseBtn = document.getElementById("login-close-btn");
const loginSubmitBtn = document.getElementById("login-submit-btn");
const appLogoutBtn = document.getElementById("app-logout-btn");
const toggleGridBtn = document.getElementById("toggle-grid-btn");

let allPoints = [],
  foundPoints = [],
  gridBoxes = [],
  selectedPoint = null,
  isDragging = false,
  dragStart = { x: 0, y: 0 },
  searchRect = { x: 0, y: 0, width: 0, height: 0 },
  mapImage = new Image(),
  animationFrameId = null,
  showGrid = true;

// --- PERFORMANCE: Preload Images on Hover ---
function preloadImages(imageArray) {
  if (!imageArray) return;
  imageArray.forEach((url) => {
    const img = new Image();
    img.src = url;
  });
}

// --- LOGIN & NAV ---
function openLogin() {
  loginModal.classList.remove("opacity-0", "pointer-events-none");
  loginPanel.classList.remove("scale-95");
  loginPanel.classList.add("scale-100");
  loginFormContent.classList.remove("hidden");
  loginLoading.classList.add("hidden");
}
function closeLogin() {
  loginModal.classList.add("opacity-0", "pointer-events-none");
  loginPanel.classList.add("scale-95");
  loginPanel.classList.remove("scale-100");
}
function handleLoginSubmit() {
  loginFormContent.classList.add("hidden");
  loginLoading.classList.remove("hidden");
  loginLoading.style.display = "flex";
  setTimeout(() => enterApp(), 1500);
}
function enterApp() {
  closeLogin();
  landingView.classList.add("opacity-0", "scale-95", "pointer-events-none");
  setTimeout(() => {
    landingView.style.display = "none";
    appView.classList.add("view-active");
    initCanvas();
  }, 500);
}
function logoutApp() {
  appView.classList.remove("view-active");
  landingView.style.display = "flex";
  setTimeout(() => landingView.classList.remove("opacity-0", "scale-95", "pointer-events-none"), 50);
  sidebar.classList.remove("visible");
  canvasWrapper.classList.remove("sidebar-active");
}

if (navLoginBtn) navLoginBtn.addEventListener("click", openLogin);
if (heroCtaBtn) heroCtaBtn.addEventListener("click", openLogin);
if (loginCloseBtn) loginCloseBtn.addEventListener("click", closeLogin);
if (loginSubmitBtn) loginSubmitBtn.addEventListener("click", handleLoginSubmit);
if (appLogoutBtn) appLogoutBtn.addEventListener("click", logoutApp);

// --- CANVAS & LOGIC ---
function initCanvas() {
  canvas.width = CANVAS_WIDTH;
  canvas.height = CANVAS_HEIGHT;
  mapImage.src = "map.jpg";
  mapImage.onload = draw;
  mapImage.onerror = draw;

  // 1. Fetch Points (Initial Load)
  fetchPoints({ x: 0, y: 0, w: CANVAS_WIDTH, h: CANVAS_HEIGHT }).then((res) => {
    if (res) {
      allPoints = res;
      draw();
    }
  });

  // 2. Fetch Quadtree Grid
  fetch(`${SERVER_URL}/grid`)
    .then((res) => res.json())
    .then((data) => {
      gridBoxes = data;
      draw();
    })
    .catch((err) => console.log("Grid fetch error:", err));
}

function draw() {
  ctx.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

  // Background
  if (mapImage.complete && mapImage.naturalWidth > 0)
    ctx.drawImage(mapImage, 0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
  else {
    ctx.fillStyle = "#f3f4f6";
    ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
  }

  // Grid
  if (showGrid) {
    ctx.strokeStyle = COLORS.GRID;
    ctx.lineWidth = 1;
    for (const box of gridBoxes) {
      ctx.strokeRect(box.x, box.y, box.w, box.h);
    }
  }

  // Points
  ctx.fillStyle = COLORS.POINT;
  for (const p of allPoints) {
    ctx.beginPath();
    ctx.arc(p.x, p.y, 3, 0, 2 * Math.PI);
    ctx.fill();
  }
  ctx.fillStyle = COLORS.FOUND;
  for (const p of foundPoints) {
    ctx.beginPath();
    ctx.arc(p.x, p.y, 5, 0, 2 * Math.PI);
    ctx.fill();
  }

  // Selected Point
  if (selectedPoint) {
    ctx.fillStyle = COLORS.SELECTED;
    ctx.strokeStyle = "white";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(selectedPoint.x, selectedPoint.y, 8, 0, 2 * Math.PI);
    ctx.fill();
    ctx.stroke();
  }

  // Drag Box
  if (isDragging) {
    ctx.fillStyle = COLORS.BOX_FILL;
    ctx.strokeStyle = COLORS.BOX_STROKE;
    ctx.lineWidth = 2;
    ctx.fillRect(searchRect.x, searchRect.y, searchRect.width, searchRect.height);
    ctx.strokeRect(searchRect.x, searchRect.y, searchRect.width, searchRect.height);
  }
}

function getCanvasCoords(e) {
  const r = canvas.getBoundingClientRect();
  const scaleX = canvas.width / r.width;
  const scaleY = canvas.height / r.height;
  return {
    x: (e.clientX - r.left) * scaleX,
    y: (e.clientY - r.top) * scaleY,
  };
}

// --- INTERACTION ---
canvas.addEventListener("mousedown", (e) => {
  const c = getCanvasCoords(e),
    list = foundPoints.length ? foundPoints : allPoints;
  let clk = null,
    min = 10;

  list.forEach((p) => {
    const d = Math.sqrt((c.x - p.x) ** 2 + (c.y - p.y) ** 2);
    if (d < min) {
      min = d;
      clk = p;
    }
  });

  if (clk) {
    selectedPoint = clk;
    document.getElementById(`card-${clk.id}`)?.scrollIntoView({ behavior: "smooth", block: "center" });
    openSidebar();
    draw();
  } else {
    isDragging = true;
    dragStart = c;
    searchRect = { x: c.x, y: c.y, width: 0, height: 0 };
    selectedPoint = null;
    foundPoints = [];
    closeSidebar();
    draw();
  }
});

canvas.addEventListener("mousemove", (e) => {
  if (!isDragging) return;
  const c = getCanvasCoords(e);
  searchRect.x = Math.min(c.x, dragStart.x);
  searchRect.y = Math.min(c.y, dragStart.y);
  searchRect.width = Math.abs(c.x - dragStart.x);
  searchRect.height = Math.abs(c.y - dragStart.y);

  if (animationFrameId) cancelAnimationFrame(animationFrameId);
  animationFrameId = requestAnimationFrame(draw);
});

// FIX: Send 'w' and 'h' correctly to the server
canvas.addEventListener("mouseup", async () => {
  if (!isDragging) return;
  isDragging = false;

  if (searchRect.width > 5 && searchRect.height > 5) {
    const searchData = {
        x: searchRect.x,
        y: searchRect.y,
        w: searchRect.width, // Explicit 'w'
        h: searchRect.height // Explicit 'h'
    };
    const res = await fetchPoints(searchData);
    if (res) {
      foundPoints = res;
      updateSidebarList();
      openSidebar();
    }
  }
  draw();
});

// --- SIDEBAR & MODAL WITH FIXES ---
function openSidebar() {
  sidebar.classList.add("visible");
  canvasWrapper.classList.add("sidebar-active");
}
function closeSidebar() {
  sidebar.classList.remove("visible");
  canvasWrapper.classList.remove("sidebar-active");
}
sidebarCloseBtn.addEventListener("click", closeSidebar);

function updateSidebarList() {
  listingContainer.innerHTML = "";
  resultCount.textContent = `${foundPoints.length} found`;
  
  foundPoints.forEach((p, i) => {
    const c = document.createElement("div");
    c.className = "listing-card";
    c.id = `card-${p.id}`;
    c.style.animationDelay = `${i * 0.04}s`;

    const img = p.photos && p.photos.length ? p.photos[0] : "https://placehold.co/100";
    
    // FIX: Added 'onerror' to prevent broken images in sidebar
    c.innerHTML = `
      <img src="${img}" 
           loading="lazy" 
           onerror="this.src='https://images.unsplash.com/photo-1484154218962-a197022b5858?w=200'">
      <div class="listing-card-info">
        <h3>${p.title}</h3>
        <p class="price">$${p.price.toLocaleString()}/mo</p>
      </div>`;

    // FIX: Preload images on hover for speed
    c.addEventListener("mouseenter", () => preloadImages(p.photos));
    c.addEventListener("click", () => openModal(p));
    listingContainer.appendChild(c);
  });
}

function openModal(p) {
  document.getElementById("modal-title").textContent = p.title;
  document.getElementById("modal-price").textContent = `$${p.price.toLocaleString()}`;
  document.getElementById("modal-address").textContent = p.address;
  document.getElementById("modal-type").textContent = p.type;
  document.getElementById("modal-coords").textContent = `${Math.round(p.x)}, ${Math.round(p.y)}`;

  modalThumbnails.innerHTML = "";
  const ph = p.photos && p.photos.length ? p.photos : ["https://placehold.co/600"];
  
  modalMainImage.src = ph[0];
  // FIX: Added 'onerror' for main modal image
  modalMainImage.onerror = () => {
    modalMainImage.src = "https://images.unsplash.com/photo-1484154218962-a197022b5858?w=800";
  };

  ph.forEach((s, i) => {
    const t = document.createElement("img");
    t.src = s;
    t.className = "thumbnail-img";
    if (i === 0) t.classList.add("active");

    // FIX: Added 'onerror' for thumbnails
    t.onerror = () => { t.src = "https://images.unsplash.com/photo-1484154218962-a197022b5858?w=200"; };

    t.addEventListener("click", () => {
      modalMainImage.src = t.src;
      document.querySelectorAll(".thumbnail-img").forEach((el) => el.classList.remove("active"));
      t.classList.add("active");
    });
    modalThumbnails.appendChild(t);
  });
  modalBackdrop.classList.add("visible");
}

modalCloseBtn.addEventListener("click", () => modalBackdrop.classList.remove("visible"));
modalBackdrop.addEventListener("click", (e) => {
  if (e.target === modalBackdrop) modalBackdrop.classList.remove("visible");
});

async function fetchPoints(r) {
  try {
    const res = await fetch(`${SERVER_URL}/search`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(r),
    });
    if (!res.ok) throw new Error("Err");
    return await res.json();
  } catch (e) {
    console.error(e);
    return null;
  }
}

// TOGGLE GRID
if (toggleGridBtn) {
  toggleGridBtn.addEventListener("click", () => {
    showGrid = !showGrid;
    draw();
  });
}
