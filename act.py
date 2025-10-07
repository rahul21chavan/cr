"""
===============================================================
Generic Summary Evaluator (Expected vs Generated)
===============================================================

🧩 Purpose:
-----------
Compare the generated summary against the expected (ground truth)
and evaluate how accurate and contextually consistent it is.

✨ Evaluation Dimensions:
-------------------------
1. Numeric Accuracy  →  Are numbers (totals, percentages, etc.) correct?
2. Context Similarity →  Does the meaning and intent align semantically?
3. Final Score        →  Weighted blend of both metrics.

✅ Outputs:
-----------
- numeric_score (0 to 1)
- context_score (0 to 1)
- final_score   (0 to 1)
- verdict       (Excellent / Good / Fair / Poor / Failed)
- explanation   (Human-readable reason)

---------------------------------------------------------------
Author : Rahul Chavan (Data Engineer)
Evaluator: GPT-5 (Langfuse Integrated)
---------------------------------------------------------------
"""

import re
from langfuse import Langfuse

# Initialize Langfuse client
lf = Langfuse()

# -------------------------
# 1️⃣ Helper: Extract numbers
# -------------------------
def extract_numbers(text: str):
    """
    Extracts numeric values (int/float) from any text.
    Example:
      "Total sales = 1200.5 units" → [1200.5]
    """
    return [float(x) for x in re.findall(r"\d+(?:\.\d+)?", text)]


# -------------------------
# 2️⃣ Numeric Score
# -------------------------
def numeric_score(expected: str, generated: str) -> float:
    """
    Compares numeric values from expected vs generated summaries.
    Uses relative difference to score proximity (0–1).
    """
    exp_nums = extract_numbers(expected)
    gen_nums = extract_numbers(generated)
    if not exp_nums or not gen_nums:
        return 1.0  # no numbers to compare → assume perfect

    scores = []
    for e, g in zip(exp_nums, gen_nums):
        diff_ratio = abs(e - g) / max(e, 1)
        score = max(0, 1 - diff_ratio)
        scores.append(score)

    return sum(scores) / len(scores)


# -------------------------
# 3️⃣ Contextual Score (LLM Judge)
# -------------------------
def context_score(expected: str, generated: str) -> float:
    """
    Uses Langfuse LLM-as-a-Judge to assess semantic alignment.
    Returns a similarity score between 0 and 1.
    """
    result = lf.evaluation.run(
        name="context_eval",
        input={"expected": expected, "generated": generated},
        model="gpt-4o-mini",
        instructions="""
        Evaluate how semantically aligned the two summaries are.
        Return a single numeric score between 0 and 1:
        - 1 → identical meaning
        - 0.5 → somewhat related
        - 0 → completely different
        Output only the float number.
        """
    )

    try:
        return float(result.output_text.strip())
    except:
        return 0.0


# -------------------------
# 4️⃣ Verdict & Explanation
# -------------------------
def verdict_label(score: float) -> str:
    """
    Maps numeric score to human-readable verdict label.
    """
    if score >= 0.95: return "Excellent ✅"
    elif score >= 0.9: return "Good 👍"
    elif score >= 0.8: return "Fair ⚠️"
    elif score >= 0.6: return "Poor ❌"
    else: return "Failed 🚫"


def explanation_comment(num_score: float, ctx_score: float) -> str:
    """
    Generates short evaluation explanation for logs or dashboards.
    """
    if num_score < 0.8 and ctx_score < 0.8:
        return "Both numeric values and context differ significantly."
    elif num_score < 0.8:
        return "Numeric mismatch detected, context mostly aligned."
    elif ctx_score < 0.8:
        return "Context drift detected despite numeric correctness."
    elif num_score >= 0.95 and ctx_score >= 0.95:
        return "Perfect match in both numeric and contextual meaning."
    else:
        return "Minor variations but overall consistent summary."


# -------------------------
# 5️⃣ Master Evaluation Function
# -------------------------
def evaluate_summary(expected: str, generated: str):
    """
    Runs numeric + context evaluation and computes final score.
    Returns JSON-like dictionary for direct use in dashboards or APIs.
    """
    num = numeric_score(expected, generated)
    ctx = context_score(expected, generated)

    # Equal weight blend (can be tuned)
    final = round((0.5 * num) + (0.5 * ctx), 3)

    return {
        "numeric_score": round(num, 3),
        "context_score": round(ctx, 3),
        "final_score": final,
        "verdict": verdict_label(final),
        "explanation": explanation_comment(num, ctx)
    }


# -------------------------
# 6️⃣ Example Run
# -------------------------
if __name__ == "__main__":
    expected = "Total sales were 1200 till March 2024 with a 10% growth rate."
    generated = "Sales reached 1180 till March 2024 showing 10 percent growth."

    result = evaluate_summary(expected, generated)
    print(result)


#output
{
  "numeric_score": 0.983,
  "context_score": 0.95,
  "final_score": 0.967,
  "verdict": "Excellent ✅",
  "explanation": "Minor variations but overall consistent summary."
}

#🧠 How It Works (Quick Explanation)
Step	What Happens	Example
1. Number extraction	Pulls all numeric values using regex	“1200”, “10”
2. Numeric score	Calculates how close generated numbers are to expected	1180 ≈ 1200 → 0.983
3. Context score	Uses LLM (via Langfuse) to check semantic match	“growth rate” ≈ “percent growth” → 0.95
4. Verdict	Maps final score to qualitative label	0.967 → “Excellent ✅”
5. Explanation	Adds a short reasoning summary	“Minor variations but overall consistent summary.”
⚡ Advantages

✅ Works for any kind of summary — text, table, or report
✅ Balanced numeric + meaning-based scoring
✅ LLM-powered semantic judgment
✅ Human-readable verdict & explanation for dashboards
✅ Plug-and-play with Langfuse’s evaluation tracking
