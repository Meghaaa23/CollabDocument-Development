# AI Workflow – CollabDocs

## How I Used AI

I used Claude Code (Opus) through the Claude desktop app while developing CollabDocs. I mainly used it to speed up coding, generate repetitive code, help with debugging, and write initial drafts of tests and documentation.

I treated Claude as a coding assistant rather than relying on it to make all the decisions. I reviewed the generated code, made changes where needed, and tested the application locally to make sure everything worked.

## Where AI Helped

Claude helped me set up the initial FastAPI backend and React frontend. It generated parts of the SQLAlchemy models, Pydantic schemas, API routes, frontend components, CSS, and Docker configuration.

It was also useful when implementing the TipTap editor, especially the toolbar and autosave functionality. There were a few details to handle, such as keeping the editor focused when clicking formatting buttons and making sure autosave didn't trigger unnecessarily when loading an existing document.

I also used Claude to draft the initial pytest cases and documentation. I reviewed these and made changes based on what I had actually implemented.

Overall, AI helped me spend less time writing repetitive code and more time working on the application's functionality.

## Decisions I Made During Development

I made the main decisions about the application's architecture and which features to prioritize.

For example, I decided to focus on document editing, saving, uploading, and sharing instead of implementing real-time collaboration. Live editing would have required additional time and testing, so I kept it outside the scope of this version.

I chose to store document content as HTML to preserve rich-text formatting. I used SQLite for simplicity while keeping the database layer structured so it could be moved to PostgreSQL later if needed.

I also kept the document permission checks in a separate `access.py` module so the same rules could be applied across different API endpoints.

For documents that a user cannot access, the API returns a 404 response instead of exposing whether the document exists.

## Security and Code Review

One area I paid particular attention to was handling document content safely.

Since users can enter rich text and upload `.docx` files, I wanted to make sure potentially unsafe HTML could not be stored and rendered directly.

I added HTML sanitization in `sanitize.py` to remove unsafe elements while preserving supported formatting.

I also included a test to verify that a `<script>` tag is removed when saving document content.

For document sharing, I made sure permissions were enforced on the backend rather than relying only on disabled buttons in the frontend.

For example, users with view access cannot edit or delete documents, and users with edit access cannot delete documents owned by someone else.

## Testing and Verification

I used `pytest`, `uvicorn`, and Vite to run and test the application locally.

During the first test run, I encountered an issue with the demo account email addresses. The Pydantic `EmailStr` validation rejected the `.test` domains I had initially used, which caused login requests to return a 422 error.

After identifying the issue, I changed the demo accounts to use `@example.com` addresses and ran the tests again.

All **8 backend tests passed** after the fix.

I also tested the application manually in a browser using the production build, where FastAPI serves the React frontend.

I checked the main user flows, including logging in, creating and opening documents, applying rich-text formatting, saving changes, and sharing documents with another user.

I also verified that owned documents and shared documents appeared in their respective sections.

Screenshots from the application are available in `docs/screenshots/`.

Apart from functionality, I added input validation, file size and type restrictions for uploads, error handling, and a `/api/health` endpoint for deployment checks.

## What I Learned

Using AI helped me complete the initial implementation much faster, especially when working across the backend and frontend.

However, I still needed to review the generated code, fix issues, and verify that the application behaved as expected.

The email validation issue was a good example. The generated code looked fine initially, but running the tests revealed a problem that needed to be fixed.

I found AI most useful for generating code and helping with implementation details, while decisions about architecture, security, testing, and feature priorities still required my own judgment.

For this project, I focused on using AI where it saved development time without skipping code review or testing.