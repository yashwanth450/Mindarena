import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from "https://esm.sh/@supabase/supabase-js@2"
import bcrypt from "https://esm.sh/bcryptjs@2.4.3"

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
}

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders })
  }

  try {
    const { name, password } = await req.json()

    if (!name || !password) {
      return new Response(JSON.stringify({ 
        success: false, 
        message: "❌ Name and password are required" 
      }), { headers: { ...corsHeaders, "Content-Type": "application/json" } })
    }

    const supabase = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
    )

    const { data: user, error } = await supabase
      .from("users")
      .select("*")
      .eq("name", name)
      .single()

    if (error || !user) {
      return new Response(JSON.stringify({ 
        success: false, 
        message: "❌ User not found" 
      }), { headers: { ...corsHeaders, "Content-Type": "application/json" } })
    }

    const passwordMatch = await bcrypt.compare(password, user.password)

    if (!passwordMatch) {
      return new Response(JSON.stringify({ 
        success: false, 
        message: "❌ Wrong password" 
      }), { headers: { ...corsHeaders, "Content-Type": "application/json" } })
    }

    const { password: _, ...safeUser } = user

    return new Response(JSON.stringify({ 
      success: true, 
      user: safeUser 
    }), { headers: { ...corsHeaders, "Content-Type": "application/json" } })

  } catch (err) {
    return new Response(JSON.stringify({ 
      success: false, 
      message: err.message 
    }), { headers: { ...corsHeaders, "Content-Type": "application/json" } })
  }
})