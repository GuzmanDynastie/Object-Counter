from simple_image_download import simple_image_download as simp

response = simp.simple_image_download

keyword = "mesas escolares"

num_images = 100

response().download(keyword, num_images)

print(f"Se han descargado {num_images} imágenes de {keyword}.")