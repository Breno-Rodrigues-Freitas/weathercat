class WeatherMood {
  final double temperatura;
  final double sensacao;
  final int umidade;
  final String condicao;
  final String condicaoMain;
  final double ventoVelocidade;
  final int? nascerSol;
  final int? porSol;
  final int timezone;
  final String humorNome;
  final String humorDesc;

  WeatherMood({
    required this.temperatura,
    required this.sensacao,
    required this.umidade,
    required this.condicao,
    required this.condicaoMain,
    required this.ventoVelocidade,
    required this.nascerSol,
    required this.porSol,
    required this.timezone,
    required this.humorNome,
    required this.humorDesc,
  });

  factory WeatherMood.fromJson(Map<String, dynamic> json) {
    return WeatherMood(
      temperatura: (json['temperatura'] as num).toDouble(),
      sensacao: (json['sensacao'] as num).toDouble(),
      umidade: (json['umidade'] as num).toInt(),
      condicao: json['condicao'] as String,
      condicaoMain: json['condicao_main'] as String,
      ventoVelocidade: (json['vento_velocidade'] as num).toDouble(),
      nascerSol: json['nascer_sol'] == null ? null : (json['nascer_sol'] as num).toInt(),
      porSol: json['por_sol'] == null ? null : (json['por_sol'] as num).toInt(),
      timezone: (json['timezone'] as num).toInt(),
      humorNome: json['humor_nome'] as String,
      humorDesc: json['humor_desc'] as String,
    );
  }
}
