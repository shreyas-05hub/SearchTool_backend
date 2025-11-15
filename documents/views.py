# from rest_framework.decorators import api_view, parser_classes
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework.response import Response
# from .models import Document
# from .serializers import DocumentSerializer
# from .utils import extract_text

# @api_view(['POST'])
# @parser_classes([MultiPartParser, FormParser])
# def upload_document(request):
#     if 'file' not in request.FILES:
#         return Response({'error':'No file provided'}, status=400)
#     f = request.FILES['file']
#     doc = Document.objects.create(title=f.name, file=f)
#     # extract text
#     try:
#         file_path = doc.file.path
#         text = extract_text(file_path)
#         doc.content = text
#         doc.save()
#     except Exception:
#         pass
#     return Response(DocumentSerializer(doc).data)

# @api_view(['GET'])
# def search_documents(request):
#     q = request.GET.get('q','').strip()
#     if not q:
#         docs = Document.objects.order_by('-uploaded_at')[:20]
#     else:
#         docs = Document.objects.filter(content__icontains=q).order_by('-uploaded_at')[:50]
#     data = DocumentSerializer(docs, many=True).data
#     # include snippet
#     for item in data:
#         item['snippet'] = (item.get('content') or '')[:300].replace('\n',' ')
#     return Response(data)


# from rest_framework.decorators import api_view, parser_classes
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework.response import Response
# from .models import Document
# from .serializers import DocumentSerializer
# from .utils import extract_text


# # ---------------------------------------------------------
# # MULTIPLE DOCUMENT UPLOAD
# # ---------------------------------------------------------
# @api_view(['POST'])
# @parser_classes([MultiPartParser, FormParser])
# def upload_documents(request):
#     """
#     Upload multiple PDF/DOCX/DOC files,
#     extract their text, and store in the database.
#     """
#     files = request.FILES.getlist("files")

#     if not files:
#         return Response({"error": "No files provided"}, status=400)

#     uploaded_docs = []

#     for f in files:
#         try:
#             # Save file
#             doc = Document.objects.create(title=f.name, file=f)

#             # Extract text content
#             try:
#                 text = extract_text(doc.file.path)
#                 doc.content = text
#                 doc.save()
#             except Exception as e:
#                 print("Text extraction failed:", e)

#             uploaded_docs.append(DocumentSerializer(doc).data)

#         except Exception as e:
#             print("File processing error:", e)
#             continue

#     return Response({"uploaded": uploaded_docs}, status=201)


# # ---------------------------------------------------------
# # SEARCH DOCUMENTS
# # ---------------------------------------------------------
# @api_view(['GET'])
# def search_documents(request):
#     q = request.GET.get('q', '').strip()

#     if not q:
#         docs = Document.objects.order_by('-uploaded_at')[:20]
#     else:
#         docs = Document.objects.filter(
#             content__icontains=q
#         ) | Document.objects.filter(
#             title__icontains=q
#         )

#     data = DocumentSerializer(docs, many=True).data

#     # add snippet
#     for item in data:
#         content = item.get("content") or ""
#         item["snippet"] = content[:300].replace("\n", " ")

#     return Response(data)


# from rest_framework.decorators import api_view, parser_classes
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework.response import Response

# from .models import Document
# from .serializers import DocumentSerializer
# from .utils import extract_text
# from .search_index import index_document, search_documents as es_search


# # ---------------------------------------------------------
# # MULTIPLE DOCUMENT UPLOAD  (WITH ELASTICSEARCH INDEXING)
# # ---------------------------------------------------------
# @api_view(['POST'])
# @parser_classes([MultiPartParser, FormParser])
# def upload_documents(request):
#     """
#     Upload multiple PDF/DOCX files,
#     extract text, save to DB, and index into Elasticsearch.
#     """
#     files = request.FILES.getlist("files")

#     if not files:
#         return Response({"error": "No files provided"}, status=400)

#     uploaded_docs = []

#     for f in files:
#         try:
#             # Save file to Django media folder
#             doc = Document.objects.create(title=f.name, file=f)

#             # Extract text
#             try:
#                 text = extract_text(doc.file.path)
#                 doc.content = text
#                 doc.save()
#             except Exception as e:
#                 print("Text extraction failed:", e)

