"""
Skill: Theme vs Topic (Grades 6 to 8)

What this is:
- A small rule-based engine that simulates adaptive tutoring:
  prompt -> score -> AI response -> reprompt -> mastery check
"""

PASSAGE = (
    "Maya started bringing extra sandwiches to school. At first she said they were "
    "“just in case,” but soon she began placing them quietly on the corner table near the window. "
    "One day she noticed the new student, Eli, always sat there with an empty tray. "
    "Maya pretended not to see him watching the sandwiches, but the next day the extra food disappeared."
)

EXPECTED_TOPICS = ["kindness", "sharing", "helping", "new student", "inclusion", "generosity"]

AI_RESPONSES = {
    0: "That’s a summary. A theme is a general message. Try starting with 'Sometimes…' or "
       "'People should…' without using names.",
    1: "Good start. Now point to one detail from the text that supports your message.",
    2: "Great. Now rewrite the theme in different words or find another detail that supports it."
}

NAMES = {"maya", "eli"}


def normalize(s: str) -> str:
    return " ".join(s.strip().lower().split())


def score_topic(answer: str) -> int:
    """
    Simple scoring for topic:
    2 = includes a reasonable topic keyword or short noun phrase
    1 = plausible but vague
    0 = empty / nonsense
    """
    a = normalize(answer)
    if not a:
        return 0
    if any(k in a for k in EXPECTED_TOPICS):
        return 2
    if len(a.split()) <= 6:
        return 1
    return 1


def score_theme(theme: str, evidence: str) -> int:
    """
    Score 0: plot summary / overly specific (names or event retell)
    Score 1: general message but vague OR missing evidence
    Score 2: general life message + evidence detail
    """
    t = normalize(theme)
    e = normalize(evidence)

    if not t:
        return 0

    # Score 0 signals (summary/overly specific)
    if any(name in t for name in NAMES):
        return 0

    summary_signals = ["brings", "gives", "leaves", "disappears", "sandwich", "tray", "table", "window"]
    if sum(1 for w in summary_signals if w in t) >= 2:
        return 0

    # Now it's at least "general-ish"
    # Evidence required for Score 2
    if not e:
        return 1

    # Evidence quality: does it reference a concrete detail from passage?
    evidence_hits = 0
    for w in ["sandwich", "sandwiches", "tray", "table", "window", "extra", "disappeared", "new student"]:
        if w in e:
            evidence_hits += 1

    # Theme quality: encourage general statements
    general_starters = ["sometimes", "people", "we", "small", "acts", "kindness", "helping", "included", "include"]
    general_hits = sum(1 for w in general_starters if w in t)

    if evidence_hits >= 1 and general_hits >= 1 and len(t.split()) >= 6:
        return 2

    return 1


def run():
    print("\n=== Adaptive ELA Lesson: Theme vs Topic (Prototype) ===\n")
    print("PASSAGE:\n")
    print(PASSAGE)
    print("\n---\n")

    # Prompt 1: Topic
    topic = input("Prompt 1 (Topic): In one sentence, what is the topic of the passage?\n> ")
    topic_score = score_topic(topic)

    if topic_score == 0:
        print("\nAI response: Give it a try—name the general subject (e.g., kindness, helping others, a new student).")
        topic = input("> ")
        topic_score = score_topic(topic)

    print(f"\nAI response: Topic recorded. (score={topic_score})\n")

    # Prompt 2: Theme with adaptation
    attempts = 0
    max_attempts = 2  # metric: reach score 2 within two attempts

    theme = ""
    evidence = ""

    while attempts < max_attempts:
        attempts += 1
        print("Prompt 2 (Theme): What message does the story suggest about people or life?")
        theme = input("> ")

        print("Now add ONE detail from the text that supports your theme (evidence).")
        evidence = input("> ")

        s = score_theme(theme, evidence)

        print(f"\n--- AI RESPONSE (attempt {attempts}/{max_attempts}) ---")
        print(f"Score: {s}")
        print("AI response:", AI_RESPONSES[s])

        if s == 2:
            break

        # Extra targeted reprompting (still labeled as AI responses)
        if s == 0:
            print("\nAI response: Sentence starter: 'Sometimes people...' or 'People should...' (no names). Try again.\n")
        elif s == 1:
            print("\nAI response: Make the theme more specific and general (no plot), then connect it to a concrete detail.\n")

        print("---\n")

    # Mastery check / exit ticket
    print("\n=== Exit Ticket (Mastery Check) ===")
    print("AI response: Write one sentence stating the theme and include one detail that supports it.")
    exit_ticket = input("> ")

    print("\n=== Summary (Telemetry) ===")
    print(f"- Attempts: {attempts}")
    print("- Reached Score 2 within two attempts:", "YES" if score_theme(theme, evidence) == 2 else "NO")
    print("- Topic entered:", topic.strip() or "(blank)")
    print("- Exit ticket captured:", "YES" if exit_ticket.strip() else "NO")
    print("\nDone.\n")


if __name__ == "__main__":
    run()
