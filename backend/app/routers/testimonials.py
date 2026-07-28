from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Testimonial
from app.schemas import TestimonialOut

router = APIRouter(prefix='/api/testimonials', tags=['testimonials'])


@router.get('', response_model=list[TestimonialOut])
def list_testimonials(db: Session = Depends(get_db)):
    return db.query(Testimonial).filter(Testimonial.active == True).order_by(Testimonial.created_at.desc()).all()
