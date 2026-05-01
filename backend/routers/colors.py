"""
Color router for managing user colors.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models import Color
from schemas import ColorCreate, ColorResponse
from database import get_db
from auth import get_current_user
from models import User

router = APIRouter(prefix="/colors", tags=["Colors"])


@router.post(
    "",
    response_model=ColorResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new color",
    description="Create a new color for the authenticated user. "
                 "Validates that hex_code is unique for the user.",
    responses={
        201: {"description": "Color created successfully"},
        400: {"description": "Color with this hex_code already exists"},
        401: {"description": "Authentication required"},
    },
    tags=["Colors"],
)
def create_color(
    color: ColorCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new color.
    
    - **hex_code**: Hex color code (e.g., #FF5733)
    - **rgb_r**, **rgb_g**, **rgb_b**: RGB values (0-255)
    - **cmyk_c**, **cmyk_m**, **cmyk_y**, **cmyk_k**: CMYK values (optional)
    - **lab_l**, **lab_a**, **lab_b**: LAB values (optional)
    - **h**, **s**, **l**: HSL values (optional)
    - **name**: Optional color name
    - **note**: Optional note
    """
    # Check if hex_code already exists for this user
    existing_color = db.query(Color).filter(
        Color.user_id == current_user.id,
        Color.hex_code == color.hex_code
    ).first()
    
    if existing_color:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Color with this hex_code already exists for this user"
        )
    
    # Create new color
    new_color = Color(
        user_id=current_user.id,
        hex_code=color.hex_code,
        rgb_r=color.rgb_r,
        rgb_g=color.rgb_g,
        rgb_b=color.rgb_b,
        cmyk_c=color.cmyk_c,
        cmyk_m=color.cmyk_m,
        cmyk_y=color.cmyk_y,
        cmyk_k=color.cmyk_k,
        lab_l=color.lab_l,
        lab_a=color.lab_a,
        lab_b=color.lab_b,
        h=color.h,
        s=color.s,
        l=color.l,
        name=color.name,
        note=color.note
    )
    db.add(new_color)
    db.commit()
    db.refresh(new_color)
    
    return new_color


@router.get(
    "",
    response_model=List[ColorResponse],
    summary="List user's colors",
    description="Get all colors belonging to the authenticated user.",
    responses={
        200: {"description": "List of colors retrieved successfully"},
        401: {"description": "Authentication required"},
    },
    tags=["Colors"],
)
def list_colors(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List all colors for the authenticated user.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100)
    """
    colors = db.query(Color).filter(
        Color.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    return colors


@router.get(
    "/{color_id}",
    response_model=ColorResponse,
    summary="Get a color by ID",
    description="Retrieve a specific color by its ID. Only the owner can view.",
    responses={
        200: {"description": "Color retrieved successfully"},
        403: {"description": "Not authorized to view this color"},
        404: {"description": "Color not found"},
    },
    tags=["Colors"],
)
def get_color(
    color_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a single color by ID (only owner can view).
    
    - **color_id**: The unique identifier of the color
    """
    db_color = db.query(Color).filter(Color.id == color_id).first()
    
    if not db_color:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Color not found"
        )
    
    if bool(db_color.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this color"
        )
    
    return db_color


@router.put(
    "/{color_id}",
    response_model=ColorResponse,
    summary="Update a color",
    description="Update an existing color. Only the owner can update.",
    responses={
        200: {"description": "Color updated successfully"},
        403: {"description": "Not authorized to update this color"},
        404: {"description": "Color not found"},
    },
    tags=["Colors"],
)
def update_color(
    color_id: int,
    color: ColorCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a color (only owner can update).
    
    - **color_id**: The unique identifier of the color
    - **hex_code**: New hex color code
    - **rgb_r**, **rgb_g**, **rgb_b**: New RGB values
    - Other color model values can be updated as needed
    """
    db_color = db.query(Color).filter(Color.id == color_id).first()
    
    if not db_color:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Color not found"
        )
    
    if bool(db_color.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this color"
        )
    
    # Update fields using setattr to avoid type checker issues
    for attr in ['hex_code', 'rgb_r', 'rgb_g', 'rgb_b', 'cmyk_c', 'cmyk_m', 'cmyk_y', 'cmyk_k', 'lab_l', 'lab_a', 'lab_b', 'h', 's', 'l', 'name', 'note']:
        setattr(db_color, attr, getattr(color, attr))
    
    db.commit()
    db.refresh(db_color)
    return db_color


@router.delete(
    "/{color_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a color",
    description="Delete a color. Only the owner can delete.",
    responses={
        204: {"description": "Color deleted successfully"},
        403: {"description": "Not authorized to delete this color"},
        404: {"description": "Color not found"},
    },
    tags=["Colors"],
)
def delete_color(
    color_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a color (only owner can delete).
    
    - **color_id**: The unique identifier of the color
    """
    db_color = db.query(Color).filter(Color.id == color_id).first()
    
    if not db_color:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Color not found"
        )
    
    if bool(db_color.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this color"
        )
    
    db.delete(db_color)
    db.commit()
    return None