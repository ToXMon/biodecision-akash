# SDL pointers (Awesome Akash)

**Do not commit filled SDL with secrets.** Copy templates locally, inject passwords/tokens via your secret mechanism, keep private copies outside git (or gitignored).

---

## Unsloth train

- Repo tree: https://github.com/akash-network/awesome-akash/tree/master/unsloth-ai  
- Console template: https://console.akash.network/new-deployment?step=edit-deployment&templateId=akash-network-awesome-akash-unsloth-ai  
- Runbook: [`../runbooks/AKASH-UNSLOTH-TRAIN.md`](../runbooks/AKASH-UNSLOTH-TRAIN.md)

Local practice:
```bash
# example — adjust to where you clone awesome-akash
cp /path/to/awesome-akash/unsloth-ai/deploy.yaml ./sdl/unsloth-ai.local.yaml
# edit passwords, pin image tag, GPU, storage — keep *.local.yaml gitignored
```

## vLLM serve

- Repo tree: https://github.com/akash-network/awesome-akash/tree/master/vllm  
- Prefer API-only YAML (e.g. `vllm_no_ui_deployment.yml` when present)  
- Runbook: [`../runbooks/AKASH-VLLM-SERVE.md`](../runbooks/AKASH-VLLM-SERVE.md)

```bash
cp /path/to/awesome-akash/vllm/vllm_no_ui_deployment.yml ./sdl/vllm.local.yaml
# set MODEL to your HF id / mount; inject API keys via env — never commit
```

## Never commit

- `JUPYTER_PASSWORD`, `USER_PASSWORD`
- HF tokens, wrapper API keys
- Provider bidding wallets / mnemonic material
- Any `*.local.yaml` with secrets filled in

Root `.gitignore` already patterns common secret/env files; still review `git status` before commit.
