import 'package:flutter/material.dart';

import '../services/local_store.dart';
import 'shell_screen.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final username = TextEditingController();
  final password = TextEditingController();
  bool busy = false;

  Future<void> signIn() async {
    if (username.text.trim().isEmpty || password.text.length < 8) return;
    setState(() => busy = true);
    await LocalStore().saveUsername(username.text.trim());
    if (!mounted) return;
    Navigator.of(context).pushReplacement(MaterialPageRoute(builder: (_) => ShellScreen(username: username.text.trim())));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Center(
          child: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 440),
            child: Padding(
              padding: const EdgeInsets.all(28),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  const Icon(Icons.forum_rounded, size: 72, color: Color(0xFF8B80F5)),
                  const SizedBox(height: 20),
                  Text('Desktop Messenger', textAlign: TextAlign.center, style: Theme.of(context).textTheme.headlineMedium?.copyWith(fontWeight: FontWeight.w800)),
                  const Text('Offline • LAN • Relay', textAlign: TextAlign.center),
                  const SizedBox(height: 32),
                  TextField(controller: username, decoration: const InputDecoration(labelText: 'Username')),
                  const SizedBox(height: 14),
                  TextField(controller: password, obscureText: true, decoration: const InputDecoration(labelText: 'Password (8+ characters)')),
                  const SizedBox(height: 20),
                  FilledButton(onPressed: busy ? null : signIn, child: Text(busy ? 'Opening…' : 'Continue')),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
