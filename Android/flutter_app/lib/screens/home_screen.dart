import 'dart:async';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:intl/intl.dart';

import '../models/weather_mood.dart';
import '../services/weather_service.dart';
import '../theme/app_colors.dart';
import '../widgets/temperature_card.dart';
import '../widgets/humidity_wind_row.dart';
import '../widgets/sun_cycle_card.dart';
import '../widgets/paw_loader.dart';
import '../widgets/error_card.dart';

enum _ViewState { idle, loading, success, error }

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final _controller = TextEditingController();
  final _service = WeatherService();

  _ViewState _state = _ViewState.idle;
  WeatherMood? _dados;
  String _cidadeConsultada = "";
  String _erro = "";

  Future<void> _buscar() async {
    final cidade = _controller.text.trim();
    if (cidade.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Por favor, digite o nome de uma cidade.")),
      );
      return;
    }

    setState(() {
      _state = _ViewState.loading;
      _cidadeConsultada = cidade;
    });

    try {
      final dados = await _service.getWeatherAndMood(cidade);
      setState(() {
        _dados = dados;
        _state = _ViewState.success;
      });
    } catch (e) {
      setState(() {
        _erro = e.toString().replaceFirst("WeatherServiceException: ", "");
        _state = _ViewState.error;
      });
    }
  }

  String _formatarHora(int? timestampUtc, int timezoneSegundos) {
    if (timestampUtc == null) return "Não disponível";
    final horaLocal = DateTime.fromMillisecondsSinceEpoch(
      (timestampUtc + timezoneSegundos) * 1000,
      isUtc: true,
    );
    return DateFormat('HH:mm').format(horaLocal);
  }

  String _imagemParaHumor(String humorNome) => 'assets/images/$humorNome.webp';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(
        child: Container(
          decoration: const BoxDecoration(
            gradient: RadialGradient(
              center: Alignment(-0.6, -1.0),
              radius: 1.1,
              colors: [Color(0xFF1C0A35), Colors.transparent],
              stops: [0.0, 0.55],
            ),
          ),
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                ClipRRect(
                  borderRadius: BorderRadius.circular(16),
                  child: Image.asset('assets/images/cat_animation.gif', fit: BoxFit.cover),
                ),
                const SizedBox(height: 16),
                Text("🐱 WeatherCat",
                    style: GoogleFonts.syne(
                        color: AppColors.yellow, fontSize: 30, fontWeight: FontWeight.w800, letterSpacing: -1)),
                const SizedBox(height: 6),
                Text("Descubra o clima e o humor do gato na sua cidade!",
                    style: GoogleFonts.dmSans(color: AppColors.textPrimary, fontSize: 14)),
                const SizedBox(height: 20),
                TextField(
                  controller: _controller,
                  style: GoogleFonts.dmSans(color: const Color(0xFFE8E8F0)),
                  onSubmitted: (_) => _buscar(),
                  decoration: InputDecoration(
                    labelText: "Digite o nome da cidade",
                    labelStyle: GoogleFonts.dmSans(color: const Color(0xFF888899), fontSize: 13),
                    hintText: "Ex: London, São Paulo",
                    hintStyle: const TextStyle(color: Color(0xFF555568)),
                    filled: true,
                    fillColor: const Color(0xFF16161F),
                    contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                      borderSide: const BorderSide(color: Color(0xFF2A2A40), width: 1.5),
                    ),
                    enabledBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                      borderSide: const BorderSide(color: Color(0xFF2A2A40), width: 1.5),
                    ),
                    focusedBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                      borderSide: const BorderSide(color: AppColors.yellow, width: 1.5),
                    ),
                  ),
                ),
                const SizedBox(height: 12),
                SizedBox(
                  height: 48,
                  child: ElevatedButton(
                    onPressed: _state == _ViewState.loading ? null : _buscar,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: AppColors.yellow,
                      foregroundColor: AppColors.background,
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
                    ),
                    child: Text("Ver clima e humor do gato",
                        style: GoogleFonts.syne(fontWeight: FontWeight.w700, fontSize: 14, letterSpacing: 0.3)),
                  ),
                ),
                const SizedBox(height: 24),
                if (_state == _ViewState.loading) const PawLoader(),
                if (_state == _ViewState.error) ErrorCard(cidade: _cidadeConsultada, erro: _erro),
                if (_state == _ViewState.success && _dados != null) _buildResultado(),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildResultado() {
    final dados = _dados!;
    final nascer = _formatarHora(dados.nascerSol, dados.timezone);
    final porSol = _formatarHora(dados.porSol, dados.timezone);
    final agora = DateTime.now().toUtc().add(Duration(seconds: dados.timezone));
    final horaLocalFormatada = DateFormat('dd/MM/yyyy HH:mm').format(agora);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        Center(
          child: Column(
            children: [
              Text("📍 LOCALIZAÇÃO",
                  style: GoogleFonts.dmSans(color: AppColors.textMuted, fontSize: 11, letterSpacing: 1.5)),
              Text(_cidadeConsultada[0].toUpperCase() + _cidadeConsultada.substring(1),
                  style: GoogleFonts.syne(color: AppColors.yellow, fontSize: 22, fontWeight: FontWeight.w800)),
            ],
          ),
        ),
        const SizedBox(height: 14),
        TemperatureCard(temp: dados.temperatura, sensacao: dados.sensacao),
        const SizedBox(height: 10),
        Center(
          child: Container(
            margin: const EdgeInsets.symmetric(vertical: 4),
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
            decoration: BoxDecoration(color: AppColors.cardBorder, borderRadius: BorderRadius.circular(50)),
            child: Text("🌥️ ${dados.condicao[0].toUpperCase()}${dados.condicao.substring(1)}",
                style: GoogleFonts.dmSans(color: AppColors.textPrimary, fontSize: 13)),
          ),
        ),
        const SizedBox(height: 10),
        HumidityWindRow(umidade: dados.umidade, vento: dados.ventoVelocidade),
        const SizedBox(height: 10),
        SunCycleCard(nascer: nascer, porSol: porSol),
        const SizedBox(height: 14),
        Center(
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
            decoration: BoxDecoration(color: AppColors.yellow.withOpacity(0.13), borderRadius: BorderRadius.circular(50)),
            child: Text("😸 ${dados.humorDesc}",
                style: GoogleFonts.dmSans(color: AppColors.yellow, fontSize: 13, fontWeight: FontWeight.w600)),
          ),
        ),
        const SizedBox(height: 6),
        Center(
          child: Text("🕐 Hora local: $horaLocalFormatada",
              style: GoogleFonts.dmSans(color: AppColors.textFaint, fontSize: 12)),
        ),
        const SizedBox(height: 16),
        ClipRRect(
          borderRadius: BorderRadius.circular(16),
          child: Image.asset(
            _imagemParaHumor(dados.humorNome),
            fit: BoxFit.cover,
            errorBuilder: (context, error, stackTrace) => Image.asset(
              'assets/images/normal_cat.webp',
              fit: BoxFit.cover,
            ),
          ),
        ),
      ],
    );
  }
}
