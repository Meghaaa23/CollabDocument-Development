CollabDocs – Project Submission

Name: Meghana Konka  
Tech Stack: FastAPI, React, Vite, TipTap, SQLAlchemy, SQLite, Docker

# About the Project

CollabDocs is a lightweight collaborative document editor where users can create, edit, save, and share documents with others.

The goal was to build a simple document editor with the essential features you'd expect from a collaborative application, including rich-text editing, automatic saving, file uploads, and document-sharing permissions.

# What's Included

The submission includes the complete source code for both the backend and frontend.

- `backend/` – FastAPI backend and API implementation.
- `frontend/` – React application built with Vite.
- `README.md` – Instructions to install and run the application locally.
- `ARCHITECTURE.md` – Overview of the application structure and technical decisions.
- `AI_WORKFLOW.md` – Details about how AI tools were used during development.
- `backend/tests/test_api.py` – Automated backend tests.
- `Dockerfile` and `render.yaml` – Deployment configuration.
- `docs/screenshots/` – Screenshots of the application.
- `VIDEO_LINK.txt` – Walkthrough video link.

# Live Application

The application is deployed and available here:

**https://collabdocs-untf.onrender.com**

It's hosted on Render's free tier, so the first request after a period of inactivity may take around 30–50 seconds to load. After that, it should respond normally.

# Demo Accounts

All accounts use the password: `demo1234`.

- **alice@example.com** – Account with sample documents.
- **bob@example.com** – Account with access to a shared document.
- **carol@example.com** – Empty account for testing document sharing.

# How to Test Document Sharing

You can test the sharing functionality using the following steps:

1. Log in as Alice.
2. Open the document **Welcome to CollabDocs**.
3. Click Share and enter `carol@example.com`.
4. Grant Carol access to the document.
5. Log out and sign in as Carol.
6. You should now see the document under **Shared with me**.

Document permissions are checked on the backend. A user with view access cannot edit or delete the document. A user with edit access can make changes but cannot delete a document owned by someone else.

# Implemented Features

The application currently supports:

- Creating, editing, renaming, saving, and reopening documents.
- Automatic saving of changes.
- Rich-text formatting, including bold, italic, underline, headings, and lists.
- Undo and redo functionality.
- Uploading `.txt`, `.md`, and `.docx` files as editable documents.
- Sharing documents with view or edit permissions.
- Separate sections for personal and shared documents.
- Preserving document content and formatting after refreshing the page.
- Input validation, error handling, and HTML sanitization for XSS protection.

I also added automated backend tests. All 8 tests are currently passing with `pytest -q`.

# What's Not Included Yet

Real-time collaboration, such as live editing by multiple users and live cursors, is not implemented in this version. Currently, users can share documents, make changes, and access the saved content when they reopen the document.

I also haven't implemented user registration, password reset, document version history, or PDF export. The application uses predefined demo accounts, and I focused on completing the core editing and sharing functionality first.

# What I Would Improve Next

Given a little more development time, I would work on real-time synchronization using WebSockets or Yjs, add PDF and Markdown export, and introduce document version history.

I would also add Playwright end-to-end tests to cover the complete workflow between users, especially document sharing and permission handling.

For more details about the implementation and technical decisions, please refer to `ARCHITECTURE.md`.