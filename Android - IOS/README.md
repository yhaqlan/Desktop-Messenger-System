# Desktop Messenger Mobile Companion - Flutter Source

This folder mirrors the mobile-deliverable category in the reference archive with Desktop Messenger content. It is a source-only Flutter companion that presents login, chats, friends, network, and settings screens and stores basic preferences locally.

The Flutter SDK was not available in the generation environment, so no Android APK or iOS archive is claimed. Run `flutter create .` in this directory to regenerate platform scaffolds if needed, then run `flutter pub get`, `flutter analyze`, and platform builds on a configured development machine.

The Windows Python client remains the primary project. The mobile source does not claim full parity with desktop synchronization or cryptographic key lifecycle until it is integrated and tested against the same protocol.
