"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Literal

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Water treatment lead schema for contact/assessment submissions
class Lead(BaseModel):
    """
    Leads collection schema for water treatment inquiries
    Collection name: "lead"
    """
    full_name: str = Field(..., description="Prospect full name")
    email: EmailStr = Field(..., description="Prospect email")
    phone: Optional[str] = Field(None, description="Prospect phone number")

    # Structured intent and context
    user_intent: Literal[
        "learn_more",
        "get_quote",
        "book_assessment",
        "service_existing",
        "other",
    ] = Field(..., description="Primary intent of the visitor")

    property_type: Optional[Literal["single_family", "condo", "multi_unit", "commercial", "spa_gym", "other"]] = Field(
        None, description="Property type"
    )
    occupants: Optional[int] = Field(None, ge=1, le=50, description="Household occupants")

    # Health and water concerns
    concerns: Optional[List[Literal[
        "taste_odor",
        "chlorine",
        "hardness_scale",
        "lead_metals",
        "pfas",
        "bacteria",
        "whole_home_filtration",
        "drinking_water",
        "shower_skin_hair",
        "appliance_protection",
        "other",
    ]]] = Field(None, description="Selected water concerns")

    budget_range: Optional[Literal[
        "under_1k",
        "1k_3k",
        "3k_6k",
        "6k_plus",
        "unsure",
    ]] = Field(None, description="Estimated budget range")

    message: Optional[str] = Field(None, description="Additional context provided by prospect")
    source: Optional[str] = Field(None, description="Marketing attribution or source tag")
