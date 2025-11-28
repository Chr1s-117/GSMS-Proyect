# src/Services/cache_manager.py
"""
In-memory cache manager for HTTP responses.

Purpose:
- Store ETags to avoid DB queries during validation
- Invalidate cache when new GPS data arrives
- Limit memory usage with LRU eviction

Architecture:
- Thread-safe (uses threading.Lock)
- LRU eviction (removes oldest entries when full)
- TTL-based expiration (entries expire after X seconds)
"""

import hashlib
import json
import time
import threading
from typing import Dict, Optional, Any
from collections import OrderedDict
from src.Core.config import settings


class CacheManager:
    """
    Thread-safe in-memory cache with LRU eviction and TTL expiration.
    
    Attributes:
        max_size: Maximum number of cache entries (default: 1000)
        default_ttl: Default TTL in seconds (default: 300s = 5min)
    """
    
    def __init__(self, max_size: int = 1000, default_ttl: int = 300):
        """
        Initialize cache manager.
        
        Args:
            max_size: Maximum cache entries before LRU eviction
            default_ttl: Default time-to-live in seconds
        
        Why these defaults:
            max_size=1000: 
                - Asume 100 usuarios * 10 queries diferentes = 1000 entries
                - Cada entry ~1KB (solo ETag + metadata) = 1MB RAM total
                - Suficiente para operación normal sin memory leaks
            
            default_ttl=300s:
                - 5 minutos es balance entre freshness y performance
                - Entries viejas se auto-limpian (no crecimiento infinito)
                - Puedes sobrescribir TTL per-endpoint
        """
        self._cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()
        self._lock = threading.Lock()
        self.max_size = max_size
        self.default_ttl = default_ttl
    
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Get cached entry if exists and not expired.
        
        Args:
            key: Cache key (typically the request path + query params)
        
        Returns:
            Cached entry dict or None if not found/expired
            
        Example:
            entry = cache.get("/gps_data/positions/latest")
            if entry:
                etag = entry["etag"]
        """
        with self._lock:
            if key not in self._cache:
                return None
            
            entry = self._cache[key]
            
            # Check if expired
            if time.time() > entry["expires_at"]:
                # Remove expired entry
                del self._cache[key]
                return None
            
            # Move to end (LRU: most recently used)
            self._cache.move_to_end(key)
            
            return entry
    
    def set(
        self, 
        key: str, 
        data: Any, 
        ttl: Optional[int] = None
    ) -> str:
        """
        Store entry in cache and return its ETag.
        
        Args:
            key: Cache key (request path + query params)
            data: Data to cache (will be serialized to JSON for ETag)
            ttl: Custom TTL in seconds (uses default_ttl if None)
        
        Returns:
            ETag (MD5 hash) of the cached data
            
        Side effects:
            - Evicts oldest entry if cache is full (LRU)
            - Generates ETag from JSON serialization
            
        Example:
            positions = get_last_gps_all_devices(db)
            etag = cache.set("/gps_data/positions/latest", positions, ttl=10)
        """
        with self._lock:
            # Generate ETag
            etag = self._generate_etag(data)
            
            # Calculate expiration
            expires_at = time.time() + (ttl or self.default_ttl)
            
            # Store entry
            self._cache[key] = {
                "etag": etag,
                "data": data,
                "expires_at": expires_at,
                "created_at": time.time()
            }
            
            # Move to end (most recent)
            self._cache.move_to_end(key)
            
            # Evict oldest if exceeded max_size (LRU)
            if len(self._cache) > self.max_size:
                # Remove first item (oldest)
                oldest_key = next(iter(self._cache))
                del self._cache[oldest_key]
            
            return etag
    
    def invalidate(self, key: str) -> bool:
        """
        Remove entry from cache (used when data changes).
        
        Args:
            key: Cache key to invalidate
        
        Returns:
            True if entry was found and removed, False otherwise
            
        Example:
            # When new GPS arrives via UDP
            cache.invalidate("/gps_data/positions/latest")
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False
    
    def invalidate_pattern(self, pattern: str) -> int:
        """
        Invalidate all keys matching a pattern.
        
        Args:
            pattern: String pattern to match (simple substring match)
        
        Returns:
            Number of entries invalidated
            
        Example:
            # Invalidate all trips for a device
            cache.invalidate_pattern("device_id=TRUCK-001")
        """
        with self._lock:
            keys_to_remove = [
                key for key in self._cache.keys() 
                if pattern in key
            ]
            
            for key in keys_to_remove:
                del self._cache[key]
            
            return len(keys_to_remove)
    
    def clear(self) -> None:
        """
        Clear entire cache (useful for testing or system reset).
        """
        with self._lock:
            self._cache.clear()
    
    def stats(self) -> Dict[str, Any]:
        """
        Get cache statistics (for monitoring/debugging).
        
        Returns:
            Dict with cache metrics
            
        Example:
            stats = cache.stats()
            print(f"Cache size: {stats['size']}/{stats['max_size']}")
        """
        with self._lock:
            now = time.time()
            expired_count = sum(
                1 for entry in self._cache.values()
                if now > entry["expires_at"]
            )
            
            return {
                "size": len(self._cache),
                "max_size": self.max_size,
                "expired_count": expired_count,
                "oldest_age_seconds": (
                    now - next(iter(self._cache.values()))["created_at"]
                    if self._cache else 0
                )
            }
    
    @staticmethod
    def _generate_etag(data: Any) -> str:
        """
        Generate MD5 hash of data (used as ETag).
        
        Args:
            data: Any JSON-serializable data
        
        Returns:
            MD5 hash (32 hex chars)
            
        Note:
            Uses sort_keys=True for deterministic hashing
            (same data always produces same ETag)
        """
        json_str = json.dumps(data, sort_keys=True, default=str)
        return hashlib.md5(json_str.encode()).hexdigest()


# Global cache instance (singleton)
# Created once when module is imported
cache_manager = CacheManager(
    max_size=settings.CACHE_MAX_SIZE,
    default_ttl=settings.CACHE_DEFAULT_TTL_S
)