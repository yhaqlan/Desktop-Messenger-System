import 'package:flutter/material.dart';

class FriendsScreen extends StatelessWidget {
  const FriendsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(20),
      child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
        const Text('Friends', style: TextStyle(fontSize: 26, fontWeight: FontWeight.w800)),
        const SizedBox(height: 14),
        const TextField(decoration: InputDecoration(prefixIcon: Icon(Icons.search), hintText: 'Search by username')),
        const SizedBox(height: 24),
        Expanded(child: Card(child: Center(child: Text('Friend requests require a connected desktop/relay service.', textAlign: TextAlign.center)))),
      ]),
    );
  }
}
