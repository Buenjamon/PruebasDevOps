import json
import os
from datetime import datetime

VERSION = os.environ.get("VERSION", "1.0")
ARCHIVO_ENTRADA = "estudiantes.json"
ARCHIVO_SALIDA = "resultados.json"
ARCHIVO_LOG = "backup.log"

def cargar_datos(archivo):
    with open(archivo, "r", encoding="utf-8") as f:
        return json.load(f)

def filtrar_estudiantes(estudiantes):
    aprobados = [e for e in estudiantes if e["calificacion"] >= 60]
    reprobados = [e for e in estudiantes if e["calificacion"] < 60]
    return aprobados, reprobados

def guardar_resultados(aprobados, reprobados, archivo):
    resultados = {
        "total_procesados": len(aprobados) + len(reprobados),
        "aprobados": aprobados,
        "reprobados": reprobados
    }
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    return resultados

def registrar_log(archivo_entrada, total, aprobados, reprobados):
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entrada = f"""
==================================================
Fecha y Hora       : {fecha_hora}
Version            : {VERSION}
Archivo procesado  : {archivo_entrada}
Total procesados   : {total}
Aprobados          : {len(aprobados)} (calificacion >= 60)
Reprobados         : {len(reprobados)} (calificacion < 60)
Resultado          : Se filtraron {total} datos. {len(aprobados)} aprobados, {len(reprobados)} reprobados.
==================================================
"""
    with open(ARCHIVO_LOG, "a", encoding="utf-8") as f:
        f.write(entrada)
    print(entrada)

def main():
    print(f"Iniciando procesamiento - Version {VERSION}")
    print(f"Leyendo archivo: {ARCHIVO_ENTRADA}")

    estudiantes = cargar_datos(ARCHIVO_ENTRADA)
    print(f"Se leyeron {len(estudiantes)} registros.")

    aprobados, reprobados = filtrar_estudiantes(estudiantes)
    print(f"Aprobados: {len(aprobados)} | Reprobados: {len(reprobados)}")

    guardar_resultados(aprobados, reprobados, ARCHIVO_SALIDA)
    print(f"Resultados guardados en: {ARCHIVO_SALIDA}")

    registrar_log(ARCHIVO_ENTRADA, len(estudiantes), aprobados, reprobados)
    print("Log registrado en: backup.log")

if __name__ == "__main__":
    main()
