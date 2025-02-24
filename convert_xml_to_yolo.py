import os
import xml.etree.ElementTree as ET

xml_folder = "./simple_images/mesas"
output_folder = "./simple_images/mesas_txt"

class_mapping = {"m01": 0}

os.makedirs(output_folder, exist_ok=True)

for xml_file in os.listdir(xml_folder):
    if not xml_file.endswith(".xml"):
        continue

    tree = ET.parse(os.path.join(xml_folder, xml_file))
    root = tree.getroot()

    # Obtener tamaño de la imagen
    size = root.find("size")
    img_width = int(size.find("width").text)
    img_height = int(size.find("height").text)

    yolo_annotations = []
    
    for obj in root.findall("object"):
        class_name = obj.find("name").text
        if class_name not in class_mapping:
            continue  # Omitir clases no deseadas

        class_id = class_mapping[class_name]
        bbox = obj.find("bndbox")
        
        # Coordenadas en formato Pascal VOC (pixeles absolutos)
        xmin = int(bbox.find("xmin").text)
        ymin = int(bbox.find("ymin").text)
        xmax = int(bbox.find("xmax").text)
        ymax = int(bbox.find("ymax").text)

        # Convertir coordenadas a formato YOLO (normalizado)
        x_center = (xmin + xmax) / 2 / img_width
        y_center = (ymin + ymax) / 2 / img_height
        width = (xmax - xmin) / img_width
        height = (ymax - ymin) / img_height

        yolo_annotations.append(f"{class_id} {x_center} {y_center} {width} {height}")

    # Guardar el archivo .txt con el mismo nombre de la imagen
    txt_filename = os.path.splitext(xml_file)[0] + ".txt"
    with open(os.path.join(output_folder, txt_filename), "w") as f:
        f.write("\n".join(yolo_annotations))

print("✅ ¡Conversión completada!")