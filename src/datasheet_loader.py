import os
import logging

# Initialize logger for this module
logger = logging.getLogger(__name__)

class OfficialDatasheetLoader:
    """
    Loads official datasheets for sensors.
    """
    def __init__(self, official_datasheets_dir: str):
        """
        Initializes the OfficialDatasheetLoader.

        Args:
            official_datasheets_dir: The base path to the official datasheets directory.
        """
        self.official_datasheets_dir = official_datasheets_dir

    def load_datasheet(self, brand: str, sensor_type: str) -> tuple[str | None, str]:
        """
        Loads the content of an official datasheet.

        Args:
            brand: The brand of the sensor.
            sensor_type: The type/model of the sensor.

        Returns:
            A tuple containing the file content string (or None if not found/error)
            and a status message ("Found", "Official Datasheet Not Found",
            "Error Fetching Official Datasheet").
        """
        filename = f"{brand}_{sensor_type}.md"
        filepath = os.path.join(self.official_datasheets_dir, filename)

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            logger.info(f"Successfully loaded official datasheet: {filepath}")
            return content, "Found"
        except FileNotFoundError:
            logger.warning(f"Official datasheet {filepath} not found.")
            return None, "Official Datasheet Not Found"
        except IOError as e:
            logger.error(f"IOError while reading official datasheet {filepath}: {e}")
            return None, "Error Fetching Official Datasheet"

if __name__ == '__main__':
    # Example Usage (for testing purposes)
    logging.basicConfig(level=logging.INFO)
    
    # Create a dummy datasheet directory and file for testing
    test_datasheet_dir = "test_datasheets"
    os.makedirs(test_datasheet_dir, exist_ok=True)
    
    dummy_brand = "TestBrand"
    dummy_sensor = "TestSensor123"
    dummy_filename = f"{dummy_brand}_{dummy_sensor}.md"
    dummy_filepath = os.path.join(test_datasheet_dir, dummy_filename)
    
    with open(dummy_filepath, 'w', encoding='utf-8') as f:
        f.write("# Test Datasheet Content\n\nThis is a test datasheet.")

    loader = OfficialDatasheetLoader(official_datasheets_dir=test_datasheet_dir)

    # Test case 1: Datasheet found
    content, status = loader.load_datasheet(dummy_brand, dummy_sensor)
    print(f"Test Case 1 (Found): Status - {status}")
    if content:
        print(f"Content:\n{content[:50]}...") # Print first 50 chars

    # Test case 2: Datasheet not found
    content_not_found, status_not_found = loader.load_datasheet("NonExistentBrand", "NonExistentSensor")
    print(f"\nTest Case 2 (Not Found): Status - {status_not_found}")

    # Test case 3: Simulate IOError (e.g. by making the file unreadable - harder to simulate directly here)
    # For now, we'll assume the FileNotFoundError covers the most common 'not found' scenario.
    # To truly test IOError, one might change file permissions temporarily if running with sufficient rights.

    # Clean up dummy directory and file
    os.remove(dummy_filepath)
    os.rmdir(test_datasheet_dir)
    logger.info("Cleaned up test datasheet directory and file.")