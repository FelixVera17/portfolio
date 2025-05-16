from django.shortcuts import render, redirect
from django.contrib import messages
from core.forms import UploadFileForm
from core.models import Ruc, CargaRuc
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

    return render(request, template_name, {'ruc_data': ruc_data})






