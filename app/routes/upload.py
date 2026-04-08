from fastapi import APIRouter

router=APIRouter(prefix="/upload",tags=["upload"])

@router.post("/")
def upload_file():
    print(f"Upload endpoint called")
    return{
        "status":"upload route ready"
    }
