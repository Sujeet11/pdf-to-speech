from django.shortcuts import render
from .forms import PDFUploadForm
import PyPDF2
import os
from django.conf import settings

def upload_pdf(request):
    message = ""
    text = ""
    
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES['pdf_file']
            page_number = form.cleaned_data['page_number'] - 1  # 0-indexed

            # Save uploaded file
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            saved_path = os.path.join(settings.MEDIA_ROOT, pdf_file.name)

            with open(saved_path, 'wb+') as destination:
                for chunk in pdf_file.chunks():
                    destination.write(chunk)

            try:
                with open(saved_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    if 0 <= page_number < len(reader.pages):
                        text = reader.pages[page_number].extract_text()
                        if text:
                            message = "✅ Text extracted successfully!"
                        else:
                            message = "⚠️ No text found on that page."
                    else:
                        message = "❌ Invalid page number."
            except Exception as e:
                message = f"❌ Error: {str(e)}"
    else:
        form = PDFUploadForm()

    return render(request, 'reader/upload.html', {
        'form': form,
        'message': message,
        'text': text
    })
