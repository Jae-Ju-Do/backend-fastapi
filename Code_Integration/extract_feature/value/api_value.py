
import_list = [
    # 시스템 정보 및 시간 관련 API
    'GetSystemInfo', 'GetNativeSystemInfo', 'GlobalMemoryStatus', 'GlobalMemoryStatusEx', 'GetTickCount', 
    'GetTickCount64', 'QueryPerformanceCounter', 'GetSystemTime', 'GetSystemTimeAsFileTime', 'GetLocalTime', 
    'GetTimeZoneInformation', 'GetVersion', 'GetVersionExA', 'GetVersionExW', 'GetComputerNameA', 'GetComputerNameW', 
    'GetUserNameA', 'GetUserNameW', 'IsProcessorFeaturePresent',

    # 프로세스 관리 관련 API
    'CreateProcessA', 'CreateProcessW', 'CreateProcessWithLogonW', 'CreateProcessAsUserA', 'CreateProcessAsUserW', 
    'OpenProcess', 'TerminateProcess', 'GetCurrentProcess', 'GetCurrentProcessId', 'GetProcessId', 'GetThreadPriority', 
    'SetThreadPriority', 'CreateThread', 'CreateRemoteThread', 'ExitThread', 'SuspendThread', 'ResumeThread', 
    'OpenThread', 'TerminateThread', 'SwitchToThread', 'GetExitCodeProcess', 'GetExitCodeThread', 'WaitForSingleObject', 
    'WaitForMultipleObjects',

    # 메모리 관리 관련 API
    'VirtualAlloc', 'VirtualAllocEx', 'VirtualFree', 'VirtualFreeEx', 'VirtualQuery', 'VirtualQueryEx', 'VirtualProtect', 
    'VirtualProtectEx', 'HeapCreate', 'HeapDestroy', 'HeapAlloc', 'HeapFree', 'GlobalAlloc', 'GlobalFree', 'GlobalLock', 
    'GlobalUnlock', 'LocalAlloc', 'LocalFree', 'MapViewOfFile', 'UnmapViewOfFile', 
    "memset", "memcpy", "memmove", "memcmp", "SetLastError", "GetLastError", 
    "WaitForSingleObjectEx", "GetCurrentThreadId", "ExitProcess", "SignalObjectAndWait",

    # 예외 처리 및 오류 관련 API
    "__C_specific_handler", "_initterm", "_CxxThrowException", "SetUnhandledExceptionFilter", "UnhandledExceptionFilter",


    # 파일 시스템 관련 API
    'CreateFileA', 'CreateFileW', 'ReadFile', 'WriteFile', 'CloseHandle', 'DeleteFileA', 'DeleteFileW', 'MoveFileA', 
    'MoveFileW', 'CopyFileA', 'CopyFileW', 'GetFileSize', 'GetFileAttributesA', 'GetFileAttributesW', 'SetFileAttributesA', 
    'SetFileAttributesW', 'FindFirstFileA', 'FindFirstFileW', 'FindNextFileA', 'FindNextFileW', 'FindClose', 'CreateDirectoryA', 
    'CreateDirectoryW', 'RemoveDirectoryA', 'RemoveDirectoryW', 'LockFile', 'UnlockFile', 'LockFileEx', 'UnlockFileEx', 
    'SetFilePointer', 'FlushFileBuffers',

    # 네트워크 및 통신 관련 API
    'socket', 'bind', 'listen', 'accept', 'connect', 'send', 'recv', 'sendto', 'recvfrom', 'shutdown', 'closesocket', 
    'gethostbyname', 'gethostbyaddr', 'getaddrinfo', 'freeaddrinfo', 'WSAStartup', 'WSACleanup', 'WSAGetLastError', 
    'InternetOpenA', 'InternetOpenW', 'InternetCloseHandle', 'InternetConnectA', 'InternetConnectW', 'InternetOpenUrlA', 
    'InternetOpenUrlW', 'HttpOpenRequestA', 'HttpOpenRequestW', 'HttpSendRequestA', 'HttpSendRequestW', 'HttpQueryInfoA', 
    'HttpQueryInfoW',

    # 암호화 및 보안 관련 API
    'CryptAcquireContextA', 'CryptAcquireContextW', 'CryptReleaseContext', 'CryptGenKey', 'CryptDestroyKey', 'CryptEncrypt', 
    'CryptDecrypt', 'CryptCreateHash', 'CryptHashData', 'CryptDeriveKey', 'CryptHashSessionKey', 'CryptSignHashA', 
    'CryptSignHashW', 'CryptVerifySignatureA', 'CryptVerifySignatureW', 'CryptProtectData', 'CryptUnprotectData', 
    'CryptExportKey', 'CryptImportKey', 'CryptSetHashParam', 'CryptGetHashParam',

    # 디버깅 및 도구 관련 API
    'IsDebuggerPresent', 'CheckRemoteDebuggerPresent', 'OutputDebugStringA', 'OutputDebugStringW', 'DebugBreak', 
    'DebugActiveProcess', 'DebugActiveProcessStop', 'WaitForDebugEvent', 'ContinueDebugEvent', 'MiniDumpWriteDump', 
    'RtlCaptureContext', 'RtlLookupFunctionEntry', 'RtlVirtualUnwind',

    # 레지스트리 조작 관련 API
    'RegOpenKeyA', 'RegOpenKeyW', 'RegCreateKeyA', 'RegCreateKeyW', 'RegSetValueA', 'RegSetValueW', 'RegSetValueExA', 
    'RegSetValueExW', 'RegQueryValueA', 'RegQueryValueW', 'RegQueryValueExA', 'RegQueryValueExW', 'RegDeleteValueA', 
    'RegDeleteValueW', 'RegDeleteKeyA', 'RegDeleteKeyW', 'RegEnumValueA', 'RegEnumValueW', 'RegEnumKeyA', 'RegEnumKeyW', 
    'RegFlushKey', 'RegCloseKey',
    "RegOpenKeyExW", "RegOpenKeyExA", "RegQueryInfoKeyA", "RegCreateKeyExA", "RegSaveKeyA", "RegRestoreKeyA", 
    "RegUnLoadKeyA", "RegLoadKeyA", "RegOpenCurrentUser", "RegConnectRegistryA", "RegConnectRegistryW", 
    "RegNotifyChangeKeyValue", "RegQueryMultipleValuesA", "RegQueryMultipleValuesW", "RegReplaceKeyA", 
    "RegReplaceKeyW", "RegRestoreKeyW", "RegSaveKeyW", "RegSetKeyValueA", "RegSetKeyValueW",

    # 인터넷 관련 API
    "InternetReadFile", "InternetSetOptionA", "InternetGetConnectedState", "InternetCrackUrlA", "InternetGetConnectedStateExA", 
    "InternetSetStatusCallback", "InternetSetStatusCallbackA", "InternetSetStatusCallbackW", "InternetSetFilePointer", 
    "InternetWriteFile", "InternetGetLastResponseInfoA", "InternetGetLastResponseInfoW", "InternetQueryOptionW",

    # 서비스 관리 관련 API
    'OpenSCManagerA', 'OpenSCManagerW', 'CreateServiceA', 'CreateServiceW', 'DeleteService', 'StartServiceA', 
    'StartServiceW', 'ControlService', 'QueryServiceStatus', 'EnumServicesStatusA', 'EnumServicesStatusW', 
    'ChangeServiceConfigA', 'ChangeServiceConfigW', 'QueryServiceConfigA',
    "OpenServiceA", "OpenServiceW", "ChangeServiceConfig2A", "ChangeServiceConfig2W", "EnumServicesStatusExA", 
    "EnumServicesStatusExW", "EnumDependentServicesA", "EnumDependentServicesW", "QueryServiceConfigW", 
    "QueryServiceConfig2A", "QueryServiceConfig2W", "QueryServiceStatusEx", "RegisterServiceCtrlHandlerA", 
    "RegisterServiceCtrlHandlerW", "RegisterServiceCtrlHandlerExA", "RegisterServiceCtrlHandlerExW", "SetServiceStatus", 
    "StartServiceCtrlDispatcherA", "StartServiceCtrlDispatcherW",


    # 윈도우 GUI 관련 API
    'FindWindowA', 'FindWindowW', 'SetWindowTextA', 'SetWindowTextW', 'PostMessageA', 'PostMessageW', 'SendMessageA', 
    'SendMessageW', 'SetWindowsHookExA', 'SetWindowsHookExW', 'CallNextHookEx', 'UnhookWindowsHookEx', 'GetMessageA', 
    'GetMessageW', 'PeekMessageA', 'PeekMessageW',

    # 추가 유용 API
    'SetWindowsHookA', 'SetWindowsHookW', 'MapVirtualKeyA', 'MapVirtualKeyW', 'ToAscii', 'ToUnicode', 'VkKeyScanA', 
    'VkKeyScanW', 'GetFocus', 'SetFocus', 'SetCursorPos', 'GetCursorPos', 'OpenClipboard', 'CloseClipboard', 
    'EmptyClipboard', 'GetClipboardData', 'SetClipboardData',

    # 보안 및 권한 관리 관련 API
    'AdjustTokenPrivileges', 'OpenProcessToken', 'OpenThreadToken', 'GetTokenInformation', 'SetTokenInformation', 
    'DuplicateToken', 'DuplicateTokenEx', 'CreateWellKnownSid', 'GetSecurityDescriptorDacl', 'SetSecurityDescriptorDacl', 
    'GetSecurityDescriptorOwner', 'SetSecurityDescriptorOwner', 'GetSecurityDescriptorGroup', 'SetSecurityDescriptorGroup', 
    'AccessCheck', 'AccessCheckAndAuditAlarm', 'AuditPolicyChanged', 'AccessCheckByType', 'GetSidSubAuthority', 
    'SetNamedSecurityInfo', 'GetNamedSecurityInfo', 'SetSecurityDescriptorControl',
    "CryptEncryptMessage", "CryptDecryptMessage", "CryptSignMessage", "CryptVerifyMessageSignature", 
    "CryptMsgOpenToDecode", "CryptMsgUpdate", "CryptMsgGetParam", "CryptMsgControl", "CryptMsgClose",


    # 외부 라이브러리 관련 API
    'LoadLibraryA', 'LoadLibraryW', 'LoadLibraryExA', 'LoadLibraryExW', 'GetModuleHandleA', 'GetModuleHandleW', 
    'GetProcAddress', 'GetModuleFileNameA', 'GetModuleFileNameW', 'FreeLibrary', 'GetModuleHandleExA', 'GetModuleHandleExW', 
    'GetModuleInformation', 'EnumDeviceDrivers', 'GetDeviceDriverFileNameA', 'GetDeviceDriverFileNameW', 'EnumResourceTypesA', 
    'EnumResourceTypesW', 'EnumResourceNamesA', 'EnumResourceNamesW',

    # 기타 유용한 API
    'SetThreadAffinityMask', 'SetThreadIdealProcessor', 'CreateJobObject', 'AssignProcessToJobObject', 
    'QueryInformationJobObject', 'SetInformationJobObject', 'GetCurrentDirectoryA', 'GetCurrentDirectoryW', 
    'SetCurrentDirectoryA', 'SetCurrentDirectoryW', 'MoveFileExA', 'MoveFileExW', 'GetFullPathNameA', 'GetFullPathNameW', 
    'QueryPerformanceFrequency',

    # 시스템 정보 관련 API
    'GetLogicalDrives', 'GetDriveTypeA', 'GetDriveTypeW', 'GetDiskFreeSpaceA', 'GetDiskFreeSpaceW', 
    'GetDiskFreeSpaceExA', 'GetDiskFreeSpaceExW', 'GetVolumeInformationA', 'GetVolumeInformationW', 'GetTempPathA', 
    'GetTempPathW', 'GetTempFileNameA', 'GetTempFileNameW',
     "ShellExecuteA", "ShellExecuteW", "ShellExecuteExA", "ShellExecuteExW", "WinExec",


    # 프로세스 관리 관련 API
    'GetProcessHeap', 'GetPriorityClass', 'SetPriorityClass', 'GetThreadId',
    "CreateProcessInternalA", "CreateProcessInternalW", "CreateProcessWithTokenW", "CreateProcessWithTokenA", 
    "GetThreadContext", "SetThreadContext", "ReadProcessMemory", "WriteProcessMemory", "CreateToolhelp32Snapshot", 
    "Process32First", "Process32Next", "Thread32First", "Thread32Next", "Module32First", "Module32Next", 
    "GetStartupInfoA", "GetStartupInfoW", "GetCommandLineA", "GetCommandLineW",

    # 뮤텍스 관련 API
    "FormatMessageW", "OpenSemaphoreW", "ReleaseMutex", "CreateMutexA", "CreateMutexW", "OpenMutexA", "OpenMutexW"
]

