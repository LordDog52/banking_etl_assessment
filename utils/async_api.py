import aiohttp
import asyncio
from functools import wraps
import logging
from typing import Optional

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def retry(max_retries: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """
    Decorator untuk retry logic dengan exponential backoff
    
    Args:
        max_retries: Jumlah maksimal percobaan ulang
        delay: Delay awal antara retry (dalam detik)
        backoff: Faktor perkalian untuk exponential backoff
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            current_delay = delay
            
            for attempt in range(max_retries + 1):  # +1 untuk include attempt pertama
                try:
                    result = await func(*args, **kwargs)
                    if attempt > 0:
                        logger.info(f"Attempt {attempt + 1} successful for {func.__name__}")
                    return result
                    
                except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                    last_exception = e
                    
                    if attempt < max_retries:
                        logger.warning(
                            f"Attempt {attempt + 1} failed for {func.__name__}: {str(e)}. "
                            f"Retrying in {current_delay:.1f}s..."
                        )
                        await asyncio.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error(
                            f"All {max_retries + 1} attempts failed for {func.__name__}. "
                            f"Last error: {str(e)}"
                        )
            
            # Jika semua retry gagal, raise exception terakhir
            raise last_exception
        return wrapper
    return decorator


@retry(max_retries=3, delay=1.0, backoff=2.0)
async def fetch_quote(symbol: str) -> dict:
    """
    Fetch quote data untuk symbol tertentu dari API dummy
    
    Args:
        symbol: Symbol saham (meskipun API dummy tidak menggunakan ini)
        
    Returns:
        dict: Data quote dari API
        
    Raises:
        aiohttp.ClientError: Jika terjadi error HTTP
        asyncio.TimeoutError: Jika request timeout
    """
    # Endpoint mock API
    url = "https://dummyjson.com/quotes/random"
    
    # Timeout configuration
    timeout = aiohttp.ClientTimeout(total=10, connect=5)
    
    # Tambahkan symbol sebagai query parameter untuk simulasi
    params = {"symbol": symbol} if symbol else {}
    
    logger.info(f"Fetching quote for symbol: {symbol}")
    
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url, params=params) as response:
            # Check HTTP status
            if response.status != 200:
                error_text = await response.text()
                raise aiohttp.ClientError(
                    f"HTTP {response.status}: {error_text}"
                )
            
            # Parse JSON response
            data = await response.json()
            
            # Tambahkan symbol ke response untuk konsistensi
            data["symbol"] = symbol
            data["fetched_at"] = asyncio.get_event_loop().time()
            
            logger.info(f"Successfully fetched quote for {symbol}")
            
            return data


# Contoh penggunaan dan testing
async def main():
    """Contoh penggunaan fetch_quote function"""
    try:
        # Test dengan symbol valid
        quote = await fetch_quote("AAPL")
        print("Quote data:", quote)
        
        # Test dengan empty symbol
        quote_empty = await fetch_quote("")
        print("Empty symbol quote:", quote_empty)
        
    except Exception as e:
        print(f"Error fetching quote: {e}")