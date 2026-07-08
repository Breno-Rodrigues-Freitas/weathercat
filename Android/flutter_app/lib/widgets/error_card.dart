import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../theme/app_colors.dart';

class ErrorCard extends StatelessWidget {
  final String cidade;
  final String erro;

  const ErrorCard({super.key, required this.cidade, required this.erro});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 32, horizontal: 24),
      decoration: BoxDecoration(
        color: AppColors.card,
        border: Border.all(color: const Color(0xFF3A1A1A)),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Column(
        children: [
          const Text("😿", style: TextStyle(fontSize: 56)),
          const SizedBox(height: 12),
          Text("Cidade não encontrada",
              style: GoogleFonts.syne(color: AppColors.red, fontSize: 20, fontWeight: FontWeight.w800)),
          const SizedBox(height: 8),
          Text.rich(
            TextSpan(
              style: GoogleFonts.dmSans(color: const Color(0xFF9999CC), fontSize: 13),
              children: [
                const TextSpan(text: "Não consegui encontrar "),
                TextSpan(text: '"$cidade"', style: const TextStyle(color: Color(0xFFE8E8F8), fontWeight: FontWeight.bold)),
                const TextSpan(text: " no mapa 🗺️"),
              ],
            ),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 20),
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(14),
            decoration: BoxDecoration(
              color: const Color(0xFF1E1010),
              border: Border.all(color: const Color(0xFF3A1A1A)),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text("💡 DICAS", style: GoogleFonts.dmSans(color: AppColors.textMuted, fontSize: 10, letterSpacing: 1)),
                const SizedBox(height: 8),
                Text("• Verifique a ortografia da cidade\n• Tente em inglês: São Paulo → Sao Paulo\n• Use o nome completo: Rio → Rio de Janeiro",
                    style: GoogleFonts.dmSans(color: const Color(0xFFAAAACC), fontSize: 12, height: 1.7)),
              ],
            ),
          ),
          const SizedBox(height: 16),
          Text("Erro: $erro", style: GoogleFonts.dmSans(color: AppColors.textFaint, fontSize: 11)),
        ],
      ),
    );
  }
}
