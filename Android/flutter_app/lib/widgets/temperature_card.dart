import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../theme/app_colors.dart';

class TemperatureCard extends StatelessWidget {
  final double temp;
  final double sensacao;

  const TemperatureCard({super.key, required this.temp, required this.sensacao});

  ({Color cor, String label, String emoji}) _faixa(double t) {
    if (t <= 0) return (cor: AppColors.blue, label: "❄️ Gelado", emoji: "🥶");
    if (t <= 10) return (cor: const Color(0xFF74B9FF), label: "🧊 Frio", emoji: "🧥");
    if (t <= 18) return (cor: AppColors.green, label: "🌤️ Fresco", emoji: "😊");
    if (t <= 26) return (cor: AppColors.yellow, label: "☀️ Agradável", emoji: "😎");
    if (t <= 33) return (cor: AppColors.orange, label: "🥵 Quente", emoji: "🌶️");
    return (cor: AppColors.hot, label: "🔥 Muito Quente", emoji: "☄️");
  }

  @override
  Widget build(BuildContext context) {
    final faixa = _faixa(temp);
    const tempMin = -10.0;
    const tempMax = 45.0;
    final progresso = ((temp - tempMin) / (tempMax - tempMin)).clamp(0.0, 1.0);

    return Container(
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: AppColors.card,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: AppColors.cardBorder),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text("🌡️ TEMPERATURA",
                      style: GoogleFonts.dmSans(
                          color: AppColors.textMuted, fontSize: 11, letterSpacing: 1.2)),
                  Row(
                    crossAxisAlignment: CrossAxisAlignment.end,
                    children: [
                      Text("${temp.toStringAsFixed(0)}",
                          style: GoogleFonts.syne(
                              color: faixa.cor, fontSize: 40, fontWeight: FontWeight.w800)),
                      Padding(
                        padding: const EdgeInsets.only(bottom: 6, left: 4),
                        child: Text("°C",
                            style: GoogleFonts.syne(
                                color: const Color(0xFF444466),
                                fontSize: 18,
                                fontWeight: FontWeight.w700)),
                      ),
                    ],
                  ),
                  Text("🤔 Sensação: ${sensacao.toStringAsFixed(0)}°C",
                      style: GoogleFonts.dmSans(color: AppColors.textFaint, fontSize: 12)),
                ],
              ),
              Column(
                children: [
                  Text(faixa.emoji, style: const TextStyle(fontSize: 30)),
                  const SizedBox(height: 4),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                    decoration: BoxDecoration(
                      color: faixa.cor.withOpacity(0.13),
                      borderRadius: BorderRadius.circular(50),
                    ),
                    child: Text(faixa.label,
                        style: GoogleFonts.dmSans(
                            color: faixa.cor, fontSize: 11, fontWeight: FontWeight.w700)),
                  ),
                ],
              ),
            ],
          ),
          const SizedBox(height: 14),
          ClipRRect(
            borderRadius: BorderRadius.circular(50),
            child: LinearProgressIndicator(
              value: progresso,
              minHeight: 10,
              backgroundColor: AppColors.cardBorder,
              valueColor: AlwaysStoppedAnimation(faixa.cor),
            ),
          ),
          const SizedBox(height: 6),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text("Muito frio", style: GoogleFonts.dmSans(color: const Color(0xFF333350), fontSize: 10)),
              Text("Ideal", style: GoogleFonts.dmSans(color: const Color(0xFF333350), fontSize: 10)),
              Text("Quente", style: GoogleFonts.dmSans(color: const Color(0xFF333350), fontSize: 10)),
            ],
          ),
        ],
      ),
    );
  }
}
