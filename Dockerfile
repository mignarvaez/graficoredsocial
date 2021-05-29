#Imagen base python 3.9
FROM python:3.9

#Instrucciones para instalar CMake
RUN apt-get update && \
  apt-get --yes install cmake

#Intrucciones para instalar poetry
RUN pip install -U pip \
  && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="${PATH}:/root/.poetry/bin"

#Instrucciones para instalar mgclient, un sistema de gestión de base de datos de gráficos en memoria totalmente distribuido
RUN apt-get install -y git cmake make gcc g++ libssl-dev && \
  git clone https://github.com/memgraph/mgclient.git /mgclient && \
  cd mgclient && \
  git checkout 5ae69ea4774e9b525a2be0c9fc25fb83490f13bb && \
  mkdir build && \
  cd build && \
  cmake .. && \
  make && \
  make install

#Instrucciones para instalar pymgclient un adaptador de python para la base de datos memgraph
#Toco instalar con pip, haciendo make no funcionaba
RUN pip3 install --user pymgclient

#Se define el directorio de trabajo
WORKDIR /app
#Permite llevar cache de los requerimientos del proyecto y solo reinstalarlos cuando los archivos indicados cambien.
COPY poetry.lock pyproject.toml /app/

#No se requiere crear un entorno virtual de python con poetry porque la aplicación estará aislada en un contenedor de docker (En la primera linea)
#En la segunda linea se le indica a poetry no haga preguntas interactivas mientras instala o actualiza dependencias, haciendo de la salida de los logs más amigable
RUN poetry config virtualenvs.create false && \
  poetry install --no-interaction --no-ansi

#Se copian los archivos de la ruta actual a la carpeta app del contenedor
#Se expone el puerto 5000
COPY . /app/
EXPOSE 5000
#Se agrega y cambia los permisos del archivo de flask en las siguientes dos lineas
ADD start.sh /
RUN chmod +x /start.sh
#Se especifica el ejecutable que usará el contenedor
ENTRYPOINT [ "poetry", "run" ]
#Se indican los parametros a usar con el ejecutable anterior
CMD ["/start.sh"]