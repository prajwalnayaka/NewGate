from states import SharedState

def final_output_staging_node(state: SharedState):
    genres=state["genre"]
    articles=state["selected_articles"]
    statuses=state["branch_statuses"]
    final_output={}

    print(f"DEBUG: selected_articles:{articles}")

    for genre in genres:
        current_genre_article=[article for article in articles if article['genre'] == genre]
        current_genre_status=next((status['message'] for status in statuses if status['genre'] == genre), None)
        final_output[genre]={"articles":current_genre_article,"status":current_genre_status}

    return {"final_output":final_output}