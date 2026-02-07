
import re
import requests
from PySide6.QtCore import QObject, QRunnable, Signal, Slot

class DiscoverySignals(QObject):
    """Signals for the Key Discovery Worker"""
    # key, list_of_models (list of dicts), error_message (str or None)
    # models dict structure: {'name': str, 'description': str}
    result = Signal(str, list, str)
    finished = Signal()

class KeyDiscoveryWorker(QRunnable):
    """
    Worker to check a single API Key.
    It queries the 'models' endpoint to see which models are available for this key.
    """
    def __init__(self, api_key):
        super().__init__()
        self.api_key = api_key
        self.signals = DiscoverySignals()

    @Slot()
    def run(self):
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={self.api_key}"
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                # data['models'] is a list of dicts: [{'name': 'models/gemini-pro', 'description': '...'}, ...]
                models = []
                for m in data.get('models', []):
                    models.append({
                        'name': m.get('name', 'Unknown'),
                        'description': m.get('description', 'No description available')
                    })
                self.signals.result.emit(self.api_key, models, None)
            else:
                try:
                    error_msg = response.json().get('error', {}).get('message', f"HTTP {response.status_code}")
                except:
                    error_msg = f"HTTP {response.status_code}"
                self.signals.result.emit(self.api_key, [], error_msg)
                
        except requests.exceptions.RequestException as e:
            self.signals.result.emit(self.api_key, [], str(e))
        finally:
            self.signals.finished.emit()

def extract_api_keys(text):
    r"""
    Extracts all unique Google AI API keys from text.
    Pattern: AIza[0-9A-Za-z\-_]{35}
    """
    # Regex for AIza key (39 chars total typically, starts with AIza)
    # Standard format: AIza + 35 chars
    pattern = r'(AIza[0-9A-Za-z\-_]{35})'
    keys = re.findall(pattern, text)
    return sorted(list(set(keys)))
