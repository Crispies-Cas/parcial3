import os
import numpy as np
import pydicom
import matplotlib.pyplot as plt

archivos_dicom = {}  # Diccionario global para guardar volumenes 

def cargar_dicom():
    ruta = input("Suba la ruta de la carpeta con los archivos DICOM: ").strip()

    # Verifica si la ruta existe
    if not os.path.isdir(ruta):
        print("Ruta invalida.")
        return

    archivos = [os.path.join(ruta, f) for f in os.listdir(ruta) if f.endswith(".dcm")]

    if not archivos:
        print("No se encontraron archivos DICOM.")
        return

    slices = [pydicom.dcmread(f) for f in sorted(archivos)]
    volumen = np.stack([s.pixel_array for s in slices])

    fig, eje = plt.subplots(1, 3, figsize=(15, 5))

    eje[0].imshow(volumen[volumen.shape[0] // 2], cmap='gray')
    eje[0].set_title('Axial')

    eje[1].imshow(volumen[:, volumen.shape[1] // 2, :], cmap='gray')
    eje[1].set_title('Coronal')

    eje[2].imshow(volumen[:, :, volumen.shape[2] // 2], cmap='gray')
    eje[2].set_title('Sagital')

    for ax in eje:
        ax.axis("off")

    plt.tight_layout()
    plt.show()

    clave = input("Ingrese una clave para guardar este volumen: ").strip()
    archivos_dicom[clave] = volumen
    print("Volumen guardado exitosamente con la clave:", clave) 


cargar_dicom()