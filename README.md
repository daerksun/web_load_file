# web_load_file

Este desarrollo es una aplicación web usando HTML, un poco de Css y Js, para la interfaz gráfica, alojada en un contenedor en Nginx. Aquí se introducen los datos, se verifican y se mandan por un POST a una API o microservicio, en donde ocupe el framework Pycerver, que guarda la información en tres colecciones en MongoDB, una llamada file.info, donde se guarda nombre, teléfono, nombre del archivo, id de la colección del archivo, y el md5 del archivo para identificarlo rápidamente, y las otras dos se generan automáticamente con GridFS, que es un elemento de mongo que nos permite guardar archivos en binario y por secciones. Adicionalmente se podría encriptar el archivo antes de guardarlo para mayor seguridad, lo cual debe ser sencillo en Python. Cabe resaltar que se ocupó Docker Compose para levantar MongoDB, PyCerver y Nginx.


## Build Docker

```
sh development.sh
```
## Run Dockers

pycerver
```
docker run -it --rm \
    -e MONGO_URL=mongodb://admin:12345@localhost:27017 \
    -p 8080:8080 \
    -v $(pwd)/service:/home/web-load-file \
    -v $(pwd)/uploads:/home/uploads \
    --name web-load-file-pycerver \
    web-load-file:development

```


## Run Compose

```
docker-compose build 

docker-compose up
```



