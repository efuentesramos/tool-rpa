import glob
import os
import cv2
import pybboxes as pbx
import albumentations as A

def colocar_clase_al_final(filename):   
    bbboxes=[]
    if  "\\" in filename:    
        element_replace=filename.replace('\\','/')
    else:
        element_replace=filename       
   
    with open(element_replace,'r') as file:
        lineas = [linea.split() for linea in file ]
        for linea in lineas:
            list_float= [float(f) for f in linea]
            clase=int(list_float.pop(0))
            list_float.append(clase)
            bbboxes.append(list_float)        
    return bbboxes

def colocar_clase_al_inicio(matriz):   
    bbboxes=[] 
    for elemento in (matriz):
        elemento=list(elemento)        
        clase=elemento.pop(-1)
        elemento.insert(0,clase)
        bbboxes.append(elemento)        
    return bbboxes

def draw_yolo(image, labels, namefile):
    H, W = image.shape[:2]    
    for label in labels:                
        yolo_normalized = label[1:]
        box_voc = pbx.convert_bbox(tuple(yolo_normalized), from_type="yolo", to_type="voc", image_size=(W,H))
        cv2.rectangle(image, (box_voc[0], box_voc[1]), 
                    (box_voc[2], box_voc[3]), (0, 0, 255), 1)
    cv2.imwrite(namefile, image)
    cv2.imshow("output_vis", image)
    cv2.waitKey(0)

def convertir_url_image_label(url_image):    
    url_label=url_image.replace("images","labels").replace("png","txt")
    return url_label

def convertir_url_label_image(url_label):    
    url_image=url_label.replace("labels", "images").replace("txt", "png")
    return url_image

def escribir_txt(txt, labels_list):
    with open(txt,'w') as txt_out:
        for line in labels_list:
            line = str(line).replace(',', ' ').replace('[', '').replace(']', '').replace('(', '').replace(')', '')
            txt_out.write(line + "\n")

def duplicar_data_especifica(clase_duplicar, num_replicas):
    lista_txt=sacar_lista_txt_conclase_duplicar(clase_duplicar)
    if lista_txt:
        for archivo_txt in lista_txt:    
            archivo_image=convertir_url_label_image(archivo_txt)
            list_clases=obtener_lista_clase(archivo_txt,clase_duplicar)      
            image=cv2.imread(archivo_image)
            alto, ancho, canales = image.shape
            bboxes=colocar_clase_al_final(archivo_txt)

            for i in range(40,60):
                alto=alto-1
                transform = A.Compose([    
                    A.RandomCrop(width=ancho, height=alto),    
                ], bbox_params=A.BboxParams(format='yolo'))
                transformed = transform(image=image, bboxes=bboxes)
                transformed_image = transformed['image']
                transformed_bboxes = transformed['bboxes']                
                new_name_image=f'{archivo_image.replace(".png","")}({i}).png'
                transformed_bboxes=colocar_clase_al_inicio(transformed_bboxes)
                cv2.imwrite(new_name_image, transformed_image)
                archivo_txt=convertir_url_image_label(new_name_image)
                escribir_txt(archivo_txt,list_clases)
    else:
        print(f'La clase {clase_duplicar} no esta contenida en los txt')
   
def sacar_lista_txt_conclase_duplicar(clase_duplicar,path_labels):
    list_txt=glob.glob(path_labels+'*.txt')
    lista_archivos_valida=[]
    for txt in list_txt:
        if obtener_lista_clase(txt, clase_duplicar):
            lista_archivos_valida.append(txt)
    return lista_archivos_valida

def obtener_lista_clase(archivo_txt, clase_duplicar):
    list_clases=[]
    with open(archivo_txt,'r') as txt_file:
        lineas=[linea.split() for linea in txt_file]
        for linea in lineas:
            clase=int(linea[0])            
            if clase == clase_duplicar:
                linea=[float(l) for l in linea]
                linea.pop(0)
                linea.insert(0,clase)
                list_clases.append(linea) 
    return list_clases
