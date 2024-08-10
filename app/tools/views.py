from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .forms import DataProcessingForm
import pandas as pd
from .utils import get_sheet_names, get_all_brands, get_column_names, process_and_export_data
import tempfile
import os

def process_excel_data(request):
    if request.method == 'POST':
        form = DataProcessingForm(request.POST, request.FILES)

        input_file = request.FILES['input_filename']
        form.fields['sheet_name'].choices = [(sheet, sheet) for sheet in get_sheet_names(input_file)]
        form.fields['brand'].choices = [(brand, brand) for brand in get_all_brands(input_file)]
        form.fields['column'].choices = [(col, col) for col in get_column_names(input_file)]

        if form.is_valid():
            print(form.cleaned_data)
            input_file = request.FILES['input_filename']
            output_filename = form.cleaned_data['output_filename']
            sheet_names = form.cleaned_data['sheet_name']
            brands = form.cleaned_data['brand']
            columns = form.cleaned_data['column']

            # Tạo tệp tạm thời để lưu kết quả
            with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                output_file_path = tmp_file.name



            # try:
            process_and_export_data(
                input_file,
                output_file_path,
                columns,
                sheet_names,
                brands
            )

            # Đọc tệp kết quả và trả về cho người dùng
            with open(output_file_path, 'rb') as file:
                response = HttpResponse(file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = f'attachment; filename="{output_filename}"'

            # Xóa tệp tạm sau khi đã gửi
            os.unlink(output_file_path)

            return response
            # except Exception as e:
            #     return JsonResponse({'error': str(e)}, status=400)
    else:
        form = DataProcessingForm()

    return render(request, "tools_template/export_data_excel.html", {'form': form})


def get_file_data(request):
    if request.method == 'POST' and request.FILES:
        form = DataProcessingForm()
        input_file = request.FILES['input_filename']
        sheets_choices = [(sheet, sheet) for sheet in get_sheet_names(input_file)]
        brands_choices = [(brand, brand) for brand in get_all_brands(input_file)]
        columns_choices = [(col, col) for col in get_column_names(input_file)]

        data = {
            'sheets_choices': sheets_choices,
            'brands_choices': brands_choices,
            'columns_choices': columns_choices
        }

        return JsonResponse(data)
    return JsonResponse({'error': 'Invalid request'}, status=400)
