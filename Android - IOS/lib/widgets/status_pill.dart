import 'package:flutter/material.dart';

class StatusPill extends StatelessWidget {
  const StatusPill({super.key, required this.label, required this.online});
  final String label;
  final bool online;

  @override
  Widget build(BuildContext context) {
    final color = online ? Colors.greenAccent : Colors.orangeAccent;
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
      decoration: BoxDecoration(color: color.withValues(alpha: 0.12), border: Border.all(color: color), borderRadius: BorderRadius.circular(99)),
      child: Text(label, style: TextStyle(color: color, fontWeight: FontWeight.w700)),
    );
  }
}
