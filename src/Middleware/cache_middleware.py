# src/Middleware/cache_middleware.py (VERSIÓN KISS DEFINITIVA)

"""
HTTP Caching Middleware with ETag-only strategy (KISS).

Purpose:
- Add ETag headers to responses for validation
- Validate If-None-Match from requests
- Return 304 Not Modified when data hasn't changed
- Use cache_manager to avoid redundant DB queries

Strategy:
- ALL endpoints: max-age=0 (always validate)
- Backend cache prevents DB queries during validation
- Simple, uniform configuration (KISS principle)
"""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.requests import Request
import json

from src.Services.cache_manager import cache_manager


class HTTPCacheMiddleware(BaseHTTPMiddleware):
    """
    Middleware that adds HTTP caching with ETag validation.
    
    Cache Strategy (KISS):
    - max-age=0: Frontend always validates (no TTL blocking)
    - must-revalidate: Backend decides freshness via ETag
    - cache_manager: Prevents DB queries during validation
    """
    
    # Endpoints that use caching
    CACHED_ENDPOINTS = [        
        # Phase 2: New REST endpoints (WebSocket replacements)
        "/gps_data/positions/latest",
        "/gps_data/timestamps/range",
        "/gps_data/history",
        "/gps_data/trips",
        
        # Phase 1: Existing GET endpoints (high value, low risk)
        "/gps_data/devices",    # List of active devices (rarely changes)
        "/gps_data/last",       # Latest GPS per device (polling use case)
        "/gps_data/oldest",     # First GPS per device (immutable historical data)
        "/gps_data/range",      # GPS range queries (historical reports)
        
        # NOT cached:
        # - POST /gps_data/post (creates data)
        # - PATCH /gps_data/{id} (modifies data)
        # - DELETE /gps_data/{id} (deletes data)
        # - GET /gps_data/{id} (low usage, optional)
    ]
    
    # Single cache configuration for all endpoints (KISS)
    DEFAULT_CACHE_CONTROL = "private, max-age=0, must-revalidate"
    
    async def dispatch(self, request: Request, call_next):
        """
        Intercept and process each request/response.
        
        Flow:
        1. Check if endpoint is cacheable
        2. Validate client ETag from backend cache (fast path)
        3. Execute endpoint if needed (may query DB)
        4. Store result in cache with ETag
        5. Return response with cache headers
        """
        # Check if this endpoint should be cached
        if not self._is_cacheable(request.url.path):
            return await call_next(request)
        
        # Generate cache key
        cache_key = self._generate_cache_key(request)
        
        # Check if client sent ETag
        client_etag = request.headers.get("if-none-match", "").strip('"')
        
        if client_etag:
            # Try to validate from backend cache
            cached_entry = cache_manager.get(cache_key)
            
            if cached_entry and cached_entry["etag"] == client_etag:
                # Data unchanged → 304 Not Modified
                return Response(
                    status_code=304,
                    headers={
                        "ETag": f'"{client_etag}"',
                        "Cache-Control": self.DEFAULT_CACHE_CONTROL
                    }
                )
        
        # Execute endpoint handler
        response = await call_next(request)
        
        # Only cache successful JSON responses
        if response.status_code != 200:
            return response
        
        if not self._is_json_response(response):
            return response
        
        # Consume response body
        # FastAPI responses are StreamingResponse - we must consume the iterator
        body_chunks = []
        async for chunk in response.body_iterator: # type: ignore[attr-defined]
            body_chunks.append(chunk)
        
        body = b"".join(body_chunks)
        
        # Parse JSON
        try:
            data = json.loads(body)
        except (json.JSONDecodeError, ValueError):
            # Not valid JSON → return without caching
            return Response(
                content=body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type
            )
        
        # Store in cache and get ETag
        etag = cache_manager.set(cache_key, data)
        
        # Add cache headers
        headers = dict(response.headers)
        headers["ETag"] = f'"{etag}"'
        headers["Cache-Control"] = self.DEFAULT_CACHE_CONTROL
        
        return Response(
            content=body,
            status_code=200,
            headers=headers,
            media_type=response.media_type
        )
    
    def _is_cacheable(self, path: str) -> bool:
        """Check if endpoint should be cached."""
        return any(path.startswith(endpoint) for endpoint in self.CACHED_ENDPOINTS)
    
    def _generate_cache_key(self, request: Request) -> str:
        """Generate unique cache key (path + sorted query params)."""
        path = request.url.path
        query_params = sorted(request.query_params.items())
        query_string = "&".join(f"{k}={v}" for k, v in query_params)
        
        return f"{path}?{query_string}" if query_string else path
    
    @staticmethod
    def _is_json_response(response: Response) -> bool:
        """Check if response is JSON."""
        content_type = response.headers.get("content-type", "")
        return "application/json" in content_type