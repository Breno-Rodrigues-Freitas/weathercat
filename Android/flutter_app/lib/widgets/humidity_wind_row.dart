import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import '../theme/app_colors.dart';

class HumidityWindRow extends StatelessWidget {
  final int umidade;
  final double vento;

  const HumidityWindRow({super.key, required this.umidade, required this.vento});

  Widget _badge({required String emoji, required String titulo, required String valor, required Color cor, required String label}) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 10),
        decoration: BoxDecoration(
          color: AppColors.card,
          border: Border.all(color: AppColors.cardBorder),
          borderRadius: BorderRadius.circular(14),
        ),
        child: Column(
          children: [
            Text(emoji, style: const TextStyle(fontSize: 22)),
            const SizedBox(height: 4),
            Text(titulo, style: GoogleFonts.dmSans(color: AppColors.textMuted, fontSize: 10, letterSpacing: 1)),
            Text(valor, style: GoogleFonts.syne(color: cor, fontSize: 18, fontWeight: FontWeight.w700)),
            const SizedBox(height: 4),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
              decoration: BoxDecoration(color: cor.withOpacity(0.13), borderRadius: BorderRadius.circular(50)),
              child: Text(label, style: GoogleFonts.dmSans(color: cor, fontSize: 10, fontWeight: FontWeight.w600)),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    Color corUmid; String labelUmid;
    if (umidade < 30) { corUmid = AppColors.red; labelUmid = "Seco"; }
    else if (umidade < 60) { corUmid = AppColors.yellow; labelUmid = "Agradável"; }
    else { corUmid = AppColors.blue; labelUmid = "Úmido"; }

    Color corVento; String labelVento;
    if (vento < 3) { corVento = AppColors.blue; labelVento = "Calmo"; }
    else if (vento < 8) { corVento = AppColors.yellow; labelVento = "Moderado"; }
    else { corVento = AppColors.red; labelVento = "Forte"; }

    return Row(
      children: [
        _badge(emoji: "💧", titulo: "UMIDADE", valor: "$umidade%", cor: corUmid, label: labelUmid),
        const SizedBox(width: 10),
        _badge(emoji: "💨", titulo: "VENTO", valor: "${vento.toStringAsFixed(1)} m/s", cor: corVento, label: labelVento),
      ],
    );
  }
}
