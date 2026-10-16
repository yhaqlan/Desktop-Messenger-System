import 'package:flutter/material.dart';

ThemeData buildDarkTheme() {
  const seed = Color(0xFF6C5CE7);
  return ThemeData(
    brightness: Brightness.dark,
    colorScheme: ColorScheme.fromSeed(seedColor: seed, brightness: Brightness.dark),
    scaffoldBackgroundColor: const Color(0xFF0B1020),
    cardTheme: const CardThemeData(color: Color(0xFF11182B), elevation: 0),
    inputDecorationTheme: InputDecorationTheme(
      filled: true,
      fillColor: const Color(0xFF11182B),
      border: OutlineInputBorder(borderRadius: BorderRadius.circular(14)),
    ),
    useMaterial3: true,
  );
}
