from typing import Optional

from core import config

def _import_psycopg2():
	try:
		import psycopg2
	except Exception:
		return None
	return psycopg2


def fetch_scalar(query: str, params: Optional[tuple] = None) -> Optional[str]:
	psycopg2 = _import_psycopg2()
	if not psycopg2:
		return None
	try:
		with psycopg2.connect(config.POSTGRES_DSN) as conn:
			with conn.cursor() as cur:
				cur.execute(query, params)
				row = cur.fetchone()
				if not row:
					return None
				return str(row[0])
	except Exception:
		return None
