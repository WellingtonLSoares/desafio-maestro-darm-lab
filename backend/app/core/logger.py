import logging
import sys

# Configuração básica
logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s [%(levelname)s] %(message)s",
  handlers=[
    logging.FileHandler("audit.log"),
    logging.StreamHandler(sys.stdout)
  ]
)

logger = logging.getLogger("maestro_audit")
