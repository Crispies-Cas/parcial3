import os
import numpy as np
import pydicom
import matplotlib.pyplot as plt
import cv2
import nibabel as nib
from nilearn import plotting, image

class sistema:
    def __init__(self):
        self.imagenes_procesadas={}
        
class Paciente:
    def __init__(self, nombre, edad, ID, imagen):
        self.nombre = nombre
        self.edad = edad
        self.ID = ID
        self.imagen = imagen

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
    
    affine = np.diag([slice_thickness, pixel_spacing[0], pixel_spacing[1], 1.0])
    nifti_img = nib.Nifti1Image(volumen, affine)

    eje[0].imshow(volumen[volumen.shape[0] // 2, :, :],cmap='gray',aspect=pixel_spacing[0] / pixel_spacing[1])
    eje[0].set_title("Axial")

    eje[1].imshow(volumen[:, volumen.shape[1] // 2, :],cmap='gray',aspect=slice_thickness / pixel_spacing[1])
    eje[1].set_title("Coronal")

    eje[2].imshow(volumen[:, :, volumen.shape[2] // 2],cmap='gray',aspect=slice_thickness / pixel_spacing[0])
    eje[2].set_title("Sagital")

    plt.tight_layout()
    plt.show()

    clave = input("Ingrese una clave para guardar este volumen: ").strip()
    nib.save(nifti_img, clave)
    print("Volumen guardado exitosamente con la clave:", clave) 

def mostrar_nii():
    img = input('ruta de la imagen nii: ')
    plotting.plot_anat(img, display_mode='ortho', title='Planos Axial, Sagital y Coronal')
    plt.show()


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
    
    _, binarizada = cv2.threshold(imagen, umbral, 255, tipos.get(opcion, cv2.THRESH_BINARY))


    # Transformacion morfologica
    tamaño_kernel = int(input("Ingrese el tamaño del kernel para la transformacion (e.g. 3): ").strip())
    kernel = np.ones((tamaño_kernel, tamaño_kernel), np.uint8)
    binarizada = cv2.morphologyEx(binarizada, cv2.MORPH_CLOSE, kernel)
        
        
        
    # Obtener las dimensiones de la imagen binarizada, #h = altura, w = ancho
    h, w = binarizada.shape       

    forma = input("Que figura desea dibujar? (cuadro/circulo): ").strip().lower()

    if forma == "cuadro":
        # Dibuja un rectangulo desde (10, 10) hasta (w-10, h-10)
        cv2.rectangle(binarizada, (10, 10), (w - 10, h - 10), (255), 2)

        # Escribe "Imagen binarizada" cerca de la esquina superior izquierda
        cv2.putText(binarizada, "Imagen binarizada", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 255, 2)

    elif forma == "circulo":
        # El radio se elige para que no se salga de la imagen (aprox 1/3 del lado mas corto)
        radio = min(w, h) // 3
        cv2.circle(binarizada, (w // 2, h // 2), radio, 255, 2)

        # Escribe "Imagen binarizada" cerca de la esquina superior izquierda
        cv2.putText(binarizada, "Imagen binarizada", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 255, 2)
        

# Mostrar y guardar
    plt.imshow(binarizada, cmap='gray')
    plt.title("Imagen Procesada")
    plt.axis("off")
    plt.show()

    clave = input("Ingrese una clave para guardar esta imagen procesada: ").strip()
    imagenes_procesadas[clave] = binarizada
    print("Imagen procesada y guardada bajo la clave:", clave)
    

procesar_imagen_png_jpg()