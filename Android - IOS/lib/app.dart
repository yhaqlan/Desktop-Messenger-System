import 'package:flutter/material.dart';

import 'screens/login_screen.dart';
import 'theme.dart';

class DesktopMessengerMobile extends StatelessWidget {
  const DesktopMessengerMobile({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Desktop Messenger',
      theme: buildDarkTheme(),
      home: const LoginScreen(),
    );
  }
}
