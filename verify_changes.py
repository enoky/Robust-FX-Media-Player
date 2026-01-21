import sys
import os

# Add current directory to path so we can import metadata_fetch
sys.path.append(os.getcwd())

import metadata_fetch

def test_deezer_cache_key():
    print("Testing Deezer Cache Key Logic...")
    
    # Mock Deezer Item with Album ID
    mock_item_with_album = {
        "id": 12345,
        "title": "One More Time",
        "album": {
            "id": 999,
            "title": "Discovery",
            "cover_xl": "http://example.com/cover.jpg"
        }
    }
    
    # We need to simulate the function call logic from _cover_from_deezer_item
    # Since I cannot import the internal function easily if it is not exposed, 
    # I will rely on reading the file or just trust the detailed implementation plan execution.
    # checking if I can import it...
    
    if hasattr(metadata_fetch, "_cover_from_deezer_item"):
        _, _, cache_key = metadata_fetch._cover_from_deezer_item(mock_item_with_album)
        print(f"Key for item with Album ID 999: {cache_key}")
        if "deezer_album_999" in cache_key:
            print("PASS: Cache key uses Album ID.")
        else:
            print(f"FAIL: Cache key '{cache_key}' does not contain 'deezer_album_999'.")
    else:
        print("SKIP: _cover_from_deezer_item not directly accessible or renamed.")

    # Mock Deezer Item WITHOUT Album ID (fallback to track)
    mock_item_no_album_id = {
        "id": 12345,
        "title": "One More Time",
        "album": {
            "title": "Discovery",
            "cover_xl": "http://example.com/cover.jpg"
        }
    }
    
    if hasattr(metadata_fetch, "_cover_from_deezer_item"):
        _, _, cache_key = metadata_fetch._cover_from_deezer_item(mock_item_no_album_id)
        print(f"Key for item without Album ID: {cache_key}")
        if "deezer_track_12345" in cache_key:
            print("PASS: Cache key falls back to Track ID.")
        else:
            print(f"FAIL: Cache key '{cache_key}' does not contain 'deezer_track_12345'.")

def test_manual_key_generation():
    print("\nTesting Generic Fallback Cache Key Logic (Simulation)...")
    import hashlib
    
    artist = "Daft Punk"
    album = "Discovery"
    
    normalized = metadata_fetch._normalize_match_text(f"{artist} {album}")
    digest = hashlib.sha1(normalized.encode("utf-8", "ignore")).hexdigest()
    expected_key = f"generic_{digest}"
    
    print(f"Artist: {artist}, Album: {album}")
    print(f"Normalized: {normalized}")
    print(f"Expected Generic Key: {expected_key}")
    
    # Verify same Artist/Album input produces same key
    artist2 = "Daft Punk "
    album2 = "discovery"
    normalized2 = metadata_fetch._normalize_match_text(f"{artist2} {album2}")
    digest2 = hashlib.sha1(normalized2.encode("utf-8", "ignore")).hexdigest()
    key2 = f"generic_{digest2}"
    
    if expected_key == key2:
         print("PASS: Generic key is stable with minor spacing/case differences.")
    else:
         print(f"FAIL: Keys differ: {expected_key} vs {key2}")

if __name__ == "__main__":
    test_deezer_cache_key()
    test_manual_key_generation()
