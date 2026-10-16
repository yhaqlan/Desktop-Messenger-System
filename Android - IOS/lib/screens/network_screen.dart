import 'package:flutter/material.dart';

class NetworkScreen extends StatelessWidget {
  const NetworkScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return ListView(padding: const EdgeInsets.all(20), children: [
      const Text('Network', style: TextStyle(fontSize: 26, fontWeight: FontWeight.w800)),
      const SizedBox(height: 14),
      Card(child: ListTile(leading: const Icon(Icons.wifi_tethering), title: const Text('LAN / Hotspot'), subtitle: const Text('Desktop host IPv4 • port 8765'), trailing: FilledButton(onPressed: () {}, child: const Text('Configure')))),
      Card(child: ListTile(leading: const Icon(Icons.cloud_outlined), title: const Text('Internet Relay'), subtitle: const Text('Reachable server • port 9876'), trailing: FilledButton(onPressed: () {}, child: const Text('Configure')))),
      const Card(child: Padding(padding: EdgeInsets.all(16), child: Text('127.0.0.1 is the current device. It is not a remote public server.'))),
    ]);
  }
}
