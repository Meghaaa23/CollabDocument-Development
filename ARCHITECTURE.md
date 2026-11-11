# Architecture – CollabDocs

## Overview

CollabDocs is built using FastAPI for the backend and React with Vite for the frontend. TipTap is used for document editing, while SQLAlchemy and SQLite handle data storage.

While building the application, I focused mainly on three areas: providing a proper document editing experience, making sure document sharing works correctly, and handling user content safely.

## Main Areas of Focus

**1. Document Editing**

I wanted to provide an actual rich-text editing experience instead of using a basic text area. I chose TipTap because it provides the formatting features needed for this application without having to build an editor from scratch.

Users can apply bold, italic, and underline formatting, add headings, create bullet and numbered lists, and use undo and redo. I also implemented autosave so that changes are saved automatically without requiring users to click a Save button every time.

**2. Document Sharing and Permissions**

Sharing was another important part of the application. Users can share their documents with others and provide either view or edit access.

I implemented the permission checks on the backend and kept them centralized in `access.py`. This ensures that permissions are checked consistently across the different API endpoints instead of depending only on frontend restrictions.

The dashboard also separates documents owned by the user from documents shared with them.

**3. Handling Document Content Safely**

Since users can enter formatted content and upload files, I wanted to make sure unsafe HTML was not stored and displayed directly.

I added an allow-list-based HTML sanitizer in `sanitize.py`. It removes unsupported or potentially unsafe elements while preserving the formatting supported by the editor.

## Application Structure

The application has two main parts:

- **Frontend:** React, Vite, and TipTap handle the user interface and document editing.
- **Backend:** FastAPI handles authentication, document operations, uploads, and sharing permissions.

The backend is organized into separate routers for authentication and document-related operations. Supporting modules handle access control, HTML sanitization, and file imports.

SQLAlchemy manages communication with the database. SQLite is used by default, but the application can also be configured to use PostgreSQL through the `DATABASE_URL` environment variable.

In production, FastAPI serves both the API endpoints and the built React application from a single container. This keeps deployment simple and avoids having to manage separate frontend and backend services.

During local development, the frontend runs through Vite and sends API requests to the FastAPI backend.

## Technical Decisions

**TipTap for the editor**

I chose TipTap because it provides the rich-text functionality needed for the application and is built on top of ProseMirror. It also produces HTML that can be sanitized and stored.

**HTML for document storage**

I decided to store document content as HTML rather than ProseMirror JSON. This makes it easier to render the content when reopening documents and provides a straightforward path for adding export functionality later.

**SQLite with PostgreSQL support**

SQLite keeps the initial setup simple. Reviewers can run the application locally without setting up an additional database server. I also kept the database configuration flexible so PostgreSQL can be used by changing the connection string.

**JWT-based authentication**

I used predefined demo accounts instead of implementing a complete registration system. Passwords are hashed, and users receive signed JWT tokens after logging in. The backend uses these tokens to identify users and check their permissions.

**Autosave**

Document changes are saved through a debounced PATCH request. This avoids sending a request for every keystroke while ensuring that changes are saved automatically.

**Centralized access control**

All document permission checks are handled through `access.py`. This makes it easier to maintain and test the rules in one place.

I also chose to return a 404 response when a user tries to access a document they don't have permission to view. This avoids revealing whether a particular document exists.

## How Document Permissions Work

There are three levels of access in the application.

- **Owner:** Can edit, rename, share, and delete the document.
- **Edit access:** Can view and modify document content but cannot delete the document or manage sharing.
- **View access:** Can open and read the document but cannot make changes.

If a user has no access to a document, the backend returns a 404 response.

These restrictions are enforced by the API, so changing frontend elements or sending requests directly cannot bypass the permission checks.

## Database Structure

The application currently uses three main database models.

**User:** Stores the user's ID, email, name, and hashed password.

**Document:** Stores the document ID, title, HTML content, owner ID, and creation and update timestamps.

**Share:** Connects a document with another user and stores their permission level (view or edit).

A unique constraint on the document and user combination prevents duplicate sharing entries for the same user.

## Security and Testing

I added validation for API requests using Pydantic schemas. File uploads are checked for supported formats and size limits before being processed.

For authentication, passwords are hashed using PBKDF2-SHA256, and JWT tokens are used for authenticated sessions.

Document content is sanitized before storage to reduce the risk of stored XSS attacks.

I also added automated tests covering the important application flows, particularly document sharing, permission restrictions, file uploads, and HTML sanitization.

The current test suite contains 8 tests, and all of them pass.

To run the tests locally:

`pytest -q`

## Features Not Included in This Version

I focused on completing the main editing and sharing functionality within the available development time. Some additional features were left out intentionally.

**Real-time collaboration:** Multiple users cannot currently edit the same document and see changes instantly. The current implementation uses autosave, so users can access the latest saved content when they reopen a document. Real-time synchronization would require an additional WebSocket-based solution or a framework such as Yjs.

**User registration and password recovery:** The application currently uses predefined demo accounts. Registration, email verification, and password reset are not implemented.

**Advanced permissions:** Only view and edit access are supported. More detailed permission levels could be added later.

**Version history and PDF export:** These were left out of the current implementation but could be added using the existing document storage structure.

## Possible Next Steps

If I had another few hours to work on the application, I would start with real-time collaboration using WebSockets or Yjs. This would allow multiple users to work on the same document and see updates without refreshing.

After that, I would add document export options, version history, and a registration flow.

I would also add Playwright end-to-end tests to verify the complete sharing process, including logging in as different users and checking their respective permissions.

Overall, I focused on getting the core functionality working properly, keeping the code organized, and making sure important operations such as document sharing and access control are handled on the backend.