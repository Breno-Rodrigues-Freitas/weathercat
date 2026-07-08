import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../theme/app_colors.dart';

class SunCycleCard extends StatelessWidget {
  final String nascer;
  final String porSol;

  const SunCycleCard({super.key, required this.nascer, required this.porSol});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [Color(0xFF1A1A2E), Color(0xFF16161F)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        border: Border.all(color: AppColors.cardBorder),
        borderRadius: BorderRadius.circular(14),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text("☀️ CICLO SOLAR",
              style: GoogleFonts.dmSans(color: AppColors.textMuted, fontSize: 11, letterSpacing: 1)),
          const SizedBox(height: 12),
          Row(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Expanded(
                child: Column(
                  children: [
                    const Text("🌅", style: TextStyle(fontSize: 22)),
                    Text(nascer, style: GoogleFonts.syne(color: AppColors.orange, fontSize: 16, fontWeight: FontWeight.w700)),
                    Text("Nascer", style: GoogleFonts.dmSans(color: AppColors.textMuted, fontSize: 10)),
                  ],
                ),
              ),
              Expanded(
                flex: 2,
                child: Container(
                  height: 6,
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(50),
                    gradient: const LinearGradient(
                      colors: [AppColors.orange, AppColors.yellow, AppColors.yellow, AppColors.red],
                    ),
                  ),
                ),
              ),
              Expanded(
                child: Column(
                  children: [
                    const Text("🌇", style: TextStyle(fontSize: 22)),
                    Text(porSol, style: GoogleFonts.syne(color: AppColors.red, fontSize: 16, fontWeight: FontWeight.w700)),
                    Text("Pôr do sol", style: GoogleFonts.dmSans(color: AppColors.textMuted, fontSize: 10)),
                  ],
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
