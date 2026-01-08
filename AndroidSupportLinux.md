# RenderDoc Android Support - Linux Build Guide

Build the RenderDoc Android APK on Linux (native or WSL2 with Debian/Ubuntu).

---

## Quick Setup (Debian/WSL2)

### 1. Install Dependencies

```bash
# Debian/WSL2
sudo apt-get update
sudo apt-get install -y wget curl unzip cmake build-essential default-jdk

# Set JAVA_HOME
export JAVA_HOME=/usr/lib/jvm/default-java
```

### 2. Install Android SDK

```bash
# Create directory and download
mkdir -p ~/android-sdk
cd ~/android-sdk
wget https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip
unzip commandlinetools-linux-11076708_latest.zip

# Fix folder structure (required!)
mv cmdline-tools latest
mkdir cmdline-tools
mv latest cmdline-tools/

# Set environment
export ANDROID_SDK=~/android-sdk
export PATH=$ANDROID_SDK/cmdline-tools/latest/bin:$PATH

# Accept licenses and install components
yes | sdkmanager --sdk_root=$ANDROID_SDK --licenses
sdkmanager --sdk_root=$ANDROID_SDK "platforms;android-23" "build-tools;30.0.3"
```

> **Important:** Use `build-tools;30.0.3` (not 26.0.1) for Java 17 compatibility!

### 3. Install Android NDK

```bash
cd ~/android-sdk
wget https://dl.google.com/android/repository/android-ndk-r21e-linux-x86_64.zip
unzip android-ndk-r21e-linux-x86_64.zip

export ANDROID_NDK=~/android-sdk/android-ndk-r21e
export ANDROID_NDK_ROOT=$ANDROID_NDK
```

### 4. Build RenderDoc Android

```bash
# Navigate to RenderDoc
cd /mnt/c/Users/vsiva/dev/RD/RenderDocTools/renderdoc

# Build arm64 (modern 64-bit devices)
mkdir -p build-android-arm64 && cd build-android-arm64
cmake -DBUILD_ANDROID=On -DANDROID_ABI=arm64-v8a \
      -DCMAKE_TOOLCHAIN_FILE=$ANDROID_NDK/build/cmake/android.toolchain.cmake \
      -DANDROID_PLATFORM=android-23 -G "Unix Makefiles" ..
make -j$(nproc)

# Build arm32 (older 32-bit devices) - optional
cd ..
mkdir -p build-android-arm32 && cd build-android-arm32
cmake -DBUILD_ANDROID=On -DANDROID_ABI=armeabi-v7a \
      -DCMAKE_TOOLCHAIN_FILE=$ANDROID_NDK/build/cmake/android.toolchain.cmake \
      -DANDROID_PLATFORM=android-23 -G "Unix Makefiles" ..
make -j$(nproc)
```

### 5. Deploy APKs

```bash
# Copy to Windows RenderDoc output folder
cp /mnt/c/Users/vsiva/dev/RD/RenderDocTools/renderdoc/build-android-arm64/bin/*.apk \
   /mnt/c/Users/vsiva/dev/RD/RenderDocTools/renderdoc/x64/Development/

cp /mnt/c/Users/vsiva/dev/RD/RenderDocTools/renderdoc/build-android-arm32/bin/*.apk \
   /mnt/c/Users/vsiva/dev/RD/RenderDocTools/renderdoc/x64/Development/
```

---

## Required CMakeLists.txt Fix

The RenderDoc source has a Java 1.7 target which doesn't work with Java 17. This fix was applied:

**File:** `renderdoc/renderdoccmd/CMakeLists.txt` (line 305)

```diff
- COMMAND ${JAVA_BIN}/javac -d ./obj -source 1.7 -target 1.7 ...
+ COMMAND ${JAVA_BIN}/javac -d ./obj -source 1.8 -target 1.8 ...
```

---

## Environment Variables Reference

Add to `~/.bashrc` for persistence:

```bash
export JAVA_HOME=/usr/lib/jvm/default-java
export ANDROID_SDK=~/android-sdk
export ANDROID_NDK=~/android-sdk/android-ndk-r21e
export ANDROID_NDK_ROOT=$ANDROID_NDK
export PATH=$ANDROID_SDK/cmdline-tools/latest/bin:$PATH
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| CMake can't find NDK | `export ANDROID_NDK_ROOT=$ANDROID_NDK` |
| sdkmanager not found | Check PATH includes `cmdline-tools/latest/bin` |
| Java not found | `export JAVA_HOME=/usr/lib/jvm/default-java` |
| `Source option 7 is no longer supported` | Change `-source 1.7 -target 1.7` to `1.8` in CMakeLists.txt |
| `apksigner` module access error | Use `build-tools;30.0.3` instead of `26.0.1` |
| Build fails on arm32 | Try `-DANDROID_PLATFORM=android-21` |
