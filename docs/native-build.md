# Building the native accelerators

## C++ (MSVC 2022 / Clang 17)

```powershell
cmake -S native/cpp -B build/native -G "Visual Studio 17 2022" -A x64
cmake --build build/native --config Release
copy build\native\Release\pdf_suite_native.dll src\pdf_suite\native_bridge\
```