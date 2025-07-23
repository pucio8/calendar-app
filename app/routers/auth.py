from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from googleapiclient.discovery import build

# Importing the function to create the flow from the services
from ..services import get_google_auth_flow

# Creating an instance of the router
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.get("/login/google")
async def login_google(request: Request):
    """
    Redirects the user to the Google login page with a dynamic redirect_uri.
    """
    # Dynamically generate the redirect_uri based on the request address
    redirect_uri = request.url_for('auth_callback')
    
    flow = get_google_auth_flow(str(redirect_uri))
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        prompt='consent'
    )
    request.session['state'] = state
    return RedirectResponse(authorization_url)


@router.get("/callback", name="auth_callback") # Added 'name', to be able to find it
async def auth_callback(request: Request):
    """
    Handles the redirect from Google after authorization.
    """
    state = request.session.get('state')
    if not state or state != request.query_params.get('state'):
        raise HTTPException(status_code=400, detail="State mismatch.")
    
    # Dynamically generate the redirect_uri
    redirect_uri = request.url_for('auth_callback')
    flow = get_google_auth_flow(str(redirect_uri))
    
    try:
        flow.fetch_token(authorization_response=str(request.url))
        credentials = flow.credentials
        
        request.session['credentials'] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }

        user_info_service = build('oauth2', 'v2', credentials=credentials)
        user_info = user_info_service.userinfo().get().execute()
        request.session['user_email'] = user_info.get('email')

        response = RedirectResponse(url="/")
        response.set_cookie(key="google_token_present", value="true")
        return response
    except Exception as e:
        print(f"Błąd podczas pobierania tokenu: {e}")
        raise HTTPException(status_code=400, detail="Nie udało się pobrać tokenu autoryzacyjnego.")


@router.get("/logout")
async def logout(request: Request):
    """
    Clears the user's session and logs them out.
    """
    request.session.clear()
    response = RedirectResponse(url="/")
    response.delete_cookie("google_token_present")
    return response
