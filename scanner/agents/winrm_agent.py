# scanner/agents/winrm_agent.py
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

import winrm

class WinRMAgent:
    def __init__(
        self,
        host: str,
        user: str,
        password: str,
        remote_dir: str = r"C:\tmp\provenance_agent",
    ):
        self.host = host
        self.user = user
        self.password = password
        self.remote_dir = remote_dir
        self.remote_bin = rf"{remote_dir}\agent.exe"

        self.session = winrm.Session(
            host,
            auth=(user, password),
            transport="ntlm"
        )

    def deploy(self):
        # Directory already created by provisioner
        pass

    def execute(self):
        cmd = f'cmd /c "cd /d {self.remote_dir} && agent.exe"'
        r = self.session.run_cmd(cmd)
        if r.status_code != 0:
            raise RuntimeError(r.std_err.decode())

    def collect(self, local_output_dir: str) -> Dict[str, Any]:
        Path(local_output_dir).mkdir(parents=True, exist_ok=True)

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        base = f"phase2_{self.host}_{ts}"

        local_json = Path(local_output_dir) / f"{base}.json"
        local_yml = Path(local_output_dir) / f"{base}.yml"

        # ---- JSON ----
        ps_json = rf'Get-Content "{self.remote_dir}\output.json" -Raw'
        rj = self.session.run_ps(ps_json)
        if rj.status_code != 0:
            raise RuntimeError(rj.std_err.decode())

        json_text = rj.std_out.decode("utf-8")
        local_json.write_text(json_text, encoding="utf-8")

        # ---- YAML ----
        ps_yml = rf'Get-Content "{self.remote_dir}\output.yml" -Raw'
        ry = self.session.run_ps(ps_yml)

        if ry.status_code != 0:
            raise RuntimeError(ry.std_err.decode())

        yml_text = ry.std_out.decode("utf-8")
        local_yml.write_text(yml_text, encoding="utf-8")

        return json.loads(json_text)

    def cleanup(self):
        pass
