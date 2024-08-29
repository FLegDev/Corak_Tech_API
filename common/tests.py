import os
import json
import logging

# Configuration du logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def determine_file_type(file_path):
    try:
        logger.info(f"Opening file {file_path} to determine file type.")
        extension = os.path.splitext(file_path)[1].lower()
        if extension not in ['.json', '.txt', '.api']:
            logger.error("Unsupported file extension.")
            return 'Unknown'

        # Lire le fichier sans le fermer prématurément
        with open(file_path, 'r') as file:
            content = file.read()
            logger.info("File read successfully.")
            data = json.loads(content)

            # Valider la structure JSON
            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                if any('promotion' in item for item in data):
                    logger.info("File type determined as Promo.")
                    return 'Promo'
                elif any('certificates' in item for item in data):
                    logger.info("File type determined as Ardoise.")
                    return 'Ardoise'
                else:
                    logger.info("File type determined as Unknown.")
                    return 'Unknown'
            else:
                logger.error("Invalid JSON structure.")
                return 'Unknown'
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return 'Unknown'
    except Exception as e:
        logger.error(f"Error determining file type: {e}")
        return 'Unknown'

if __name__ == "__main__":
    # Chemin du fichier à tester
    file_path = '../media/uploads/monoprix_fr_lab.vlab_monoprix_fr_lab.vlab_c56fc847-810f-41a6-b899-0dcec2a47c30_items.api'
    
    # Appeler la fonction de détermination du type de fichier
    file_type = determine_file_type(file_path)
    print(f"File type: {file_type}")
