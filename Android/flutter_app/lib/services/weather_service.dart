import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/weather_mood.dart';

/// Exceção lançada quando a cidade não é encontrada ou há erro na API.
class WeatherServiceException implements Exception {
  final String message;
  WeatherServiceException(this.message);
}

class WeatherService {
  /// IMPORTANTE: troque pela URL do seu backend depois do deploy.
  /// - Emulador Android: use http://10.0.2.2:8000
  /// - Emulador iOS / dispositivo físico na mesma rede: use o IP da sua máquina
  /// - Produção: URL do serviço (Render, Railway, Fly.io, etc.)
  static const String baseUrl = "http://10.0.2.2:8000";

  Future<WeatherMood> getWeatherAndMood(String cidade) async {
    final uri = Uri.parse("$baseUrl/weather-mood").replace(
      queryParameters: {"cidade": cidade},
    );

    try {
      final response = await http.get(uri).timeout(const Duration(seconds: 15));

      if (response.statusCode == 200) {
        final Map<String, dynamic> json = jsonDecode(utf8.decode(response.bodyBytes));
        return WeatherMood.fromJson(json);
      } else {
        final Map<String, dynamic> errorJson = jsonDecode(utf8.decode(response.bodyBytes));
        final detail = errorJson['detail'] ?? 'Cidade não encontrada.';
        throw WeatherServiceException(detail);
      }
    } on WeatherServiceException {
      rethrow;
    } catch (e) {
      throw WeatherServiceException("Não foi possível conectar ao servidor. Verifique sua conexão.");
    }
  }
}
