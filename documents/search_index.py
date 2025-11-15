import os
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from django.conf import settings

# Where index directory will be stored
INDEX_DIR = os.path.join(settings.BASE_DIR, "documents", "search_index", "indexdir")

# -----------------------------
# DEFINE SCHEMA
# -----------------------------
schema = Schema(
    doc_id=ID(stored=True, unique=True),
    title=TEXT(stored=True),
    content=TEXT(stored=True),
    path=ID(stored=True)
)

# -----------------------------
# GET OR CREATE INDEX
# -----------------------------
def get_or_create_index():
    """Creates index if it does not exist."""
    if not os.path.exists(INDEX_DIR):
        os.makedirs(INDEX_DIR)

    # If directory is empty → create new index
    if not os.listdir(INDEX_DIR):
        return create_in(INDEX_DIR, schema)

    # Otherwise open existing index
    return open_dir(INDEX_DIR)

# -----------------------------
# INDEX DOCUMENT
# -----------------------------
def index_document(doc_id, title, content, path):
    ix = get_or_create_index()
    writer = ix.writer()

    writer.update_document(
        doc_id=str(doc_id),
        title=title,
        content=content,
        path=path
    )

    writer.commit()

# -----------------------------
# SEARCH DOCUMENTS (TITLE × CONTENT)
# -----------------------------
def search_documents(query):
    ix = get_or_create_index()
    results_list = []

    from whoosh.qparser import MultifieldParser

    with ix.searcher() as searcher:
        parser = MultifieldParser(["title", "content"], schema=ix.schema)
        q = parser.parse(query)

        results = searcher.search(q, limit=20)

        for r in results:
            results_list.append({
                "id": r["doc_id"],
                "title": r["title"],
                "content": r["content"],
                "path": r["path"]
            })

    return results_list
