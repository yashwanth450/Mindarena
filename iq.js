 function showLoader(duration, callback) {
            var loader = document.getElementById("loader");

            loader.style.display = "flex";

            setTimeout(function () {
                loader.style.display = "none";
                callback();
            }, duration);

        }
function showLoader_game(duration, callback) {
            var loader_game = document.getElementById("loader-game");
            loader_game.style.display = "flex";

            setTimeout(function () {
                loader_game.style.display = "none";
             
                setTimeout(function () {
                    callback();
                }, 300);  
            }, duration);
        }

const SUPABASE_URL = "https://aouumcwtemruqcxquigd.supabase.co";
const SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFvdXVtY3d0ZW1ydXFjeHF1aWdkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODIwMTY5MTYsImV4cCI6MjA5NzU5MjkxNn0.OpLIfmiqcvK1eh0zjnQj0vKsyKUv47d4MZ_hJbBKBOc";

const supabaseClient = window.supabase.createClient(
  SUPABASE_URL,
  SUPABASE_KEY
);
async function saveUser(name, age,final_score) {
    const { data, error } = await supabaseClient
        .from("users")
        .insert([
            {
                name: name,
                age: parseInt(age),
                final_score: parseInt(final_score)
            }
        ]);
        

    if (error) {
        console.error(error);
    } else {
        console.log("Saved Successfully");
    }
}

window.saveUser = saveUser;
