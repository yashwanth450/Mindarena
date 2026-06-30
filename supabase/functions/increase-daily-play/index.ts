import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from "https://esm.sh/@supabase/supabase-js@2"

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
}

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders })
  }

  try {
    const { name } = await req.json()

    if (!name) {
      return new Response(JSON.stringify({ 
        allowed: false, 
        message: "❌ Name is required" 
      }), { headers: { ...corsHeaders, "Content-Type": "application/json" } })
    }

    const supabase = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
    )

    const today = new Date().toISOString().split("T")[0]

    const { data, error } = await supabase
      .from("users")
      .select("plays_today, play_date")
      .eq("name", name)
      .single()

    if (error || !data) {
      return new Response(JSON.stringify({ 
        allowed: false, 
        message: "❌ User not found" 
      }), { headers: { ...corsHeaders, "Content-Type": "application/json" } })
    }

    let playsToday = data.plays_today || 0

    if (data.play_date !== today) {
      playsToday = 0
    }

    if (playsToday >= 2) {
      return new Response(JSON.stringify({ 
        allowed: false, 
        message: "You already played 2 times today. Come back tomorrow!" 
      }), { headers: { ...corsHeaders, "Content-Type": "application/json" } })
    }

    const { error: updateError } = await supabase
      .from("users")
      .update({ 
        plays_today: playsToday + 1, 
        play_date: today 
      })
      .eq("name", name)

    if (updateError) {
      return new Response(JSON.stringify({ 
        allowed: false, 
        message: updateError.message 
      }), { headers: { ...corsHeaders, "Content-Type": "application/json" } })
    }

    return new Response(JSON.stringify({ 
      allowed: true, 
      playsToday: playsToday + 1 
    }), { headers: { ...corsHeaders, "Content-Type": "application/json" } })

  } catch (err) {
    return new Response(JSON.stringify({ 
      allowed: false, 
      message: err.message 
    }), { headers: { ...corsHeaders, "Content-Type": "application/json" } })
  }
})