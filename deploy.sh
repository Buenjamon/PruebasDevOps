#!/bin/bash

BUCKET_NAME="mi-bucket-ejemplo"
BACKUP_FILE="backup_$(date +%F).tar.gz"
LOG_FILE="backup.log"

echo "Iniciando respaldo..." | tee -a $LOG_FILE

# Carpeta actual (donde está tu código en CodeBuild)
SOURCE_DIR="."

# Crear backup
tar -czf $BACKUP_FILE $SOURCE_DIR >> $LOG_FILE 2>&1

# Subir a S3
if aws s3 cp $BACKUP_FILE s3://$BUCKET_NAME/ >> $LOG_FILE 2>&1; then
    echo "Respaldo subido exitosamente." | tee -a $LOG_FILE
else
    echo "Error en la subida del respaldo." | tee -a $LOG_FILE
fi
