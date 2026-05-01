"""
Palette router for CRUD operations on color palettes.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models import Palette
from schemas import PaletteCreate, PaletteUpdate, PaletteResponse
from database import get_db
from auth import get_current_user
from models import User

router = APIRouter(prefix="/palettes", tags=["Palettes"])


@router.get(
    "",
    response_model=List[PaletteResponse],
    summary="List all palettes",
    description="Get a paginated list of all palettes. "
                 "Use skip and limit for pagination.",
    responses={
        200: {"description": "List of palettes retrieved successfully"},
    },
    tags=["Palettes"],
)
def get_palettes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all palettes with pagination.
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records to return (default: 100)
    """
    palettes = db.query(Palette).offset(skip).limit(limit).all()
    return palettes


@router.get(
    "/my",
    response_model=List[PaletteResponse],
    summary="Get user's palettes",
    description="Get all palettes belonging to the authenticated user.",
    responses={
        200: {"description": "List of user's palettes"},
        401: {"description": "Authentication required"},
    },
    tags=["Palettes"],
)
def get_my_palettes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all palettes for the authenticated user.
    """
    palettes = db.query(Palette).filter(Palette.user_id == current_user.id).all()
    return palettes


@router.get(
    "/{palette_id}",
    response_model=PaletteResponse,
    summary="Get palette by ID",
    description="Retrieve a specific palette by its ID.",
    responses={
        200: {"description": "Palette retrieved successfully"},
        404: {"description": "Palette not found"},
    },
    tags=["Palettes"],
)
def get_palette(palette_id: int, db: Session = Depends(get_db)):
    """
    Get a single palette by ID.
    
    - **palette_id**: The unique identifier of the palette
    """
    palette = db.query(Palette).filter(Palette.id == palette_id).first()
    if not palette:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Palette not found"
        )
    return palette


@router.post(
    "",
    response_model=PaletteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new palette",
    description="Create a new color palette for the authenticated user.",
    responses={
        201: {"description": "Palette created successfully"},
        401: {"description": "Authentication required"},
    },
    tags=["Palettes"],
)
def create_palette(
    palette: PaletteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new palette.
    
    - **name**: Name of the palette (required)
    - **description**: Optional description
    - **is_public**: Whether the palette is public (default: false)
    - **tags**: Optional list of tags
    """
    new_palette = Palette(
        user_id=current_user.id,
        name=palette.name,
        description=palette.description,
        is_public=palette.is_public,
        tags=palette.tags
    )
    db.add(new_palette)
    db.commit()
    db.refresh(new_palette)
    return new_palette


@router.put(
    "/{palette_id}",
    response_model=PaletteResponse,
    summary="Update a palette",
    description="Update an existing palette. Only the owner can update.",
    responses={
        200: {"description": "Palette updated successfully"},
        403: {"description": "Not authorized to update this palette"},
        404: {"description": "Palette not found"},
    },
    tags=["Palettes"],
)
def update_palette(
    palette_id: int,
    palette: PaletteUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a palette (only owner can update).
    
    - **palette_id**: The unique identifier of the palette
    - **name**: New name (optional)
    - **description**: New description (optional)
    - **is_public**: New visibility (optional)
    - **tags**: New tags (optional)
    """
    db_palette = db.query(Palette).filter(Palette.id == palette_id).first()
    if not db_palette:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Palette not found"
        )
    if bool(db_palette.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this palette"
        )
    
    # Update fields if provided using setattr
    if palette.name is not None:
        setattr(db_palette, 'name', palette.name)
    if palette.description is not None:
        setattr(db_palette, 'description', palette.description)
    if palette.is_public is not None:
        setattr(db_palette, 'is_public', palette.is_public)
    if palette.tags is not None:
        setattr(db_palette, 'tags', palette.tags)
    
    db.commit()
    db.refresh(db_palette)
    return db_palette


@router.delete(
    "/{palette_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a palette",
    description="Delete a palette. Only the owner can delete.",
    responses={
        204: {"description": "Palette deleted successfully"},
        403: {"description": "Not authorized to delete this palette"},
        404: {"description": "Palette not found"},
    },
    tags=["Palettes"],
)
def delete_palette(
    palette_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a palette (only owner can delete).
    
    - **palette_id**: The unique identifier of the palette
    """
    db_palette = db.query(Palette).filter(Palette.id == palette_id).first()
    if not db_palette:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Palette not found"
        )
    if bool(db_palette.user_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this palette"
        )
    
    db.delete(db_palette)
    db.commit()
    return None