import 'package:flutter/material.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key, required this.username});
  final String username;

  @override
  Widget build(BuildContext context) {
    return ListView(padding: const EdgeInsets.all(20), children: [
      const Text('Settings', style: TextStyle(fontSize: 26, fontWeight: FontWeight.w800)),
      ListTile(leading: const Icon(Icons.person_outline), title: Text(username), subtitle: const Text('Local companion identity')),
      SwitchListTile(value: true, onChanged: (_) {}, title: const Text('Dark theme')),
      SwitchListTile(value: true, onChanged: (_) {}, title: const Text('Show synchronization status')),
      const ListTile(leading: Icon(Icons.info_outline), title: Text('Source-only companion'), subtitle: Text('Build and protocol validation are still required.')),
    ]);
  }
}
