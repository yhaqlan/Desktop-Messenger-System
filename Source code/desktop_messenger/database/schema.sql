PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

CREATE TABLE IF NOT EXISTS app_meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

INSERT OR IGNORE INTO app_meta(key, value) VALUES ('schema_version', '1');

CREATE TABLE IF NOT EXISTS users (
    user_uuid TEXT PRIMARY KEY,
    username TEXT NOT NULL COLLATE NOCASE UNIQUE,
    display_name TEXT NOT NULL,
    email TEXT COLLATE NOCASE UNIQUE,
    password_hash TEXT NOT NULL,
    profile_image_path TEXT,
    public_key BLOB NOT NULL,
    protected_private_key TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    deleted_at TEXT
);

CREATE TABLE IF NOT EXISTS devices (
    device_uuid TEXT PRIMARY KEY,
    user_uuid TEXT NOT NULL REFERENCES users(user_uuid) ON DELETE CASCADE,
    device_name TEXT NOT NULL,
    public_key BLOB,
    created_at TEXT NOT NULL,
    last_seen_at TEXT
);

CREATE TABLE IF NOT EXISTS sessions (
    session_uuid TEXT PRIMARY KEY,
    user_uuid TEXT NOT NULL REFERENCES users(user_uuid) ON DELETE CASCADE,
    device_uuid TEXT REFERENCES devices(device_uuid) ON DELETE SET NULL,
    token_hash TEXT NOT NULL,
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL,
    revoked_at TEXT
);

CREATE TABLE IF NOT EXISTS friend_requests (
    request_uuid TEXT PRIMARY KEY,
    sender_user_uuid TEXT NOT NULL REFERENCES users(user_uuid) ON DELETE CASCADE,
    receiver_user_uuid TEXT NOT NULL REFERENCES users(user_uuid) ON DELETE CASCADE,
    status TEXT NOT NULL CHECK (status IN ('pending', 'accepted', 'rejected', 'cancelled')),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    CHECK (sender_user_uuid <> receiver_user_uuid),
    UNIQUE(sender_user_uuid, receiver_user_uuid)
);

CREATE TABLE IF NOT EXISTS friendships (
    friendship_uuid TEXT PRIMARY KEY,
    user_low_uuid TEXT NOT NULL REFERENCES users(user_uuid) ON DELETE CASCADE,
    user_high_uuid TEXT NOT NULL REFERENCES users(user_uuid) ON DELETE CASCADE,
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'removed', 'blocked')),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    CHECK (user_low_uuid < user_high_uuid),
    UNIQUE(user_low_uuid, user_high_uuid)
);

CREATE TABLE IF NOT EXISTS chats (
    chat_uuid TEXT PRIMARY KEY,
    chat_type TEXT NOT NULL DEFAULT 'direct' CHECK (chat_type IN ('direct', 'group')),
    title TEXT,
    created_by_uuid TEXT NOT NULL REFERENCES users(user_uuid),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS chat_members (
    chat_uuid TEXT NOT NULL REFERENCES chats(chat_uuid) ON DELETE CASCADE,
    user_uuid TEXT NOT NULL REFERENCES users(user_uuid) ON DELETE CASCADE,
    role TEXT NOT NULL DEFAULT 'member' CHECK (role IN ('owner', 'member')),
    joined_at TEXT NOT NULL,
    left_at TEXT,
    PRIMARY KEY(chat_uuid, user_uuid)
);

CREATE TABLE IF NOT EXISTS messages (
    message_uuid TEXT PRIMARY KEY,
    chat_uuid TEXT NOT NULL REFERENCES chats(chat_uuid) ON DELETE CASCADE,
    sender_user_uuid TEXT NOT NULL REFERENCES users(user_uuid),
    sender_device_uuid TEXT REFERENCES devices(device_uuid) ON DELETE SET NULL,
    ciphertext BLOB NOT NULL,
    nonce BLOB NOT NULL,
    algorithm TEXT NOT NULL DEFAULT 'AES-256-GCM',
    status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'sent', 'delivered', 'read', 'failed', 'deleted')),
    client_created_at TEXT NOT NULL,
    server_received_at TEXT,
    edited_at TEXT,
    deleted_at TEXT,
    reply_to_message_uuid TEXT REFERENCES messages(message_uuid) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS message_receipts (
    message_uuid TEXT NOT NULL REFERENCES messages(message_uuid) ON DELETE CASCADE,
    user_uuid TEXT NOT NULL REFERENCES users(user_uuid) ON DELETE CASCADE,
    receipt_type TEXT NOT NULL CHECK (receipt_type IN ('delivered', 'read')),
    received_at TEXT NOT NULL,
    PRIMARY KEY(message_uuid, user_uuid, receipt_type)
);

