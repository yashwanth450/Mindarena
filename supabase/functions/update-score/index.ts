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
    const { name, finalScore, fastAnswers, mediumAnswers, slowAnswers, totalGames } = await req.json()

    if (!name || finalScore === undefined) {
      return new Response(JSON.stringify({ 
        success: false, 
        message: "❌ Invalid data" 
      }), { 
        status: 400,
        headers: { ...corsHeaders, "Content-Type": "application/json" } 
      })
    }

    if (finalScore < 0 || finalScore > 10000) {
      return new Response(JSON.stringify({ 
        success: false, 
        message: "❌ Invalid score" 
      }), { 
        status: 400,
        headers: { ...corsHeaders, "Content-Type": "application/json" } 
      })
    }

    if (fastAnswers < 0 || mediumAnswers < 0 || slowAnswers < 0) {
      return new Response(JSON.stringify({ 
        success: false, 
        message: "❌ Invalid answer counts" 
      }), { 
        status: 400,
        headers: { ...corsHeaders, "Content-Type": "application/json" } 
      })
    }

    const supabase = createClient(
      Deno.env.get("SUPABASE_URL")!,
      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
    )

    const { data: userData, error: fetchError } = await supabase
      .from("users")
      .select("total_score, fast_answers, medium_answers, slow_answers, total_games")
      .eq("name", name)
      .single()

    if (fetchError || !userData) {
      return new Response(JSON.stringify({ 
        success: false, 
        message: "❌ User not found" 
      }), { headers: { ...corsHeaders, "Content-Type": "application/json" } })
    }

    const newTotalScore    = (userData.total_score || 0) + finalScore
    const newFastAnswers   = (userData.fast_answers || 0) + fastAnswers
    const newMediumAnswers = (userData.medium_answers || 0) + mediumAnswers
    const newSlowAnswers   = (userData.slow_answers || 0) + slowAnswers
    const totalAnswers     = newFastAnswers + newMediumAnswers + newSlowAnswers
    const overallAccuracy  = totalAnswers > 0
      ?  ((newFastAnswers /totalAnswers)*100)*0.5+
        ((newMediumAnswers / totalAnswers)*100)*0.3+
        ((newSlowAnswers / totalAnswers)*100)*0.2
      : 0
    const  overallIQ = totalGames > 0
      ? Math.round(100+((newFastAnswers*6.5+newMediumAnswers*5+newSlowAnswers*3.5)/ (100*totalGames)-0.5)*60)
      : 0

    const { error: updateError } = await supabase
      .from("users")
      .update({
        total_score:    newTotalScore,
        fast_answers:   newFastAnswers,
        medium_answers: newMediumAnswers,
        slow_answers:   newSlowAnswers,
        total_games:    totalGames,
        avg_accuracy:       overallAccuracy,
        total_answers:  totalAnswers,
        avg_iq: overallIQ
      })
      .eq("name", name)

    if (updateError) {
      return new Response(JSON.stringify({ 
        success: false, 
        message: updateError.message 
      }), { headers: { ...corsHeaders, "Content-Type": "application/json" } })
    }

    return new Response(JSON.stringify({ 
      success: true,
      newTotalScore,
      overallAccuracy,
      overallIQ
    }), { headers: { ...corsHeaders, "Content-Type": "application/json" } })

  } catch (err) {
    return new Response(JSON.stringify({ 
      success: false, 
      message: err.message 
    }), { headers: { ...corsHeaders, "Content-Type": "application/json" } })
  }
})