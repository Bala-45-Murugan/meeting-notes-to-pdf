import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.pdf_generator import generate_pdf

data = {
    "title": "Quarterly Product Review",
    "date": "2026-08-31",
    "attendees": ["Alice", "Bob", "Carol"],
    "summary": "The team reviewed quarterly progress, approved the new roadmap, and assigned owners for Q3 milestones.",
    "discussion_points": [
        "Strong growth in user adoption, up 25% quarter over quarter.",
        "Server costs exceeded budget due to increased traffic.",
        "Feedback survey showed high satisfaction with new UI.",
    ],
    "decisions": [
        "Approve the Q3 product roadmap.",
        "Move to a scalable hosting plan to manage costs.",
    ],
    "action_items": [
        "Alice: Draft the new pricing page by Friday.",
        "Bob: Prepare cost optimization report.",
        "Carol: Schedule beta test for the onboarding flow.",
    ],
    "next_steps": [
        "Review beta test results in two weeks.",
        "Present roadmap to leadership next Monday.",
    ],
}

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_output.pdf")
generate_pdf(data, out)
print("PDF generated successfully:", out)