#             # Index in Elasticsearch
#             try:
#                 index_document(
#                     doc.id,
#                     doc.title,
#                     doc.content or "",
#                     doc.file.path
#                 )
#             except Exception as e:
#                 print("Elasticsearch indexing failed:", e)

#             uploaded_docs.append(DocumentSerializer(doc).data)

#         except Exception as e:
#             print("File processing error:", e)
#             continue

#     return Response({"uploaded": uploaded_docs}, status=201)


# # ---------------------------------------------------------
# # SEARCH DOCUMENTS  (TITLE PRIORITY + FULL TEXT SEARCH)
# # ---------------------------------------------------------
# @api_view(['GET'])
# def search_documents(request):
#     q = request.GET.get("q", "").strip()

#     if not q:
#         # return last 20 uploaded
#         docs = Document.objects.order_by('-uploaded_at')[:20]
#         return Response(DocumentSerializer(docs, many=True).data)

#     # -----------------------------------------------------
#     # 1) Search in Elasticsearch (title boosted)
#     # -----------------------------------------------------
#     try:
#         hits = es_search(q)
#         ids = [hit["_id"] for hit in hits]

#         if ids:
#             docs = Document.objects.filter(id__in=ids)
#         else:
#             docs = []
#     except Exception as e:
#         print("Elasticsearch search failed → using fallback:", e)
#         docs = []

#     # -----------------------------------------------------
#     # 2) If ES returns nothing → fallback to Django Query
#     # -----------------------------------------------------
#     if not docs:
#         docs = Document.objects.filter(
#             title__icontains=q
#         ) | Document.objects.filter(
#             content__icontains=q
#         )

#     serialized = DocumentSerializer(docs, many=True).data

#     # Add snippet
#     for item in serialized:
#         content = item.get("content") or ""
#         item["snippet"] = content[:300].replace("\n", " ")

#     return Response(serialized)


from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from .models import Document
from .serializers import DocumentSerializer
from .utils import extract_text

# Replace ES with Whoosh
from .search_index import (
    index_document as whoosh_index,
    search_documents as whoosh_search
)


# ---------------------------------------------------------
# MULTIPLE DOCUMENT UPLOAD  (WHOOSH INDEXING)
# ---------------------------------------------------------
@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_documents(request):
    """
    Upload multiple PDF/DOCX files,
    extract text, save to DB, and index into Whoosh.
    """
    files = request.FILES.getlist("files")

    if not files:
        return Response({"error": "No files provided"}, status=400)

    uploaded_docs = []

    for f in files:
        try:
            # Save file in database + media folder
            doc = Document.objects.create(title=f.name, file=f)

            # Extract text from PDF/DOCX
            try:
                text = extract_text(doc.file.path)
                doc.content = text
                doc.save()
            except Exception as e:
                print("Text extraction failed:", e)
                doc.content = ""
                doc.save()

            # Index with Whoosh
            try:
                whoosh_index(
                    doc_id=str(doc.id),
                    title=doc.title,
                    content=doc.content,
                    path=doc.file.path
                )
            except Exception as e:
                print("Whoosh indexing failed:", e)

            uploaded_docs.append(DocumentSerializer(doc).data)

        except Exception as e:
            print("File processing error:", e)
            continue

    return Response({"uploaded": uploaded_docs}, status=201)


# ---------------------------------------------------------
# SEARCH DOCUMENTS (WHOOSH SEARCH)
# ---------------------------------------------------------
@api_view(['GET'])
def search_documents(request):
    q = request.GET.get("q", "").strip()

    # If no query → return latest 20 uploads
    if not q:
        docs = Document.objects.order_by("-uploaded_at")[:20]
        data = DocumentSerializer(docs, many=True).data

        for item in data:
            content = item.get("content", "")
            item["snippet"] = content[:300].replace("\n", " ")

        return Response(data)

    # Whoosh search
    results = whoosh_search(q)

    final = []
    for r in results:
        doc = Document.objects.filter(id=r["id"]).first()
        if doc:
            final.append({
                "id": doc.id,
                "title": doc.title,
                "content": doc.content,
                "snippet": (doc.content or "")[:300].replace("\n", " "),
                "uploaded_at": doc.uploaded_at
            })

    return Response(final)
