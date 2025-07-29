import asyncio
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel
from typing import List
from fastapi.staticfiles import StaticFiles
# Importing the settings and routers
from .config import settings
from .routers import auth
from .services import GoogleCalendarService

# --- Application configuration ---
app = FastAPI(title="Interactive Duty Scheduler")

# Mounting the 'static' folder to serve CSS and JS files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.include_router(auth.router)
templates = Jinja2Templates(directory="app/templates")
calendar_service = GoogleCalendarService()

class EventItem(BaseModel):
    date: str
    type: str

class BatchEventRequest(BaseModel):
    events: List[EventItem]

# --- Main application endpoints ---
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/add-events")
async def add_events(request: Request, event_request: BatchEventRequest):
    if 'credentials' not in request.session:
        raise HTTPException(status_code=401, detail="No authorization.")

    event_configs = {
        "duty": {"summary": "Służba", "colorId": "5"},
        "duty_off": {"summary": "Wolna służba", "colorId": "9"},
        "delegation": {"summary": "Delegacja", "colorId": "6"},
        "training": {"summary": "Szkolenie", "colorId": "2"},
        "blood": {"summary": "Krew", "colorId": "11"},
    }
    
    try:
        creds = calendar_service.get_credentials_from_session(request.session['credentials'])
        tasks = []
        added_events_details = []
        for event_item in event_request.events:
            config = event_configs.get(event_item.type)
            if config:
                summary = config["summary"]
                tasks.append(
                    calendar_service.add_calendar_event(
                        creds, 
                        event_item.date, 
                        summary=summary, 
                        color_id=config["colorId"]
                    )
                )
                added_events_details.append({"summary": summary, "date": event_item.date})
               
        if not tasks:
            raise HTTPException(status_code=400, detail="No valid events to add.")

        await asyncio.gather(*tasks)
        
        user_email = request.session.get('user_email')
        redirect_url = f"https://calendar.google.com/calendar/u/{user_email}/r" if user_email else "https://calendar.google.com/"
        
        return {
            "message": f"Pomyślnie dodano {len(tasks)} wydarzeń.",
            "added_events": added_events_details,
            "redirect_url": redirect_url
        }
    except Exception as e:
        print(f"Wystąpił błąd w procesie: {e}")
        raise HTTPException(status_code=500, detail=str(e))
