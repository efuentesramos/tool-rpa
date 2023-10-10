import albumentations as A
import cv2
import glob
import utils as u

folder_path='./images/'
list_images=glob.glob(folder_path+'*.png')

for image in list_images:
    image_replace=image.replace('\\','/')   
    image = cv2.imread(image_replace)  # Reemplaza 'example.jpg' con la ruta de tu imagen
    alto, ancho, canales = image.shape
    label_replace = u.convertir_url_image_label(image_replace)
    bboxes=u.colocar_clase_al_final(label_replace)
    
    for i in range(1,6):
        alto=alto-10
        transform = A.Compose([    
            A.RandomCrop(width=ancho, height=alto),    
        ], bbox_params=A.BboxParams(format='yolo'))
        transformed = transform(image=image, bboxes=bboxes)
        transformed_image = transformed['image']
        transformed_bboxes = transformed['bboxes']
        new_name_image=f'{image_replace.replace(".png","")}({i}).png'
        cv2.imwrite(new_name_image, transformed_image)        
        transformed_bboxes=u.colocar_clase_al_inicio(transformed_bboxes)
        u.draw_yolo(transformed_image, transformed_bboxes, new_name_image)
                
        file_txt=f'{label_replace.replace("images","labels").replace(".txt","")}({i}).txt'
        with open(file_txt,'w') as txt_output:
            print(file_txt)
            for bbox in transformed_bboxes:                
                print(type(bbox[0]))
                updated_bbox = str(bbox).replace(',', ' ').replace('[', '').replace(']', '').replace('(', '').replace(')', '')            
                txt_output.write(updated_bbox + '\n')

