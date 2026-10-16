enum NetworkMode { offline, lan, relay }

extension NetworkModeLabel on NetworkMode {
  String get label => switch (this) {
        NetworkMode.offline => 'Offline',
        NetworkMode.lan => 'LAN / Hotspot',
        NetworkMode.relay => 'Internet Relay',
      };
}
