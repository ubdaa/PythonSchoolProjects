from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
import csv
import io

from schemas.common import (
    StatsResponse, BookStatsResponse, AuthorStatsResponse, 
    MonthlyReportResponse, NeverBorrowedBookResponse, UserActivityResponse
)
from services.stats_service import StatsService
from data.orm import SessionDep

router = APIRouter(prefix="/stats", tags=["Statistics"])

def get_service(session: SessionDep):
    return StatsService(session)

@router.get("/", response_model=StatsResponse)
async def get_statistics(service: StatsService = Depends(get_service)):
    return await service.get_global_stats()

@router.get("/books/{book_id}", response_model=BookStatsResponse)
async def get_book_statistics(book_id: int, service: StatsService = Depends(get_service)):
    stats = await service.get_book_stats(book_id)
    if not stats:
        raise HTTPException(status_code=404, detail="Book not found")
    return stats

@router.get("/authors/{author_id}", response_model=AuthorStatsResponse)
async def get_author_statistics(author_id: int, service: StatsService = Depends(get_service)):
    stats = await service.get_author_stats(author_id)
    if not stats:
        raise HTTPException(status_code=404, detail="Author not found")
    return stats

@router.get("/reports/monthly", response_model=MonthlyReportResponse)
async def get_monthly_report(year: int, month: int, service: StatsService = Depends(get_service)):
    return await service.get_monthly_report(year, month)

@router.get("/reports/never-borrowed", response_model=list[NeverBorrowedBookResponse])
async def get_never_borrowed_books(service: StatsService = Depends(get_service)):
    return await service.get_never_borrowed_books()

@router.get("/reports/active-users", response_model=list[UserActivityResponse])
async def get_active_users(limit: int = 10, service: StatsService = Depends(get_service)):
    return await service.get_active_users(limit)

@router.get("/export/csv")
async def export_stats_csv(service: StatsService = Depends(get_service)):
    stats = await service.get_global_stats()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Metric", "Value"])
    for key, value in stats.items():
        writer.writerow([key, value])
    
    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode()),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=library_stats.csv"}
    )
