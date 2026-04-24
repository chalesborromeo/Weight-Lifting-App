from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.schemas.spot_request import SpotRequestCreate, SpotRequestResponse, SpotRequestUpdate
from app.db.postgresql.factory import PostgreSQLFactory
from app.db.postgresql.connection import PostgreSQLConnection
from sqlalchemy import select
from app.models.spot_Request import Spot_Request


def get_db():
    connection = PostgreSQLConnection.get_instance()
    with connection.get_session() as session:
        yield session


class SpottersRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/spotters", tags=["spotters"])
        self.router.add_api_route("/requests", self.create_request, methods=["POST"], response_model=SpotRequestResponse)
        self.router.add_api_route("/requests", self.get_requests, methods=["GET"], response_model=List[SpotRequestResponse])
        self.router.add_api_route("/requests/{request_id}", self.get_request, methods=["GET"], response_model=SpotRequestResponse)
        self.router.add_api_route("/requests/{request_id}", self.update_request, methods=["PUT"], response_model=SpotRequestResponse)
        self.router.add_api_route("/requests/{request_id}", self.delete_request, methods=["DELETE"], response_model=SpotRequestResponse)

    async def create_request(self, spot_request: SpotRequestCreate, session=Depends(get_db)):
        """Create a spot request"""
        new_request = Spot_Request(
            spotter_id=spot_request.spotter_id,
            requester_id=spot_request.requester_id,
            status=False
        )
        session.add(new_request)
        session.commit()
        session.refresh(new_request)
        return SpotRequestResponse.model_validate(new_request)

    async def get_requests(self, session=Depends(get_db)):
        """Get all spot requests"""
        stmt = select(Spot_Request)
        results = session.execute(stmt).scalars().all()
        return [SpotRequestResponse.model_validate(r) for r in results]

    async def get_request(self, request_id: int, session=Depends(get_db)):
        """Get a specific spot request"""
        stmt = select(Spot_Request).where(Spot_Request.id == request_id)
        spot_request = session.execute(stmt).scalars().first()
        if not spot_request:
            raise HTTPException(status_code=404, detail="Spot request not found")
        return SpotRequestResponse.model_validate(spot_request)

    async def update_request(self, request_id: int, data: SpotRequestUpdate, session=Depends(get_db)):
        """Update a spot request status"""
        stmt = select(Spot_Request).where(Spot_Request.id == request_id)
        spot_request = session.execute(stmt).scalars().first()
        if not spot_request:
            raise HTTPException(status_code=404, detail="Spot request not found")
        
        spot_request.status = data.status
        session.commit()
        session.refresh(spot_request)
        return SpotRequestResponse.model_validate(spot_request)

    async def delete_request(self, request_id: int, session=Depends(get_db)):
        """Delete a spot request"""
        stmt = select(Spot_Request).where(Spot_Request.id == request_id)
        spot_request = session.execute(stmt).scalars().first()
        if not spot_request:
            raise HTTPException(status_code=404, detail="Spot request not found")
        
        session.delete(spot_request)
        session.commit()
        return SpotRequestResponse.model_validate(spot_request)
