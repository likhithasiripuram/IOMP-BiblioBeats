from sqlalchemy import create_engine, MetaData, Table, select, text
import ollama

def get_book_recommendations():
    # Connect to SQLite database
    engine = create_engine('sqlite:///test.db')
    metadata = MetaData()
    tracks_table = Table('track_table', metadata, autoload_with=engine)

    # Query 5 random tracks (name + album only)
    with engine.connect() as conn:
        stmt = (
            select(tracks_table.c.track_name, tracks_table.c.album_name)
            .order_by(text("RANDOM()"))
            .limit(5)
        )
        result = conn.execute(stmt)
        tracks = result.fetchall()

    # Format the 5 random tracks into a prompt string
    track_list = "\n".join([f"{i+1}. {row.track_name} from album '{row.album_name}'" for i, row in enumerate(tracks)])

    prompt = f"""Here are 5 randomly selected music tracks and their album names:

{track_list}

Suggest 5 book recommendations on the basis of these tracks."""

    response = ollama.chat(
        model="llama2",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['message']['content']