// lib/main.dart

import 'package:flutter/material.dart';
import 'screens/login_screen.dart';

void main() {
  runApp(const DevDhamApp());
}

class DevDhamApp extends StatelessWidget {
  const DevDhamApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'DevDham Path',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        colorSchemeSeed: Colors.orange,
        fontFamily: 'Roboto',
      ),
      home: const LoginScreen(),
    );
  }
}