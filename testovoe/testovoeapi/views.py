from django.shortcuts import render

# Create your views here.
from rest_framework import serializers
from rest_framework import views, status
from rest_framework.response import Response
from .serializers import UploadedFileSerializer, SelectedMethodSerializer
import yaml
import json

from .models import UploadedFile, SelectedMethod


class UploadAPIFileView(views.APIView):

    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'Файла нет'}, status=status.HTTP_400_BAD_REQUEST)

        # Если не перезаписывать код
        existing_file = UploadedFile.objects.filter(uploaded_file=file.name).first()
        if existing_file:
            return Response({'error': 'Файл уже существует'}, status=status.HTTP_400_BAD_REQUEST)
        if not file:
            return Response({'error': 'Файла нет'}, status=status.HTTP_400_BAD_REQUEST)
        if file.name.endswith('.yaml') or file.name.endswith('.yml'):
            try:
                parsed_file = yaml.safe_load(file)
            except yaml.YAMLError as exc:
                return Response({'error': 'YAML ошибка'}, status=status.HTTP_400_BAD_REQUEST)
        elif file.name.endswith('.json'):
            try:
                parsed_file = json.load(file)
            except json.JSONDecodeError as exc:
                return Response({'error': 'JSON ошибка'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Неподдерживаемый формат'}, status=status.HTTP_400_BAD_REQUEST)
        api_methods = []

        for path, methods in parsed_file.get("paths", {}).items():
            for method_type, method_info in methods.items():
                description = method_info.get("description", "No description")
                api_method = {
                    "type": method_type,
                    "name": path,
                    "description": description
                }
                api_methods.append(api_method)

        uploaded_file_instance = UploadedFile.objects.create(uploaded_file=file.name, file_content=parsed_file)
        return Response(api_methods, status=status.HTTP_200_OK)


class SelectMethodsView(views.APIView):
    def post(self, request):
        selected_methods = request.data.get('selected_methods', [])

        for method_data in selected_methods:
            serializer = SelectedMethodSerializer(data=method_data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Методы успешно сохранены"}, status=status.HTTP_201_CREATED)


from django.shortcuts import render

# Create your views here.
