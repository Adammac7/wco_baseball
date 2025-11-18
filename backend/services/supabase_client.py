"""
GitHub push quick commands — run from repo root (c:\Users\Adam\wco_baseball)

# Configure git (if not already configured)
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# Initialize repo (if needed)
git init
git add .
git commit -m "Initial commit"

# Option A — create and push with gh CLI (recommended)
gh auth login
gh repo create your-username/your-repo-name --public --source=. --remote=origin --push

# Option B — create repo on github.com then push manually
git branch -M main
git remote add origin https://github.com/your-username/your-repo-name.git
git push -u origin main

# Notes:
# - Do not commit secrets (.env). Use GitHub Secrets for SUPABASE_URL and SUPABASE_KEY.
# - Replace your-username/your-repo-name and 'main' as needed.
"""

import os
from typing import Any, Dict, Optional, List, Tuple, Union
from supabase import create_client, Client

from dotenv import load_dotenv  
load_dotenv()


class SupabaseClient:
	"""
	Simple wrapper for supabase-py.
	Reads SUPABASE_URL and SUPABASE_KEY from env if not provided.
	Methods return the raw response from supabase (so caller can inspect .data/.error/.status_code).
	"""

	def __init__(self, url: Optional[str] = None, key: Optional[str] = None):
		self.url = url or os.getenv("SUPABASE_URL")
		self.key = key or os.getenv("SUPABASE_KEY")
		if not self.url or not self.key:
			raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set (env or args)")
		self.client: Client = create_client(self.url, self.key)

	# -------------------
	# Table helpers
	# -------------------
	def select(
		self,
		table: str,
		columns: str = "*",
		filters: Optional[Dict[str, Any]] = None,
		limit: Optional[int] = None,
		offset: Optional[int] = None,
	) -> Any:
		"""
		Select rows from a table.
		- filters: simple equality filters as {column: value}
		- returns the raw response (res.data, res.error, res.status_code)
		"""
		q = self.client.table(table).select(columns)
		if filters:
			for k, v in filters.items():
				q = q.eq(k, v)
		if limit is not None:
			q = q.limit(limit)
		if offset is not None:
			q = q.range(offset, (offset + limit - 1) if limit is not None else None)
		return q.execute()

	def insert(self, table: str, payload: Union[Dict, List[Dict]], returning: str = "representation") -> Any:
		"""
		Insert one or many rows.
		- payload: dict or list of dicts
		- returning: 'representation' (default) or 'minimal'
		"""
		return self.client.table(table).insert(payload, returning=returning).execute()

	def update(self, table: str, payload: Dict[str, Any], filters: Dict[str, Any]) -> Any:
		"""
		Update rows matching filters.
		- filters: equality filters {column: value}
		"""
		q = self.client.table(table).update(payload)
		for k, v in filters.items():
			q = q.eq(k, v)
		return q.execute()

	def delete(self, table: str, filters: Dict[str, Any]) -> Any:
		"""
		Delete rows matching filters.
		- filters: equality filters {column: value}
		"""
		q = self.client.table(table).delete()
		for k, v in filters.items():
			q = q.eq(k, v)
		return q.execute()

	# -------------------
	# Auth helpers
	# -------------------
	def auth_sign_up(self, email: str = None, password: str = None, provider: Optional[str] = None, data: Optional[Dict] = None) -> Any:
		"""
		Sign up with email/password or provider.
		- If provider is provided, pass provider arg (e.g. 'google')
		"""
		if provider:
			# provider flow (redirect handled externally)
			return self.client.auth.sign_in(provider=provider)
		return self.client.auth.sign_up({"email": email, "password": password, **(data or {})})

	def auth_sign_in(self, email: str = None, password: str = None) -> Any:
		"""Sign in with email/password. Returns auth response (access token, session info)."""
		return self.client.auth.sign_in({"email": email, "password": password})

	def auth_get_user(self, access_token: str) -> Any:
		"""Get user info from an access token."""
		return self.client.auth.get_user(access_token)

	# -------------------
	# Storage helpers
	# -------------------
	def storage_upload(self, bucket: str, path: str, file_bytes: bytes, content_type: Optional[str] = None) -> Any:
		"""
		Upload bytes to storage bucket at path.
		- file_bytes: bytes to upload
		"""
		options = {}
		if content_type:
			options["contentType"] = content_type
		return self.client.storage.from_(bucket).upload(path, file_bytes, **options)

	def storage_download(self, bucket: str, path: str) -> Any:
		"""Download object bytes from storage."""
		return self.client.storage.from_(bucket).download(path)

	# -------------------
	# Convenience accessor
	# -------------------
	def raw(self) -> Client:
		"""Return the underlying supabase Client for advanced operations."""
		return self.client