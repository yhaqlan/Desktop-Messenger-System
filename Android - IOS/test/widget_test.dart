import 'package:desktop_messenger_mobile/app.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('shows Desktop Messenger login title', (tester) async {
    await tester.pumpWidget(const DesktopMessengerMobile());
    expect(find.text('Desktop Messenger'), findsOneWidget);
  });
}
