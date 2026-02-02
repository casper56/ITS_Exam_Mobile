# Building the APK

The project has been reorganized to support Android APK generation using [Capacitor](https://capacitorjs.com/).

## Prerequisites
- Node.js installed.
- Java Development Kit (JDK) installed.
- Android Studio installed (includes Android SDK).

## Directory Structure
- `www/`: Contains all your web assets (HTML, JS, CSS, Exam content).
- `android/`: Contains the generated Android project.
- `capacitor.config.json`: Configuration for the mobile app.

## How to Build

1. **Sync Changes**:
   Whenever you modify files in `www/`, run:
   ```bash
   npx cap sync
   ```

2. **Open in Android Studio**:
   ```bash
   npx cap open android
   ```
   - Once Android Studio opens, wait for Gradle sync to finish.
   - Click the "Run" button (green play icon) to test on an emulator or device.
   - To build a release APK: Go to `Build` > `Build Bundle(s) / APK(s)` > `Build APK(s)`.

3. **Command Line Build (Advanced)**:
   If you have JDK and Android SDK configured in your path:
   ```bash
   cd android
   ./gradlew assembleDebug
   ```
   The APK will be at `android/app/build/outputs/apk/debug/app-debug.apk`.
