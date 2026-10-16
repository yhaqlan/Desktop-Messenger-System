class ConnectivityConfig {
  const ConnectivityConfig({this.host = '127.0.0.1', this.lanPort = 8765, this.relayPort = 9876});

  final String host;
  final int lanPort;
  final int relayPort;

  bool get isLoopback => host == '127.0.0.1' || host == 'localhost';
}
