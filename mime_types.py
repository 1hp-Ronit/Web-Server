import os

EXTENSION_TO_CONTENT_TYPE = {
    # Text
    ".txt":  "text/plain",
    ".html": "text/html",
    ".htm":  "text/html",
    ".css":  "text/css",
    ".csv":  "text/csv",
    ".xml":  "text/xml",
    ".md":   "text/markdown",

    # JavaScript / JSON
    ".js":   "application/javascript",
    ".mjs":  "application/javascript",
    ".json": "application/json",

    # Images
    ".jpg":  "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png":  "image/png",
    ".gif":  "image/gif",
    ".webp": "image/webp",
    ".svg":  "image/svg+xml",
    ".ico":  "image/x-icon",
    ".bmp":  "image/bmp",
    ".tiff": "image/tiff",
    ".tif":  "image/tiff",

    # Audio
    ".mp3":  "audio/mpeg",
    ".wav":  "audio/wav",
    ".ogg":  "audio/ogg",
    ".flac": "audio/flac",
    ".aac":  "audio/aac",
    ".m4a":  "audio/mp4",

    # Video
    ".mp4":  "video/mp4",
    ".webm": "video/webm",
    ".ogv":  "video/ogg",
    ".avi":  "video/x-msvideo",
    ".mov":  "video/quicktime",
    ".mkv":  "video/x-matroska",

    # Documents
    ".pdf":  "application/pdf",
    ".doc":  "application/msword",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".xls":  "application/vnd.ms-excel",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".ppt":  "application/vnd.ms-powerpoint",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".odt":  "application/vnd.oasis.opendocument.text",
    ".ods":  "application/vnd.oasis.opendocument.spreadsheet",
    ".odp":  "application/vnd.oasis.opendocument.presentation",

    # Archives
    ".zip":  "application/zip",
    ".tar":  "application/x-tar",
    ".gz":   "application/gzip",
    ".bz2":  "application/x-bzip2",
    ".7z":   "application/x-7z-compressed",
    ".rar":  "application/x-rar-compressed",

    # Fonts
    ".ttf":  "font/ttf",
    ".otf":  "font/otf",
    ".woff": "font/woff",
    ".woff2":"font/woff2",
    ".eot":  "application/vnd.ms-fontobject",

    # Data / Config
    ".yaml": "application/yaml",
    ".yml":  "application/yaml",
    ".toml": "application/toml",
    ".ini":  "text/plain",
    ".env":  "text/plain",

    # Code (served as text)
    ".py":   "text/x-python",
    ".ts":   "text/typescript",
    ".jsx":  "text/jsx",
    ".tsx":  "text/tsx",
    ".sh":   "application/x-sh",
    ".bat":  "application/x-bat",
    ".rs":   "text/x-rustsrc",
    ".go":   "text/x-go",
    ".java": "text/x-java-source",
    ".c":    "text/x-csrc",
    ".cpp":  "text/x-c++src",
    ".h":    "text/x-chdr",
    ".rb":   "text/x-ruby",
    ".php":  "application/x-httpd-php",

    # Binary / Other
    ".bin":  "application/octet-stream",
    ".exe":  "application/octet-stream",
    ".dll":  "application/octet-stream",
    ".so":   "application/octet-stream",
    ".wasm": "application/wasm",
    ".map":  "application/json",
}

def get_content_type(path: str)-> str:
    _, extension = os.path.splitext(path)
    
    return EXTENSION_TO_CONTENT_TYPE.get(extension.lower(), 'application/octet-stream')

