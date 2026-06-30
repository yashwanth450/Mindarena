const SUPABASE_URL = "https://aouumcwtemruqcxquigd.supabase.co";
const SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFvdXVtY3d0ZW1ydXFjeHF1aWdkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODIwMTY5MTYsImV4cCI6MjA5NzU5MjkxNn0.OpLIfmiqcvK1eh0zjnQj0vKsyKUv47d4MZ_hJbBKBOc";

const supabaseClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

// ─── Helper to call any edge function ───────────────────────────
async function callEdge(functionName, body) {
    try {
        const { data, error } = await supabaseClient.functions.invoke(functionName, { body });
        if (error) return { success: false, message: error.message };
        return data;
    } catch (err) {
        return { success: false, message: err.message };
    }
}

////////////////////////////////////////////////////////////create account section///////////////////////////////////////
async function registerUser(name, age, password) {
    return await callEdge("register-user", { name, age, password });
}

///////////////////////////////////////////////login section////////////////////////////////////////////////
async function loginUser(name, password) {
    return await callEdge("login-user", { name, password });
}

function getTodayKey() {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, "0");
    const day = String(today.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
}

async function getDailyPlayStatus(name) {
    const today = getTodayKey();

    const { data, error } = await supabaseClient
        .from("users")
        .select("plays_today, play_date")
        .eq("name", name)
        .single();

    if (error || !data) {
        return { allowed: false, message: "Could not check daily limit" };
    }

    if (data.play_date !== today) {
        return { allowed: true, playsToday: 0 };
    }

    if ((data.plays_today || 0) >= 2) {
        return {
            allowed: false,
            message: "You already played 2 times today. Come back tomorrow!"
        };
    }

    return {
        allowed: true,
        playsToday: data.plays_today || 0
    };
}

async function increaseDailyPlay(name) {
    return await callEdge("increase-daily-play", { name });
}

///////////////////////////////// instruction page popup///////////////////////////////////////////////////////////
document.getElementById("closeModal").addEventListener("click", () => {
    document.getElementById("modal").classList.remove("show");
});

//////////////////////////////////////////////////////////////profile section/////////////////////////////////////
const offcanvas = document.getElementById("offcanvas");
const overlay = document.getElementById("overlay-profile");

document.getElementById("openBtn").onclick = () => {
    offcanvas.classList.add("show");
    overlay.classList.add("show");
    if (window._load_profile_proxy) {
        window._load_profile_proxy(null);
    }
};

document.getElementById("closeBtn").onclick = () => {
    offcanvas.classList.remove("show");
    overlay.classList.remove("show");
};

overlay.onclick = () => {
    offcanvas.classList.remove("show");
    overlay.classList.remove("show");
};

///////////////////////////////////////////////////loaders section////////////////////////////////////////
function showLoader(duration, message, callback) {
    var loader = document.getElementById("loader");
    loader.style.display = "flex";
    document.getElementById("loader-message").innerText = message;
    setTimeout(function () {
        loader.style.display = "none";
        if (callback) callback();
    }, duration);
}

function showLoader_game(duration, callback) {
    var loader_game = document.getElementById("loader-game");
    loader_game.style.display = "flex";
    setTimeout(function () {
        loader_game.style.display = "none";
        setTimeout(function () {
            if (callback) callback();
        }, 300);
    }, duration);
}

////////////////////////////////////////////contact_page/////////////////////////////////////////////////////////////
const offcanvasContact = document.getElementById("offcanvas-contact");
const overlayContact   = document.getElementById("overlay-contact");

document.getElementById("contact_link").onclick = (e) => {
    e.preventDefault();
    offcanvasContact.classList.add("show");
    overlayContact.classList.add("show");
};

document.getElementById("closeBtnContact").onclick = () => {
    offcanvasContact.classList.remove("show");
    overlayContact.classList.remove("show");
};

overlayContact.onclick = () => {
    offcanvasContact.classList.remove("show");
    overlayContact.classList.remove("show");
};

document.getElementById("contact-send").addEventListener("click", async () => {
    const msg = document.getElementById("contact-msg").value.trim();
    if (!msg) return;

    let name = "Anonymous";
    try {
        name = window._currentUser?.name 
            || window._currentUser?.["name"] 
            || "Anonymous";
    } catch(e) {}

    const { error } = await supabaseClient.from("feedback").insert([{
        name: name,
        message: msg
    }]);

    if (error) {
        alert("❌ Failed: " + error.message);
        return;
    }

    document.getElementById("contact-msg").value = "";
    alert("✅ Sent! Thank you for your feedback #SyrX");
});

