import csv
import os
from datetime import datetime

ARCHIVO_ENTRADA = "data.txt"
ARCHIVO_SALIDA = "resultado.txt"
VERSION = os.environ.get("VERSION", "1.0")

def leer_datos(archivo):
    estados = []
    with open(archivo, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            estados.append({
                "estado": row["Estado"],
                "temperatura": float(row["Temperatura"]),
                "humedad": float(row["Humedad"]),
                "costo_alojamiento": float(row["Costo_Alojamiento"]),
                "costo_transporte": float(row["Costo_Transporte"]),
                "dias_promedio": float(row["Dias_Promedio"]),
                "tiempo_traslado": float(row["Tiempo_Traslado"]),
            })
    return estados

def calcular_costo_total(e):
    return e["costo_alojamiento"] * e["dias_promedio"] + e["costo_transporte"]

def procesar(estados):
    for e in estados:
        e["costo_total"] = calcular_costo_total(e)

    mas_barato = min(estados, key=lambda x: x["costo_total"])
    mas_caro = max(estados, key=lambda x: x["costo_total"])
    mas_caliente = max(estados, key=lambda x: x["temperatura"])
    mas_frio = min(estados, key=lambda x: x["temperatura"])
    mas_humedo = max(estados, key=lambda x: x["humedad"])
    menos_humedo = min(estados, key=lambda x: x["humedad"])
    mas_cercano = min(estados, key=lambda x: x["tiempo_traslado"])
    mas_lejano = max(estados, key=lambda x: x["tiempo_traslado"])

    promedio_costo = sum(e["costo_total"] for e in estados) / len(estados)
    promedio_temp = sum(e["temperatura"] for e in estados) / len(estados)

    top5_baratos = sorted(estados, key=lambda x: x["costo_total"])[:5]
    top5_caros = sorted(estados, key=lambda x: x["costo_total"], reverse=True)[:5]

    return {
        "total": len(estados),
        "mas_barato": mas_barato,
        "mas_caro": mas_caro,
        "mas_caliente": mas_caliente,
        "mas_frio": mas_frio,
        "mas_humedo": mas_humedo,
        "menos_humedo": menos_humedo,
        "mas_cercano": mas_cercano,
        "mas_lejano": mas_lejano,
        "promedio_costo": round(promedio_costo, 2),
        "promedio_temp": round(promedio_temp, 2),
        "top5_baratos": top5_baratos,
        "top5_caros": top5_caros,
    }

def guardar_resultado(r, archivo):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lineas = [
        "================================================",
        f"  REPORTE DE ESTADOS DE MEXICO",
        f"  Generado: {fecha}",
        f"  Version: {VERSION}",
        f"  Archivo procesado: data.txt",
        f"  Total de estados procesados: {r['total']}",
        "================================================",
        "",
        "--- COSTOS ---",
        f"Estado mas economico : {r['mas_barato']['estado']} (${r['mas_barato']['costo_total']:.0f} MXN total)",
        f"Estado mas caro      : {r['mas_caro']['estado']} (${r['mas_caro']['costo_total']:.0f} MXN total)",
        f"Promedio de costo    : ${r['promedio_costo']:.0f} MXN",
        "",
        "--- CLIMA ---",
        f"Estado mas caliente  : {r['mas_caliente']['estado']} ({r['mas_caliente']['temperatura']}°C)",
        f"Estado mas frio      : {r['mas_frio']['estado']} ({r['mas_frio']['temperatura']}°C)",
        f"Temperatura promedio : {r['promedio_temp']:.1f}°C",
        f"Estado mas humedo    : {r['mas_humedo']['estado']} ({r['mas_humedo']['humedad']}%)",
        f"Estado menos humedo  : {r['menos_humedo']['estado']} ({r['menos_humedo']['humedad']}%)",
        "",
        "--- DISTANCIA DESDE CDMX ---",
        f"Estado mas cercano   : {r['mas_cercano']['estado']} ({r['mas_cercano']['tiempo_traslado']:.0f} hrs)",
        f"Estado mas lejano    : {r['mas_lejano']['estado']} ({r['mas_lejano']['tiempo_traslado']:.0f} hrs)",
        "",
        "--- TOP 5 DESTINOS MAS ECONOMICOS ---",
    ]
    for i, e in enumerate(r["top5_baratos"], 1):
        lineas.append(f"  {i}. {e['estado']:<25} ${e['costo_total']:.0f} MXN")
    lineas += [
        "",
        "--- TOP 5 DESTINOS MAS CAROS ---",
    ]
    for i, e in enumerate(r["top5_caros"], 1):
        lineas.append(f"  {i}. {e['estado']:<25} ${e['costo_total']:.0f} MXN")
    lineas.append("")
    lineas.append("================================================")

    contenido = "\n".join(lineas)
    with open(archivo, "w", encoding="utf-8") as f:
        f.write(contenido)
    print(contenido)
    return contenido

def main():
    print(f"Iniciando procesamiento - Version {VERSION}")
    estados = leer_datos(ARCHIVO_ENTRADA)
    print(f"Se leyeron {len(estados)} estados.")
    resultados = procesar(estados)
    contenido = guardar_resultado(resultados, ARCHIVO_SALIDA)
    print(f"\nArchivo '{ARCHIVO_SALIDA}' generado correctamente.")

if __name__ == "__main__":
    main()
