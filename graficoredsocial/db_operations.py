import json

# Limpia cualquier cosa que pudiera haber estado en la base de datos


def clear(db):
    command = "MATCH (node) DETACH DELETE node"
    db.execute_query(command)

# Carga la información en la base de datos ejecutando las consultas openCypher(Lenguage de consulta para bases de datos orientadas a grafos) dentro de los archivos suministrados


def populate_database(db, path):
    file = open(path)
    lines = file.readlines()
    file.close()
    for line in lines:
        if len(line.strip()) != 0 and line[0] != '/':
            db.execute_query(line)

#Método encargado de obtener los usuarios
def get_users(db):
    command = "MATCH (n:User) RETURN n;"
    users = db.execute_and_fetch(command)

    user_objects = []
    for user in users:
        u = user['n']
        data = {"id": u.properties['id'], "name": u.properties['name']}
        user_objects.append(data)

    return json.dumps(user_objects)

#Método encargado de obtener las relaciones
def get_relationships(db):
    command = "MATCH (n1)-[e:FRIENDS]-(n2) RETURN n1,n2,e;"
    relationships = db.execute_and_fetch(command)

    relationship_objects = []
    for relationship in relationships:
        n1 = relationship['n1']
        n2 = relationship['n2']

        data = {"userOne": n1.properties['name'],
                "userTwo": n2.properties['name']}
        relationship_objects.append(data)

    return json.dumps(relationship_objects)

# Método que se encarga de recuperar toda la información relevante de la base de datos cuando un usuario asi lo requiera


def get_graph(db):
    #El query que se va a ejecutar y almacenar en relationships
    command = "MATCH (n1)-[e:FRIENDS]-(n2) RETURN n1,n2,e;"
    relationships = db.execute_and_fetch(command)

    link_objects = []
    node_objects = []
    added_nodes = []
    #Se itera sobre las relaciones
    for relationship in relationships:
        e = relationship['e']
        data = {"source": e.nodes[0], "target": e.nodes[1]}
        link_objects.append(data)
        #Se comprueba si los nodos han sido o no previamente agregados al objeto de nodos.
        n1 = relationship['n1']
        if not (n1.id in added_nodes):
            data = {"id": n1.id, "name": n1.properties['name']}
            node_objects.append(data)
            added_nodes.append(n1.id)

        n2 = relationship['n2']
        if not (n2.id in added_nodes):
            data = {"id": n2.id, "name": n2.properties['name']}
            node_objects.append(data)
            added_nodes.append(n2.id)
    #Se retorna los objetos almacenados en pares clave-valor(los links o relaciones que estan en el grafo como pares de fuente y ojetivo de propiedades ID)
    #y los nodos, que son todos los nodos del grafo que forman relación con otros nodos
    data = {"links": link_objects, "nodes": node_objects}

    return json.dumps(data)
