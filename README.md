Django backend for Knowledge Discovery project.
Setup:
1. Create virtualenv & activate
   python -m venv venv
   source venv/bin/activate  (Windows: venv\Scripts\activate)
2. Install requirements:
   pip install -r requirements.txt
3. Run migrations and start server:
   python manage.py migrate
   python manage.py runserver
4. Upload files via POST /api/upload/ (multipart form 'file')
5. Search via GET /api/search/?q=your+query
