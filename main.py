import openai
import random
import time
import threading

client = openai.OpenAI(
    base_url="http://10.0.0.188:8080/v1",
    api_key="not-needed",
)

# -------- CONFIG --------
MODEL = "asdf"
ROUNDS = 30
SCORING_INTERVAL = 10

POLITICAL_FIGURES = [
    "Gavin Newsom",
    "Nikki Haley",
    "Ron DeSantis",
    "Kamala Harris",
    "Donald Trump",
    "AOC",
    "J.D. Vance",
    "Greg Abbott",
    "Bernie Sanders",
    "Kristi Noem",
    "Hakeem Jeffries",
    "Mike Johnson",
    "Elon Musk"
]

# ----------------------------------------
# INITIAL WORLD STATE
# ----------------------------------------
world_state = """It is the current moment in American politics.
It is the present moment in American politics, months before the 2026 midterms. The national atmosphere is tense, reactive, and hypersensitive to narrative swings. Immigration dominates the news in a way that angers everyone for opposite reasons: the right is furious that despite constant headlines about crimes by undocumented immigrants, the President hasn’t executed the mass deportations he once promised, while the left is equally furious that any deportations continue at all, calling them immoral and discriminatory. Border agents leak stories of overwhelmed facilities; activists leak stories of nighttime removals; neither side believes the numbers DHS reports. AI and tech issues create a different kind of polarization: one camp insists that AI layoffs signal a coming societal collapse and the quiet end of human labor, while another insists AI is a hype-fueled smokescreen used by tech firms to justify firing employees and inflating valuations. Congress cannot agree on even a basic regulatory framework. At the same time, a wave of resentment is forming against AI-driven workplace monitoring and algorithmic firings, adding economic anxiety to technological fear.

Urban politics have taken an unexpected turn after New York City elected an openly socialist mayor backed by tenant unions, gig workers, and young voters disillusioned with the political establishment. This victory shocked both parties: progressives celebrate it as proof that materialist politics can win, while moderates warn it will alienate suburban swing voters. Republicans point to it as evidence of “left-wing extremism,” but privately acknowledge confusion about how to run against a candidate who is both a socialist and pro-policing. Meanwhile, the right is fracturing internally over foreign policy—especially unconditional support for Israel. Older GOP leadership remains firmly aligned with traditional pro-Israel positions, but a rapidly growing cohort of young right-wing creators and activists is challenging this, arguing for restraint and a focus on domestic issues. This has triggered a genuine generational rift inside the right’s coalition.

The left is no less divided: progressives push for sweeping climate policy, rent control, and wealth redistribution, while moderates warn these proposals are electoral suicide. Labor unions clash with environmental groups over energy infrastructure; young activists distrust party leadership; and much of the coalition holds together more through shared opposition to Republicans than through coherent strategy. Media ecosystems intensify all divisions: social platforms are swamped with deepfakes, hyper-personalized misinformation, ideological influencers, and rapidly mutating outrage loops. Legacy media still shapes narratives but is weaker than ever, while independent online creators increasingly determine daily political mood swings.

Economically, headline inflation is supposedly “under control,” but voters do not feel relief: housing is crushingly expensive, insurance premiums keep rising, groceries and utilities feel permanently inflated, and younger generations increasingly view the system as rigged for those who already own assets. The macro numbers say stability; public sentiment says crisis. Overall, the political environment is unstable, low-trust, and primed for disruption. Small events can cause outsized political shifts, coalitions are brittle, and narrative momentum is everything.
"""

# ----------------------------------------
# RANDOM PLAYER ASSIGNMENTS
# ----------------------------------------
playerA = random.choice(POLITICAL_FIGURES)
remaining = [p for p in POLITICAL_FIGURES if p != playerA]
playerB = random.choice(remaining)

print(f"Player A: {playerA}")
print(f"Player B: {playerB}")
print("--------------------------------------------------------")


# ----------------------------------------
# PLAYER PROMPTS
# ----------------------------------------
def player_prompt(person, world):
    return f"""
You are {person}. You are attempting to increase your influence in current U.S. politics.

Given the current world state, output ONE concrete political move in ONE concise sentence.

Do NOT explain yourself.
Do NOT add commentary.
Do NOT discuss the opponent.
Just output an action like:
- "I leak internal polling showing..."
- "I launch a national tour focused on..."
- "I quietly meet with..."
- "I coordinate a media hit against..."
- "I pressure a key committee to..."

WORLD STATE:
{world}
"""


# ----------------------------------------
# Dungeon Master PROMPT
# ----------------------------------------
def dm_prompt(world, person, action):
    return f"""
Below is the current U.S. political landscape.

WORLD STATE:
{world}

ACTION TAKEN BY {person}:
{action}

You are a D&D-style Dungeon Master, but you are reactive, not proactive (you don't have an agenda, you're just trying to deduce likely outcomes).
Describe the immediate political consequences in U.S. politics in 3–5 sentences.
Update the world state realistically and organically.
Do NOT mention that this is a game.
Do NOT mention opponents or turns.
Just apply normal political cause-and-effect.
"""


# ----------------------------------------
# JUDGE PROMPT
# ----------------------------------------
def judge_prompt(world, A, B):
    return f"""
Here is the evolving U.S. political landscape:

{world}

Two political figures have been acting: {A} and {B}.

Based solely on the political consequences described in the world state,
which figure appears to have gained broader political advantage so far?

Choose ONLY one: "{A}" or "{B}"

Explain in 2–3 sentences.
"""


# ----------------------------------------
# API helper
# ----------------------------------------
def ask(prompt):
    r = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.7,
    )
    return r.choices[0].message.content.strip()


# ----------------------------------------
# Turn: collect player moves, race the responses
# ----------------------------------------
def get_first_response(person, world, results, key):
    action = ask(player_prompt(person, world))
    results[key] = action


def race_players(world):
    results = {}
    threads = []

    tA = threading.Thread(target=get_first_response, args=(playerA, world, results, "A"))
    tB = threading.Thread(target=get_first_response, args=(playerB, world, results, "B"))

    tA.start(); tB.start()

    # Poll for first completion
    while True:
        if "A" in results:
            return playerA, results["A"]
        if "B" in results:
            return playerB, results["B"]
        time.sleep(0.01)


# ----------------------------------------
# MAIN LOOP
# ----------------------------------------
for round_num in range(1, ROUNDS + 1):
    print(f"\n=== ROUND {round_num} ===")

    # Race the players
    winner, action = race_players(world_state)
    print(f"{winner} acted first:")
    print(f"  {action}")

    # DM updates the world
    world_state = ask(dm_prompt(world_state, winner, action))
    print("\n--- Updated World State ---")
    print(world_state)

    # Scoring interval
    if round_num % SCORING_INTERVAL == 0:
        print("\n=== SCORE CHECK ===")
        score = ask(judge_prompt(world_state, playerA, playerB))
        print(score)
        print("====================")

print("\nSimulation complete.")
