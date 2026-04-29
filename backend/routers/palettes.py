from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models import Palette
from schemas import PaletteCreate, PaletteUpdate, PaletteResponse
from database import get_db

router = APIRouter(prefix="/palettes", tags=["palettes"])


@router.get("", response_model=List[PaletteResponse])
def get_palettes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all palettes (public only or all based on filter)"""
    palettes = db.query(Palette).offset(skip).limit(limit).all()
    return palettes


@router.get("/my", response_model=List[PaletteResponse])
def get_my_palettes(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get palettes for a specific user"""
    palettes = db.query(Palette).filter(Palette.user_id == user_id).all()
    return palettes


@router.get("/{palette_id}", response_model=PaletteResponse)
def get_palette(palette_id: int, db: Session = Depends(get_db)):
    """Get a single palette by ID"""
    palette = db.query(Palette).filter(Palette.id == palette_id).first()
    if not palette:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Palette not found"
        )
    return palette


@router.post("", response_model=PaletteResponse, status_code=status.HTTP_201_CREATED)
def create_palette(
    palette: PaletteCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Create a new palette"""
    new_palette = Palette(
        user_id=user_id,
        name=palette.name,
        description=palette.description,
        is_public=palette.is_public,
        tags=palette.tags
    )
    db.add(new_palette)
    db.commit()
    db.refresh(new_palette)
    return new_palette


@router.put("/{palette_id}", response_model=PaletteResponse)
def update_palette(
    palette_id: int,
    palette: PaletteUpdate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Update a palette (only owner can update)"""
    db_palette = db.query(Palette).filter(Palette.id == palette_id).first()
    if not db_palette:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Palette not found"
        )
    if db_palette.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this palette"
        )
    
    # Update fields if provided
    if palette.name is not None:
        db_palette.name = palette.name
    if palette.description is not None:
        db_palette.description = palette.description
    if palette.is_public is not None:
        db_palette.is_public = palette.is_public
    if palette.tags is not None:
        db_palette.tags = palette.tags
    
    db.commit()
    db.refresh(db_palette)
    return db_palette


@router.delete("/{palette_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_palette(
    palette_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Delete a palette (only owner can delete)"""
    db_palette = db.query(Palette).filter(Palette.id == palette_id).first()
    if not db_palette:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Palette not found"
        )
    if db_palette.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this palette"
        )
    
    db.delete(db_palette)
    db.commit()
    return None