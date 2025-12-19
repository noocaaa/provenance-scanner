# scanner/agents/ssh_agent.py
import os
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

class SSHAgent:
    def __init__(
        self,
        host: str,
        user: str,
        key_path: str,
        remote_dir: str = "/tmp/provenance_agent",
        timeout: int = 60,
    ):
        self.host = host
        self.user = user
        self.key_path = os.path.expanduser(key_path)
        self.remote_dir = remote_dir
        self.timeout = timeout
        self.remote_bin: Optional[str] = None

    def _ssh(self, cmd: str, timeout: Optional[int] = None) -> subprocess.CompletedProcess:
        ssh_cmd = [
            "ssh",
            "-i", self.key_path,
            "-o", "StrictHostKeyChecking=no",
            "-o", "BatchMode=yes",
            f"{self.user}@{self.host}",
            cmd,
        ]

        return subprocess.run(
            ssh_cmd,
            capture_output=True,
            text=True,
            timeout=timeout or self.timeout,
        )

    def _scp_to_remote(self, src: str, dst: str) -> subprocess.CompletedProcess:
        scp_cmd = [
            "scp",
            "-i", self.key_path,
            "-o", "StrictHostKeyChecking=no",
            src,
            f"{self.user}@{self.host}:{dst}",
        ]
        return subprocess.run(scp_cmd, capture_output=True, text=True, timeout=self.timeout)

    def _scp_from_remote(self, src: str, dst: str) -> subprocess.CompletedProcess:
        scp_cmd = [
            "scp",
            "-i", self.key_path,
            "-o", "StrictHostKeyChecking=no",
            f"{self.user}@{self.host}:{src}",
            dst,
        ]
        return subprocess.run(scp_cmd, capture_output=True, text=True, timeout=self.timeout)

    def detect_remote_os(self) -> str:
        r = self._ssh("uname -s", timeout=10)
        if r.returncode == 0:
            s = (r.stdout or "").strip().lower()
            if "linux" in s:
                return "linux"
            if "darwin" in s:
                return "macos"

        r = self._ssh("cmd /c echo WINDOWS", timeout=10)
        if r.returncode == 0 and "WINDOWS" in (r.stdout or ""):
            return "windows"

        raise RuntimeError(
            f"[{self.host}] Unable to detect remote OS.\n"
            f"stdout={r.stdout}\nstderr={r.stderr}"
        )

    def deploy(self):
        os_name = self.detect_remote_os()

        if os_name == "windows":
            local_bin = "build/windows/provenance_agent.exe"
            remote_dir = "C:/tmp/provenance_agent"
            remote_bin = f"{remote_dir}/agent.exe"
            mkdir_cmd = f'mkdir "{remote_dir}"'
        else:
            local_bin = f"build/{os_name}/provenance_agent"
            remote_dir = self.remote_dir
            remote_bin = f"{remote_dir}/agent"
            mkdir_cmd = f"mkdir -p {remote_dir}"

        r = self._ssh(mkdir_cmd)
        if r.returncode != 0:
            raise RuntimeError(f"[{self.host}] mkdir failed: {r.stderr}")

        r = self._scp_to_remote(local_bin, remote_bin)
        if r.returncode != 0:
            raise RuntimeError(f"[{self.host}] scp deploy failed: {r.stderr}")

        if os_name != "windows":
            r = self._ssh(f"chmod +x {remote_bin}")
            if r.returncode != 0:
                raise RuntimeError(f"[{self.host}] chmod failed: {r.stderr}")

        self.remote_bin = remote_bin
        self.remote_dir = remote_dir

    def execute(self):
        if not self.remote_bin:
            raise RuntimeError("deploy() must run before execute()")

        if self.remote_bin.lower().endswith(".exe"):
            cmd = f'"{self.remote_bin}"'
        else:
            cmd = f"cd {self.remote_dir} && {self.remote_bin}"

        r = self._ssh(cmd)
        if r.returncode != 0:
            raise RuntimeError(f"[{self.host}] agent failed:\n{r.stderr}\n{r.stdout}")

    def collect(self, local_output_dir: str) -> Dict[str, Any]:
        Path(local_output_dir).mkdir(parents=True, exist_ok=True)

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        base = f"phase2_{self.host}_{ts}"

        local_json = str(Path(local_output_dir) / f"{base}.json")
        local_yml  = str(Path(local_output_dir) / f"{base}.yml")

        remote_json = f"{self.remote_dir}/output.json"
        remote_yml  = f"{self.remote_dir}/output.yml"

        r = self._scp_from_remote(remote_json, local_json)
        if r.returncode != 0:
            raise RuntimeError(f"[{self.host}] scp output.json failed: {r.stderr}")

        r2 = self._scp_from_remote(remote_yml, local_yml)

        if r2.returncode != 0:
            pass

        with open(local_json, "r", encoding="utf-8") as f:
            return json.load(f)

    def cleanup(self):
        self._ssh(f"rm -rf {self.remote_dir}")
