from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Portfolio API")

# CORS for frontend previews
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In a production app you'd store this in a DB. For demo we keep it simple.
BLOG_DB = [
    {
        "id": 1,
        "title": "Shaping delightful DX",
        "date": "2024-09-12",
        "excerpt": "Principles I use to design APIs and tools developers love.",
        "image": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?q=80&w=1974&auto=format&fit=crop",
    },
    {
        "id": 2,
        "title": "Type safety at scale",
        "date": "2024-08-28",
        "excerpt": "How to keep types ergonomic while your codebase grows.",
        "image": "https://images.unsplash.com/photo-1518779578993-ec3579fee39f?q=80&w=2070&auto=format&fit=crop",
    },
    {
        "id": 3,
        "title": "Frontend performance 101",
        "date": "2024-08-03",
        "excerpt": "Budgeting, metrics, and practical ways to speed up apps.",
        "image": "https://images.unsplash.com/photo-1487014679447-9f8336841d58?q=80&w=2070&auto=format&fit=crop",
    },
    {
        "id": 4,
        "title": "Pastel palettes and motion",
        "date": "2024-07-19",
        "excerpt": "Soft gradients, glass, and tasteful animation for web UIs.",
        "image": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?q=80&w=2069&auto=format&fit=crop",
    },
]

class BlogListResponse(BaseModel):
    total: int
    page: int
    limit: int
    items: List[dict]

class ContactRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=80)
    email: EmailStr
    message: str = Field(..., min_length=10, max_length=2000)

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/blog", response_model=BlogListResponse)
def list_blog(page: int = 1, limit: int = 6, q: Optional[str] = None):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Invalid page or limit")
    items = BLOG_DB
    if q:
        ql = q.lower()
        items = [b for b in BLOG_DB if ql in b["title"].lower() or ql in b["excerpt"].lower()]
    total = len(items)
    start = (page - 1) * limit
    end = start + limit
    paged = items[start:end]
    return {"total": total, "page": page, "limit": limit, "items": paged}

@app.post("/contact")
def contact(req: ContactRequest):
    # In real world you'd send to email/Slack. Here we just acknowledge.
    return {"ok": True, "message": "Thanks, I'll reach out soon!"}
