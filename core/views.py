from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from core.forms import UploadFileForm
from core.models import Ruc, CargaRuc
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, Spacer, TableStyle
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from core.functions import timSort, quicksort
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import pandas as pd


def index(request):
    template_name = 'core/index.html'
    historial_cargas = CargaRuc.objects.all().order_by('-fecha_carga')[:10]
    return render(request, template_name, {'historial_cargas': historial_cargas})



def upload_ruc(request):
    template_name = 'core/upload.html'
    form = UploadFileForm(request.POST or None)
    
    if request.POST:
        form= UploadFileForm(request.POST, request.FILES)
        print('post recibido', request.POST)
        print('archivo recibido', request.FILES)
        if form.is_valid():
            print('form valido')
            try:
                uploaded_file = request.FILES['file']
                uploaded_file.seek(0)
                try:
                    df = pd.read_csv(uploaded_file, sep = '|',encoding = 'latin1', header= None)
                except Exception as e:
                    print(f"error reading file with '|': {e}")
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, sep = '\t',encoding = 'latin1', header= None)
                
                df = df.dropna(how='all')
                df = df[df[0].notna() & df[1].notna() & df[2].notna() & df[3].notna()]
                df = df.head(50)
                print(df)
                for _, row in df.iterrows():
                    if len(row) >= 4:
                        Ruc.objects.create(
                            documento = str(row[0]).strip(),
                            nombre = str(row[1]).strip(),
                            codigo = str(row[2]).strip(),
                            clave = str(row[3]).strip()
                        )
                    else:
                        print(f"ignored row for invalid format: {row}")
                CargaRuc.objects.create(name_arc = uploaded_file.name, registros= df.shape[0])
                messages.success(request, 'file uploaded to database successfully!')
                return redirect('core:visualize_ruc')
            except Exception as e:
                print(e)
                messages.error(request, f'error uploading file {e}.')
    return render(request, template_name, {'form': form})    




def visualize_ruc(request):
    template_name = 'core/visualize_ruc.html'
    ruc_data = Ruc.objects.all()[:50]

    if request.POST.get('accion') == 'PDF':
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte_ruc.pdf"'
        buff = BytesIO()

        doc = SimpleDocTemplate(buff,
                                 pagesize=portrait(A4),
                                 rightMargin=60,
                                 leftMargin=60,
                                 topMargin=20,
                                 bottomMargin=45)
        
        doc.title = 'RUC PDF'

        
        styles = getSampleStyleSheet()
        text_center = styles['Normal']
        text_center.fontSize = 8
        text_center.leading = 10
        text_center.alignment = 1  

        text_right = styles['Normal']
        text_right.fontSize = 8
        text_right.leading = 8
        text_right.alignment = 2 

        text_left = styles['Normal']
        text_left.fontSize = 8
        text_left.leading = 8
        text_left.alignment = 0

       
        story = []

        title = Paragraph("Reporte de RUC", text_center)
        story.append(title)
        story.append(Spacer(1, 12))

        data = [['id','documento', 'nombre', 'codigo' , 'codigo']] 
        for ruc in ruc_data:
            data.append([ruc.id, ruc.documento, ruc.nombre, ruc.codigo, ruc.clave])  

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        story.append(table)

        doc.build(story)

        pdf = buff.getvalue()
        buff.close()
        response.write(pdf)
        return response

    return render(request, template_name, {'ruc_data': ruc_data})



def sort_ruc_timsort(request):
    template_name = 'core/visualize_ruc.html'
    ruc_data = Ruc.objects.all()[:50]

    nombres = [ruc.nombre for ruc in ruc_data]
    
    timSort(nombres)


    ruc_data_sorted = []
    
    for nombre in nombres:
        for ruc in ruc_data:
            if ruc.nombre == nombre:
                ruc_data_sorted.append(ruc)
                break


    return render(request, template_name, {'ruc_data':ruc_data_sorted})




def sort_quicksort(request):
    template_name = 'core/visualize_ruc.html'
    ruc_data = Ruc.objects.all()[:50]
    
    nombres = [str(ruc.nombre) for ruc in ruc_data]
    
    quicksort(nombres,0 , len(nombres)-1)
    
    ruc_data_sorted = []
    
    for nombre in nombres:
        for ruc in ruc_data:
            if ruc.nombre == nombre:
                ruc_data_sorted.append(ruc)
                break
    return render(request, template_name, {'ruc_data': ruc_data_sorted})