dll_list = [
    # 시스템 기본 DLL
    'kernel32.dll', 'ntdll.dll', 'advapi32.dll', 'user32.dll', 'gdi32.dll', 'shell32.dll', 
    'comdlg32.dll', 'shlwapi.dll', 'ole32.dll', 'oleaut32.dll', 'ws2_32.dll', 'comctl32.dll', 

    # 네트워크 및 웹 관련 DLL
    'wininet.dll', 'urlmon.dll', 'mshtml.dll', 'winhttp.dll', 'hnetcfg.dll', 'rasapi32.dll', 
    'dhcpcsvc.dll', 'dnsapi.dll', 'iphlpapi.dll', 'netapi32.dll', 'wsock32.dll'

    # 암호화 및 보안 관련 DLL
    'crypt32.dll', 'bcrypt.dll', 'cryptdll.dll', 'secur32.dll', 'schannel.dll', 

    # 디버깅 및 프로파일링 DLL
    'dbghelp.dll', 'imagehlp.dll', 'psapi.dll', 'tlhelp32.dll', 'winsta.dll', 

    # 하드웨어 및 장치 접근 DLL
    'hid.dll', 'cfgmgr32.dll', 'powrprof.dll', 'setupapi.dll', 'winusb.dll', 

    # 미디어 및 그래픽 DLL
    'winmm.dll', 'dsound.dll', 'd3d9.dll', 'dxgi.dll', 'opengl32.dll', 

    # 데이터베이스 및 COM DLL
    'msvcrt.dll', 'rpcrt4.dll', 'activeds.dll', 'adsldpc.dll', 'wldap32.dll', 

    # 서비스 및 시스템 관리 DLL
    'services.exe', 'svchost.exe', 'taskschd.dll', 'eventlog.dll', 'esent.dll', 

    # 추가적인 시스템 DLL
    'mpr.dll', 'version.dll', 'wow64.dll', 'wow64cpu.dll', 'ntoskrnl.exe', 'hal.dll', 'winspool.drv'
]