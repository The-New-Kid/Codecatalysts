import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  // CHANGE FOR YOUR SETUP:
  // Android Emulator:  http://10.0.2.2:5000
  // iOS Simulator:     http://127.0.0.1:5000
  // Real Device:       http://<YOUR-LAPTOP-IP>:5000  (Flask host=0.0.0.0)
  static const String baseUrl = "http://127.0.0.1:5000";

  // ----------------------------------------------------------------------
  // EMAIL + PASSWORD LOGIN
  // ----------------------------------------------------------------------
  static Future<Map<String, dynamic>> login(
      String email, String password) async {
    final url = Uri.parse("$baseUrl/api/login");

    http.Response response;
    try {
      response = await http.post(
        url,
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({"email": email, "password": password}),
      );
    } catch (_) {
      // yaha aana matlab server se connection hi nahi hua
      throw Exception(
          "Unable to connect to server. Please check your internet and try again.");
    }

    final body = _safeDecode(response);

    if (response.statusCode == 200) {
      // { message, user_id, role, name }
      return body;
    } else {
      // flask ka exact message dikhao (User not found, Incorrect password...)
      throw Exception(body['message'] ?? "Login failed");
    }
  }

  // ----------------------------------------------------------------------
  // REGISTER
  // ----------------------------------------------------------------------
  static Future<String> register({
    required String name,
    required String email,
    required String password,
    required String mobileNumber,
    required String pincode,
    required String address,
  }) async {
    final url = Uri.parse("$baseUrl/api/register");

    http.Response response;
    try {
      response = await http.post(
        url,
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({
          "name": name,
          "email": email,
          "password": password,
          "mobile_number": mobileNumber,
          "pincode": pincode,
          "address": address,
          "role": 1, // normal user
        }),
      );
    } catch (_) {
      throw Exception(
          "Unable to connect to server. Please check your internet and try again.");
    }

    final body = _safeDecode(response);
    final message = body['message'] ?? "Registration failed";

    if (response.statusCode == 201) {
      // Registration successful
      return message;
    } else {
      // yaha sab backend errors: All fields required, Email already registered, Invalid mobile...
      throw Exception(message);
    }
  }

  // ----------------------------------------------------------------------
  // MOBILE LOGIN - SEND OTP  (/api/mobile-login)
  // ----------------------------------------------------------------------
  static Future<String> sendLoginOtp(String mobileNumber) async {
    final url = Uri.parse("$baseUrl/api/mobile-login");

    http.Response response;
    try {
      response = await http.post(
        url,
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({"mobile_number": mobileNumber}),
      );
    } catch (_) {
      throw Exception(
          "Unable to connect to server. Please check your internet and try again.");
    }

    final body = _safeDecode(response);
    final message = body['message'] ?? "Failed to send OTP";

    if (response.statusCode == 200) {
      return message; // "OTP sent successfully"
    } else {
      throw Exception(message); // "User not found", "Invalid mobile number", "OTP service failed"
    }
  }

  // ----------------------------------------------------------------------
  // MOBILE LOGIN - VERIFY OTP  (/api/login-verify-otp)
  // ----------------------------------------------------------------------
  static Future<Map<String, dynamic>> verifyLoginOtp({
    required String mobileNumber,
    required String otp,
  }) async {
    final url = Uri.parse("$baseUrl/api/login-verify-otp");

    http.Response response;
    try {
      response = await http.post(
        url,
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({
          "mobile_number": mobileNumber,
          "otp": otp,
        }),
      );
    } catch (_) {
      throw Exception(
          "Unable to connect to server. Please check your internet and try again.");
    }

    final body = _safeDecode(response);

    if (response.statusCode == 200) {
      // { message, user_id, role, name }
      return body;
    } else {
      // "OTP expired", "Wrong OTP", "OTP not generated" etc.
      throw Exception(body['message'] ?? "OTP verification failed");
    }
  }

  // ----------------------------------------------------------------------
  // Helper: safely decode JSON
  // ----------------------------------------------------------------------
  static Map<String, dynamic> _safeDecode(http.Response response) {
    try {
      return jsonDecode(response.body) as Map<String, dynamic>;
    } catch (_) {
      return {
        "message": "Unexpected server response (${response.statusCode})."
      };
    }
  }
}