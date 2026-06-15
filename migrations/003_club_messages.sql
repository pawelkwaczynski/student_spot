CREATE TABLE IF NOT EXISTS club_messages (
    id INTEGER PRIMARY KEY,
    club_id INTEGER NOT NULL,
    sender_id INTEGER NOT NULL,
    subject VARCHAR(180) NOT NULL,
    body TEXT NOT NULL,
    created_at DATETIME NOT NULL,
    FOREIGN KEY(club_id) REFERENCES clubs (id),
    FOREIGN KEY(sender_id) REFERENCES users (id)
);

CREATE INDEX IF NOT EXISTS ix_club_messages_club_id ON club_messages (club_id);
CREATE INDEX IF NOT EXISTS ix_club_messages_sender_id ON club_messages (sender_id);
CREATE INDEX IF NOT EXISTS ix_club_messages_created_at ON club_messages (created_at);

CREATE TABLE IF NOT EXISTS club_message_recipients (
    id INTEGER PRIMARY KEY,
    message_id INTEGER NOT NULL,
    recipient_id INTEGER NOT NULL,
    read_at DATETIME,
    created_at DATETIME NOT NULL,
    CONSTRAINT uq_message_recipient UNIQUE (message_id, recipient_id),
    FOREIGN KEY(message_id) REFERENCES club_messages (id),
    FOREIGN KEY(recipient_id) REFERENCES users (id)
);

CREATE INDEX IF NOT EXISTS ix_club_message_recipients_message_id ON club_message_recipients (message_id);
CREATE INDEX IF NOT EXISTS ix_club_message_recipients_recipient_id ON club_message_recipients (recipient_id);
