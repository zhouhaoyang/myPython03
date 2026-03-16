"""简单 TCP Server：可接受客户端消息并回执。"""

from __future__ import annotations

import argparse
import socketserver
from datetime import datetime

from message_store import MessageStore

STORE = MessageStore()


class TCPMessageHandler(socketserver.BaseRequestHandler):
    """处理每个客户端连接。"""

    def handle(self) -> None:
        peer = f"{self.client_address[0]}:{self.client_address[1]}"
        print(f"[+] 客户端连接: {peer}")

        while True:
            data = self.request.recv(1024)
            if not data:
                print(f"[-] 客户端断开: {peer}")
                break

            message = data.decode("utf-8", errors="replace").strip()
            if not message:
                continue

            timestamp = datetime.now().isoformat(timespec="seconds")
            full_message = f"[{timestamp}] {peer} -> {message}"
            STORE.add(full_message)
            print(full_message)

            self.request.sendall(f"ACK: {message}\n".encode("utf-8"))


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """多线程 TCP Server。"""

    allow_reuse_address = True
    daemon_threads = True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="启动 TCP 消息服务")
    parser.add_argument("--host", default="0.0.0.0", help="监听地址")
    parser.add_argument("--port", type=int, default=9000, help="监听端口")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    with ThreadedTCPServer((args.host, args.port), TCPMessageHandler) as server:
        print(f"TCP server 正在监听 {args.host}:{args.port}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\n收到中断，正在关闭服务...")
            server.shutdown()


if __name__ == "__main__":
    main()
