// let chatSocket = null;
// const clientId = "Kannan"; // Hardcoded for your project

// async function loadMyTickets() {
//     const response = await fetch(`/api/tickets/${clientId}`);
//     let tickets = await response.json();
    
//     // IF NO TICKETS IN DB, SHOW DUMMY FOR TESTING
//     if (tickets.length === 0) {
//         tickets = [{id: "TKT-DUMMY", subject: "Test Ticket", status: "Open", type: "General"}];
//     }

//     const container = document.getElementById('ticketContainer');
//     container.innerHTML = "";
//     tickets.forEach(ticket => {
//         container.innerHTML += `
//             <div class="col-md-4 mb-3">
//                 <div class="card p-3 shadow-sm">
//                     <h5>${ticket.id}</h5>
//                     <p>${ticket.subject}</p>
//                     <span class="badge bg-primary mb-2">${ticket.status}</span>
//                     <button class="btn btn-primary btn-sm" onclick="openChat('${ticket.id}')">Chat with Agent</button>
//                 </div>
//             </div>`;
//     });
// }

// function openChat(ticketId) {
//     document.getElementById("chatPopup").style.display = "block";
//     document.getElementById("chatTicketId").innerText = ticketId;
//     document.getElementById("chatMessages").innerHTML = ""; // Clear box

//     if (chatSocket) chatSocket.close();
//     chatSocket = new WebSocket(`ws://localhost:8000/ws/chat/${ticketId}/Customer`);

//     chatSocket.onmessage = function(event) {
//         const data = JSON.parse(event.data);
//         const chatBox = document.getElementById("chatMessages");
//         const div = document.createElement("div");
//         div.className = data.sender === "Customer" ? "user-msg" : "agent-msg";
//         div.innerText = data.message;
//         chatBox.appendChild(div);
//         chatBox.scrollTop = chatBox.scrollHeight;
//     };
// }

// function sendMessage() {
//     const input = document.getElementById("chatInput");
//     if (input.value && chatSocket) {
//         chatSocket.send(input.value);
//         input.value = "";
//     }
// }

// window.onload = loadMyTickets;


let currentTicketId = "";
let socket = null;
const clientId = "Kannan"; // Simulated logged-in user

// 1. Fetch Tickets from DB on Load

async function loadTickets() {
    const container = document.getElementById('ticketContainer');
    try {
        const response = await fetch(`/api/tickets/${clientId}`);
        if (!response.ok) throw new Error("Failed to fetch");
        
        const tickets = await response.json();
        container.innerHTML = ""; // Clear the spinner

        if (tickets.length === 0) {
            container.innerHTML = `
                <div class="col-12 text-center mt-5">
                    <div class="alert alert-info">No tickets found for ${clientId}.</div>
                </div>`;
            return;
        }

        // tickets.forEach(ticket => {
        //     // ... (keep the existing ticketDiv creation logic here) ...
        //     const ticketDiv = document.createElement('div');
        //     ticketDiv.className = 'col-12 col-md-6 col-lg-4';
        //     // (rest of your existing innerHTML logic)
        //     container.appendChild(ticketDiv);
        // });

        // Inside your loadTickets function loop:
tickets.forEach(ticket => {
    // This line handles BOTH old and new column names to be safe
    const displayType = ticket.type || ticket.issue_type || "General"; 
    
    const ticketDiv = document.createElement('div');
    ticketDiv.className = 'col-12 col-md-6 col-lg-4 mb-3';
    ticketDiv.innerHTML = `
        <div class="card ticket-card h-100 shadow-sm">
            <div class="card-header bg-primary text-white"><strong>${ticket.id}</strong></div>
            <div class="card-body">
                <h6 class="card-title">${ticket.subject}</h6>
                <p class="text-muted small"><i class="bi bi-tag"></i> ${displayType}</p>
                <span class="badge bg-info">${ticket.status}</span>
                <div class="text-center mt-3">
                    <button class="btn btn-primary btn-sm" onclick="openChat('${ticket.id}')">
                        Chat with Agent
                    </button>
                </div>
            </div>
        </div>`;
    container.appendChild(ticketDiv);
});
    } catch (error) {
        console.error("Error loading tickets:", error);
        container.innerHTML = '<div class="alert alert-danger">Error connecting to server. Make sure FastAPI is running.</div>';
    }
}
// async function loadTickets() {
//     const response = await fetch(`/api/tickets/${clientId}`);
//     const tickets = await response.json();
//     const container = document.getElementById('ticketContainer');
//     container.innerHTML = "";

