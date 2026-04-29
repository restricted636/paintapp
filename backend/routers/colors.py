from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models import Color
from schemas import ColorCreate, ColorResponse
from database import get_db

router = APIRouter(prefix="/colors", tags=["colors"])


@router.post("", response_model=ColorResponse, status_code=status.HTTP_201_CREATED)
def create_color(
    color: ColorCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Create a new color. Validates unique hex_code per user."""
    # Check if hex_code already exists for this user
    existing_color = db.query(Color).filter(
        Color.user_id == user_id,
        Color.hex_code == color.hex_code
    ).first()
    
    if existing_color:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Color with this hex_code already exists for this user"
        )
    
    # Create new color
    new_color = Color(
        user_id=user_id,
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


@router.get("", response_model=List[ColorResponse])
def list_colors(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all colors for a user"""
    colors = db.query(Color).filter(
        Color.user_id == user_id
    ).offset(skip).limit(limit).all()
    
    return colors


@router.delete("/{color_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_color(
    color_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Delete a color (only owner can delete)"""
    db_color = db.query(Color).filter(Color.id == color_id).first()
    
    if not db_color:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Color not found"
        )
    
    if db_color.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this color"
        )
    
    db.delete(db_color)
    db.commit()
    return None