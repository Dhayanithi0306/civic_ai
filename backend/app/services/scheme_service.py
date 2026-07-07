from app.utils.json_loader import JSONLoader

class SchemeService:
    """Service to handle government scheme data."""
    
    @staticmethod
    def get_all_schemes() -> list[dict]:
        """Retrieve all loaded government schemes."""
        return JSONLoader.load_schemes()
