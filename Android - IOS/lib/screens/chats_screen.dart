import 'package:flutter/material.dart';

class ChatsScreen extends StatelessWidget {
  const ChatsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return ListView(padding: const EdgeInsets.all(20), children: const [
      Text('Chats', style: TextStyle(fontSize: 26, fontWeight: FontWeight.w800)),
      SizedBox(height: 8),
      Text('No synchronized conversations on this device.'),
      SizedBox(height: 24),
      Card(child: Padding(padding: EdgeInsets.all(28), child: Column(children: [Icon(Icons.lock_outline, size: 46), SizedBox(height: 12), Text('Encrypted direct conversations will appear here after protocol integration.', textAlign: TextAlign.center)]))),
    ]);
  }
}
