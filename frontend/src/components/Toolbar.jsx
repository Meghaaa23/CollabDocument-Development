function Btn({ onClick, active, disabled, title, children }) {
  return (
    <button
      type="button"
      className={`tb-btn${active ? " active" : ""}`}
      onMouseDown={(e) => e.preventDefault()}
      onClick={onClick}
      disabled={disabled}
      title={title}
    >
      {children}
    </button>
  );
}

export default function Toolbar({ editor, disabled }) {
  if (!editor) return null;

  return (
    <div className="toolbar" role="toolbar" aria-label="Formatting">
      <Btn
        title="Bold (Ctrl+B)"
        disabled={disabled}
        active={editor.isActive("bold")}
        onClick={() => editor.chain().focus().toggleBold().run()}
      >
        <strong>B</strong>
      </Btn>
      <Btn
        title="Italic (Ctrl+I)"
        disabled={disabled}
        active={editor.isActive("italic")}
        onClick={() => editor.chain().focus().toggleItalic().run()}
      >
        <em>I</em>
      </Btn>
      <Btn
        title="Underline (Ctrl+U)"
        disabled={disabled}
        active={editor.isActive("underline")}
        onClick={() => editor.chain().focus().toggleUnderline().run()}
      >
        <u>U</u>
      </Btn>

      <span className="tb-divider" />

      <Btn
        title="Heading 1"
        disabled={disabled}
        active={editor.isActive("heading", { level: 1 })}
        onClick={() => editor.chain().focus().toggleHeading({ level: 1 }).run()}
      >
        H1
      </Btn>
      <Btn
        title="Heading 2"
        disabled={disabled}
        active={editor.isActive("heading", { level: 2 })}
        onClick={() => editor.chain().focus().toggleHeading({ level: 2 }).run()}
      >
        H2
      </Btn>
      <Btn
        title="Normal text"
        disabled={disabled}
        active={editor.isActive("paragraph")}
        onClick={() => editor.chain().focus().setParagraph().run()}
      >
        Text
      </Btn>

      <span className="tb-divider" />

      <Btn
        title="Bulleted list"
        disabled={disabled}
        active={editor.isActive("bulletList")}
        onClick={() => editor.chain().focus().toggleBulletList().run()}
      >
        Bullets
      </Btn>
      <Btn
        title="Numbered list"
        disabled={disabled}
        active={editor.isActive("orderedList")}
        onClick={() => editor.chain().focus().toggleOrderedList().run()}
      >
        Numbered
      </Btn>

      <span className="tb-divider" />

      <Btn
        title="Undo (Ctrl+Z)"
        disabled={disabled || !editor.can().undo()}
        onClick={() => editor.chain().focus().undo().run()}
      >
        Undo
      </Btn>
      <Btn
        title="Redo (Ctrl+Y)"
        disabled={disabled || !editor.can().redo()}
        onClick={() => editor.chain().focus().redo().run()}
      >
        Redo
      </Btn>
    </div>
  );
}
