from google_play_scraper import reviews, Sort

# ID APLIKASI SUDAH TETAP
APP_ID = 'id.go.pajak.djp'

def get_reviews(limit=200):
    result, _ = reviews(
        APP_ID,
        lang='id',
        country='id',
        sort=Sort.NEWEST,
        count=limit
    )

    return [r['content'] for r in result if r.get('content')]
