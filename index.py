import os
import numpy as np
import pydicom
import matplotlib.pyplot as plt
import cv2

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
    pixel_spacing = [float(p) for p in slices[0].PixelSpacing]
    
    volumen = np.stack([s.pixel_array for s in slices])
    slice_thickness = float(slices[0].SliceThickness)

    fig, eje = plt.subplots(1, 3, figsize=(15, 5))
    

    eje[0].imshow(volumen[volumen.shape[0] // 2, :, :],cmap='gray',aspect=pixel_spacing[0] / pixel_spacing[1])
    eje[0].set_title("Axial")

    eje[1].imshow(volumen[:, volumen.shape[1] // 2, :],cmap='gray',aspect=slice_thickness / pixel_spacing[1])
    eje[1].set_title("Coronal")

    eje[2].imshow(volumen[:, :, volumen.shape[2] // 2],cmap='gray',aspect=slice_thickness / pixel_spacing[0])
    eje[2].set_title("Sagital")

    plt.tight_layout()
    plt.show()

    clave = input("Ingrese una clave para guardar este volumen: ").strip()
    archivos_dicom[clave] = volumen
    print("Volumen guardado exitosamente con la clave:", clave) 


def procesar_imagen_png_jpg():
    ruta = input("Ingrese la ruta de la imagen PNG o JPG: ").strip()
    if not os.path.isfile(ruta):
        print("Ruta invalida.")
        return

    imagen = cv2.imread(ruta, cv2.IMREAD_GRAYSCALE)
    if imagen is None:
        print("No se pudo leer la imagen.")
        return

    print("\nOpciones de binarizacion:")
    print("1. Binario")
    print("2. Binario invertido")
    print("3. Truncado")
    print("4. Tozero")
    print("5. Tozero invertido")
    opcion = int(input("Seleccione tipo de binarizacion (1-5): ").strip())
    umbral = int(input("Ingrese el umbral de binarizacion (0-255): ").strip())
    
    tipos = {
        1: cv2.THRESH_BINARY,
        2: cv2.THRESH_BINARY_INV,
        3: cv2.THRESH_TRUNC,
        4: cv2.THRESH_TOZERO,
        5: cv2.THRESH_TOZERO_INV
    }
    
    binarizada = cv2.threshold(imagen, umbral, 255, tipos.get(opcion, cv2.THRESH_BINARY))


# Transformacion morfologica
    tamaño_kernel = int(input("Ingrese el tamaño del kernel para la transformacion (e.g. 3): ").strip())
    kernel = np.ones((tamaño_kernel, tamaño_kernel), np.uint8)
    binarizada = cv2.morphologyEx(binarizada, cv2.MORPH_CLOSE, kernel)
    
    
