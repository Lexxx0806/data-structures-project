// script.js
// v4: Added image gallery modal

// --- Settings ---
const CANVAS_WIDTH = 800;
const CANVAS_HEIGHT = 600;
const POINT_COUNT = 100;
const POINT_COLOR = "black";
const FOUND_COLOR = "lime";
const SELECTED_COLOR = "aqua";
const BOX_COLOR = "blue";

// --- Setup ---
const canvas = document.getElementById('search-canvas');
const ctx = canvas.getContext('2d');
canvas.width = CANVAS_WIDTH;
canvas.height = CANVAS_HEIGHT;

const sidebar = document.getElementById('sidebar');
const sidebarTitle = document.getElementById('sidebar-title');
const listingContainer = document.getElementById('listing-container');

// --- NEW: Get Modal (Gallery) Elements ---
const modalBackdrop = document.getElementById('modal-backdrop');
const modalContent = document.getElementById('modal-content');
const modalCloseBtn = document.getElementById('modal-close-btn');
const modalMainImage = document.getElementById('modal-main-image');
const modalThumbnails = document.getElementById('modal-thumbnails');

const mapImage = new Image();

let isDragging = false;
let dragStart = { x: 0, y: 0 };
let searchRect = { x: 0, y: 0, width: 0, height: 0 };

let allPoints = [];
let foundPoints = [];
let selectedPoint = null;

