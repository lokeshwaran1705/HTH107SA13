def calculate_frustration(message):
    text = message.lower()

    score = 0
    reasons = []

    # Negative / frustration words
    negative_words = [
        "angry",
        "frustrated",
        "terrible",
        "worst",
        "useless",
        "disappointed",
        "unacceptable",
        "ridiculous",
        "annoyed",
        "bad",
    ]

    # Repeated-contact words
    repeat_words = [
        "again",
        "already contacted",
        "already reported",
        "multiple times",
        "three times",
        "several times",
        "still not",
        "still haven't",
    ]

    # Urgency / pressure words
    urgency_words = [
        "urgent",
        "urgently",
        "immediately",
        "asap",
        "critical",
        "emergency",
        "cannot wait",
        "need this now",
    ]

    # Complaint indicators
    complaint_words = [
        "no response",
        "nobody helped",
        "not solved",
        "not fixed",
        "waiting",
        "delay",
        "wasting my time",
    ]

    negative_count = sum(
        1 for word in negative_words if word in text
    )

    repeat_count = sum(
        1 for word in repeat_words if word in text
    )

    urgency_count = sum(
        1 for word in urgency_words if word in text
    )

    complaint_count = sum(
        1 for word in complaint_words if word in text
    )

    # Score calculation
    score += min(negative_count * 15, 30)
    score += min(repeat_count * 20, 25)
    score += min(urgency_count * 10, 20)
    score += min(complaint_count * 10, 20)

    # Excessive punctuation
    if "!!!" in message:
        score += 5
        reasons.append("Excessive punctuation")

    # Keep score between 0 and 100
    score = min(score, 100)

    # Determine level
    if score >= 80:
        level = "critical"
    elif score >= 60:
        level = "high"
    elif score >= 30:
        level = "medium"
    else:
        level = "low"

    if negative_count:
        reasons.append("Negative language")

    if repeat_count:
        reasons.append("Repeated contact")

    if urgency_count:
        reasons.append("Urgent language")

    if complaint_count:
        reasons.append("Unresolved complaint")

    return {
        "score": score,
        "level": level,
        "reasons": reasons,
    }