/////////////////////////////////////////updating section/////////////////////////////////////////////////
async function updateScore(name, finalScore, fastAnswers, mediumAnswers, slowAnswers, totalGames) {
    return await callEdge("update-score", {
        name, finalScore, fastAnswers, mediumAnswers, slowAnswers, totalGames
    });
}

async function getUserRank(name) {
    const { data, error } = await supabaseClient
        .from("public_leaderboard")
        .select("name, total_score")
        .order("total_score", { ascending: false });

    if (error || !data) return null;

    const rank = data.findIndex(u => u.name === name) + 1;
    return rank > 0 ? rank : null;
}

window.registerUser = registerUser;
window.loginUser = loginUser;
window.updateScore = updateScore;
window.getLeaderboard = getLeaderboard;
window.getUserRank = getUserRank;
window.showLoader = showLoader;
window.showLoader_game = showLoader_game;
window.getDailyPlayStatus = getDailyPlayStatus;
window.increaseDailyPlay = increaseDailyPlay;

//////////////////////////Leaderboard///////////////////////////////

const offcanvasLb = document.getElementById("offcanvas-lb");
const overlayLb = document.getElementById("overlay-lb");

document.getElementById("leaderboard_status").onclick = (e) => {
    e.preventDefault();
    offcanvasLb.classList.add("show");
    overlayLb.classList.add("show");
    loadLeaderboard();
};
document.getElementById("closeBtnLb").onclick = () => {
    offcanvasLb.classList.remove("show");
    overlayLb.classList.remove("show");
};
overlayLb.onclick = () => {
    offcanvasLb.classList.remove("show");
    overlayLb.classList.remove("show");
};

async function getLeaderboard() {
    const { data, error } = await supabaseClient
        .from("public_leaderboard")
        .select("name, total_score")
        .order("total_score", { ascending: false });
    if (error || !data) return [];
    return data;
}
async function loadLeaderboard() {
    const listEl = document.getElementById("lb-list");
    listEl.innerHTML = `<div style="text-align:center;padding:30px;color:#8899aa;font-size:14px;">Loading...</div>`;

    const currentUser = window._currentUser?.name || null;
    const data = await getLeaderboard();
    if (!data.length) {
        listEl.innerHTML = `<div style="text-align:center;padding:30px;color:#8899aa;">No players yet.</div>`;
        return;
    }

    const medals = ["🥇", "🥈", "🥉"];
    const top10 = data.slice(0, 10);
    let html = "";

    top10.forEach((player, i) => {
        const rank = i + 1;
        const isMe = currentUser && player.name === currentUser;
        const initials = player.name.slice(0, 2).toUpperCase();
        const medal = rank <= 3 ? medals[rank - 1] : rank;
        const topCls = rank <= 3 ? " lb-top3" : "";
        const meCls = isMe ? " lb-me-row" : "";
        const meTag = isMe ? `<span class="lb-me-badge">YOU</span>` : "";
        const displayName =
            player.name.length > 7
                ? player.name.substring(0, 7) + "..."
                : player.name;

        html += `
        <div class="lb-row${topCls}${meCls}">
          <div class="lb-rank-num">${medal}</div>
          <div class="lb-avatar-circle">${initials}</div>
          <div class="lb-player-name" title="${player.name}">
           ${displayName}${meTag}
          </div>
          <div class="lb-player-score">${player.total_score.toLocaleString()} pts</div>
        </div>`;
    });

    if (currentUser) {
        const myIndex = data.findIndex(p => p.name === currentUser);
        if (myIndex >= 10) {
            const me = data[myIndex];
            const initials = me.name.slice(0, 2).toUpperCase();
            const displayName =
                me.name.length > 7
                    ? me.name.substring(0, 7) + "..."
                    : me.name;
            html += `<div class="lb-dots">• • •</div>`;
            html += `
            <div class="lb-row lb-me-row">
              <div class="lb-rank-num">${myIndex + 1}</div>
              <div class="lb-avatar-circle">${initials}</div>
              <div class="lb-player-name" title="${me.name}">
                ${displayName}<span class="lb-me-badge">YOU</span>
              </div>
              <div class="lb-player-score">${me.total_score.toLocaleString()} pts</div>
            </div>`;
        }
    }

    listEl.innerHTML = html;
}

window.getLeaderboard = getLeaderboard;
window.loadLeaderboard = loadLeaderboard;