// --- LISTING TEMPLATES ---
// (Your extensive LISTING_TEMPLATES array remains here)
const LISTING_TEMPLATES = [
    {
        title: "Cozy Studio near YZU",
        type: "Studio",
        address: "123 Yongfu Rd, Zhongli",
        price: 8500,
        photos: [
            'fakeimages/fakeroom1.jpg', 
            'fakeimages/fakeroom1.1.jpg',
            'fakeimages/fakeroom1.2.jpg',
            'fakeimages/fakeroom1.3.jpg',
            'fakeimages/fakeroom1.4.jpg'
        ]
    },
    {
        title: "Modern 1-BR Apartment",
        type: "1-BR Apartment",
        address: "456 Luguang Rd, Zhongli",
        price: 14000,
        photos: [
            'fakeimages/room2_a.jpg',
            'fakeimages/room2_b.jpg'
        ]
    },
    // ... (The remaining 56 templates have been preserved in the final code)
    {
        title: "Spacious Family Home",
        type: "3-BR Home",
        address: "789 Rongmin Rd, Zhongli",
        price: 26000,
        photos: [
            'fakeimages/room3_a.jpg'
        ]
    },
    {
        title: "Bright Studio by the Park",
        type: "Studio",
        address: "50 Xinxing Rd, Zhongli",
        price: 9500,
        photos: [
            'fakeimages/room4_a.jpg',
            'fakeimages/room4_b.jpg'
        ]
    },
    {
        title: "Simple Room (Shared Bath)",
        type: "Room",
        address: "21 Huanzhong Rd, Zhongli",
        price: 5500,
        photos: [
            'fakeimages/room5_a.jpg'
        ]
    },
    {
        title: "Renovated 2-BR",
        type: "2-BR Apartment",
        address: "33 Huamei 1st Rd, Zhongli",
        price: 18000,
        photos: [
            'fakeimages/room6_a.jpg',
            'fakeimages/room6_b.jpg',
            'fakeimages/room6_c.jpg'
        ]
    },
    {
        title: "Luxury Loft",
        type: "Loft",
        address: "88 Guangfu Rd, Zhongli",
        price: 27500,
        photos: [
            'fakeimages/room7_a.jpg',
            'fakeimages/room7_b.jpg'
        ]
    },
    {
        title: "Affordable Single Room",
        type: "Room",
        address: "112 Fuhua St, Zhongli",
        price: 6000,
        photos: [
            'fakeimages/room8_a.jpg'
        ]
    },
    {
        title: "Sunny 1-BR near Dazhentou",
        type: "1-BR Apartment",
        address: "45 Jixian Rd, Zhongli",
        price: 13500,
        photos: ['fakeimages/room9_a.jpg', 'fakeimages/room9_b.jpg']
    },
    {
        title: "Quiet Room for Students",
        type: "Room",
        address: "220 Zhongbei Rd, Zhongli",
        price: 7000,
        photos: ['fakeimages/room10_a.jpg']
    },
    {
        title: "2-BR w/ Balcony",
        type: "2-BR Apartment",
        address: "77 Puzhong Rd, Zhongli",
        price: 16500,
        photos: ['fakeimages/room11_a.jpg', 'fakeimages/room11_b.jpg']
    },
    {
        title: "Studio near Zhongli Station",
        type: "Studio",
        address: "19 Jianxing Rd, Zhongli",
        price: 10000,
        photos: ['fakeimages/room12_a.jpg']
    },
    {
        title: "Large 4-BR House",
        type: "4-BR Home",
        address: "30 Lane 725, Jiadong Rd",
        price: 28000,
        photos: ['fakeimages/room13_a.jpg', 'fakeimages/room13_b.jpg']
    },
    {
        title: "Penthouse Loft",
        type: "Loft",
        address: "500 Minzu Rd, Zhongli",
        price: 27000,
        photos: ['fakeimages/room14_a.jpg']
    },
    {
        title: "Basic Room, All Utilities Incl.",
        type: "Room",
        address: "88 Zhongmei Rd, Zhongli",
        price: 6500,
        photos: ['fakeimages/room15_a.jpg']
    },
    {
        title: "New 1-BR Condo",
        type: "1-BR Apartment",
        address: "12 Long'an St, Zhongli",
        price: 15000,
        photos: ['fakeimages/room16_a.jpg', 'fakeimages/room16_b.jpg']
    },
    {
        title: "YZU Student Dorm (Private)",
        type: "Room",
        address: "55 Wenhua 2nd Rd, Zhongli",
        price: 7200,
        photos: ['fakeimages/room17_a.jpg']
    },
    {
        title: "2-BR near Xinjin Park",
        type: "2-BR Apartment",
        address: "210 Xinxing Rd, Zhongli",
        price: 17000,
        photos: ['fakeimages/room18_a.jpg']
    },
    {
        title: "Studio (Newly Furnished)",
        type: "Studio",
        address: "90 Longgang Rd, Zhongli",
        price: 11000,
        photos: ['fakeimages/room19_a.jpg']
    },
    {
        title: "Small Studio",
        type: "Studio",
        address: "13 Huanbei Rd, Zhongli",
        price: 8000,
        photos: ['fakeimages/room20_a.jpg']
    },
    {
        title: "3-BR for Family or Shares",
        type: "3-BR Home",
        address: "25 Yixing Rd, Zhongli",
        price: 22000,
        photos: ['fakeimages/room1_b.jpg', 'fakeimages/room3_a.jpg']
    },
    {
        title: "Minimalist Room",
        type: "Room",
        address: "300 Zhongshan Rd, Zhongli",
        price: 5000,
        photos: ['fakeimages/room2_b.jpg']
    },
    {
        title: "Loft near Luguang",
        type: "Loft",
        address: "44 Zhongxiao Rd, Zhongli",
        price: 21000,
        photos: ['fakeimages/room4_a.jpg']
    },
    {
        title: "1-BR with City View",
        type: "1-BR Apartment",
        address: "99 Jianguo Rd, Zhongli",
        price: 14500,
        photos: ['fakeimages/room5_a.jpg']
    },
    {
        title: "Studio near Night Market",
        type: "Studio",
        address: "12 Mingde Rd, Zhongli",
        price: 9000,
        photos: ['fakeimages/room6_b.jpg']
    },
    {
        title: "Large Room in Shared Apt",
        type: "Room",
        address: "34 Wuquan Rd, Zhongli",
        price: 7500,
        photos: ['fakeimages/room7_b.jpg']
    },
    {
        title: "2-BR, Pet Friendly",
        type: "2-BR Apartment",
        address: "58 Yumin St, Zhongli",
        price: 19000,
        photos: ['fakeimages/room8_a.jpg', 'fakeimages/room9_a.jpg']
    },
    {
        title: "Single Room, Female Only",
        type: "Room",
        address: "70 Wenhua Rd, Zhongli",
        price: 6200,
        photos: ['fakeimages/room10_a.jpg']
    },
    {
        title: "Studio, Top Floor",
        type: "Studio",
        address: "22 Yongle Rd, Zhongli",
        price: 10500,
        photos: ['fakeimages/room11_b.jpg']
    },
    {
        title: "Massive 3-BR Condo",
        type: "3-BR Home",
        address: "150 Zhongzheng Rd, Zhongli",
        price: 27500,
        photos: ['fakeimages/room12_a.jpg']
    },
    {
        title: "Economic Room",
        type: "Room",
        address: "43 Chang'an St, Zhongli",
        price: 5000,
        photos: ['fakeimages/room13_b.jpg']
    },
    {
        title: "1-BR with Kitchen",
        type: "1-BR Apartment",
        address: "18 Longdong Rd, Zhongli",
        price: 13000,
        photos: ['fakeimages/room14_a.jpg']
    },
    {
        title: "Studio+Balcony",
        type: "Studio",
        address: "66 Sanyuan Rd, Zhongli",
        price: 11500,
        photos: ['fakeimages/room15_a.jpg']
    },
    {
        title: "Shared Apartment",
        type: "Room",
        address: "9 Longci Rd, Zhongli",
        price: 6800,
        photos: ['fakeimages/room16_b.jpg']
    },
    {
        title: "2-BR near Ring Rd",
        type: "2-BR Apartment",
        address: "140 Huanxi Rd, Zhongli",
        price: 17500,
        photos: ['fakeimages/room17_a.jpg']
    },
    {
        title: "New Building Studio",
        type: "Studio",
        address: "200 Minquan Rd, Zhongli",
        price: 12000,
        photos: ['fakeimages/room18_a.jpg']
    },
    {
        title: "3-BR near Zhongli Arts Hall",
        type: "3-BR Home",
        address: "100 Zhonghe Rd, Zhongli",
        price: 24000,
        photos: ['fakeimages/room19_a.jpg']
    },
    {
        title: "Simple Studio",
        type: "Studio",
        address: "35 Yanping Rd, Zhongli",
        price: 8800,
        photos: ['fakeimages/room20_a.jpg']
    },
    {
        title: "1-BR near Jungli Train Station",
        type: "1-BR Apartment",
        address: "55 Zhonghe Rd, Zhongli",
        price: 13000,
        photos: ['fakeimages/room1_c.jpg']
    },
    {
        title: "Room with Private Bath",
        type: "Room",
        address: "80 Zhongxiao Rd, Zhongli",
        price: 7800,
        photos: ['fakeimages/room2_a.jpg']
    },
    {
        title: "2-BR in Luguang Village",
        type: "2-BR Apartment",
        address: "12 Luguang Rd, Zhongli",
        price: 15500,
        photos: ['fakeimages/room3_a.jpg']
    },
    {
        title: "Studio with a View",
        type: "Studio",
        address: "210 Fuhua St, Zhongli",
        price: 10000,
        photos: ['fakeimages/room4_b.jpg']
    },
    {
        title: "Cheapest Room in Town",
        type: "Room",
        address: "5 Jiadong Rd, Zhongli",
        price: 5000,
        photos: ['fakeimages/room5_a.jpg']
    },
    {
        title: "Modern 2-BR",
        type: "2-BR Apartment",
        address: "66 Rongmin Rd, Zhongli",
        price: 19000,
        photos: ['fakeimages/room6_c.jpg']
    },
    {
        title: "YZU Area Studio",
        type: "Studio",
        address: "30 Lane 123, Yongfu Rd",
        price: 9200,
        photos: ['fakeimages/room7_a.jpg']
    },
    {
        title: "1-BR, Fully Furnished",
        type: "1-BR Apartment",
        address: "45 Xinxing Rd, Zhongli",
        price: 14200,
        photos: ['fakeimages/room8_a.jpg']
    },
    {
        title: "Large Room",
        type: "Room",
        address: "180 Huanzhong Rd, Zhongli",
        price: 7300,
        photos: ['fakeimages/room9_b.jpg']
    },
    {
        title: "3-BR near YZU",
        type: "3-BR Home",
        address: "55 Wenhua 2nd Rd, Zhongli",
        price: 23000,
        photos: ['fakeimages/room10_a.jpg']
    },
    {
        title: "Studio w/ Kitchenette",
        type: "Studio",
        address: "77 Puzhong Rd, Zhongli",
        price: 10800,
        photos: ['fakeimages/room11_a.jpg']
    },
    {
        title: "2-BR near Xinjin",
        type: "2-BR Apartment",
        address: "250 Xinxing Rd, Zhongli",
        price: 16000,
        photos: ['fakeimages/room12_a.jpg']
    },
    {
        title: "Shared Room, Low Price",
        type: "Room",
        address: "33 Huamei 1st Rd, Zhongli",
        price: 5200,
        photos: ['fakeimages/room13_a.jpg']
    },
    {
        title: "1-BR by Park",
        type: "1-BR Apartment",
        address: "80 Guangfu Rd, Zhongli",
        price: 13800,
        photos: ['fakeimages/room14_a.jpg']
    },
    {
        title: "Studio (All Inclusive)",
        type: "Studio",
        address: "42 Fuhua St, Zhongli",
        price: 11000,
        photos: ['fakeimages/room15_a.jpg']
    },
    {
        title: "Room in Quiet Area",
        type: "Room",
        address: "10 Lane 725, Jiadong Rd",
        price: 5800,
        photos: ['fakeimages/room16_a.jpg']
    },
    {
        title: "2-BR Condo, New Bldg",
        type: "2-BR Apartment",
        address: "300 Minzu Rd, Zhongli",
        price: 21000,
        photos: ['fakeimages/room17_a.jpg']
    },
    {
        title: "Bright Studio",
        type: "Studio",
        address: "15 Jianxing Rd, Zhongli",
        price: 9000,
        photos: ['fakeimages/room18_a.jpg']
    },
    {
        title: "3-BR (Pets OK)",
        type: "3-BR Home",
        address: "70 Long'an St, Zhongli",
        price: 24500,
        photos: ['fakeimages/room19_a.jpg']
    },
    {
        title: "Small Room",
        type: "Room",
        address: "50 Zhongbei Rd, Zhongli",
        price: 5300,
        photos: ['fakeimages/room20_a.jpg']
    }
];


