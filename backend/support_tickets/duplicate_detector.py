from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .models import Ticket


def find_duplicate_ticket(message, current_ticket_id=None):
    """
    Compare a new ticket message with existing tickets
    and return the most similar ticket.
    """

    tickets = Ticket.objects.all()

    if current_ticket_id:
        tickets = tickets.exclude(id=current_ticket_id)

    if not tickets.exists():
        return None

    existing_tickets = list(tickets)

    messages = [ticket.message for ticket in existing_tickets]

    # Add the new message to the documents
    documents = messages + [message]

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english"
    )

    tfidf_matrix = vectorizer.fit_transform(documents)

    similarities = cosine_similarity(
        tfidf_matrix[-1],
        tfidf_matrix[:-1]
    )[0]

    if len(similarities) == 0:
        return None

    best_index = similarities.argmax()
    best_score = similarities[best_index]

    best_ticket = existing_tickets[best_index]

    similarity_percentage = round(
        best_score * 100,
        2
    )

    # Duplicate threshold
    if similarity_percentage >= 70:
        return {
            "is_duplicate": True,
            "ticket_id": best_ticket.id,
            "similarity": similarity_percentage,
        }

    return {
        "is_duplicate": False,
        "ticket_id": best_ticket.id,
        "similarity": similarity_percentage,
    }