from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import Document
from .serializers import DocumentSerializer
from .utils import extract_text

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_document(request):
    if 'file' not in request.FILES:
        return Response({'error':'No file provided'}, status=400)
    f = request.FILES['file']
    doc = Document.objects.create(title=f.name, file=f)
    # extract text
    try:
        file_path = doc.file.path
        text = extract_text(file_path)
        doc.content = text
        doc.save()
    except Exception:
        pass
    return Response(DocumentSerializer(doc).data)

@api_view(['GET'])
def search_documents(request):
    q = request.GET.get('q','').strip()
    if not q:
        docs = Document.objects.order_by('-uploaded_at')[:20]
    else:
        docs = Document.objects.filter(content__icontains=q).order_by('-uploaded_at')[:50]
    data = DocumentSerializer(docs, many=True).data
    # include snippet
    for item in data:
        item['snippet'] = (item.get('content') or '')[:300].replace('\n',' ')
    return Response(data)
