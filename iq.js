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

const SUPABASE_URL = "https://aouumcwtemruqcxquigd.supabase.co";
const SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFvdXVtY3d0ZW1ydXFjeHF1aWdkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODIwMTY5MTYsImV4cCI6MjA5NzU5MjkxNn0.OpLIfmiqcvK1eh0zjnQj0vKsyKUv47d4MZ_hJbBKBOc";

const supabaseClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);

// ─── REGISTER ────────────────────────────────────────────────────────────────
async function registerUser(name, age, password) {
    try {
        const { data, error: checkError } = await supabaseClient
            .from("users")
            .select("name")
            .eq("name", name)
            .maybeSingle();

        if (checkError) return { success: false, message: checkError.message };
        if (data) return { success: false, message: "❌ This name is already taken!" };

        const { error } = await supabaseClient
            .from("users")
            .insert([{
                name: name,
                age: parseInt(age),
                password: password,
                total_score: 0,
                total_games: 0,
                fast_answers: 0,
                medium_answers: 0,
                slow_answers: 0
            }]);

        if (error) return { success: false, message: error.message };
        return { success: true, message: "Account created successfully" };

    } catch (err) {
        return { success: false, message: err.message };
    }
}

// ─── LOGIN ────────────────────────────────────────────────────────────────────
async function loginUser(name, password) {
    const { data, error } = await supabaseClient
        .from("users")
        .select("*")
        .eq("name", name)
        .single();

    if (error || !data) return { success: false, message: "❌ User not found" };

    // ✅ Password check
    if (data.password !== password) {
        return { success: false, message: "❌ Wrong password" };
    }

    return { success: true, user: data };
}

// ─── UPDATE SCORE ─────────────────────────────────────────────────────────────
// ─── UPDATE SCORE ─────────────────────────────────────────────────────────────
async function updateScore(name, finalScore, fastAnswers, mediumAnswers, slowAnswers, totalGames,accuracy) {
    console.log("Updating scores for:", name);

    // First, fetch the current user data to get existing scores
    const { data: userData, error: fetchError } = await supabaseClient
        .from("users")
        .select("total_score, fast_answers, medium_answers, slow_answers, total_games,accuracy, total_answers")
        .eq("name", name)
        .single();

    if (fetchError) {
        console.error("Fetch error:", fetchError);
        return false;
    }

    // Calculate cumulative scores (add new score to existing score)
    const newTotalScore = (userData.total_score || 0) + finalScore;
    const newFastAnswers = (userData.fast_answers || 0) + fastAnswers;
    const newMediumAnswers = (userData.medium_answers || 0) + mediumAnswers;
    const newSlowAnswers = (userData.slow_answers || 0) + slowAnswers;
    const totalAnswers = newFastAnswers + newMediumAnswers + newSlowAnswers;
    const overallAccuracy = totalAnswers > 0 ? Math.round((newFastAnswers / totalAnswers) * 100) : 0;
 
    console.log(`Cumulative - Fast: ${newFastAnswers}, Medium: ${newMediumAnswers}, Slow: ${newSlowAnswers}`);
    console.log(`Overall Accuracy: ${overallAccuracy}%`);
    const { error: updateError } = await supabaseClient
        .from("users")
        .update({
            total_score: newTotalScore,
            fast_answers: newFastAnswers,
            medium_answers: newMediumAnswers,
            slow_answers: newSlowAnswers,
            total_games: totalGames,
            accuracy: overallAccuracy,
            total_answers: totalAnswers
        })
        .eq("name", name);

    if (updateError) {
        console.error("Update error:", updateError);
        return false;
    }

    console.log("Score updated successfully");
    console.log(`New total score: ${newTotalScore}, Overall Accuracy: ${overallAccuracy}%`);
    return true;
}
// ─── LEADERBOARD ──────────────────────────────────────────────────────────────
// ============================================================
// LEADERBOARD
// ============================================================

// ─── GET USER RANK ────────────────────────────────────────────────────────────
async function getUserRank(name) {
    const { data, error } = await supabaseClient
        .from("users")
        .select("name, total_score")
        .order("total_score", { ascending: false });

    if (error || !data) return null;

    const rank = data.findIndex(u => u.name === name) + 1;
    return rank > 0 ? rank : null;
}

window.registerUser   = registerUser;
window.loginUser      = loginUser;
window.updateScore    = updateScore;
window.getLeaderboard = getLeaderboard;
window.getUserRank    = getUserRank;
window.showLoader     = showLoader;
window.showLoader_game = showLoader_game;