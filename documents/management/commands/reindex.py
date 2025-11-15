from django.core.management.base import BaseCommand
from documents.models import Document
from documents.search_index import index_document

class Command(BaseCommand):
    help = "Reindex all existing documents into Whoosh"

    def handle(self, *args, **kwargs):
        print("Reindexing all documents...")

        docs = Document.objects.all()

        for doc in docs:
            try:
                index_document(
                    doc_id=doc.id,
                    title=doc.title,
                    content=doc.content or "",
                    path=doc.file.path if doc.file else "",
                )
                print(f"Indexed: {doc.title}")
            except Exception as e:
                print(f"Error indexing {doc.title}: {e}")

        print("Reindex complete!")
