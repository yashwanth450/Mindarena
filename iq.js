function showLoader(duration, message, callback) {

    var loader = document.getElementById("loader");

    loader.style.display = "flex";

    document.getElementById("loader-message").innerText = message;

    setTimeout(function () {

        loader.style.display = "none";

        if (callback) {
            callback();
        }

    }, duration);
}

function showLoader_game(duration, callback) {

    var loader_game = document.getElementById("loader-game");

    loader_game.style.display = "flex";

    setTimeout(function () {

        loader_game.style.display = "none";

        setTimeout(function () {

            if (callback) {
                callback();
            }

        }, 300);

    }, duration);
}

const SUPABASE_URL = "https://aouumcwtemruqcxquigd.supabase.co";
const SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFvdXVtY3d0ZW1ydXFjeHF1aWdkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODIwMTY5MTYsImV4cCI6MjA5NzU5MjkxNn0.OpLIfmiqcvK1eh0zjnQj0vKsyKUv47d4MZ_hJbBKBOc";

const supabaseClient = window.supabase.createClient(
  SUPABASE_URL,
  SUPABASE_KEY
);

async function registerUser(name, age, password) {

    try {

        const { data, error: checkError } =
            await supabaseClient
                .from("users")
                .select("name")
                .eq("name", name)
                .maybeSingle();

        if (checkError) {

            return {
                success: false,
                message: checkError.message
            };

        }

        if (data) {

            return {
                success: false,
                message: "❌ This name is already taken!"
            };

        }

        const { error } =
            await supabaseClient
                .from("users")
                .insert([
                    {
                        name: name,
                        age: parseInt(age),
                        password: password
                    }
                ]);

        if (error) {

            return {
                success: false,
                message: error.message
            };

        }

        return {
            success: true,
            message: "Account created successfully"
        };

    } catch (err) {

        return {
            success: false,
            message: err.message
        };

    }
}

window.registerUser = registerUser;
window.showLoader = showLoader;
window.showLoader_game = showLoader_game;