// --- UPDATED `generateRandomPoints` ---
function generateRandomPoints(count, width, height) {
    let points = [];
    for (let i = 0; i < count; i++) {
        const template = LISTING_TEMPLATES[Math.floor(Math.random() * LISTING_TEMPLATES.length)];
        points.push({
            id: `listing-${i}`,
            x: Math.floor(Math.random() * width),
            y: Math.floor(Math.random() * height),
            title: template.title,
            type: template.type,
            address: template.address,
            price: template.price,
            photos: template.photos 
        });
    }
    return points;
}

// --- Main Draw Function ---
function draw() {
    // Handle map load error
    if (!mapImage.complete || mapImage.naturalWidth === 0) {
        ctx.fillStyle = "#333";
        ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
    } else {
        ctx.drawImage(mapImage, 0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
    }

    // Draw all points
    ctx.fillStyle = POINT_COLOR;
    for (const point of allPoints) {
        ctx.beginPath();
        ctx.arc(point.x, point.y, 3, 0, 2 * Math.PI);
        ctx.fill();
    }

    // Draw the found points (green)
    ctx.fillStyle = FOUND_COLOR;
    for (const point of foundPoints) {
        ctx.beginPath();
        ctx.arc(point.x, point.y, 4, 0, 2 * Math.PI);
        ctx.fill();
    }
    
    // Draw the *selected* point (aqua)
    if (selectedPoint) {
        ctx.fillStyle = SELECTED_COLOR;
        ctx.strokeStyle = "white";
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(selectedPoint.x, selectedPoint.y, 6, 0, 2 * Math.PI);
        ctx.fill();
        ctx.stroke();
    }
    
    // Draw the search box
    if (isDragging) {
        ctx.strokeStyle = BOX_COLOR;
        ctx.lineWidth = 3;
        ctx.fillStyle = "rgba(0, 150, 255, 0.2)";
        ctx.fillRect(searchRect.x, searchRect.y, searchRect.width, searchRect.height);
        ctx.strokeRect(searchRect.x, searchRect.y, searchRect.width, searchRect.height);
    }
}

// --- MODIFIED `updateSidebar` (Includes Empty State Logic) ---
function updateSidebar() {
    listingContainer.innerHTML = ''; 
    
    // Update the sidebar title text
    sidebarTitle.textContent = `Found ${foundPoints.length} Listings`;

    // Check if the sidebar should be visible or show the empty state
    if (foundPoints.length === 0) {
        // --- NEW: Empty State Logic (Uses the .empty-state CSS) ---
        const emptyStateHTML = `
            <div class="empty-state">
                <span class="emoji">😔</span>
                <h3>No listings found!</h3>
                <p>Try moving or expanding your search area on the map.</p>
            </div>
        `;
        listingContainer.innerHTML = emptyStateHTML;
        sidebar.classList.remove('visible'); // Hides the sidebar if no results
        // -----------------------------------------------------------
        
    } else {
        sidebar.classList.add('visible'); 

        for (const point of foundPoints) {
            const card = document.createElement('div');
            card.className = 'listing-card';
            card.id = point.id; 

            // Use the *first* photo (photos[0]) for the thumbnail
            card.innerHTML = `
                <img src="${point.photos[0]}" alt="${point.title}" onerror="this.src='https://placehold.co/120x120/505050/f5f5f5?text=Img+Err';">
                <div class="listing-card-info">
                    <h3>${point.title}</h3>
                    <p>${point.type} • ${point.address}</p>
                    <p class="price">NT$${point.price.toLocaleString()}/month</p>
                </div>
            `;
            
            // --- Add click listener to open the gallery ---
            card.addEventListener('click', () => {
                openImageGallery(point);
            });
            
            listingContainer.appendChild(card);
        }
    }
}

// --- FUNCTION TO FIND THE CLOSEST DOT TO A CLICK ---
function findClickedPoint(clickX, clickY) {
    let closestPoint = null;
    let minDistance = 10; 

    for (const point of foundPoints) {
        const distance = Math.sqrt((clickX - point.x) ** 2 + (clickY - point.y) ** 2);
        if (distance < minDistance) {
            minDistance = distance;
            closestPoint = point;
        }
    }
    return closestPoint;
}

// --- NEW: IMAGE GALLERY (MODAL) FUNCTIONS ---

function openImageGallery(point) {
    // Clear old thumbnails
    modalThumbnails.innerHTML = '';
    
    // Set the first image as the main one
    modalMainImage.src = point.photos[0];

    // Create all the thumbnails
    point.photos.forEach((photoSrc, index) => {
        const thumb = document.createElement('img');
        thumb.src = photoSrc;
        thumb.alt = `${point.title} thumbnail ${index + 1}`;
        thumb.className = 'thumbnail-img';
        
        // Add "active" class to the first thumbnail
        if (index === 0) {
            thumb.classList.add('active');
        }
        
        // Add click listener to the thumbnail
        thumb.addEventListener('click', () => {
            // Change main image
            modalMainImage.src = photoSrc;
            
            // Update "active" class
            document.querySelectorAll('#modal-thumbnails .thumbnail-img').forEach(t => {
                t.classList.remove('active');
            });
            thumb.classList.add('active');
        });
        
        modalThumbnails.appendChild(thumb);
    });

    // Show the modal
    modalBackdrop.classList.add('visible');
}

function closeImageGallery() {
    modalBackdrop.classList.remove('visible');
}

// Add listeners to close the modal
modalCloseBtn.addEventListener('click', closeImageGallery);
modalBackdrop.addEventListener('click', (e) => {
    // Only close if the click is on the backdrop itself, not the content
    if (e.target === modalBackdrop) {
        closeImageGallery();
    }
});


// --- Mouse Event Handlers ---
canvas.addEventListener('mousedown', (e) => {
    if (e.detail === 1) { 
        selectedPoint = findClickedPoint(e.offsetX, e.offsetY);
        
        document.querySelectorAll('.listing-card').forEach(c => {
            c.classList.remove('selected');
        });

        if (selectedPoint) {
            console.log("Clicked on:", selectedPoint.title);
            const selectedCard = document.getElementById(selectedPoint.id);
            if (selectedCard) {
                selectedCard.classList.add('selected');
                selectedCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        }
        draw();
        isDragging = false;
    } 
});

canvas.addEventListener('dragstart', (e) => e.preventDefault());

canvas.addEventListener('mousemove', (e) => {
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

// --- NEW: FAST SEARCH (QUADTREE INTEGRATION) FUNCTION ---
// Placed here for clean organization with other primary functions
async function fastSearch(searchBox) {
    console.log("Running FAST search via Quadtree server...");

    // 1. Prepare the search boundary coordinates
    const boundary = {
        minX: searchBox.x,
        minY: searchBox.y,
        maxX: searchBox.x + searchBox.width,
        maxY: searchBox.y + searchBox.height
    };
    
    // 2. Build the URL with query parameters for Team 1's server
    const query = new URLSearchParams(boundary).toString();
    const url = `http://127.0.0.1:5000/search?${query}`; 
    
    try {
        // 3. Fetch data from the Python server
        const response = await fetch(url);
        
        if (!response.ok) {
            console.error(`HTTP Error: Server returned status ${response.status}`);
            return []; 
        }
        
        // 4. Parse the JSON response
        const foundListings = await response.json();
        
        console.log(`Quadtree server found ${foundListings.length} listings.`);
        return foundListings; 
        
    } catch (error) {
        console.error("Connection Error: Failed to fetch listings from Python server. Is server.py running?", error);
        return []; 
    }
}


// --- MODIFIED `mouseup` HANDLER (Replaces Slow Search) ---
canvas.addEventListener('mouseup', async (e) => { // CRITICAL: Added 'async'
    if (!isDragging) return; 
    isDragging = false;
    
    // The old SLOW search loop has been removed/replaced here.
    
    // --- NEW: FAST SEARCH CALL (Calls the Back-End server) ---
    // Wait for the results from the Quadtree search
    foundPoints = await fastSearch(searchRect); 
    // ------------------------------------------------------
    
    updateSidebar(); // Renders the results (or the empty state)
    draw();
});

// --- Initialization ---
function init() {
    mapImage.onload = () => {
        allPoints = generateRandomPoints(POINT_COUNT, CANVAS_WIDTH, CANVAS_HEIGHT);
        draw();
    };
    mapImage.onerror = () => {
        console.error("Map image failed to load! Check 'map.jpg' path.");
        allPoints = generateRandomPoints(POINT_COUNT, CANVAS_WIDTH, CANVAS_HEIGHT);
        draw();
    }
    mapImage.src = 'map.jpg'; // Make sure this file exists!
}

init();
