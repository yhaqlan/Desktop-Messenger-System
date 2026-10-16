import 'package:shared_preferences/shared_preferences.dart';

class LocalStore {
  Future<void> saveUsername(String username) async {
    final preferences = await SharedPreferences.getInstance();
    await preferences.setString('username', username);
  }

  Future<String?> loadUsername() async {
    final preferences = await SharedPreferences.getInstance();
    return preferences.getString('username');
  }
}
