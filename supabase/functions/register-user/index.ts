import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from "https://esm.sh/@supabase/supabase-js@2"
import bcrypt from "https://esm.sh/bcryptjs@2.4.3"

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
}

serve(async (req) => {
  // ✅ Handle preflight request
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders })
  }

  try {
    const { name, age, password } = await req.json()

    if (!name || !age || !password) {
      return new Response(JSON.stringify({ 
        success: false, 
        message: "❌ All fields are required" 
      }), { headers: { ...corsHeaders, "Content-Type": "application/json" } })
    }

    const supabase = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
    )

    const { data: existing } = await supabase
      .from("users")
      .select("name")
      .eq("name", name)
      .maybeSingle()

    if (existing) {
      return new Response(JSON.stringify({ 
        success: false, 
        message: "❌ This name already existed! Please choose different!" 
      }), { headers: { ...corsHeaders, "Content-Type": "application/json" } })
    }

    const hashedPassword = await bcrypt.hash(password, 10)
    const today = new Date().toISOString().split("T")[0]

    const { error } = await supabase
      .from("users")
      .insert([{
        name: name,
        age: parseInt(age),
        password: hashedPassword,
        total_score: 0,
        total_games: 0,
        fast_answers: 0,
        medium_answers: 0,
        slow_answers: 0,
        plays_today: 0,
        play_date: today
      }])

    if (error) {
      return new Response(JSON.stringify({ 
        success: false, 
        message: error.message 
      }), { headers: { ...corsHeaders, "Content-Type": "application/json" } })
    }

    return new Response(JSON.stringify({ 
      success: true, 
      message: "Account created successfully" 
    }), { headers: { ...corsHeaders, "Content-Type": "application/json" } })

  } catch (err) {
    return new Response(JSON.stringify({ 
      success: false, 
      message: err.message 
    }), { headers: { ...corsHeaders, "Content-Type": "application/json" } })
  }
})