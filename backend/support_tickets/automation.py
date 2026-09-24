def classify_ticket(message):
    text = message.lower()

    # Category detection
    if any(word in text for word in [
        "payment", "paid", "deducted", "transaction"
    ]):
        category = "payment"

    elif any(word in text for word in [
        "login", "password", "sign in", "signin"
    ]):
        category = "login"

    elif any(word in text for word in [
        "refund", "money back", "refund amount"
    ]):
        category = "refund"

    elif any(word in text for word in [
        "delivery", "delivered", "shipping", "order"
    ]):
        category = "delivery"

    elif any(word in text for word in [
        "account", "profile", "username"
    ]):
        category = "account"

    elif any(word in text for word in [
        "error", "bug", "crash", "not working"
    ]):
        category = "technical"

    else:
        category = "other"

    # Urgency detection
    if any(word in text for word in [
        "urgent",
        "urgently",
        "immediately",
        "critical",
        "emergency",
        "failed",
        "deducted",
        "blocked",
        "locked",
        "fraud",
        "cannot access",
        "not received"
    ]):
        urgency = "high"

    elif any(word in text for word in [
        "soon",
        "quickly",
        "important",
        "delay",
        "waiting"
    ]):
        urgency = "medium"

    else:
        urgency = "low"

    return category, urgency