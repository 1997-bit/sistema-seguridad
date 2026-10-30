# Guardar en MariaDB

import pymysql


def conectar():
    return pymysql.connect(host="localhost", user="ds8", password="ds8", database="seguridad", autocommit=True)


def ejecutar(sql, valores):
    with conectar() as conexion:
        with conexion.cursor() as cursor:
            cursor.execute(sql, valores)


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

