#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
github_dir="$(cd "${script_dir}/.." && pwd)/github"
failure_log="${script_dir}/clone-failures.log"

mkdir -p "${github_dir}"
: > "${failure_log}"

clone_reference() {
  local name="$1"
  local url="$2"
  local destination="${github_dir}/${name}"

  if [[ -e "${destination}" ]]; then
    printf 'SKIP %s (destination exists)\n' "${name}"
    return 0
  fi

  if git clone --depth 1 "${url}" "${destination}"; then
    printf '%s\n' "${name}"
  else
    printf '%s,%s\n' "${name}" "${url}" >> "${failure_log}"
    printf 'FAILED %s\n' "${name}" >&2
  fi
}

clone_reference "llm-council" "https://github.com/karpathy/llm-council.git"
clone_reference "notebooklm-mcp-cli" "https://github.com/jacob-bd/notebooklm-mcp-cli.git"
clone_reference "ngmeyer-skills" "https://github.com/ngmeyer/skills.git"
clone_reference "boardroom_skills" "https://github.com/teemutuo/boardroom_skills.git"
clone_reference "llm-council-skill" "https://github.com/tenfoldmarc/llm-council-skill.git"
clone_reference "agent-council" "https://github.com/yogirk/agent-council.git"
clone_reference "agent-tower-plugin" "https://github.com/BayramAnnakov/agent-tower-plugin.git"
clone_reference "Deep-Research-skills" "https://github.com/Weizhena/Deep-Research-skills.git"
clone_reference "ai-research-skills" "https://github.com/WenyuChiou/ai-research-skills.git"
clone_reference "pm-skills" "https://github.com/product-on-purpose/pm-skills.git"
clone_reference "agentbrain" "https://github.com/rohitg00/agentbrain.git"
clone_reference "agent-skills" "https://github.com/addyosmani/agent-skills.git"
