import os
import numpy as np
import pydicom
import matplotlib.pyplot as plt
import cv2
import nibabel as nib
from nilearn import plotting, image
        
class Paciente:
    def __init__(self, nombre, fecha, ID, imagen):
        self.nombre = nombre
        self.fecha = fecha
        self.ID = ID
        self.imagen = imagen
    def __str__(self):
        return f'el paciente {self.nombre} de {self.edad} e ID:{self.imagen}'

class sistema:
    def __init__(self):
        self.pacientes=[]
        self.imagenes_procesadas={}
    def nuevo_paciente(self, ruta):
        archivos_dcm = sorted([f for f in os.listdir(ruta) if f.lower().endswith(".dcm")])
        if archivos_dcm:
            pop = os.path.join(ruta, archivos_dcm[0])
        ds = pydicom.dcmread(pop)
        nombre= ds.get(0x0010,0x0010)
        fecha=ds.get(0x0010,0x0030)
        ID= ds.get(0x0010,0x0020)
        nombre=Paciente(nombre, fecha, ID, self.imagenes_procesadas[-1])
        self.pacientes.append
        
        

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
    # Obtener el espaciado
    z = float(slices[0].SliceThickness)
    y, x = map(float, slices[0].PixelSpacing)

    # Crear matriz affine con spacing real
    affine = np.diag([z, y, x, 1])

    # Crear imagen NIfTI
    nifti_img = nib.Nifti1Image(volumen, affine)

    nib.save(nifti_img, 'img'+len(sistema.imagenes_procesadas))
    print(f"✔ Volumen guardado como archivo NIfTI: {'img'+len(sistema.imagenes_procesadas)}


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
    

def mostrar_imagen_por_clave():
    clave = input("Ingrese la clave de la imagen que quiere visualizar: ").strip()
    if clave in imagenes_procesadas:
        imagen = imagenes_procesadas[clave]
        plt.imshow(imagen, cmap='gray')
        plt.title(f"Imagen asociada a la clave: {clave}")
        plt.axis('off')
        plt.show()
    else:
        print("No se encontro ninguna imagen con esa clave.")


imagenes_procesadas={}
archivos_dicom={}

def trasladar_imagen_dicom():
    if not archivos_dicom:
        print("No hay volúmenes cargados.")
        return

    # Muestra claves disponibles
    print("Volumenes disponibles:")
    for clave in archivos_dicom.keys():
        print("-", clave)

    clave = input("Ingrese la clave del volumen que desea usar: ").strip()

    if clave not in archivos_dicom:
        print("Clave no encontrada.")
        return

    volumen = archivos_dicom[clave]

    # Escoge un solo corte (por defecto el del medio)
    corte = volumen[volumen.shape[0] // 2]

    # Muestra opciones de traslacion
    print("\nOpciones de traslacion:")
    opciones = {
        "1": (20, 0),     # mover 20 pixeles a la derecha
        "2": (0, 20),     # mover 20 pixeles hacia abajo
        "3": (-20, 0),    # mover 20 pixeles a la izquierda
        "4": (0, -20)     # mover 20 pixeles hacia arriba
    }

    for i, (dx, dy) in enumerate(opciones.values(), 1):
        print(f"{i}. dx = {dx}, dy = {dy}")

    eleccion = input("Seleccione una opcion de traslacion (1-4): ").strip()
    if eleccion not in opciones:
        print("Opción invalida.")
        return

    dx, dy = opciones[eleccion]

    # Crea la matriz de transformacion
    M = np.float32([[1, 0, dx], [0, 1, dy]])

    # Aplica la traslacion
    trasladada = cv2.warpAffine(corte, M, (corte.shape[1], corte.shape[0]))

    # Muestra ambas imagenes
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    axes[0].imshow(corte, cmap='gray')
    axes[0].set_title("Imagen Original")
    axes[0].axis('off')

    axes[1].imshow(trasladada, cmap='gray')
    axes[1].set_title(f"Trasladada dx={dx}, dy={dy}")
    axes[1].axis('off')

    plt.tight_layout()
    plt.show()

    # Guarda imagen trasladada
    nombre_salida = input("Nombre para guardar la imagen trasladada (ej. trasladada.png): ").strip()
    if not nombre_salida.lower().endswith('.png'):
        nombre_salida += ".png"

    cv2.imwrite(nombre_salida, trasladada)
    print("Imagen trasladada guardada como:", nombre_salida)



trasladar_imagen_dicom()