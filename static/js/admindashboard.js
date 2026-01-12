
/*****************************************************
 * Admin Dashboard – Agent Chat (FINAL FIXED VERSION)
 *****************************************************/

/* ========= GLOBAL STATE ========= */
let socket = null;
let currentTicketId = null;

/* ========= LOAD ALL TICKETS ========= */
async function loadAllTickets() {
    const tableBody = document.getElementById("ticketTableBody");
    if (!tableBody) return;

    try {
        const response = await fetch("/api/all-tickets");
        const tickets = await response.json();

        tableBody.innerHTML = "";

        tickets.forEach(ticket => {
            const type = ticket.type || ticket.issue_type || "General Support";
            const date = new Date(ticket.created_at).toLocaleDateString();

            tableBody.innerHTML += `
                <tr>
                    <td><strong>${ticket.id}</strong></td>
                    <td>${ticket.subject}</td>
                    <td>${type}</td>
                    <td><span class="badge bg-info">${ticket.status}</span></td>
                    <td>${date}</td>
                    <td>
                        <button class="btn btn-primary btn-sm"
                            onclick="openChat('${ticket.id}')">
                            Chat
                        </button>
                    </td>
                </tr>
            `;
        });
    } catch (err) {
        console.error("Failed to load tickets", err);
    }
}


/* ========= OPEN CHAT ========= */
window.openChat = async function (ticketId) {
    currentTicketId = ticketId;
    document.getElementById("chatPopup").style.display = "block";
    document.getElementById("chatTicketId").innerText = ticketId;
    const chatBox = document.getElementById("chatMessages");
    chatBox.innerHTML = "";

    try {
        const res = await fetch(`/api/messages/${ticketId}`);
        const history = await res.json();
        history.forEach(m => {
            // FIX: Pass history through the same cleaning logic as live messages
            let cleanText = m.content;
            try {
                // If the DB stored '{"sender":"Agent","message":"hi"}', extract 'hi'
                const parsed = JSON.parse(m.content);
                cleanText = parsed.message || cleanText;
            } catch (e) {
                // Not JSON, keep as is
            }
            appendMessage(m.sender, cleanText);
        });
    } catch (err) {
        console.error("Failed to load chat history", err);
    }

    if (socket) socket.close();
    socket = new WebSocket(`ws://${window.location.host}/ws/chat/${ticketId}/Agent`);
    socket.onmessage = (event) => handleIncomingMessage(event.data);
};

/* ========= OPEN CHAT ========= */
// window.openChat = async function (ticketId) {
//     currentTicketId = ticketId;

//     // Show popup
//     document.getElementById("chatPopup").style.display = "block";
//     document.getElementById("chatTicketId").innerText = ticketId;

//     // Clear UI
//     const chatBox = document.getElementById("chatMessages");
//     chatBox.innerHTML = "";

//     // Load chat history
//     try {
//         const res = await fetch(`/api/messages/${ticketId}`);
//         const history = await res.json();
//         history.forEach(m => appendMessage(m.sender, m.content));
//     } catch (err) {
//         console.error("Failed to load chat history", err);
//     }

//     // Close old socket
//     if (socket) socket.close();

//     // Connect WebSocket as Agent
//     socket = new WebSocket(
//         `ws://${window.location.host}/ws/chat/${ticketId}/Agent`
//     );

//     socket.onmessage = function (event) {
//         handleIncomingMessage(event.data);
//     };

//     socket.onerror = err => console.error("WebSocket error", err);
// };

/* ========= SEND MESSAGE ========= */
window.sendMessage = function () {
    const input = document.getElementById("chatInput");
    const text = input.value.trim();

    if (!text || !socket || socket.readyState !== WebSocket.OPEN) return;

    // Always send clean JSON
    socket.send(JSON.stringify({
        sender: "Agent",
        message: text
    }));

    input.value = "";
};

/* ========= HANDLE INCOMING MESSAGE ========= */
function handleIncomingMessage(raw) {
    try {
        const data = JSON.parse(raw);

        let sender = data.sender || "Customer";
        let message = data.message;

        // 🟢 Handle double-encoded JSON
        if (typeof message === "string" && message.startsWith("{")) {
            try {
                const inner = JSON.parse(message);
                message = inner.message || message;
            } catch (_) {}
        }

        appendMessage(sender, message);
    } catch {
        // Plain text fallback
        appendMessage("Customer", raw);
    }
}

/* ========= APPEND MESSAGE TO UI ========= */
function appendMessage(sender, text) {
    const box = document.getElementById("chatMessages");
    if (!box) return;

    const msg = document.createElement("div");
    msg.style.marginBottom = "8px";
    msg.style.padding = "8px";
    msg.style.borderRadius = "6px";
    msg.style.maxWidth = "80%";

    if (sender === "Agent") {
        msg.style.background = "#d1e7dd";
        msg.style.marginLeft = "auto";
    } else {
        msg.style.background = "#f8f9fa";
        msg.style.marginRight = "auto";
    }

    msg.innerHTML = `<strong>${sender}:</strong> ${text}`;
    box.appendChild(msg);
    box.scrollTop = box.scrollHeight;
}

/* ========= CLOSE CHAT ========= */
function closeChat() {
    document.getElementById("chatPopup").style.display = "none";
    if (socket) socket.close();
}

/* ========= INIT ========= */
window.onload = loadAllTickets;
