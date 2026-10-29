# Guardar y consultar en MariaDB

import pymysql


def conectar():
    return pymysql.connect(host="localhost", user="ds8", password="ds8", database="seguridad", autocommit=True)


def ejecutar(sql, valores=()):
    with conectar() as conexion:
        with conexion.cursor() as cursor:
            cursor.execute(sql, valores)
            return cursor.fetchall()


def guardar_lectura(datos):
    ejecutar(
        "INSERT INTO lecturas (movimiento, distancia, estado) VALUES (%s, %s, %s)",
        (datos["movimiento"], datos["distancia"], datos["estado"]),
    )


def guardar_evento(datos):
    ejecutar(
        "INSERT INTO eventos (tipo, sensor) VALUES (%s, %s)",
        (datos["tipo"], datos["sensor"]),
    )


def guardar_comando(datos):
    ejecutar(
        "INSERT INTO comandos (accion, origen, resultado) VALUES (%s, %s, %s)",
        (datos["accion"], datos["origen"], datos["resultado"]),
    )


def ultimas_lecturas(cantidad=10):
    return ejecutar("SELECT * FROM lecturas ORDER BY id DESC LIMIT %s", (cantidad,))


def ultimos_eventos(cantidad=10):
    return ejecutar("SELECT * FROM eventos ORDER BY id DESC LIMIT %s", (cantidad,))


def ultimos_comandos(cantidad=10):
    return ejecutar("SELECT * FROM comandos ORDER BY id DESC LIMIT %s", (cantidad,))


def lecturas_entre(desde, hasta):
    return ejecutar("SELECT * FROM lecturas WHERE fecha BETWEEN %s AND %s", (desde, hasta))


if __name__ == "__main__":
    print("Lecturas:")
    for fila in ultimas_lecturas():
        print(fila)
    print("Eventos:")
    for fila in ultimos_eventos():
        print(fila)
    print("Comandos:")
    for fila in ultimos_comandos():
        print(fila)
