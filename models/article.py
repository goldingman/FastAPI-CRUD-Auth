from pydantic import BaseModel


class Article(BaseModel):
    """Schema for article information."""
    id: int
    name: str
    price: float

    def to_dict(self):
        """Convert article to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price
        }