CREATE TABLE IF NOT EXISTS attachments (
    attachment_uuid TEXT PRIMARY KEY,
    message_uuid TEXT NOT NULL REFERENCES messages(message_uuid) ON DELETE CASCADE,
    original_name TEXT NOT NULL,
    media_type TEXT,
    byte_size INTEGER NOT NULL CHECK (byte_size >= 0),
    sha256 TEXT NOT NULL,
    encrypted_path TEXT NOT NULL,
    nonce BLOB NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS notifications (
    notification_uuid TEXT PRIMARY KEY,
    user_uuid TEXT NOT NULL REFERENCES users(user_uuid) ON DELETE CASCADE,
    actor_user_uuid TEXT REFERENCES users(user_uuid) ON DELETE SET NULL,
    notification_type TEXT NOT NULL,
    related_entity_uuid TEXT,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    is_read INTEGER NOT NULL DEFAULT 0 CHECK (is_read IN (0, 1)),
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS settings (
    user_uuid TEXT NOT NULL REFERENCES users(user_uuid) ON DELETE CASCADE,
    setting_key TEXT NOT NULL,
    setting_value TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    PRIMARY KEY(user_uuid, setting_key)
);

CREATE TABLE IF NOT EXISTS peer_connections (
    peer_uuid TEXT PRIMARY KEY,
    transport TEXT NOT NULL CHECK (transport IN ('lan', 'relay')),
    address TEXT NOT NULL,
    port INTEGER NOT NULL CHECK (port BETWEEN 1 AND 65535),
    peer_public_key BLOB,
    first_seen_at TEXT NOT NULL,
    last_seen_at TEXT NOT NULL,
    trusted INTEGER NOT NULL DEFAULT 0 CHECK (trusted IN (0, 1))
);

CREATE TABLE IF NOT EXISTS pending_operations (
    operation_uuid TEXT PRIMARY KEY,
    owner_user_uuid TEXT NOT NULL REFERENCES users(user_uuid) ON DELETE CASCADE,
    device_uuid TEXT REFERENCES devices(device_uuid) ON DELETE SET NULL,
    operation_type TEXT NOT NULL,
    entity_uuid TEXT NOT NULL,
    payload_json TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'inflight', 'completed', 'failed')),
    attempt_count INTEGER NOT NULL DEFAULT 0,
    next_retry_at TEXT,
    last_error TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS applied_operations (
    operation_uuid TEXT PRIMARY KEY,
    source_peer_uuid TEXT,
    applied_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sync_state (
    peer_uuid TEXT NOT NULL,
    entity_type TEXT NOT NULL,
    last_cursor TEXT,
    last_sync_at TEXT,
    PRIMARY KEY(peer_uuid, entity_type)
);

CREATE TABLE IF NOT EXISTS sync_log (
    sync_uuid TEXT PRIMARY KEY,
    peer_uuid TEXT,
    direction TEXT NOT NULL CHECK (direction IN ('push', 'pull', 'bidirectional')),
    operation_count INTEGER NOT NULL DEFAULT 0,
    status TEXT NOT NULL CHECK (status IN ('started', 'completed', 'failed')),
    error_text TEXT,
    started_at TEXT NOT NULL,
    completed_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_friend_requests_receiver_status ON friend_requests(receiver_user_uuid, status);
CREATE INDEX IF NOT EXISTS idx_friendships_low ON friendships(user_low_uuid, status);
CREATE INDEX IF NOT EXISTS idx_friendships_high ON friendships(user_high_uuid, status);
CREATE INDEX IF NOT EXISTS idx_messages_chat_created ON messages(chat_uuid, client_created_at);
CREATE INDEX IF NOT EXISTS idx_notifications_user_read ON notifications(user_uuid, is_read, created_at);
CREATE INDEX IF NOT EXISTS idx_pending_status_retry ON pending_operations(status, next_retry_at);
