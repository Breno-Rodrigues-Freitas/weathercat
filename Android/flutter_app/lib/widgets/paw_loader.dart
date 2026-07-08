import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../theme/app_colors.dart';

class PawLoader extends StatefulWidget {
  const PawLoader({super.key});

  @override
  State<PawLoader> createState() => _PawLoaderState();
}

class _PawLoaderState extends State<PawLoader> with SingleTickerProviderStateMixin {
  late final AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this, duration: const Duration(milliseconds: 1000))..repeat();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Widget _paw(double delay) {
    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        final t = (_controller.value + delay) % 1.0;
        final bounce = -10 * (t < 0.5 ? (t * 2) : (2 - t * 2));
        final opacity = 1.0 - 0.6 * (t < 0.5 ? (t * 2) : (2 - t * 2));
        return Transform.translate(
          offset: Offset(0, bounce),
          child: Opacity(opacity: opacity, child: child),
        );
      },
      child: const Text("🐾", style: TextStyle(fontSize: 28)),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 40),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              _paw(0.0),
              const SizedBox(width: 14),
              _paw(0.2),
              const SizedBox(width: 14),
              _paw(0.4),
            ],
          ),
          const SizedBox(height: 20),
          Text("CONSULTANDO O TEMPO...",
              style: GoogleFonts.syne(color: AppColors.yellow, fontSize: 15, fontWeight: FontWeight.w700, letterSpacing: 1)),
          const SizedBox(height: 4),
          Text("O gato está farejando as nuvens ☁️",
              style: GoogleFonts.dmSans(color: AppColors.textFaint, fontSize: 12)),
        ],
      ),
    );
  }
}