//     tickets.forEach(ticket => {
//         const ticketDiv = document.createElement('div');
//         ticketDiv.className = 'col-12 col-md-6 col-lg-4';
        
//         const statuses = ['Open', 'In Progress', 'Resolved', 'Closed'];
//         let statusHtml = '<div class="status-bar">';
//         statuses.forEach(s => {
//             let activeClass = (s === ticket.status) ? 'status-active' : '';
//             statusHtml += `<span class="status-pill ${activeClass}">${s}</span>`;
//         });
//         statusHtml += '</div>';

//         ticketDiv.innerHTML = `
//             <div class="card ticket-card h-100 shadow-sm">
//                 <div class="card-header bg-primary-blue text-white"><strong>${ticket.id}</strong></div>
//                 <div class="card-body">
//                     <h6 class="card-title">${ticket.subject}</h6>
//                     <p class="text-muted small"><i class="bi bi-tag"></i> ${ticket.issue_type}</p>
//                     ${statusHtml}
//                     <div class="text-center mt-4">
//                         <button class="btn btn-outline-primary btn-sm" onclick="openChat('${ticket.id}')">
//                             <i class="bi bi-chat-dots"></i> Chat with Agent
//                         </button>
//                     </div>
//                 </div>
//             </div>`;
//         container.appendChild(ticketDiv);
//     });
// }

// 2. Open Chat & Connect WebSocket
async function openChat(ticketId) {
    currentTicketId = ticketId;
    document.getElementById("chatPopup").style.display = "block";
    document.getElementById("chatTicketId").innerText = ticketId;
    document.getElementById("chatMessages").innerHTML = "";

    // Load History
    const history = await fetch(`/api/messages/${ticketId}`);
    const messages = await history.json();
    messages.forEach(msg => appendMessage(msg.sender, msg.content));

    // Connect WebSocket
    if (socket) socket.close();
    socket = new WebSocket(`ws://${window.location.host}/ws/chat/${ticketId}/Customer`);

    socket.onmessage = function(event) {
    try {
        // Parse the string into a real JavaScript object
        const data = JSON.parse(event.data);
        
        // If 'data.message' is somehow STILL a stringified JSON, parse it again
        let finalMessage = data.message;
        if (typeof finalMessage === 'string' && finalMessage.startsWith('{')) {
            const innerData = JSON.parse(finalMessage);
            finalMessage = innerData.message || finalMessage;
        }

        appendMessage(data.sender, finalMessage);
    } catch (e) {
        // If it's just a plain string, show it as is
        appendMessage("System", event.data);
    }
};
}

// function appendMessage(sender, text) {
//     const chatBox = document.getElementById("chatMessages");
//     const div = document.createElement("div");
//     div.className = (sender === "Customer") ? "user-msg" : "agent-msg";
//     div.innerText = text;
//     chatBox.appendChild(div);
//     chatBox.scrollTop = chatBox.scrollHeight;
// }

/* ========= APPEND MESSAGE TO UI (Customer Side) ========= */
function appendMessage(sender, text) {
    const box = document.getElementById("chatMessages");
    if (!box) return;

    const msg = document.createElement("div");
    msg.style.marginBottom = "8px";
    msg.style.padding = "8px";
    msg.style.borderRadius = "6px";
    msg.style.maxWidth = "80%";

    // Determine the Display Name and Alignment
    let displayName = "";
    if (sender === "Agent") {
        displayName = "Agent";
        msg.style.background = "#f8f9fa"; // Light grey for Agent
        msg.style.marginRight = "auto";
    } else {
        displayName = "You"; // Change Customer to 'You'
        msg.style.background = "#cfe2ff"; // Light blue for Customer
        msg.style.marginLeft = "auto";
    }

    msg.innerHTML = `<strong>${displayName}:</strong> ${text}`;
    box.appendChild(msg);
    box.scrollTop = box.scrollHeight;
}

function sendMessage() {
    const input = document.getElementById("chatInput");
    if (input.value.trim() !== "" && socket) {
        socket.send(input.value);
        input.value = "";
    }
}

function closeChat() {
    document.getElementById("chatPopup").style.display = "none";
    if (socket) socket.close();
}

window.onload = loadTickets;

